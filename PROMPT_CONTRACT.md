# Prompt Contract — Consumer Astrology Marketplace Platform
**Version:** 1.0  
**Framework:** BMAD Multi-Agent SDLC  
**Target:** Claude Cowork (agent orchestration) + Claude Code (implementation)

---

## 0. How to Use This Document

This is the **master source of truth** for all agents. Each agent reads this document in full before producing any output.

| Agent | Primary Input | Primary Output |
|---|---|---|
| PM — Product Analyst | This document | `PRD.md` |
| Architect | This document + `PRD.md` | `ARCHITECTURE.md`, `openapi.yaml`, `schema.prisma`, ADRs |
| Scrum Master | `PRD.md` + `ARCHITECTURE.md` | `BACKLOG.md`, sprint plans |
| Developer | One story at a time from SM | Implementation + unit tests |
| QA | Story acceptance criteria + PR | Sprint QA report |
| Product Owner (human) | Sprint demo | Accept / reject decision |

---

## 1. Mission Statement

Build a functional replica of a two-sided astrology consultation marketplace — targeting **75–80% feature parity** with a production-grade platform. The platform connects users seeking astrological guidance with astrologers providing real-time text consultations, automated chart generation, horoscopes, and a spiritual commerce store.

**Prediction accuracy is NOT an evaluation criterion for v1.** The goal is a working product framework with correct data flows, billing mechanics, and UI completeness.

### 1.1 Success Criteria

| Criterion | Target | How to Verify |
|---|---|---|
| P0 features working end-to-end | 100% | Manual smoke test per P0 story |
| P1 features working | ≥ 90% | Manual smoke test |
| Unit test coverage (service layer) | ≥ 70% | Jest coverage report |
| TypeScript strict mode — zero errors | 100% | `tsc --noEmit` |
| Lighthouse Performance (homepage) | ≥ 80 | Lighthouse CLI |
| DECISIONS.md maintained | Yes | File exists with dated entries |

---

## 2. Product Vision (For PM Agent)

> **▶ AGENT: PM — Product Analyst**  
> Your input is this entire document. Your output is `PRD.md`. Read the full brief, then produce the PRD. Ask clarifying questions (list them) before writing any story.

### 2.1 Target Personas

| Persona | Goal | Pain Point Solved |
|---|---|---|
| Anonymous Visitor | Explore horoscopes, browse astrologers | Free access without sign-up friction |
| Registered User | Book consultations, generate Kundli, get predictions | On-demand astrologer access 24/7 |
| Astrologer | Accept consultations, manage schedule, earn income | Reach wider audience; streamlined billing |
| Platform Admin | Manage users, content, transactions | Visibility and moderation tools |

### 2.2 Feature Scope (P0/P1/P2)

| Epic | Key Features | Priority |
|---|---|---|
| Auth & Profiles | OTP login, email/password, Google SSO, profile with birth details | P0 |
| Astrologer Directory | Listing with filters, detail page, real-time availability, onboarding | P0 |
| Kundli Engine | Birth chart form, SVG chart, planetary table, AI report, PDF export | P0/P1 |
| Horoscope Content | Daily/weekly/monthly (12 signs), Panchang, Muhurat calculator | P0/P1 |
| Consultation Chat | Real-time text chat, per-minute billing, wallet pre-check, auto-disconnect | P0 |
| Wallet & Payments | Recharge (mock), transaction ledger, cashback, astrologer payout | P0/P1 |
| AstroMall | Product catalogue, cart, mock checkout, order history | P1/P2 |
| Blog & Tools | Numerology calculator, compatibility checker, baby name tool | P1/P2 |
| Admin Panel | KPI dashboard, user/astrologer management, content CRUD | P0/P1 |
| Notifications | In-app bell, transactional email, low-wallet alert | P1/P2 |

### 2.3 PM Deliverables
- `PRD.md` with all epics and stories in Given/When/Then BDD format
- Priority matrix: P0 (Sprint 1–3), P1 (Sprint 4–6), P2 (Sprint 7+)
- Open questions log
- Domain glossary (Kundli, Lagna, Dasha, Panchang, etc.)

---

## 3. Architecture Brief (For Architect Agent)

> **▶ AGENT: Architect**  
> Your input is `PRD.md` + this document. Do not begin until `PRD.md` is finalised and reviewed by PO.

### 3.1 Mandated Stack (Non-Negotiable)

| Layer | Technology | Notes |
|---|---|---|
| Monorepo | pnpm workspaces | `packages/web`, `packages/api`, `packages/shared` |
| Frontend | React 18 + Vite + TypeScript strict | Tailwind CSS + Shadcn/UI. SSR decision → ADR-001 |
| Backend | Node.js 20 + Express or Fastify | TypeScript strict throughout |
| Database | PostgreSQL 16 + Prisma ORM | Architect produces full `schema.prisma` |
| Real-time | Socket.io | Consultation rooms, billing loop events |
| Background Jobs | BullMQ + Redis | Per-minute billing, scheduled content generation |
| AI Integration | Anthropic Claude API | Kundli reports, horoscope generation, content pipeline |
| Ephemeris | Swiss Ephemeris (via bridge) | Native FFI vs Python gRPC sidecar → ADR-003 |
| Auth | JWT + OTP (SMS) + Google OAuth | Refresh token rotation required |
| Deployment | Docker Compose (local dev) | Production topology in `DEPLOYMENT.md` |

### 3.2 Critical Design: Real-Time Billing Loop

The Architect **must** fully specify in `ARCHITECTURE.md`:
- Socket.io room/namespace design for consultation sessions
- BullMQ job structure (repeatable job keyed by `consultation_id`)
- PostgreSQL transaction pattern for wallet deduction (`SELECT FOR UPDATE`)
- Race condition handling for concurrent sessions
- Auto-disconnect sequence with 30-second grace period

### 3.3 Architect Deliverables
- `ARCHITECTURE.md` — system overview, Mermaid component diagram, data flow diagrams
- `openapi.yaml` — OpenAPI 3.1 spec for all REST endpoints
- `schema.prisma` — complete schema with all models, relations, enums, indexes
- `ADR-001` through `ADR-008` — one file per architectural decision (see §3.4)
- `DEPLOYMENT.md` — Docker Compose for local dev + production topology
- `SECURITY.md` — auth flow, encryption strategy, rate limiting, RBAC design

### 3.4 Required ADRs

| ADR | Decision |
|---|---|
| ADR-001 | SSR vs CSR — Next.js vs Vite for SEO on horoscope content pages |
| ADR-002 | Socket.io topology — single namespace vs per-consultation namespace |
| ADR-003 | Swiss Ephemeris bridge — native Node FFI vs Python gRPC sidecar |
| ADR-004 | Redis cache TTL strategy for AI-generated horoscope content |
| ADR-005 | Billing loop design — BullMQ job lifecycle and failure recovery |
| ADR-006 | Wallet transaction isolation — PostgreSQL locking strategy |
| ADR-007 | AI content pipeline — sync vs async generation, fallback strategy |
| ADR-008 | Monorepo structure — package boundaries and shared type strategy |

---

## 4. Scrum Master Brief (For SM Agent)

> **▶ AGENT: Scrum Master**  
> Your input is `PRD.md` and `ARCHITECTURE.md`. Produce the sprint-ready backlog and sprint plans. Enforce story dependencies explicitly.

### 4.1 Sprint Structure

| Sprint | Duration | Focus | Key Dependency |
|---|---|---|---|
| Sprint 0 | 1 week | Repo scaffold, CI/CD, DB schema, Docker Compose, seed data | ARCHITECTURE.md ready |
| Sprint 1 | 2 weeks | Auth, user profile, astrologer directory (read-only) | Sprint 0 complete |
| Sprint 2 | 2 weeks | Kundli engine, daily horoscopes (all 12 signs), BullMQ job | Sprint 1 complete |
| Sprint 3 | 2 weeks | Wallet, consultation chat + billing loop, session review | Sprint 1 + billing ADR finalised |
| Sprint 4 | 2 weeks | Astrologer dashboard, post-session review, admin core | Sprint 3 complete |
| Sprint 5 | 2 weeks | Panchang, weekly/monthly horoscopes, Kundli matching, blog | Sprint 2 complete |
| Sprint 6 | 2 weeks | AstroMall, notifications, first free session | Sprint 3 + 4 complete |
| Sprint 7 | 1 week | QA hardening, Playwright E2E, Lighthouse, DECISIONS.md | All sprints complete |

### 4.2 Story Format (Mandatory)
```
STORY-[EPIC]-[NNN]: [Title]
Priority: P0 / P1 / P2
Points: [Fibonacci]
Depends on: [STORY-ID or "none"]
As a [persona], I want to [action], so that [benefit].
Given [context], When [action], Then [outcome].
Acceptance Criteria:
  1. ...
  2. ...
Out of scope: ...
```

### 4.3 SM Deliverables
- `BACKLOG.md` — full 76-story backlog across 11 epics with dependencies
- `SPRINT-N-plan.md` for each sprint — committed stories, points, capacity, blockers

---

## 5. Developer Brief (For Developer Agent / Claude Code)

> **▶ AGENT: Developer (Claude Code)**  
> You receive one user story at a time. Implement it. Write unit tests. Update DECISIONS.md for any autonomous architectural choice. Do NOT decide what to build next — that is the SM's role.

### 5.1 Coding Standards
- TypeScript strict mode throughout — no `any`
- Service layer unit test coverage ≥ 70% per story
- Every PR must include: what was built, tests added, DECISIONS.md updated (Y/N), OpenAPI spec updated (Y/N)
- Follow existing patterns — read the codebase before writing new files

### 5.2 Developer Deliverables (per story)
- Implementation code with unit tests
- PR summary following the template above
- DECISIONS.md entry for any autonomous architectural choice

---

## 6. QA Brief (For QA Agent)

> **▶ AGENT: QA**  
> Review PRs against acceptance criteria. Produce a sprint QA report. Do not write feature code.

### 6.1 Critical Test Scenarios (Pre-defined)

| ID | Scenario | Sprint |
|---|---|---|
| QA-001 | Concurrent wallet debit race condition — two sessions debit simultaneously | Sprint 3 |
| QA-002 | Billing loop auto-disconnect — wallet reaches zero mid-session | Sprint 3 |
| QA-003 | Mid-session admin ban — astrologer banned during active consultation | Sprint 4 |
| QA-004 | Kundli generation with missing birth time — graceful fallback | Sprint 2 |
| QA-005 | Token expiry during active Socket.io session — reconnect flow | Sprint 3 |
| QA-006 | Network interruption during billing loop — orphaned job recovery | Sprint 3 |
| QA-007 | Astrologer goes offline mid-consultation — user experience | Sprint 3 |
| QA-008 | Mock payment failure during wallet recharge | Sprint 3 |
| QA-009 | Admin bulk content CRUD under concurrent load | Sprint 4 |
| QA-010 | Lighthouse performance regression on horoscope content page | Sprint 7 |

### 6.2 QA Deliverables (per sprint)
- `QA-REPORT-S[N].md` — stories passed, returned for rework, open issues by severity

---

## 7. Product Owner Protocol (Human)

### 7.1 Sprint Demo Acceptance Format
```
Sprint [N] Demo — [Date]
Acceptance Criteria Met: YES / NO
Stories Accepted: [list]
Stories Returned for Rework: [list with reason]
Scope Decisions: [any P2→P1 promotions or descopes]
Next Sprint Gate: [specific binary criteria for Sprint N+1 acceptance]
```

### 7.2 PO Acceptance Criteria by Sprint
- **Sprint 0:** Monorepo builds, Docker Compose starts all services, DB schema matches schema.prisma
- **Sprint 1:** Full auth flow works (OTP + Google), astrologer directory renders with seed data
- **Sprint 2:** Kundli chart renders for any birth date/time/location; daily horoscope shows for all 12 signs
- **Sprint 3:** Full billing loop end-to-end — connect, chat, wallet depletes, disconnect, transcript saved, review prompt fires. QA-001 and QA-002 pass.
- **Sprint 4:** Astrologer dashboard shows session history and earnings; admin can manage users and astrologers
- **Sprint 5:** Panchang shows today's data; compatibility checker returns result for any two signs
- **Sprint 6:** Cart-to-mock-checkout flow complete; in-app notifications fire for wallet alerts
- **Sprint 7:** Lighthouse ≥ 80 on homepage; zero TypeScript errors; all QA-001–QA-010 pass

---

## 8. Comparison Framework (Track A vs Track B)

This project uses **Track B (BMAD)**. For comparison purposes, Track A is the same build using Claude Code as a solo agent with no BMAD planning structure.

| Dimension | Track A (Claude Code solo) | Track B (BMAD) |
|---|---|---|
| Speed to first code | Faster | Slower |
| Planning artifact quality | Low (implicit) | High (explicit) |
| Architectural coherence | Medium | High |
| Requirement traceability | Low | High |
| Token cost | Lower | Higher |
| Best for | Prototypes | Full product builds |

---

## 9. Out of Scope (v1)

- Astrological prediction accuracy
- Real payment gateway integration (mock only)
- Video/voice consultation (text only)
- Multi-language support
- Mobile native apps
- Real SMS OTP (mock OTP accepted for v1)
