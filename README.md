# BMAD Multi-Agent SDLC Experiment — Consumer Marketplace Platform

> **An experiment in running a full software delivery lifecycle using 6 AI agent personas, structured as an agile scrum team, powered by Anthropic's Claude Cowork + Claude Code.**

[![Claude Code](https://img.shields.io/badge/Built%20With-Claude%20Code-blue)](https://claude.ai)
[![BMAD Framework](https://img.shields.io/badge/Framework-BMAD-orange)](https://github.com/bmad-framework)
[![Certification](https://img.shields.io/badge/Certified-Claude%20Code%20in%20Action-green)](https://verify.skilljar.com/c/yq5fvqcn6vbg)

---

## 🧪 What Is This?

This repository documents a personal engineering experiment: using the **BMAD (Build–Measure–Analyze–Deploy)** agile framework to simulate a complete scrum team with AI agents — running the full SDLC from requirements through sprint planning and implementation for a complex two-sided consumer marketplace.

The target: a **consumer astrology marketplace platform** (two-sided, real-time billing, wallet engine, AI-generated content, consultation system, admin panel) — targeting **75–80% feature parity** with a production-grade marketplace.

> **No code is committed here. This repo captures the planning artifacts, prompt contracts, agent briefs, ADRs, sprint backlogs, and methodology documentation** — the outputs of the AI agent scrum team's planning phases.

---

## 🤖 The Agent Team

| Agent Role | Tool Used | Primary Output |
|---|---|---|
| **PM — Product Analyst** | Claude Cowork (PM persona) | `docs/PRD.md` — full PRD with 76 BDD user stories |
| **Architect** | Claude Cowork (Architect persona) | `docs/ARCHITECTURE.md`, `docs/openapi.yaml`, `docs/schema.prisma`, ADR-001–008 |
| **Scrum Master** | Claude Cowork (SM persona) | `docs/sprints/` — 8 sprint plans, backlog, velocity tracker |
| **Developer Agent** | Claude Code (per-story) | Implementation, unit tests, DECISIONS.md entries |
| **QA Agent** | Claude Cowork (QA persona) | Sprint QA reports, 10 named critical test scenarios |
| **Product Owner** | Me (human in the loop) | Sprint demo approvals, scope decisions |

---

## 📦 Repository Structure

```
bmad-marketplace/
│
├── README.md                        # This file
│
├── planning/
│   └── PROMPT_CONTRACT.md           # Master 12-section requirements contract (input to all agents)
│
├── agent-briefs/
│   ├── PM_BRIEF.md                  # Instructions for PM agent persona
│   ├── ARCHITECT_BRIEF.md           # Instructions for Architect agent persona
│   ├── SCRUM_MASTER_BRIEF.md        # Instructions for SM agent persona
│   ├── DEVELOPER_BRIEF.md           # Instructions for Developer agent persona
│   └── QA_BRIEF.md                  # Instructions for QA agent persona
│
├── docs/
│   ├── PRD.md                       # Product Requirements Document (PM output)
│   ├── ARCHITECTURE.md              # System design document (Architect output)
│   ├── openapi.yaml                 # OpenAPI 3.1 spec (Architect output)
│   ├── schema.prisma                # Full database schema (Architect output)
│   ├── DEPLOYMENT.md                # Docker Compose + deployment topology
│   ├── SECURITY.md                  # Auth flow, RBAC, encryption strategy
│   ├── DECISIONS.md                 # Running log of autonomous agent decisions
│   │
│   ├── adr/
│   │   ├── ADR-001-ssr-vs-csr.md
│   │   ├── ADR-002-socketio-topology.md
│   │   ├── ADR-003-ephemeris-bridge.md
│   │   ├── ADR-004-redis-cache-strategy.md
│   │   ├── ADR-005-billing-loop-design.md
│   │   ├── ADR-006-wallet-transaction-isolation.md
│   │   ├── ADR-007-ai-content-pipeline.md
│   │   └── ADR-008-monorepo-structure.md
│   │
│   └── sprints/
│       ├── BACKLOG.md               # Full 76-story backlog across 11 epics
│       ├── SPRINT-0-plan.md
│       ├── SPRINT-1-plan.md
│       ├── SPRINT-2-plan.md
│       ├── SPRINT-3-plan.md
│       ├── SPRINT-4-plan.md
│       ├── SPRINT-5-plan.md
│       ├── SPRINT-6-plan.md
│       └── SPRINT-7-plan.md
│
└── METHODOLOGY.md                   # Lessons learned, token cost analysis, BMAD vs solo comparison
```

---

## 🏗️ Platform Scope

A two-sided astrology consultation marketplace with:

- **User side:** OTP/email/Google auth, Kundli birth chart generation, daily/weekly/monthly horoscopes, real-time chat consultations, wallet recharge, AstroMall commerce
- **Astrologer side:** Consultation acceptance, per-minute billing, schedule management, earnings dashboard
- **Platform:** Admin KPI dashboard, content management, transaction monitoring, promotional codes
- **Real-time engine:** Socket.io consultation rooms, BullMQ per-minute billing loop, PostgreSQL wallet with SELECT FOR UPDATE transaction isolation

---

## ⚡ Key Stats

| Metric | Value |
|---|---|
| Agent personas | 6 |
| User stories produced | 76 |
| Epics | 11 |
| Architecture Decision Records | 8 |
| Sprint plans | 8 (Sprint 0–7) |
| Estimated delivery timeline | 15 weeks |
| Token budgets consumed | 2 |
| Human time investment | ~12 hours (requirements authoring + PO reviews) |

---

## 💡 Key Methodology: The Prompt Contract

The single most impactful practice across this entire experiment was the **Prompt Contract** — a structured 12-section requirements document authored before activating any agent.

It covers:
- Product vision and success criteria
- Feature scope with priority tiers (P0/P1/P2)
- Mandated tech stack (non-negotiable per agent)
- Agent role definitions and handoff protocols
- Data models and API surface area
- Coding constraints and quality gates
- Comparison framework (BMAD vs Claude Code solo)

> Without the Prompt Contract, agent outputs are locally coherent but systemically broken. With it, each agent produces artifacts that feed the next without loss of context.

See [`planning/PROMPT_CONTRACT.md`](./planning/PROMPT_CONTRACT.md) for the full document.

---

## 🔑 Lessons Learned

1. **Requirements authoring is the real work.** 3 hours building the Prompt Contract saved weeks of downstream rework.
2. **Token budget hits are manageable** if your inputs are structured. Re-feeding context after a limit reset produced coherent continuations because the artifacts were well-formed.
3. **Agent role separation prevents rabbit holes.** Claude Code implementing one story at a time (not deciding what to build next) eliminated the classic AI failure mode of scope creep.
4. **ADRs are underrated.** Forcing the Architect agent to document trade-offs produced better architectural decisions than most human-led projects achieve.
5. **The PO role is non-negotiable.** Binary sprint acceptance criteria per sprint kept the process honest.

---

## 🔗 Related Projects

| Project | GitHub | Stack |
|---|---|---|
| Reddit Community Tracker | [asnarun75/reddit-alert-dashboard](https://github.com/asnarun75/reddit-alert-dashboard) | Python, FastAPI, PRAW, WhatsApp API |
| Distributed Order Management | [asnarun75/distributed-order-management](https://github.com/asnarun75/distributed-order-management) | Java 17, Kafka, ZooKeeper, Envoy |
| Real-Time Video Streaming Analytics | [asnarun75/RealTimeVideoStream](https://github.com/asnarun75/RealTimeVideoStream) | Java 17, Kafka, ClickHouse, Docker |

---

## 🎓 Certification

This project was built as part of hands-on learning following completion of Anthropic's **Claude Code in Action** course.

- **Certificate:** [verify.skilljar.com/c/yq5fvqcn6vbg](https://verify.skilljar.com/c/yq5fvqcn6vbg)
- **GitHub:** [github.com/asnarun75](https://github.com/asnarun75)

---

## 📄 License

MIT — feel free to use the prompt contracts, agent briefs, and methodology documentation for your own experiments.
