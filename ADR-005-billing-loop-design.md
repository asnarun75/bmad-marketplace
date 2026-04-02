# ADR-005: Billing Loop Design — BullMQ Job Lifecycle

**Date:** 2026-03  
**Status:** Accepted  
**Decided by:** Architect Agent  
**Reviewed by:** Product Owner  
**QA Scenarios:** QA-001, QA-002, QA-006

---

## Context

The per-minute billing loop is the most financially critical component of the platform. It must:

1. Deduct the astrologer's per-minute rate from the user's wallet every 60 seconds
2. Stop and disconnect the session when the wallet balance reaches zero
3. Recover gracefully from network interruptions, server restarts, and concurrent sessions
4. Never double-charge (idempotent deduction)
5. Never leave an orphaned job running after a session ends

---

## Decision

**Use BullMQ repeatable jobs keyed by `consultation_id`, with PostgreSQL `SELECT FOR UPDATE` for wallet deductions, and Socket.io events for client-side disconnect signalling.**

---

## Architecture

### Job Creation (on session start)
```typescript
// When consultation starts
await billingQueue.add(
  `billing-${consultationId}`,
  { consultationId, userId, astrologerId, ratePerMinute },
  {
    repeat: { every: 60_000 },
    jobId: `billing-${consultationId}`,  // idempotent
    removeOnComplete: false,             // keep for audit trail
  }
);
```

### Deduction Logic (job processor)
```typescript
// Atomic wallet deduction with SELECT FOR UPDATE
await prisma.$transaction(async (tx) => {
  const wallet = await tx.wallet.findUnique({
    where: { userId },
    select: { balance: true },
    // Prisma raw for advisory lock
  });

  if (wallet.balance < ratePerMinute) {
    // Trigger auto-disconnect sequence
    await triggerAutoDisconnect(consultationId, userId);
    await billingQueue.removeRepeatable(`billing-${consultationId}`, { every: 60_000 });
    return;
  }

  await tx.wallet.update({
    where: { userId },
    data: { balance: { decrement: ratePerMinute } },
  });

  await tx.transaction.create({
    data: {
      walletId,
      consultationId,
      amount: -ratePerMinute,
      type: 'DEBIT',
      idempotencyKey: `${consultationId}-${Date.now()}`,
    }
  });
});
```

### Auto-Disconnect Sequence
1. BullMQ processor detects `balance < ratePerMinute`
2. Emits `session:warning` Socket.io event to client (30-second countdown starts)
3. After 30 seconds, emits `session:end` with reason `WALLET_EXHAUSTED`
4. Client-side: displays warning modal, then disconnects Socket.io room
5. Server-side: saves transcript, creates session record, fires post-session review prompt
6. BullMQ job removed: `billingQueue.removeRepeatable(...)`

---

## Failure Modes & Recovery

| Failure | Detection | Recovery |
|---|---|---|
| Server restart mid-session | BullMQ Redis persistence | Job survives restart; resumes on next worker boot |
| Network interruption (client) | Socket.io heartbeat timeout (30s) | Server emits `session:end` after timeout; job removed |
| Network interruption (server→Redis) | BullMQ connection retry | Exponential backoff; alert if > 3 retries |
| Concurrent sessions (same user) | `SELECT FOR UPDATE` + idempotency key | Only one deduction per `consultationId` per minute |
| Orphaned job (session ended but job not removed) | Nightly reconciliation job | Scan active jobs vs active sessions; remove orphans |

---

## Consequences

- Redis is a **required** infrastructure component (not optional) — BullMQ depends on it
- `DEPLOYMENT.md` must include Redis in Docker Compose
- Nightly reconciliation job required from Sprint 3 (STORY-INFRA-003, added to backlog)
- All wallet transactions must carry an `idempotencyKey` — schema.prisma enforced with `@unique`
- QA-001 (concurrent debit) and QA-002 (wallet zero) are **Sprint 3 blocking** — sprint cannot be accepted without these passing

---

## Alternatives Considered

- **Setinterval on the server:** Rejected. Not persistent across restarts, no retry logic, no visibility.
- **Cron job (node-cron):** Rejected. Same persistence issues; no per-session granularity.
- **Database polling:** Rejected. High read load at scale, no real-time event capability.
- **Agenda.js:** Considered but BullMQ has better Redis integration, dashboard visibility, and active maintenance.
