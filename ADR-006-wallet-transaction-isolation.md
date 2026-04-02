# ADR-006: Wallet Transaction Isolation — PostgreSQL Locking Strategy

**Date:** 2026-03  
**Status:** Accepted  
**Decided by:** Architect Agent  
**QA Scenario:** QA-001 (concurrent wallet debit race condition)

---

## Context

The wallet is the financial core of the platform. Two concurrent operations can race on the same wallet:
- Two consultation sessions debiting simultaneously (unlikely but possible if a user somehow has two active sessions)
- A recharge completing at the exact moment a debit fires
- An admin refund concurrent with a session debit

PostgreSQL provides several isolation mechanisms. The choice affects correctness, performance, and deadlock risk.

---

## Decision

**Use `SELECT FOR UPDATE` within a serializable Prisma transaction for all wallet debit operations.**

---

## Implementation

```sql
-- Pseudocode for the atomic debit pattern
BEGIN;
  SELECT balance FROM wallets WHERE user_id = $1 FOR UPDATE;
  -- Row is now locked; concurrent transactions wait here
  
  IF balance < rate_per_minute THEN
    ROLLBACK;
    -- trigger disconnect
  END IF;
  
  UPDATE wallets SET balance = balance - rate_per_minute WHERE user_id = $1;
  INSERT INTO transactions (wallet_id, amount, type, idempotency_key) 
    VALUES ($2, -rate_per_minute, 'DEBIT', $3);
COMMIT;
```

---

## Rationale

| Approach | Correctness | Performance | Deadlock Risk |
|---|---|---|---|
| `SELECT FOR UPDATE` (chosen) | ✅ Correct | ✅ Good | ⚠️ Low — single row lock |
| Optimistic locking (version field) | ⚠️ Requires retry loop | ✅ Best | ✅ None |
| Serializable isolation (full TX) | ✅ Correct | ❌ Poor at scale | ⚠️ Higher |
| Application-level mutex (Redis) | ⚠️ Complex | ✅ Good | ✅ None |

`SELECT FOR UPDATE` is chosen because:
1. Simple to implement correctly in Prisma
2. Single-row locks have minimal contention at this scale
3. No retry loop complexity (unlike optimistic locking)
4. Deadlock risk is negligible — wallets are always locked in the same order (by `userId`)

---

## Idempotency

All transactions carry an `idempotencyKey` (`consultation_id + minute_timestamp`) with a `@unique` constraint in Prisma. This ensures that even if the billing job fires twice in the same minute (e.g., due to a Redis retry), only one deduction is recorded.

---

## Consequences

- `schema.prisma` must include `idempotencyKey String @unique` on the `Transaction` model
- All wallet mutations (debit, credit, recharge, refund) must go through the same locked transaction pattern
- QA-001 must simulate two concurrent debits on the same wallet and verify only one succeeds
