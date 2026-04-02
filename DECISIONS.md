# DECISIONS.md — Autonomous Agent Decision Log

> This file records every significant decision made autonomously by an AI agent during this project. Entries are dated and attributed to the agent that made the decision. The Product Owner reviews this log at each sprint demo.

---

## Format

```
### [DATE] [AGENT] — [SHORT TITLE]
**Context:** What situation triggered this decision
**Decision:** What was decided
**Rationale:** Why this option over alternatives
**PO Review:** Accepted / Needs discussion
```

---

## Sprint 0 Decisions

### 2026-03-01 | Architect Agent — pnpm over npm for monorepo
**Context:** Prompt Contract specified pnpm workspaces for the monorepo. Architect needed to decide on lock file strategy and workspace hoisting configuration.  
**Decision:** Use `pnpm-workspace.yaml` with strict hoisting (`hoist-pattern=[]`) to prevent phantom dependency issues.  
**Rationale:** Strict hoisting catches dependency issues in CI that permissive hoisting would hide. Minor setup cost, significant reliability benefit.  
**PO Review:** Accepted

### 2026-03-01 | Architect Agent — PostgreSQL 16 over MySQL
**Context:** Prompt Contract specified PostgreSQL but not a version. Architect chose version.  
**Decision:** PostgreSQL 16 (latest stable at time of build).  
**Rationale:** Native JSON columns, `SELECT FOR UPDATE SKIP LOCKED` for BullMQ compatibility, superior full-text search for astrologer directory. No MySQL-specific features are needed.  
**PO Review:** Accepted

### 2026-03-02 | Architect Agent — Redis 7 as BullMQ backend
**Context:** BullMQ requires Redis. Architect chose version and persistence configuration.  
**Decision:** Redis 7 with `appendonly yes` (AOF persistence) in Docker Compose.  
**Rationale:** AOF persistence ensures BullMQ jobs survive container restarts. RDB snapshots alone are insufficient for billing loop job durability.  
**PO Review:** Accepted

---

## Sprint 1 Decisions

### 2026-03-08 | Developer Agent — Mock OTP via console.log
**Context:** STORY-AUTH-001 requires OTP login. Real SMS provider (Twilio) is out of scope for v1 per Prompt Contract §9.  
**Decision:** OTP is logged to server console in development mode. A `MOCK_OTP=true` env flag bypasses SMS sending.  
**Rationale:** Keeps auth flow testable without external dependency. Production readiness is out of scope for v1.  
**PO Review:** Accepted — note for production: replace console.log with Twilio SDK

### 2026-03-09 | Developer Agent — Shadcn/UI Button variant for astrologer availability
**Context:** STORY-DIR-003 requires a real-time availability indicator. Shadcn/UI has Badge and Button variants; neither exactly matches the "online/offline" pill design.  
**Decision:** Use Shadcn Badge with custom `online` and `offline` CSS variants added to `globals.css`.  
**Rationale:** Extending an existing component is less risky than building a new one. CSS variables ensure theme consistency.  
**PO Review:** Accepted

---

## Sprint 2 Decisions

### 2026-03-15 | Architect Agent — Swiss Ephemeris via Python gRPC sidecar (ADR-003)
**Context:** STORY-KUNDLI-002 requires planetary position calculations via Swiss Ephemeris. Two options: Node.js FFI binding or Python gRPC sidecar.  
**Decision:** Python gRPC sidecar (`packages/ephemeris-service` — Python 3.11 + Flask/gRPC).  
**Rationale:** The Node.js `swisseph` npm package is poorly maintained and has known FFI stability issues on ARM64 (Apple Silicon). A Python sidecar uses the well-maintained `pyswisseph` package and isolates the ephemeris dependency entirely from the Node.js process.  
**PO Review:** Accepted — adds one container to Docker Compose

### 2026-03-16 | Developer Agent — AI report generation is async (ADR-007 alignment)
**Context:** STORY-KUNDLI-004 generates an AI Kundli report via Claude API. Synchronous generation blocks the request for 5–15 seconds.  
**Decision:** Kundli report generation is async. User sees "Report generating..." state; report arrives via Server-Sent Events when Claude API returns.  
**Rationale:** 5–15 second synchronous hold is unacceptable UX. SSE is simpler than WebSocket for one-way server push and fits this use case well.  
**PO Review:** Accepted

---

## Sprint 3 Decisions

### 2026-03-22 | Developer Agent — BullMQ dashboard enabled in development only
**Context:** BullMQ provides `@bull-board/express` for a visual job dashboard. Useful for debugging the billing loop.  
**Decision:** Bull Board enabled in development (`NODE_ENV=development`) at `/admin/queues`. Disabled in production.  
**Rationale:** Exposes sensitive billing job data; must not be public. Development utility is high — allows direct inspection of repeatable job state during QA-001 and QA-002 testing.  
**PO Review:** Accepted

### 2026-03-23 | Developer Agent — Grace period is client-enforced, not server-enforced
**Context:** STORY-CHAT-005 specifies a 30-second grace period warning before auto-disconnect.  
**Decision:** The 30-second countdown is displayed client-side after `session:warning` Socket.io event. The server sends `session:end` after a separate 35-second server-side timer (5-second buffer).  
**Rationale:** Client-side countdown provides smooth UX. Server-side timer ensures disconnect happens even if client is unresponsive. The 5-second buffer prevents race conditions where the client might reconnect just as the server disconnects.  
**PO Review:** Accepted — note: 35 seconds server timer must be configurable via env var

---

*Log continues as development progresses. All agents are required to add entries here for any decision not explicitly specified in the Prompt Contract or ADRs.*
