# ADR-001: SSR vs CSR — Next.js vs Vite

**Date:** 2026-03  
**Status:** Accepted  
**Decided by:** Architect Agent  
**Reviewed by:** Product Owner

---

## Context

The platform has two types of content with opposing rendering requirements:

1. **Horoscope content pages** (daily/weekly/monthly horoscope, Kundli info, zodiac pages) — highly SEO-sensitive. These pages need to rank in search results for queries like "Aries daily horoscope today". Server-side rendering (SSR) or static generation (SSG) is strongly preferred.

2. **Application pages** (consultation chat, wallet, dashboard, Kundli form) — highly interactive, real-time, user-authenticated. Client-side rendering (CSR) is acceptable and preferred for lower server load.

The stack mandates React 18 + TypeScript. The decision is whether to use **Next.js** (SSR/SSG capable) or **Vite** (CSR by default, SSR possible but manual).

---

## Decision

**Use Next.js 14 (App Router) for the entire frontend.**

---

## Rationale

| Factor | Next.js | Vite (CSR) |
|---|---|---|
| Horoscope SEO | ✅ Native SSG/ISR | ❌ Requires manual SSR setup |
| App Router file-based routing | ✅ Built-in | ❌ Requires React Router |
| Streaming + Suspense | ✅ Native | ⚠️ Manual |
| Real-time pages (chat) | ✅ Client components | ✅ Full CSR |
| Deployment complexity | ⚠️ Node server required | ✅ Static files |
| Team familiarity (assumed) | ✅ Widely known | ✅ Widely known |

**SEO is the deciding factor.** Horoscope content is the primary organic acquisition channel for a platform of this type. Missing SSR/SSG on these pages would be a structural disadvantage that is very expensive to retrofit later.

---

## Consequences

- All pages under `/horoscope/*`, `/kundli/info/*`, `/blog/*`, `/zodiac/*` use **Server Components** or **generateStaticParams** for SSG.
- All authenticated/interactive pages (`/dashboard`, `/chat`, `/wallet`) use **Client Components** with `'use client'` directive.
- Docker Compose must include a Node.js server for the Next.js frontend (not purely static file serving).
- `DEPLOYMENT.md` must document the Node server requirement.

---

## Alternatives Considered

- **Vite + manual SSR:** Possible but adds significant complexity with no ecosystem benefit over Next.js for this use case.
- **Remix:** Stronger SSR story but smaller ecosystem; team familiarity lower; ruled out.
- **Astro:** Excellent for content-heavy sites but poor fit for highly interactive consultation and wallet flows.
