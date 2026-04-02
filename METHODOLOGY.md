# BMAD Methodology — Lessons Learned & Analysis

## What Is BMAD?

**BMAD (Build–Measure–Analyze–Deploy)** is an agile framework adapted for AI agent orchestration. Its core insight: the bottleneck in AI-assisted development is not code generation speed — it's **context coherence across the full delivery lifecycle**.

Most engineers use AI as a pair programmer at the unit level. When building a real system, failure modes compound fast. The AI that wrote your wallet service has no memory of what the architect decided about transaction isolation. BMAD fixes this by separating concerns across specialized agent personas, each producing artifacts that feed the next, with a human Product Owner as the only approval gate.

---

## The Agent Handoff Chain

```
Prompt Contract (human-authored)
    ↓
PM Agent → PRD.md (76 stories, 11 epics, BDD format)
    ↓
Architect Agent → ARCHITECTURE.md + openapi.yaml + schema.prisma + 8 ADRs
    ↓
Scrum Master Agent → BACKLOG.md + 8 Sprint Plans + velocity tracker
    ↓
Developer Agent (Claude Code) → implementation, 1 story at a time
    ↓
QA Agent → PR reviews + sprint QA reports + 10 critical test scenarios
    ↓
Product Owner (human) → sprint demo approval, scope decisions
```

---

## Token Budget Analysis

| Phase | Token Pressure | Notes |
|---|---|---|
| PM — PRD authoring | Medium | 76 stories × full BDD format is substantial |
| Architect — ADRs + OpenAPI + Prisma | **HIGH — hit limit here** | 8 ADRs + full OpenAPI 3.1 spec + Prisma schema with 12 entities filled the context window |
| SM — Sprint planning | Medium | 8 sprint plans with story dependencies |
| Dev — Sprint 1–2 | Low-Medium | Single story per session kept context manageable |
| Dev + QA — Sprint 3 (billing loop) | **HIGH — hit limit here** | Socket.io room design + BullMQ jobs + PostgreSQL SELECT FOR UPDATE + auto-disconnect sequence all in one sprint |

**Total cost:** More than a standard Claude Code session. Less than a single day of contractor time.

**Key finding:** Context limit resets are recoverable if your input artifacts are well-structured. Re-feeding a well-formed Prompt Contract + prior agent outputs produced coherent continuations with no loss of architectural intent.

---

## What Worked Well

### 1. The Prompt Contract
Spending 3 hours authoring a 12-section requirements document before activating any agent was the single highest-ROI investment. It gave every agent enough context to make real architectural decisions rather than defaulting to generic patterns.

### 2. Role Separation
Preventing Claude Code from deciding what to build next (that was the SM's job) eliminated the most common AI coding failure mode: going deep on an interesting problem while losing the sprint goal.

### 3. ADR Format
Forcing the Architect to document trade-offs in ADR format produced better architectural decisions than most human-led projects achieve. The SSR vs CSR decision alone (ADR-001) surfaced SEO requirements for the horoscope content pages that a solo developer would have missed.

### 4. Binary Sprint Acceptance Criteria
Pre-defining sprint acceptance rubrics ("Full billing loop works end-to-end — connect, chat, wallet depletes, disconnect, transcript saved, review prompt fires. QA-001 and QA-002 pass.") kept the PO role honest and prevented scope creep.

### 5. QA Scenario Pre-building
Defining QA-001 through QA-010 before any code was written meant the QA agent had unambiguous targets. The 10 scenarios covered the failure modes that mattered: concurrent wallet debits, mid-session admin bans, billing loop under network interruption, Kundli generation with missing birth time.

---

## What Was Hard

### 1. Context Re-feeding After Token Limits
When the context window reset, re-feeding the prior agent's output took time. Mitigation: keep each artifact self-contained and versioned. An ARCHITECTURE.md that references only its own section numbers (not "as we discussed") survives a context reset.

### 2. Agent Persona Drift
Over long sessions, Claude Cowork personas occasionally drifted toward more general responses. Fix: restate the role tag at the start of each new session ("You are the Architect. Your inputs are PRD.md and the Prompt Contract. Do not begin until you have read both.").

### 3. Story Dependency Enforcement
The SM produced correct dependency chains (STORY-CHAT-003 cannot start until STORY-WALLET-001 is merged), but the Developer agent occasionally tried to implement dependent stories before prerequisites. Mitigation: enforce the SM's dependency table in the Developer brief.

### 4. The Upfront Investment
3 hours on the Prompt Contract is non-negotiable. Engineers who want to shortcut this step will get locally coherent but systemically broken outputs. Treat requirements authoring as a first-class engineering activity.

---

## BMAD vs Claude Code Solo — Comparison

| Dimension | Claude Code Solo | BMAD + Cowork |
|---|---|---|
| Speed to first code | Faster | Slower (planning phase first) |
| Planning artifact quality | Low (implicit) | High (explicit PRD, ADRs, sprint plans) |
| Architectural coherence | Medium | High |
| Requirement traceability | Low | High (every story → code) |
| Context window management | Hard at scale | Easier (artifacts are the context) |
| Best for | Prototypes, scripts, single-service tools | Multi-service systems, full product builds |
| Token cost | Lower | Higher |
| Human time investment | Lower | Higher upfront, lower downstream |

**Verdict:** BMAD's ROI is clearest in the planning phase. For a 15-week, 76-story, multi-service platform build, the planning investment pays back in reduced rework and architectural coherence. For a 2-day prototype, Claude Code solo wins.

---

## Broader Implications for Engineering Leaders

We are not at the point of replacing engineering teams with agents. But we are at the point where a single experienced engineer — one who can write a solid requirements contract, make architectural judgment calls, and play PO at sprint demos — can produce the planning and scaffolding output of a 5-person cross-functional team.

**The skill that matters is not prompting. It's systems thinking and requirements clarity.** BMAD amplifies that capability. It does not substitute for it.

For engineering leaders: consider whether your next product initiative's planning phase — PRD, architecture, backlog — could be accelerated by 3–4 weeks using a structured multi-agent approach. That's where the ROI is clearest and the token cost is most obviously justified.

---

*Two token limits. 76 stories. 8 ADRs. A full OpenAPI spec. Eight weeks of delivery scaffolding. I'd do it again.*
