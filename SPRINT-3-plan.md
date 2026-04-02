# Sprint 3 Plan — Wallet, Consultation Chat & Billing Loop

**Duration:** 2 weeks  
**Sprint Goal:** Full end-to-end consultation flow — connect, chat, wallet depletes, disconnect, transcript saved, review prompt fires.  
**PO Acceptance Gate:** QA-001 and QA-002 must pass. Billing loop is end-to-end verified.

---

## Committed Stories

| Story ID | Title | Points | Owner | Depends On |
|---|---|---|---|---|
| STORY-WALLET-001 | Wallet balance display | 2 | Dev Agent | STORY-AUTH-001 ✅ |
| STORY-WALLET-002 | Wallet recharge (mock payment) | 5 | Dev Agent | STORY-WALLET-001 |
| STORY-WALLET-003 | Transaction ledger | 3 | Dev Agent | STORY-WALLET-002 |
| STORY-WALLET-004 | Low wallet alert (< threshold) | 2 | Dev Agent | STORY-NOTIF-001 |
| STORY-CHAT-001 | Socket.io consultation room setup | 5 | Dev Agent | STORY-WALLET-001 |
| STORY-CHAT-002 | Wallet pre-check before session start | 3 | Dev Agent | STORY-WALLET-001 |
| STORY-CHAT-003 | Per-minute billing loop (BullMQ) | 8 | Dev Agent | STORY-CHAT-001 + STORY-WALLET-002 |
| STORY-CHAT-004 | Auto-disconnect on wallet zero | 5 | Dev Agent | STORY-CHAT-003 |
| STORY-CHAT-005 | 30-second grace period warning | 2 | Dev Agent | STORY-CHAT-004 |
| STORY-CHAT-006 | Session transcript save | 3 | Dev Agent | STORY-CHAT-001 |
| STORY-CHAT-007 | Post-session review prompt | 2 | Dev Agent | STORY-CHAT-006 |
| STORY-NOTIF-001 | In-app notification bell | 3 | Dev Agent | STORY-AUTH-001 ✅ |
| STORY-NOTIF-004 | Low wallet push notification | 2 | Dev Agent | STORY-WALLET-004 |
| **Total** | | **45 pts** | | |

---

## Sprint Capacity

| Resource | Availability | Notes |
|---|---|---|
| Dev Agent (Claude Code) | Full sprint | One story at a time, sequential |
| QA Agent | Sprint review | Reviews PRs + produces QA-REPORT-S3 |
| Product Owner | Sprint demo | Binary accept/reject per story |

**Velocity assumption:** 40–45 points per 2-week sprint based on Sprint 1–2 actuals.

---

## Story Implementation Order (Enforced by SM)

```
Day 1-2:   STORY-WALLET-001 → STORY-WALLET-002 → STORY-WALLET-003
Day 3:     STORY-NOTIF-001 → STORY-WALLET-004 → STORY-NOTIF-004
Day 4-5:   STORY-CHAT-001 (Socket.io rooms — critical path)
Day 6:     STORY-CHAT-002 (wallet pre-check)
Day 7-9:   STORY-CHAT-003 (billing loop — highest complexity, most points)
Day 10:    STORY-CHAT-004 + STORY-CHAT-005 (auto-disconnect sequence)
Day 11:    STORY-CHAT-006 + STORY-CHAT-007 (transcript + review prompt)
Day 12-14: QA review, bug fixes, PO demo prep
```

---

## Critical Path Notes

**STORY-CHAT-003 is the highest-risk story in the entire project.** It touches:
- BullMQ repeatable job creation and lifecycle management
- PostgreSQL `SELECT FOR UPDATE` wallet deduction (ADR-006)
- Redis connectivity for BullMQ
- Socket.io event emission from the job processor (crosses service boundaries)
- Idempotency key enforcement on the Transaction model

**Dev Agent instruction for STORY-CHAT-003:** Read ADR-005 and ADR-006 in full before writing any code. The billing loop implementation must exactly follow the patterns specified. Do not deviate without a DECISIONS.md entry and PO approval.

---

## QA Critical Scenarios for This Sprint

| QA ID | Scenario | Blocking? |
|---|---|---|
| QA-001 | Concurrent wallet debit race condition | ✅ Sprint blocking |
| QA-002 | Billing loop auto-disconnect — wallet reaches zero | ✅ Sprint blocking |
| QA-006 | Network interruption during billing loop — orphaned job recovery | ⚠️ High severity |
| QA-008 | Mock payment failure during wallet recharge | ⚠️ High severity |

**Sprint 3 cannot be accepted by PO until QA-001 and QA-002 pass.**

---

## Sprint 3 Demo Acceptance Criteria (PO Gate)

```
Sprint 3 Demo Checklist:
[ ] User can view wallet balance
[ ] User can recharge wallet (mock payment succeeds)
[ ] Transaction ledger shows recharge entry
[ ] User can start a consultation (wallet pre-check passes)
[ ] Per-minute billing loop runs — wallet balance decreases every 60 seconds
[ ] When wallet reaches zero: 30-second warning fires → session ends → transcript saved
[ ] Post-session review prompt appears
[ ] Low wallet notification fires when balance < threshold
[ ] QA-001: Concurrent debit test passes (only one deduction per minute)
[ ] QA-002: Auto-disconnect test passes end-to-end
```

---

## Blockers & Risks

| Risk | Probability | Mitigation |
|---|---|---|
| Socket.io + BullMQ cross-service event complexity | High | Follow ADR-005 exactly; Dev Agent reads ADR before starting |
| Redis not available in Docker Compose | Medium | STORY-INFRA-001 must include Redis service |
| Token budget pressure (billing loop is large) | High | Split STORY-CHAT-003 into sub-tasks if context window fills |
| Race condition in test environment | Medium | QA must run concurrent debit test 10 times, not once |

---

## Sprint Retrospective Template (SM fills after demo)

```
Sprint 3 Retrospective
Velocity: ___ pts delivered / 45 committed
Stories accepted: ___
Stories returned: ___

What went well:
-

What was hard:
-

DECISIONS.md entries this sprint:
-

Carry-over to Sprint 4:
-
```
