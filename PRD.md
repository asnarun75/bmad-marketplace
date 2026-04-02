# PRD.md — AstroTalk Replica (Track B · BMAD Framework)

**Document Status:** Draft v1.0 — Pending PO Review
**Produced by:** PM Agent (BMAD Persona 1)
**Date:** March 2026
**Product Owner:** Arun
**Companion:** Track A Architecture Plan (Laravel stack) — comparison target

---

## Table of Contents

1. [Product Vision & Goals](#1-product-vision--goals)
2. [Target Personas](#2-target-personas)
3. [Scope Boundary](#3-scope-boundary)
4. [PM Assumptions Log](#4-pm-assumptions-log)
5. [Epic Overview & Priority Matrix](#5-epic-overview--priority-matrix)
6. [Epic: AUTH — Authentication & Profiles](#epic-auth--authentication--profiles)
7. [Epic: ASTR — Astrologer Directory & Profiles](#epic-astr--astrologer-directory--profiles)
8. [Epic: KUNDL — Kundli Engine](#epic-kundl--kundli-engine)
9. [Epic: HORO — Horoscope Content](#epic-horo--horoscope-content)
10. [Epic: CHAT — Consultation Chat & Billing](#epic-chat--consultation-chat--billing)
11. [Epic: WALLET — Wallet & Payments](#epic-wallet--wallet--payments)
12. [Epic: ADMIN — Admin Panel](#epic-admin--admin-panel)
13. [Epic: MALL — AstroMall](#epic-mall--astromall)
14. [Epic: CONTENT — Blog & Tools](#epic-content--blog--tools)
15. [Epic: NOTIF — Notifications](#epic-notif--notifications)
16. [Epic: INFRA — Infrastructure & DevOps](#epic-infra--infrastructure--devops)
17. [Open Questions Log](#17-open-questions-log)
18. [Domain Glossary](#18-domain-glossary)

---

## 1. Product Vision & Goals

### 1.1 Vision Statement

Build a production-grade, two-sided astrology marketplace modelled on AstroTalk.com with 75–80% feature parity. Users access personalised Vedic astrology services (horoscopes, Kundli charts, live consultations). Astrologers earn per-minute fees through a transparent billing system. The platform earns commission on every consultation.

### 1.2 Success Criteria

| Criterion | Target |
|-----------|--------|
| Feature parity with AstroTalk.com | ≥ 75% of core features functional |
| Billing loop accuracy | Per-minute deduction error ≤ 0 (strict) |
| Astrological computation | Lahiri Ayanamsa enforced; Swiss Ephemeris authoritative |
| P0 stories accepted by PO | 100% before Sprint 3 close |
| Track B vs Track A | Comparable or superior on ≥ 6 of 10 dimensions |

### 1.3 Out of Scope (v1)

- Voice and video consultations
- React Native / mobile app
- Real payment gateway integration (Stripe, Razorpay — mock only)
- Multi-language support (English only)
- Cryptocurrency payments
- Astrologer live streaming
- AI-generated images / horoscope cards
- SMS OTP fallback (Firebase Auth only)

---

## 2. Target Personas

| Persona | Goal | Pain Point Solved |
|---------|------|-------------------|
| **Anonymous Visitor** | Explore horoscopes, browse astrologers, read blog | Free instant access — no account required |
| **Registered User (Seeker)** | Book real-time chat consultations, generate Kundli, get personalised predictions | On-demand access to astrologers 24/7; no travel or appointments |
| **Astrologer** | Accept consultations, manage schedule, earn income, build reputation | Wider audience reach; streamlined per-minute billing; earnings transparency |
| **Platform Admin** | Manage users, content, transactions, platform health | Full operational visibility; moderation and scaling tools |

---

## 3. Scope Boundary

### 3.1 In Scope

- Authentication: OTP (Firebase), email/password, Google OAuth
- User and astrologer profiles with birth details and PII encryption
- Kundli engine: ephemeris computation, SVG chart, AI narrative, PDF export, matching
- Horoscope content: daily/weekly/monthly for all 12 signs + Panchang + Muhurat
- Real-time consultation chat with per-minute billing loop and auto-disconnect
- Wallet: mock recharge, ledger, cashback, astrologer payout, refund
- AstroMall: catalogue, cart, mock checkout, order history, wishlist
- Blog and tools: numerology, compatibility checker, baby name generator
- Admin panel: KPI, user/astrologer management, content CRUD, promo codes
- Notifications: in-app bell, transactional email, low-wallet alert

### 3.2 Mandated Technology Stack (Non-Negotiable)

| Layer | Technology |
|-------|-----------|
| Monorepo | pnpm workspaces (packages/web, packages/api, packages/shared) |
| Frontend | React 18 + Vite + TypeScript strict + Tailwind CSS + Shadcn/UI |
| State | Zustand (UI) + TanStack Query (server state) |
| Backend | Node.js + Express + TypeScript strict |
| Auth | Passport.js + JWT (15m access / 7d refresh) + Firebase Auth |
| Database | PostgreSQL 16 + Prisma ORM |
| Cache/Queue | Redis (ioredis) + BullMQ |
| Storage | AWS S3 (presigned URLs) |
| Astrology | node-swisseph + Python sidecar (flatlib) |
| AI Content | Anthropic Claude API via ContentService |
| Real-time | Socket.io |
| CI/CD | GitHub Actions → Docker → ECS or Cloud Run |

---

## 4. PM Assumptions Log

| ID | Assumption | Impact if Wrong |
|----|-----------|-----------------|
| A1 | Track B stays on Node.js stack (not Laravel) | Architecture docs would need to change |
| A2 | Firebase Auth is sole OTP provider | Auth epic stories reference Firebase only |
| A3 | Mock payment: simulated card form, no real gateway | Wallet stories use mock success/failure |
| A4 | Currency: INR; 1 Coin = ₹1 | All wallet stories denominated in INR/Coins |
| A5 | Text chat only; voice/video out of scope | CHAT epic scoped to text only |
| A6 | Web-responsive React; no React Native | No mobile app stories in backlog |
| A7 | English only for v1 | No i18n stories |
| A8 | Self-register → admin approval for astrologers | ASTR onboarding includes approval gate |
| A9 | Every new registered user: one free 5-minute consultation | CHAT-008 story includes eligibility check |
| A10 | Notifications: in-app bell + email only | No browser push stories |

---

## 5. Epic Overview & Priority Matrix

| Epic Code | Epic Name | Stories | Priority | Sprint Window | Points Est. |
|-----------|-----------|---------|----------|---------------|-------------|
| INFRA | Infrastructure & DevOps | 4 | P0 | Sprint 0 | 21 |
| AUTH | Authentication & Profiles | 8 | P0 | Sprint 0–1 | 42 |
| ASTR | Astrologer Directory | 7 | P0 | Sprint 1 | 34 |
| CHAT | Consultation Chat & Billing | 9 | P0 | Sprint 3 | 55 |
| WALLET | Wallet & Payments | 7 | P0/P1 | Sprint 3–4 | 38 |
| KUNDL | Kundli Engine | 9 | P0/P1 | Sprint 2 | 51 |
| HORO | Horoscope Content | 8 | P0/P1 | Sprint 2, 5 | 34 |
| ADMIN | Admin Panel | 8 | P0/P1 | Sprint 4 | 42 |
| CONTENT | Blog & Tools | 5 | P1/P2 | Sprint 5–6 | 22 |
| MALL | AstroMall | 6 | P1/P2 | Sprint 6 | 28 |
| NOTIF | Notifications | 5 | P1/P2 | Sprint 6 | 18 |
| **TOTAL** | | **76** | | | **385** |

**Priority Definitions:**
- **P0** — Must ship in Sprint 1–3; blocks all other work
- **P1** — Ship in Sprint 4–6; core product completeness
- **P2** — Ship in Sprint 7 or defer to v1.1

---

## Epic: INFRA — Infrastructure & DevOps

**Epic Goal:** Establish a fully working local development environment, CI/CD pipeline, and database schema so all subsequent development can start without environment blockers.

---

### STORY-INFRA-001: Monorepo Scaffold and Local Dev Environment

**Persona:** As a developer,
**I want:** a pnpm monorepo with packages/web, packages/api, packages/shared, Docker Compose, and ESLint/Prettier/TypeScript strict configured,
**So that:** all team members can `docker-compose up` and have a working local environment within 10 minutes.

**Acceptance Criteria:**

```
Given a fresh clone of the repository
When the developer runs `docker-compose up`
Then the API server starts on port 4000, the web app on port 3000, PostgreSQL on 5432, and Redis on 6379
And all health check endpoints return 200 OK

Given the TypeScript compiler is run across all packages
When `pnpm run typecheck` is executed from the monorepo root
Then it exits with code 0 and zero errors

Given ESLint and Prettier are configured
When `pnpm run lint` is run
Then it exits with code 0 and zero violations
```

**Out of scope:** Production deployment, CI/CD pipeline (separate story).
**Technical Notes:** pnpm workspace; shared tsconfig extending strict base; packages/shared must be built before api and web.
**Story Points:** 8
**Dependencies:** None
**Definition of Done:** docker-compose up produces running services; CI passes.

---

### STORY-INFRA-002: PostgreSQL Schema Migration via Prisma

**Persona:** As a developer,
**I want:** the complete Prisma schema applied to the local PostgreSQL database via `prisma migrate dev`,
**So that:** all tables, indexes, enums, and relations are created correctly and seed data can be loaded.

**Acceptance Criteria:**

```
Given the Docker Compose environment is running
When `pnpm prisma migrate dev` is run from packages/api
Then all migrations apply without error and schema.prisma models match the live database

Given the migration has been run
When `pnpm prisma db seed` is executed
Then seed data (10 astrologers, 12 zodiac signs, 27 Nakshatras, 9 Grahas, 12 Bhavas, 50 Yogas, 5 AstroMall categories × 5 products) is present in the database

Given a wallet_balance column exists on the users table
When inspected via psql
Then it is of type Decimal(10,2) and NOT Float
```

**Out of scope:** Data migration from existing systems.
**Technical Notes:** Prisma schema must include composite index on consultations(status, start_at); unique on reviews(consultation_id); unique on panchang_cache(date, location_key).
**Story Points:** 5
**Dependencies:** INFRA-001
**Definition of Done:** `prisma migrate dev` and `prisma db seed` succeed cleanly.

---

### STORY-INFRA-003: GitHub Actions CI Pipeline

**Persona:** As a developer,
**I want:** a GitHub Actions workflow that runs typecheck, lint, unit tests, and builds Docker images on every push to main and on every PR,
**So that:** no broken code can reach main branch.

**Acceptance Criteria:**

```
Given a pull request is opened against main
When the PR CI workflow runs
Then it runs `pnpm typecheck`, `pnpm lint`, `pnpm test`, and `pnpm build` in sequence

Given any of the above steps fail
When the CI completes
Then the PR is marked as failing and merge is blocked

Given all steps pass
When the CI completes
Then a Docker image is built and pushed to the container registry with the commit SHA as tag
```

**Out of scope:** Automatic production deployment (manual trigger only in v1).
**Technical Notes:** GitHub Actions matrix for Node 20; pnpm caching; Docker BuildKit.
**Story Points:** 5
**Dependencies:** INFRA-001
**Definition of Done:** CI runs on PR open; merge blocked on failure.

---

### STORY-INFRA-004: BullMQ Worker Process and Redis Connection

**Persona:** As a developer,
**I want:** a BullMQ worker process connected to Redis that can process background jobs (horoscope generation, email dispatch, billing ticks),
**So that:** all background work runs reliably outside the request/response cycle.

**Acceptance Criteria:**

```
Given the Docker Compose environment is running
When the worker process starts
Then it connects to Redis successfully and logs "BullMQ worker ready" with queue names

Given a test job is dispatched to the horoscope-generation queue
When the worker processes it
Then it logs the job ID, processes it, and marks it as complete

Given Redis is temporarily unavailable
When the worker attempts to process a job
Then it retries with exponential backoff (1s, 2s, 4s) before failing and logging the error
```

**Out of scope:** Specific job implementations (covered per epic).
**Technical Notes:** BullMQ sandbox processors; separate worker entrypoint (packages/api/src/worker.ts); no setInterval() in production code.
**Story Points:** 3
**Dependencies:** INFRA-001, INFRA-002
**Definition of Done:** Worker starts, connects to Redis, processes a test job.

---

## Epic: AUTH — Authentication & Profiles

**Epic Goal:** Users can register and log in using OTP, email/password, or Google OAuth. Profiles store birth details used across Kundli and horoscope features. PII is encrypted at rest.

---

### STORY-AUTH-001: OTP Login via Firebase Auth

**Persona:** As an anonymous visitor,
**I want:** to enter my phone number and receive an OTP to log in without setting a password,
**So that:** I can access the platform quickly without remembering credentials.

**Acceptance Criteria:**

```
Given I am on the login page
When I enter a valid 10-digit phone number and submit
Then Firebase Auth sends an OTP SMS to that number
And the UI shows an OTP input field with a 60-second resend countdown

Given I have received the OTP
When I enter the correct 6-digit code within 5 minutes
Then the API verifies the Firebase ID token, creates or retrieves my user record, and returns a JWT access token (15m TTL) and sets an httpOnly refresh cookie (7d TTL)
And I am redirected to the home dashboard

Given I enter an incorrect OTP
When I submit the code
Then I see the error "Invalid OTP. Please try again." and the attempt is logged
And after 5 failed attempts the OTP is invalidated and I must request a new one
```

**Out of scope:** SMS provider fallback; TOTP (Google Authenticator).
**Technical Notes:** Firebase ID token verified server-side via Firebase Admin SDK; Passport.js JWT strategy for subsequent requests.
**Story Points:** 8
**Dependencies:** INFRA-001, INFRA-004
**Definition of Done:** OTP flow works end-to-end; JWT returned; refresh cookie set.

---

### STORY-AUTH-002: Email/Password Registration and Login

**Persona:** As an anonymous visitor,
**I want:** to register with my email and password and log in with those credentials,
**So that:** I have a persistent account without requiring a phone number.

**Acceptance Criteria:**

```
Given I am on the registration page
When I submit a valid email, a password (min 8 chars, 1 uppercase, 1 number), and confirm password
Then a new user record is created with hashed password (bcrypt, cost 12), a verification email is sent, and I am shown "Please verify your email"

Given I click the verification link in the email
When the token is valid (TTL 24h)
Then my email is marked as verified and I am redirected to the login page with a success toast

Given I am on the login page with a verified email
When I submit correct email and password
Then I receive a JWT access token and httpOnly refresh cookie identical to the OTP flow

Given I submit an incorrect password
When the login attempt is made
Then I see "Invalid email or password" (no distinction between wrong email and wrong password)
And after 10 failed attempts in 15 minutes the account is rate-limited for 15 minutes
```

**Out of scope:** Social email providers (Gmail-specific login beyond OAuth in AUTH-003).
**Technical Notes:** bcrypt hash stored in users.password_hash; rate limit via Redis key per email.
**Story Points:** 5
**Dependencies:** INFRA-001
**Definition of Done:** Register → verify email → login → JWT issued.

---

### STORY-AUTH-003: Google OAuth Login

**Persona:** As an anonymous visitor,
**I want:** to log in with my Google account using one click,
**So that:** I can access the platform without entering credentials.

**Acceptance Criteria:**

```
Given I click "Continue with Google" on the login page
When I complete the Google OAuth consent flow
Then I am redirected back with a Firebase Google credential, the server creates or retrieves my user record using my Google email, and I receive a JWT + refresh cookie

Given I have previously registered with the same email via email/password
When I log in with Google using that email
Then my existing account is found and linked to the Google provider
And no duplicate account is created

Given the Google OAuth callback fails (network error)
When I am redirected back
Then I see "Google login failed. Please try again." with a retry button
```

**Out of scope:** Apple Sign In, Facebook Login.
**Technical Notes:** Firebase Auth Google provider; passport-google-oauth20 strategy.
**Story Points:** 5
**Dependencies:** AUTH-001
**Definition of Done:** Google OAuth → account created/linked → JWT issued.

---

### STORY-AUTH-004: JWT Token Refresh

**Persona:** As a logged-in user,
**I want:** my session to transparently refresh before my access token expires,
**So that:** I am not unexpectedly logged out during active use.

**Acceptance Criteria:**

```
Given my access token is within 60 seconds of expiry
When I make any authenticated API request
Then the API returns a new access token in the response header (X-Access-Token)
And the client stores the new token in memory (never localStorage)

Given my refresh token has expired (>7d)
When my access token expires and a refresh is attempted
Then the API returns 401 with {"error": "SESSION_EXPIRED"}
And the client clears the cookie and redirects me to the login page

Given the refresh endpoint is called with a valid httpOnly cookie
When POST /auth/refresh is received
Then a new access token is issued and the refresh cookie TTL is extended
```

**Out of scope:** Multi-device session management.
**Technical Notes:** Access token: memory-only (never localStorage/sessionStorage); refresh token: httpOnly Secure SameSite=Strict cookie.
**Story Points:** 3
**Dependencies:** AUTH-001
**Definition of Done:** Token refresh works; expired session redirects to login.

---

### STORY-AUTH-005: User Profile — View and Edit

**Persona:** As a registered user,
**I want:** to view and update my profile including my name, birth details, profile photo, and preferred language,
**So that:** my Kundli and horoscope content is personalised to me.

**Acceptance Criteria:**

```
Given I am logged in and navigate to My Profile
When the page loads
Then I see my display name, email/phone, profile photo, and birth details (DOB, TOB, birth city, gender) if set

Given I click Edit Profile
When I submit valid updated birth details (DOB as date, TOB as HH:MM, birth city as text)
Then the values are saved with DOB, TOB, and birth_city AES-256-GCM encrypted in the database
And a success toast "Profile updated" is shown

Given I upload a new profile photo
When the file is ≤ 5 MB and is JPEG/PNG
Then it is uploaded to S3 via presigned URL and the profile_photo_url is updated in the database
And the new photo appears immediately in the header
```

**Out of scope:** Profile deletion (separate story); public profile URL.
**Technical Notes:** CryptoService used for DOB/TOB/birth_city/phone encryption; S3 presigned PUT URL for photo upload; photo stored at users/{userId}/avatar.{ext}.
**Story Points:** 5
**Dependencies:** AUTH-001, INFRA-002
**Definition of Done:** Profile save/load works; PII encrypted in DB; photo upload to S3.

---

### STORY-AUTH-006: Saved Kundlis on Profile

**Persona:** As a registered user,
**I want:** to see all my saved Kundli charts on my profile page,
**So that:** I can access previous birth chart analyses without re-entering birth details.

**Acceptance Criteria:**

```
Given I am on my Profile page
When I click "My Kundlis"
Then I see a list of my saved Kundlis with chart name, date of generation, and a thumbnail

Given I click on a saved Kundli
When the Kundli detail page loads
Then I see the full SVG chart, planetary table, and AI-generated narrative without re-generating

Given I have no saved Kundlis
When I view "My Kundlis"
Then I see an empty state with a CTA "Generate your first Kundli"
```

**Out of scope:** Sharing Kundlis with other users; Kundli deletion.
**Technical Notes:** GET /users/:id/kundlis returns paginated list; Kundli records linked via kundlis.user_id FK.
**Story Points:** 3
**Dependencies:** AUTH-005, KUNDL-001
**Definition of Done:** Saved Kundli list renders; click navigates to detail.

---

### STORY-AUTH-007: Account Logout

**Persona:** As a logged-in user,
**I want:** to log out of my account,
**So that:** my session is terminated and my data is not accessible to anyone else using the device.

**Acceptance Criteria:**

```
Given I click the Logout button in the navigation
When the logout request is sent
Then POST /auth/logout clears the httpOnly refresh cookie server-side
And the client clears the in-memory access token
And I am redirected to the login page

Given I am logged in on multiple tabs
When I log out from one tab
When I attempt an API call from another tab
Then I receive a 401 response and am redirected to login

Given my refresh token has been revoked
When I attempt POST /auth/refresh
Then I receive 401 with {"error": "TOKEN_REVOKED"}
```

**Out of scope:** Remote logout from other devices.
**Technical Notes:** Refresh tokens stored in Redis; logout deletes the Redis key.
**Story Points:** 2
**Dependencies:** AUTH-004
**Definition of Done:** Logout clears cookie and Redis token; subsequent requests return 401.

---

### STORY-AUTH-008: Account Deletion

**Persona:** As a registered user,
**I want:** to permanently delete my account and all associated data,
**So that:** my personal information is removed from the platform in compliance with data privacy expectations.

**Acceptance Criteria:**

```
Given I navigate to Account Settings
When I click "Delete Account" and confirm via a typed phrase "DELETE"
Then a soft-delete flag is set (users.deleted_at timestamp) and I am logged out immediately

Given my account is soft-deleted
When I attempt to log in with the same credentials within 30 days
Then I see "Your account is scheduled for deletion. Contact support to restore it."
And no new consultations can be started

Given 30 days have passed since soft-delete
When the nightly purge job runs
Then my PII fields (dob, tob, birth_city, phone, email) are overwritten with null
And my user record is retained as a skeleton for billing audit purposes
```

**Out of scope:** Immediate hard-delete of S3 assets (async cleanup job).
**Technical Notes:** Purge handled by BullMQ nightly job; soft-delete pattern preserves audit trail.
**Story Points:** 5
**Dependencies:** AUTH-007, INFRA-004
**Definition of Done:** Soft-delete sets flag; purge job clears PII after 30d.

---

## Epic: ASTR — Astrologer Directory & Profiles

**Epic Goal:** Users can browse, filter, and view astrologer profiles. Astrologers can onboard, manage their availability, and view their earnings.

---

### STORY-ASTR-001: Astrologer Directory Listing

**Persona:** As an anonymous visitor,
**I want:** to browse a paginated list of verified astrologers with filters for speciality, language, rating, and price,
**So that:** I can find the right astrologer for my needs without signing up first.

**Acceptance Criteria:**

```
Given I navigate to the Astrologers page
When the page loads
Then I see a grid of astrologer cards showing photo, name, speciality tags, rating (1–5 stars), experience years, per-minute rate, and online/offline badge

Given I apply a filter (e.g., Speciality: Vedic, Min Rating: 4)
When the filter is applied
Then only astrologers matching all active filters are shown
And the URL updates with filter params for shareability

Given 100+ astrologers exist
When I scroll to the bottom of the list
Then the next page loads automatically (infinite scroll, page size 20)
And the total count is shown ("Showing 20 of 143 astrologers")
```

**Out of scope:** Map view of astrologers.
**Technical Notes:** GET /astrologers supports query params: speciality, language, minRating, maxRate, page, pageSize; Redis cache TTL 5 minutes for directory listing.
**Story Points:** 5
**Dependencies:** INFRA-002 (seed astrologers)
**Definition of Done:** Directory renders seed astrologers; filters work; pagination works.

---

### STORY-ASTR-002: Astrologer Detail Page

**Persona:** As an anonymous visitor,
**I want:** to view a detailed profile page for a specific astrologer,
**So that:** I can read their bio, specialities, reviews, and decide whether to book a consultation.

**Acceptance Criteria:**

```
Given I click on an astrologer card in the directory
When the detail page loads
Then I see: photo, full name, verified badge, bio (up to 500 words), specialities list, languages spoken, experience years, per-minute rate, total consultations count, rating distribution, and the 5 most recent reviews

Given the astrologer is currently Online
When the detail page loads
Then a green "Available Now" badge is shown and a "Start Consultation" CTA is enabled

Given the astrologer is Offline
When the detail page loads
Then a grey "Offline" badge is shown and the "Start Consultation" CTA is disabled with tooltip "Astrologer is currently offline"
```

**Out of scope:** Astrologer scheduling/calendar (v2).
**Technical Notes:** GET /astrologers/:id; availability driven by Socket.io presence (ASTR-005).
**Story Points:** 5
**Dependencies:** ASTR-001
**Definition of Done:** Detail page renders all fields; online/offline badge reflects real-time status.

---

### STORY-ASTR-003: Astrologer Self-Registration (Onboarding Form)

**Persona:** As a prospective astrologer,
**I want:** to submit an onboarding application with my credentials, specialities, and experience,
**So that:** I can be reviewed and approved by the admin to join the platform.

**Acceptance Criteria:**

```
Given I navigate to /astrologers/onboard
When I complete and submit the onboarding form (name, phone, email, years_experience, specialities[], languages[], bio, per_minute_rate, profile_photo)
Then a new astrologer record is created with status = PENDING_APPROVAL
And the admin receives an in-app notification of the new application
And I see "Application submitted. You will be notified once reviewed."

Given I submit the form without required fields
When validation runs
Then I see inline validation errors per field; form is not submitted

Given I have already submitted an application
When I attempt to submit again with the same email
Then I see "An application with this email already exists."
```

**Out of scope:** Document verification upload (v2).
**Technical Notes:** POST /astrologers/onboard; status enum: PENDING_APPROVAL, APPROVED, REJECTED, SUSPENDED.
**Story Points:** 5
**Dependencies:** AUTH-001, INFRA-002
**Definition of Done:** Form submits; record created with PENDING_APPROVAL; admin notified.

---

### STORY-ASTR-004: Astrologer Profile Edit (Astrologer Portal)

**Persona:** As an approved astrologer,
**I want:** to update my bio, specialities, profile photo, and per-minute rate from my dashboard,
**So that:** my profile stays accurate and attractive to potential clients.

**Acceptance Criteria:**

```
Given I am logged in as an approved astrologer and navigate to My Profile
When I update my bio and per-minute rate and save
Then the changes are saved via PUT /astrologers/me and my public profile reflects the updates within 30 seconds

Given I upload a new profile photo
When the file is ≤ 5 MB and is JPEG/PNG
Then it is uploaded to S3 and my profile photo is updated

Given I set my per-minute rate below the platform minimum (1 Coin/min)
When I attempt to save
Then I see "Rate must be at least 1 Coin per minute" and the form is not saved
```

**Out of scope:** Changing onboarding credentials (name, experience) without admin re-approval.
**Technical Notes:** PUT /astrologers/me requires astrologer role JWT; S3 presigned PUT URL.
**Story Points:** 3
**Dependencies:** ASTR-003, AUTH-001
**Definition of Done:** Profile edits persist; photo uploads to S3.

---

### STORY-ASTR-005: Astrologer Real-Time Availability Toggle

**Persona:** As an approved astrologer,
**I want:** to toggle my availability status between Online and Offline from my dashboard,
**So that:** seekers only see me as available when I am ready to accept consultations.

**Acceptance Criteria:**

```
Given I am logged in as an approved astrologer
When I toggle the availability switch to Online
Then my status is updated in the database (astrologers.is_online = true) and propagated via Socket.io to all connected clients within 2 seconds

Given I toggle back to Offline
When the toggle is switched
Then seekers viewing my detail page see the "Offline" badge immediately (within 2 seconds)

Given I disconnect from the app without toggling Offline (e.g., browser crash)
When 90 seconds have passed without a heartbeat
Then the server marks me Offline automatically and notifies subscribed clients
```

**Out of scope:** Scheduled availability (v2 calendar feature).
**Technical Notes:** Socket.io presence room per astrologer; heartbeat ping every 30s; server-side timeout after 3 missed pings.
**Story Points:** 5
**Dependencies:** ASTR-003, INFRA-004
**Definition of Done:** Toggle updates DB and propagates to clients in ≤ 2s; disconnect auto-sets offline.

---

### STORY-ASTR-006: Astrologer Earnings Dashboard

**Persona:** As an approved astrologer,
**I want:** to view my total earnings, session history, and pending payout from my dashboard,
**So that:** I have full transparency into my income from the platform.

**Acceptance Criteria:**

```
Given I am logged in as an approved astrologer and navigate to Earnings
When the page loads
Then I see: total lifetime earnings, earnings this month, pending payout balance, and a paginated list of completed sessions with: user (anonymised first name + last initial), date, duration minutes, rate, amount earned

Given I click "Request Payout"
When my pending balance is ≥ 100 Coins
Then a payout request record is created with status PENDING_ADMIN_APPROVAL
And I see "Payout of ₹X requested. Processing within 3–5 business days."

Given my pending balance is < 100 Coins
When I click "Request Payout"
Then I see "Minimum payout is ₹100. Your current balance is ₹X."
```

**Out of scope:** Real bank transfer; UPI integration (mock only).
**Technical Notes:** Earnings derived from consultations table; platform commission applied; payout_requests table.
**Story Points:** 5
**Dependencies:** ASTR-003, WALLET-005
**Definition of Done:** Earnings dashboard renders real data; payout request creates record.

---

### STORY-ASTR-007: Verified Astrologer Badge

**Persona:** As a seeker,
**I want:** to see a "Verified" badge on astrologers who have been reviewed and approved by the platform,
**So that:** I can trust that the astrologer's credentials have been validated.

**Acceptance Criteria:**

```
Given an astrologer's status is APPROVED
When their card or profile page is rendered
Then a blue "Verified" badge is displayed next to their name

Given an astrologer's status is PENDING_APPROVAL or SUSPENDED
When their profile is rendered
Then no Verified badge is shown
And their profile does not appear in the public directory

Given an admin changes an astrologer's status from APPROVED to SUSPENDED
When the directory is refreshed
Then the astrologer no longer appears in the listing
```

**Out of scope:** Third-party credential verification.
**Technical Notes:** astrologers.status enum drives visibility; directory query filters on status = APPROVED.
**Story Points:** 2
**Dependencies:** ASTR-001, ADMIN-002
**Definition of Done:** Badge renders for APPROVED only; non-APPROVED astrologers hidden from directory.

---

## Epic: KUNDL — Kundli Engine

**Epic Goal:** Users can generate a full Vedic birth chart (Kundli) by entering birth details. The system computes planetary positions using Swiss Ephemeris, renders an SVG chart, produces an AI narrative, supports Kundli matching (Gun Milan), and exports a PDF.

---

### STORY-KUNDL-001: Kundli Generation Form

**Persona:** As a registered user,
**I want:** to enter my birth details (name, DOB, TOB, birth city, gender) and generate a Kundli,
**So that:** I receive a personalised Vedic birth chart.

**Acceptance Criteria:**

```
Given I am on the Kundli page
When I submit a valid form (name, date of birth, time of birth, birth city)
Then POST /kundli/generate is called with the birth details
And a Kundli record is created in the database
And I am redirected to the Kundli result page

Given I omit the Time of Birth (TOB)
When the Kundli is generated
Then the chart renders without the Lagna (Ascendant)
And a yellow warning banner reads: "Time of birth not provided — Lagna (Ascendant) cannot be calculated"
And all other planets are computed correctly

Given I submit an invalid date of birth (future date)
When validation runs
Then I see "Date of birth must be in the past" and the form is not submitted
```

**Out of scope:** Chart for deceased persons (no special handling); celebrity chart lookup.
**Technical Notes:** POST /kundli/generate calls the Python sidecar (flatlib) via JSON IPC bridge; Lahiri Ayanamsa (SIDM_LAHIRI) enforced; node-swisseph authoritative for planet positions.
**Story Points:** 8
**Dependencies:** INFRA-002, AUTH-001
**Definition of Done:** Form submits; Kundli record created; Lagna warning shown when TOB absent.

---

### STORY-KUNDL-002: SVG Birth Chart Rendering

**Persona:** As a registered user,
**I want:** to see my birth chart rendered as an SVG diagram in the North Indian or South Indian style,
**So that:** I can visually understand my planetary placements at birth.

**Acceptance Criteria:**

```
Given a Kundli has been generated with full birth details
When the Kundli result page loads
Then a valid SVG birth chart is rendered showing all 12 Bhavas and all 9 Grahas in their correct positions

Given the user selects "South Indian" style from the chart style toggle
When the toggle is applied
Then the SVG re-renders in South Indian grid format without page reload

Given the SVG chart is viewed on a mobile screen (375px wide)
When the page is loaded on mobile
Then the chart fits within the viewport and all house labels are legible
```

**Out of scope:** 3D chart visualisation; Western tropical chart.
**Technical Notes:** kerylia/astrochart npm package for SVG rendering; chart style preference stored in user localStorage.
**Story Points:** 8
**Dependencies:** KUNDL-001
**Definition of Done:** SVG chart renders correctly for test birth data; N/S Indian style toggle works.

---

### STORY-KUNDL-003: Planetary Table

**Persona:** As a registered user,
**I want:** to see a table of all 9 Vedic Grahas with their sign, degree, nakshatra, house, and dignity,
**So that:** I can understand the precise placements without reading the chart visually.

**Acceptance Criteria:**

```
Given the Kundli result page has loaded
When I scroll to the Planetary Table section
Then I see a table with columns: Planet, Sign, Degrees, Nakshatra, House (Bhava), Dignity (Exalted/Debilitated/Neutral/Own Sign)
And all 9 Grahas (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu) are present

Given I hover over a planet name
When the tooltip appears
Then it shows the Vedic significance of that Graha (from seed data)

Given the birth chart was generated without TOB
When the planetary table renders
Then the House (Bhava) column shows "—" for all planets with a note "House positions require time of birth"
```

**Out of scope:** Arabic parts; fixed stars.
**Technical Notes:** Planet data from node-swisseph; dignity computed from sign position constants; nakshatra derived from longitude (each nakshatra = 13°20').
**Story Points:** 5
**Dependencies:** KUNDL-001
**Definition of Done:** Planetary table renders 9 Grahas with correct data for test birth date.

---

### STORY-KUNDL-004: AI-Generated Kundli Narrative

**Persona:** As a registered user,
**I want:** to read an AI-generated narrative interpretation of my birth chart,
**So that:** I understand what my planetary placements mean in plain language without needing astrological expertise.

**Acceptance Criteria:**

```
Given a Kundli has been computed with planetary positions
When the AI narrative is requested
Then ContentService checks Redis for a cached narrative keyed by kundli_id
And on cache miss calls the Claude API with the planet positions, sign placements, and house positions as context
And the returned narrative (500–800 words) is stored in Redis with TTL 7 days and saved to the kundlis.ai_narrative column

Given the Claude API is unavailable
When ContentService retries 3 times (1s, 2s, 4s backoff) and all fail
Then a graceful fallback narrative ("Your chart shows significant planetary influence. A detailed reading is temporarily unavailable.") is shown

Given the narrative has been generated
When I revisit the Kundli page
Then the narrative loads from the database in < 200ms without calling the Claude API
```

**Out of scope:** Real-time re-generation; personalised follow-up questions.
**Technical Notes:** ContentService pattern: Redis cache-first → Claude API on miss → 3x retry → fallback. Claude interprets; never computes positions.
**Story Points:** 8
**Dependencies:** KUNDL-003, INFRA-004
**Definition of Done:** Narrative generated and cached; fallback shown on API failure.

---

### STORY-KUNDL-005: Vimshottari Dasha Timeline

**Persona:** As a registered user,
**I want:** to see my current and upcoming Dasha and Antardasha periods on a timeline,
**So that:** I can understand which planetary period governs my life and when it changes.

**Acceptance Criteria:**

```
Given a Kundli has been generated with date of birth
When I view the Dasha section
Then I see the Mahadasha sequence from birth calculated using the Vimshottari system: Ketu(7y) → Venus(20y) → Sun(6y) → Moon(10y) → Mars(7y) → Rahu(18y) → Jupiter(16y) → Saturn(19y) → Mercury(17y)
And the current active Mahadasha and Antardasha are highlighted with start and end dates

Given today's date falls within a Mahadasha period
When the timeline renders
Then the current period is visually highlighted and a label "Current Period" is shown

Given a user has DOB but no TOB
When the Dasha timeline is computed
Then the Moon's nakshatra at birth is still used for Dasha calculation (TOB affects only Lagna, not Dasha start planet)
```

**Out of scope:** Pratyantardasha (3rd level); Sookshma Dasha.
**Technical Notes:** Vimshottari sequence hardcoded in packages/shared/src/constants.ts; Dasha start date derived from Moon nakshatra position.
**Story Points:** 5
**Dependencies:** KUNDL-001
**Definition of Done:** Dasha timeline renders for test DOB; current period highlighted correctly.

---

### STORY-KUNDL-006: Save Kundli

**Persona:** As a registered user,
**I want:** to save a generated Kundli to my profile,
**So that:** I can access it later without re-entering birth details.

**Acceptance Criteria:**

```
Given I have generated a Kundli
When I click "Save Kundli"
Then the kundli record's user_id is linked to my account and saved_at is set
And I see a success toast "Kundli saved to your profile"
And it appears in My Kundlis on my profile page

Given I generate a Kundli for someone else (a family member)
When I enter a different name and save
Then the Kundli is labelled with the name I entered and listed under My Kundlis

Given I have already saved the same Kundli (same kundli_id)
When I attempt to save again
Then I see "This Kundli is already saved to your profile"
```

**Out of scope:** Sharing a Kundli with another user.
**Technical Notes:** PATCH /kundli/:id/save; links kundlis.user_id FK; name label stored in kundlis.label.
**Story Points:** 2
**Dependencies:** KUNDL-001, AUTH-005
**Definition of Done:** Save links Kundli to user; appears in profile list.

---

### STORY-KUNDL-007: PDF Export

**Persona:** As a registered user,
**I want:** to download my Kundli as a PDF containing the chart, planetary table, and AI narrative,
**So that:** I can share it with my astrologer or keep a physical copy.

**Acceptance Criteria:**

```
Given I am viewing a completed Kundli
When I click "Download PDF"
Then a BullMQ job is dispatched to generate the PDF
And I see "Your PDF is being prepared. You'll be notified when it's ready."
And within 30 seconds the PDF is generated, stored in S3, and a presigned download URL is returned

Given the PDF has been generated
When I click the download link
Then a multi-page PDF opens with: cover page (name + birth details), SVG chart, planetary table, and AI narrative
And the PDF is ≥ 3 pages

Given PDF generation fails
When the BullMQ job errors after 3 retries
Then I see "PDF generation failed. Please try again." with a retry button
```

**Out of scope:** Custom branded PDF (v2).
**Technical Notes:** PDF generated via Puppeteer (headless Chrome) — per ADR-006; stored in S3 at kundlis/{kundliId}/report.pdf; presigned URL TTL 1 hour.
**Story Points:** 8
**Dependencies:** KUNDL-004, INFRA-004
**Definition of Done:** PDF generated by BullMQ; stored in S3; presigned URL returned.

---

### STORY-KUNDL-008: Kundli Matching (Gun Milan)

**Persona:** As a registered user,
**I want:** to enter two sets of birth details and receive a Vedic compatibility report (Ashta Koot analysis),
**So that:** I can assess marriage compatibility according to traditional Vedic methodology.

**Acceptance Criteria:**

```
Given I navigate to Kundli Matching
When I submit two valid birth detail forms (Boy and Girl)
Then POST /kundli/match computes the Ashta Koot scoring for all 8 Kootas
And returns the total score out of 36 with individual Koota scores and a 200-word narrative interpretation

Given the Nadi Koota results in Nadi Dosha (score = 0)
When the report renders
Then the Nadi row shows 0/8 and the narrative explicitly mentions "Nadi Dosha detected"

Given the total score is < 18 (below the traditional threshold)
When the report renders
Then a red banner reads: "Total compatibility score is below the recommended threshold of 18/36"
```

**Out of scope:** Mangal Dosha analysis (v2).
**Technical Notes:** Ashta Koot computation uses nakshatra positions of Moon; configuration in ashta_koot_config table/constant; POST /kundli/match.
**Story Points:** 8
**Dependencies:** KUNDL-001
**Definition of Done:** Matching computes all 8 Kootas; Nadi Dosha case handled; narrative included.

---

### STORY-KUNDL-009: Anonymous Kundli Generation (No Account Required)

**Persona:** As an anonymous visitor,
**I want:** to generate a basic Kundli without creating an account,
**So that:** I can experience the product before committing to registration.

**Acceptance Criteria:**

```
Given I am not logged in and navigate to the Kundli page
When I submit birth details
Then a Kundli is generated and displayed in full (chart + planetary table + Dasha timeline)
And the AI narrative is replaced with a teaser: first 100 words + "Sign in to read the full interpretation"

Given the anonymous Kundli session is complete
When I am shown the teaser
Then a prominent CTA "Create Free Account to Unlock Full Report" is displayed

Given I create an account after generating an anonymous Kundli
When I log in
Then I am prompted "Save the Kundli you just generated?" with one click to link it to my account
```

**Out of scope:** Saving anonymous Kundlis to a guest session beyond the browser tab.
**Technical Notes:** Anonymous Kundli stored temporarily with guest_session_id; prompt on login to claim.
**Story Points:** 3
**Dependencies:** KUNDL-001, AUTH-001
**Definition of Done:** Anonymous Kundli renders; AI narrative teasered; claim on login.

---

## Epic: HORO — Horoscope Content

**Epic Goal:** Users can access daily, weekly, and monthly horoscopes for all 12 zodiac signs, as well as love horoscopes, Panchang, and Shubh Muhurat. Content is AI-generated by Claude and cached in Redis.

---

### STORY-HORO-001: Daily Horoscope for All 12 Signs

**Persona:** As an anonymous visitor,
**I want:** to read today's daily horoscope for any of the 12 zodiac signs,
**So that:** I get free astrological guidance without needing to sign up.

**Acceptance Criteria:**

```
Given I navigate to the Daily Horoscope page
When I select a zodiac sign (e.g., Aries)
Then GET /horoscope/aries/daily returns a 150–200 word horoscope for today
And the content is served from Redis cache (TTL: until midnight UTC)
And page load time is < 500ms

Given today's horoscope is not yet in Redis (first request of the day)
When the cache miss is detected
Then ContentService calls the Claude API for all 12 signs in a single BullMQ batch job
And results are cached in Redis with TTL to midnight UTC
And the response is returned within 3 seconds

Given I view the horoscope for my profile's zodiac sign (if logged in)
When the page loads
Then my sign is pre-selected automatically
```

**Out of scope:** Personalised horoscope based on full birth chart (that is Kundli-generated).
**Technical Notes:** BullMQ nightly horoscope generation job fires at 00:01 UTC; Redis key: horoscope:{sign}:{date}:{period}.
**Story Points:** 5
**Dependencies:** INFRA-004, AUTH-001 (for pre-selection)
**Definition of Done:** All 12 daily horoscopes generated by BullMQ job; cached in Redis; page loads in < 500ms.

---

### STORY-HORO-002: Weekly and Monthly Horoscopes

**Persona:** As a registered user,
**I want:** to read weekly and monthly horoscope forecasts for my zodiac sign,
**So that:** I can plan ahead with astrological guidance.

**Acceptance Criteria:**

```
Given I select "Weekly" from the period toggle on the horoscope page
When the content loads
Then GET /horoscope/:sign/weekly returns a 300–400 word weekly forecast for the current ISO week
And the content is cached in Redis with TTL: end of the current week (Sunday 23:59 UTC)

Given I select "Monthly"
When the content loads
Then GET /horoscope/:sign/monthly returns a 400–500 word monthly forecast for the current calendar month
And the content is cached in Redis with TTL: end of the current month

Given no weekly content exists for the current week
When ContentService is called
Then Claude API is called to generate all 12 weekly forecasts, stored in Redis and the horoscopes DB table
```

**Out of scope:** Year-ahead horoscope (v2).
**Story Points:** 3
**Dependencies:** HORO-001
**Definition of Done:** Weekly and monthly routes work for all 12 signs; cache TTLs correct.

---

### STORY-HORO-003: Love Horoscope

**Persona:** As a registered user,
**I want:** to read a love and relationship-focused horoscope for my zodiac sign,
**So that:** I get specific romantic guidance alongside the general forecast.

**Acceptance Criteria:**

```
Given I navigate to the Love Horoscope section
When I select my sign
Then GET /horoscope/:sign/love returns a 150–200 word love horoscope for today
And the content is distinct from the general daily horoscope (not repeated)

Given I am logged in and my profile has a zodiac sign set
When I navigate to Love Horoscope
Then my sign is pre-selected

Given the love horoscope content is cached
When the same user requests it again within the same day
Then the response is served from Redis in < 100ms
```

**Out of scope:** Compatibility horoscope between two signs (that is in CONTENT-002).
**Story Points:** 2
**Dependencies:** HORO-001
**Definition of Done:** Love horoscope route returns content for all 12 signs; cached.

---

### STORY-HORO-004: Zodiac Sign Information Pages

**Persona:** As an anonymous visitor,
**I want:** to read a detailed information page about each of the 12 zodiac signs,
**So that:** I can learn about my sign's personality, ruling planet, element, and characteristics.

**Acceptance Criteria:**

```
Given I navigate to /signs/aries (or any sign slug)
When the page loads
Then I see the sign's: name, symbol, glyph, element (Fire/Earth/Air/Water), modality (Cardinal/Fixed/Mutable), ruling planet, lucky numbers, lucky colours, compatible signs, and a 500-word personality description from seed data

Given I click the compatible signs
When the link is followed
Then I am taken to the Compatibility Checker (CONTENT-002) pre-filled with this sign

Given the page is viewed by a search engine (SSR consideration)
When the HTML is inspected
Then title and meta description tags contain the sign name (SEO requirement — subject to ADR-001 decision)
```

**Out of scope:** Dynamic content updates to sign descriptions.
**Technical Notes:** Content served from zodiac_signs seed table; served statically or via SSR per ADR-001.
**Story Points:** 3
**Dependencies:** INFRA-002 (seed data)
**Definition of Done:** All 12 sign pages render with seed data; SEO meta tags present.

---

### STORY-HORO-005: Panchang (Daily Hindu Calendar)

**Persona:** As a registered user,
**I want:** to view today's Panchang (Hindu almanac) with Tithi, Vara, Nakshatra, Yoga, Karana, and Rahu Kaal,
**So that:** I can identify auspicious and inauspicious times for activities today.

**Acceptance Criteria:**

```
Given I navigate to the Panchang page
When I select today's date and my city
Then GET /panchang returns the 5 Panchang elements (Tithi, Vara, Nakshatra, Yoga, Karana) and Rahu Kaal for my location and time zone

Given the Panchang data has been calculated for today and this location
When a second request is made
Then the response is served from panchang_cache table (unique on date + location_key) in < 100ms

Given no Panchang data exists for this date and location
When the request is received
Then panchang-engine npm library computes the values, stores in panchang_cache, and returns the result
```

**Out of scope:** Panchang for past dates or future date navigation (v2).
**Technical Notes:** panchang-engine npm; location key = {lat_rounded_2dp}_{lon_rounded_2dp}; data cached 24h in panchang_cache table.
**Story Points:** 5
**Dependencies:** INFRA-002
**Definition of Done:** Panchang renders for today's date; location-specific; cached after first request.

---

### STORY-HORO-006: Shubh Muhurat Calculator

**Persona:** As a registered user,
**I want:** to find auspicious time windows (Muhurat) for a specific activity (e.g., wedding, business launch) on a chosen date,
**So that:** I can schedule important events at the most auspicious time.

**Acceptance Criteria:**

```
Given I navigate to the Muhurat Calculator
When I select an activity type (Wedding, Griha Pravesh, Business Launch, Travel) and a target date and location
Then the system computes and displays all auspicious Muhurat windows for that date and activity

Given no auspicious Muhurat exists for the selected date
When the computation is complete
Then I see "No Shubh Muhurat found for this activity on the selected date. Consider choosing an adjacent date."

Given the Muhurat is computed
When I view the results
Then each window shows: start time, end time, duration, and the Panchang element that makes it auspicious
```

**Out of scope:** Electional astrology beyond Panchang-based Muhurat.
**Technical Notes:** Muhurat logic built on top of panchang-engine; activity rules configurable in constants.
**Story Points:** 5
**Dependencies:** HORO-005
**Definition of Done:** Muhurat computed for all 4 activity types; empty state handled.

---

### STORY-HORO-007: Horoscope Sign Selector (Onboarding Nudge)

**Persona:** As a registered user who has not set their zodiac sign,
**I want:** to be gently prompted to add my date of birth so my zodiac sign can be auto-detected,
**So that:** the horoscope pages are personalised without manual sign selection every visit.

**Acceptance Criteria:**

```
Given I am logged in and my profile does not have a DOB set
When I visit any horoscope page
Then a non-blocking nudge banner appears: "Add your date of birth to personalise your horoscope" with a link to Profile

Given I have set my DOB on my profile
When I visit any horoscope page
Then my zodiac sign is pre-selected and no nudge is shown

Given I dismiss the nudge banner
When I visit the page again in the same session
Then the nudge does not reappear (dismissed flag in sessionStorage)
```

**Out of scope:** Forced redirect to profile completion.
**Story Points:** 2
**Dependencies:** AUTH-005, HORO-001
**Definition of Done:** Nudge shown when DOB absent; pre-selection works when DOB set.

---

### STORY-HORO-008: Horoscope Archive (Last 7 Days)

**Persona:** As a registered user,
**I want:** to access horoscopes from the past 7 days for my sign,
**So that:** I can review recent predictions and compare them with events in my life.

**Acceptance Criteria:**

```
Given I am on the Daily Horoscope page
When I click "View Previous Days"
Then a date picker shows the last 7 days (today − 6 days to today)
And selecting a past date loads the horoscope for that date from the horoscopes table

Given a past date's horoscope is requested
When the data is fetched
Then the content is served from the horoscopes DB table (not regenerated via Claude API)

Given a date older than 7 days is requested
When the query runs
Then I see "Horoscope archive available for the last 7 days only"
```

**Out of scope:** Full historical archive (v2 premium feature).
**Story Points:** 2
**Dependencies:** HORO-001
**Definition of Done:** 7-day archive accessible; older dates blocked.

---

## Epic: CHAT — Consultation Chat & Billing

**Epic Goal:** Seekers can initiate real-time text chat consultations with online astrologers. Per-minute billing is enforced via a BullMQ billing tick job with SELECT FOR UPDATE. Sessions auto-disconnect when the wallet is empty. Transcripts are saved and review is prompted post-session.

---

### STORY-CHAT-001: Consultation Initiation and Wallet Pre-Check

**Persona:** As a registered user with wallet balance,
**I want:** to start a chat consultation with an online astrologer,
**So that:** I can receive personalised astrological guidance in real-time.

**Acceptance Criteria:**

```
Given I am on an astrologer's detail page and they are Online
When I click "Start Consultation"
Then the system checks my wallet balance against (astrologer.per_minute_rate × 5) as a minimum opening balance
And if sufficient, POST /consultations creates a consultation record with status = ACTIVE
And I am redirected to the chat room

Given my wallet balance is insufficient for a 5-minute minimum
When I click "Start Consultation"
Then I see a modal: "Insufficient balance. You need at least X Coins to start. Recharge now?" with a Recharge CTA
And no consultation record is created

Given the astrologer goes offline between my click and the server processing
When POST /consultations is received
Then the API returns 409 with {"error": "ASTROLOGER_OFFLINE"} and I see "This astrologer just went offline. Please try another."
```

**Out of scope:** Scheduling future consultations.
**Technical Notes:** Minimum balance check = 5 × rate; atomic check-and-lock via Prisma.$transaction(); consultation record: status enum ACTIVE/COMPLETED/CANCELLED/DISPUTED.
**Story Points:** 8
**Dependencies:** AUTH-001, ASTR-005, WALLET-001
**Definition of Done:** Wallet pre-check enforced; consultation created atomically; insufficient balance modal shown.

---

### STORY-CHAT-002: Real-Time Chat Room (Socket.io)

**Persona:** As an active consultation participant (seeker or astrologer),
**I want:** to send and receive text messages in real-time within a consultation room,
**So that:** we can communicate instantly with no perceptible delay.

**Acceptance Criteria:**

```
Given a consultation is ACTIVE and both parties are connected to the Socket.io room
When the seeker sends a message
Then the message is delivered to the astrologer within 500ms

Given a message is sent by either party
When it arrives
Then it is persisted to the messages table with sender_id, consultation_id, content, and sent_at timestamp

Given one party loses internet connection temporarily
When they reconnect within 30 seconds
Then they automatically rejoin the Socket.io room and see messages sent while they were disconnected (loaded from DB)

Given a consultation is not ACTIVE (COMPLETED or CANCELLED)
When either party attempts to send a message
Then the Socket.io server returns an error event: {event: "CONSULTATION_CLOSED", message: "This session has ended"}
```

**Out of scope:** File/image sharing; message read receipts (v2).
**Technical Notes:** Socket.io room ID = consultation_id; event names from packages/shared/src/events.ts; messages persisted synchronously before emit.
**Story Points:** 8
**Dependencies:** CHAT-001, INFRA-004
**Definition of Done:** Messages delivered in ≤ 500ms; persisted to DB; reconnect works.

---

### STORY-CHAT-003: Per-Minute Billing Tick

**Persona:** As the platform,
**I want:** to deduct wallet coins from the seeker every minute during an active consultation,
**So that:** billing is accurate and neither party is deceived about the cost.

**Acceptance Criteria:**

```
Given a consultation is ACTIVE
When 60 seconds have elapsed since the last billing tick
Then a BullMQ repeatable job deducts (astrologer.per_minute_rate) Coins from the seeker's wallet using Prisma.$transaction() with SELECT ... FOR UPDATE on the users row
And a wallet_transactions record is created with type = CONSULTATION_DEBIT
And the updated balance is emitted via Socket.io to the seeker's connection: {event: "WALLET_UPDATED", balance: N}

Given two concurrent billing ticks attempt to deduct from the same wallet simultaneously
When the SELECT FOR UPDATE lock is acquired by the first job
Then the second job waits until the first commits; no double-deduction occurs and balance never goes negative

Given the billing tick job fails (Redis unavailable)
When the job errors
Then BullMQ retries with backoff; the consultation remains ACTIVE; the seeker is not disconnected due to billing failure alone
```

**Out of scope:** Partial-minute billing (full-minute increments only in v1).
**Technical Notes:** BullMQ repeatable job keyed by consultation_id; job removed when consultation status changes from ACTIVE; SELECT FOR UPDATE critical path — QA-002 scenario.
**Story Points:** 13
**Dependencies:** CHAT-001, WALLET-001, INFRA-004
**Definition of Done:** Billing tick fires every 60s; SELECT FOR UPDATE used; QA-001 and QA-002 pass.

---

### STORY-CHAT-004: Auto-Disconnect on Wallet Depletion

**Persona:** As the platform,
**I want:** to automatically end a consultation when the seeker's wallet balance drops to zero,
**So that:** no credit is extended and the astrologer is not kept waiting without payment.

**Acceptance Criteria:**

```
Given the billing tick runs and the seeker's post-deduction balance is zero or negative
When the deduction completes
Then the consultation status is set to COMPLETED with end_reason = WALLET_DEPLETED
And the BullMQ billing tick job is removed
And a Socket.io event is emitted to both parties: {event: "SESSION_ENDED", reason: "WALLET_DEPLETED"}
And the seeker sees a notification: "Your session has ended. Your wallet has been depleted. Recharge to continue."

Given the wallet balance is exactly enough for one more minute when the tick fires
When that final tick completes
Then the balance is exactly 0 and the session ends (no negative balance is possible)

Given the session ends due to wallet depletion
When the seeker is redirected
Then they land on the session review page (CHAT-007) with a Recharge CTA visible
```

**Out of scope:** Pre-depletion warning notification (covered in NOTIF epic).
**Technical Notes:** Check balance after every tick; if balance <= 0 post-deduction: set COMPLETED, stop job, emit event.
**Story Points:** 8
**Dependencies:** CHAT-003
**Definition of Done:** Auto-disconnect fires on depletion; balance never goes negative; QA-001 passes.

---

### STORY-CHAT-005: Manual Session End

**Persona:** As a consultation participant (seeker or astrologer),
**I want:** to manually end a consultation at any time,
**So that:** I am not billed further after I am done with the session.

**Acceptance Criteria:**

```
Given I am in an active consultation
When I click "End Session" and confirm in the modal
Then POST /consultations/:id/end is called
And the consultation status is set to COMPLETED with end_reason = USER_INITIATED (or ASTROLOGER_INITIATED)
And the billing tick BullMQ job is removed immediately
And both parties receive: {event: "SESSION_ENDED", reason: "USER_INITIATED"}

Given the seeker ends the session mid-minute
When the consultation ends
Then no further coins are deducted for the partial minute (no pro-rata billing in v1)

Given the astrologer ends the session
When the Socket.io event is received by the seeker
Then the seeker sees "The astrologer has ended this session." and is redirected to the review page
```

**Out of scope:** Pro-rata partial-minute billing (v2).
**Story Points:** 5
**Dependencies:** CHAT-003
**Definition of Done:** Manual end stops billing; both parties notified; review page shown.

---

### STORY-CHAT-006: Astrologer Disconnect Handling

**Persona:** As the platform,
**I want:** to detect when an astrologer disconnects mid-session and handle it gracefully,
**So that:** the seeker is refunded for time lost and the session is cleanly terminated.

**Acceptance Criteria:**

```
Given an astrologer loses connection during an ACTIVE consultation
When 30 seconds pass without a heartbeat from the astrologer
Then the consultation is set to COMPLETED with end_reason = ASTROLOGER_DISCONNECTED
And the seeker receives: {event: "SESSION_ENDED", reason: "ASTROLOGER_DISCONNECTED", message: "Your astrologer lost connection."}
And a refund equal to the cost of the last incomplete minute is credited to the seeker's wallet
And a wallet_transactions record is created with type = REFUND, reference = consultation_id

Given the astrologer reconnects within the 30-second grace period
When their heartbeat resumes
Then the session continues without interruption
And the seeker sees no disconnect notification
```

**Out of scope:** Automatic reconnection of the entire session (user must restart).
**Technical Notes:** Heartbeat via Socket.io ping/pong; server-side 30s timer; refund via Prisma.$transaction(); QA-010 scenario.
**Story Points:** 8
**Dependencies:** CHAT-003, WALLET-002
**Definition of Done:** Disconnection detected after 30s; refund credited; QA-010 passes.

---

### STORY-CHAT-007: Post-Session Transcript and Review Prompt

**Persona:** As a seeker who has completed a consultation,
**I want:** to read a transcript of my session and leave a star rating and review for the astrologer,
**So that:** I have a record of the advice received and can help other users choose well.

**Acceptance Criteria:**

```
Given a consultation has ended (any end_reason)
When I navigate to the session detail page
Then I see the full message transcript in chronological order with timestamps
And a "Rate Your Session" form with 1–5 stars and an optional 200-character review text

Given I submit a review
When POST /reviews is called
Then a reviews record is created with star_rating, text, and consultation_id
And the astrologer's average rating is recalculated and updated
And I see "Thank you for your review!"

Given I have already submitted a review for this consultation
When I attempt to submit again
Then I see "You have already reviewed this session" (unique constraint on reviews.consultation_id)
```

**Out of scope:** Editing a submitted review.
**Technical Notes:** Unique constraint on reviews(consultation_id) enforced at DB level; rating recalculation via DB aggregation.
**Story Points:** 5
**Dependencies:** CHAT-001
**Definition of Done:** Transcript visible; review submitted; rating updates; duplicate prevented.

---

### STORY-CHAT-008: First Free Consultation (5 Minutes)

**Persona:** As a newly registered user,
**I want:** to have one free 5-minute consultation with any online astrologer,
**So that:** I can experience a real consultation before committing to wallet recharge.

**Acceptance Criteria:**

```
Given I am a registered user and has_used_free_session = false
When I click "Start Consultation" on any astrologer's page
Then the UI shows "Free Session — 5 Minutes" banner in the chat room
And the billing ticker does NOT deduct Coins for the first 5 minutes
And after 5 minutes the session auto-ends with end_reason = FREE_SESSION_EXPIRED
And has_used_free_session is set to true in the database

Given has_used_free_session = true
When I attempt to start a new consultation
Then the free session offer is not shown and normal billing applies from minute 1

Given my free session ends
When I am redirected
Then I see: "Your free session has ended. Recharge to continue consulting with astrologers." with a Recharge CTA
```

**Out of scope:** Free session reset (one per user, permanent).
**Technical Notes:** has_used_free_session boolean on users table; billing tick skipped for first 5 ticks if free session; QA-008 scenario.
**Story Points:** 5
**Dependencies:** CHAT-003, AUTH-001
**Definition of Done:** Free session allows 5 minutes unbilled; flag set after; QA-008 passes.

---

### STORY-CHAT-009: Consultation History

**Persona:** As a registered user,
**I want:** to view a list of all my past consultations,
**So that:** I can track my spending, revisit transcripts, and see which astrologers I have spoken to.

**Acceptance Criteria:**

```
Given I navigate to Consultation History
When the page loads
Then I see a paginated list of my past consultations sorted by date (newest first): astrologer name, date, duration, coins spent, and status badge

Given I click on a past consultation
When the detail page loads
Then I see the full transcript and my review (if submitted) or a prompt to review (if not)

Given I have no past consultations
When I view the history page
Then I see an empty state: "You haven't started any consultations yet." with a CTA to browse astrologers
```

**Story Points:** 3
**Dependencies:** CHAT-001
**Definition of Done:** History list renders paginated; click navigates to transcript; empty state shown.

---

## Epic: WALLET — Wallet & Payments

**Epic Goal:** Users can recharge their wallet using a mock payment flow, view their transaction ledger, receive cashback, and request refunds. Astrologers can request payouts.

---

### STORY-WALLET-001: Wallet Balance Display

**Persona:** As a registered user,
**I want:** to see my current wallet balance prominently in the navigation bar,
**So that:** I always know how many Coins I have available before starting a consultation.

**Acceptance Criteria:**

```
Given I am logged in
When any page loads
Then my current wallet balance is shown in the top navigation bar as "X Coins"

Given a billing tick deducts from my wallet
When the Socket.io WALLET_UPDATED event is received
Then the balance in the navigation bar updates in real-time without page reload

Given I am not logged in
When I view the navigation bar
Then no wallet balance is shown; a "Sign in" CTA is shown instead
```

**Story Points:** 2
**Dependencies:** AUTH-001, INFRA-004
**Definition of Done:** Balance shown in nav; updates in real-time via Socket.io.

---

### STORY-WALLET-002: Mock Wallet Recharge

**Persona:** As a registered user,
**I want:** to add Coins to my wallet using a simulated payment form,
**So that:** I can fund consultations in a realistic flow without real money.

**Acceptance Criteria:**

```
Given I navigate to the Wallet page and click "Recharge"
When I select a recharge amount (₹99, ₹199, ₹499, ₹999) and submit the mock card form
Then if the card number ends in an even digit (mock success), wallet_balance is increased by the Coin amount, a wallet_transactions record (type = RECHARGE) is created, and I see "₹X added to your wallet"

Given I submit the mock card form with a card number ending in an odd digit (mock failure)
When the payment is processed
Then wallet_balance is unchanged, no transaction record is created, and I see "Payment failed. Please try again."

Given the recharge is successful
When I check my wallet balance
Then the new balance reflects the added Coins within 2 seconds
```

**Out of scope:** Real Stripe or Razorpay integration; cryptocurrency.
**Technical Notes:** Mock payment logic in server; coin amounts = INR amounts (1:1 in v1); ALL wallet mutations use Prisma.$transaction().
**Story Points:** 8
**Dependencies:** WALLET-001, INFRA-002
**Definition of Done:** Mock success adds coins; mock failure changes nothing; QA-006 passes.

---

### STORY-WALLET-003: Transaction Ledger

**Persona:** As a registered user,
**I want:** to view a full history of my wallet transactions (recharges, consultation debits, cashbacks, refunds),
**So that:** I can reconcile my spending and verify charges.

**Acceptance Criteria:**

```
Given I navigate to the Wallet page
When I click "Transaction History"
Then I see a paginated list of all my transactions sorted by date (newest first): date, type badge (Recharge/Debit/Cashback/Refund), description, and amount (+ or −)

Given I apply a filter by transaction type
When the filter is applied
Then only transactions of that type are shown

Given I have no transactions
When I view the ledger
Then I see "No transactions yet. Recharge your wallet to get started."
```

**Story Points:** 3
**Dependencies:** WALLET-002
**Definition of Done:** Ledger renders all transaction types; filters work.

---

### STORY-WALLET-004: Cashback on Recharge

**Persona:** As a registered user,
**I want:** to receive a cashback bonus when I recharge above a threshold,
**So that:** I am incentivised to recharge more.

**Acceptance Criteria:**

```
Given I recharge ₹499 or more
When the recharge is successfully processed
Then an additional 10% Coins cashback is added to my wallet in a separate wallet_transactions record (type = CASHBACK) within 5 seconds

Given I recharge less than ₹499
When the recharge is processed
Then no cashback is credited

Given the cashback rate is changed by an admin
When the new rate is active
Then all subsequent eligible recharges use the new rate; existing transactions are unchanged
```

**Out of scope:** Referral cashback (v2).
**Technical Notes:** Cashback rate configurable in platform_settings table; cashback applied synchronously within same Prisma transaction as recharge.
**Story Points:** 3
**Dependencies:** WALLET-002
**Definition of Done:** Cashback credited on ≥ ₹499 recharge; configurable rate; separate transaction record.

---

### STORY-WALLET-005: Astrologer Earnings and Payout Request

**Persona:** As an approved astrologer,
**I want:** to see my total platform earnings and request a payout,
**So that:** I receive my earned income on demand.

**Acceptance Criteria:**

```
Given I am an approved astrologer and navigate to Earnings
When the page loads
Then I see: gross earnings (sum of consultation fees earned), platform commission deducted (e.g., 20%), net payout balance, and total withdrawn to date

Given I click "Request Payout" and my payout balance ≥ ₹100
When the request is submitted
Then a payout_requests record is created with status = PENDING, amount = current payout balance
And my payout balance is zeroed (reserved for payout)
And admin sees the new request in the Admin panel

Given my payout balance < ₹100
When I click "Request Payout"
Then I see "Minimum payout is ₹100."
```

**Out of scope:** Real bank transfer; UPI integration.
**Technical Notes:** Commission rate in platform_settings; payout_requests table; payout balance reservation uses Prisma.$transaction().
**Story Points:** 5
**Dependencies:** ASTR-006, INFRA-002
**Definition of Done:** Earnings computed correctly; payout request reserves balance; admin sees request.

---

### STORY-WALLET-006: Refund Flow

**Persona:** As a registered user who experienced a session issue,
**I want:** to receive an automatic or admin-initiated refund to my wallet,
**So that:** I am made whole for time I paid for but did not receive.

**Acceptance Criteria:**

```
Given an astrologer disconnects mid-session (CHAT-006)
When the auto-refund is processed
Then the last incomplete minute's cost is credited to the seeker's wallet as type = REFUND within 10 seconds
And a wallet_transactions record is created referencing the consultation_id

Given an admin initiates a manual refund via the Admin panel
When the refund is submitted
Then the specified Coin amount is credited to the user's wallet as type = REFUND
And both the user and admin see the transaction in the ledger

Given a refund would bring the wallet above a platform maximum (99,999 Coins)
When the refund is processed
Then the amount is capped at the maximum and the surplus is noted in the transaction description
```

**Out of scope:** Cash refund to original payment method.
**Story Points:** 5
**Dependencies:** CHAT-006, ADMIN-004
**Definition of Done:** Auto-refund on disconnect; admin refund works; wallet never exceeds maximum.

---

### STORY-WALLET-007: Low Wallet Warning in Chat

**Persona:** As a seeker in an active consultation,
**I want:** to receive a warning when my wallet has less than 3 minutes of balance remaining,
**So that:** I can recharge before being auto-disconnected.

**Acceptance Criteria:**

```
Given I am in an active consultation and my wallet balance drops to ≤ (3 × astrologer.per_minute_rate)
When the billing tick fires
Then a Socket.io event {event: "LOW_WALLET_WARNING", balance: N, minutesRemaining: 3} is emitted to my connection
And a yellow warning toast appears in the chat room: "⚠️ Your wallet has ~3 minutes remaining"

Given the balance drops to ≤ (1 × rate)
When the billing tick fires
Then a red urgent alert appears: "⚠️ Last minute! Your session will end soon."

Given I recharge during the consultation
When the wallet is recharged
Then the low wallet warning clears automatically upon receipt of the WALLET_UPDATED event
```

**Story Points:** 3
**Dependencies:** CHAT-003, WALLET-002
**Definition of Done:** 3-minute and 1-minute warnings fire; alerts appear in chat room; clears on recharge.

---

## Epic: ADMIN — Admin Panel

**Epic Goal:** Admins can monitor platform KPIs, manage users and astrologers, moderate content, and handle transactions.

---

### STORY-ADMIN-001: Admin KPI Dashboard

**Persona:** As a platform admin,
**I want:** to see a real-time KPI dashboard with key platform metrics,
**So that:** I can monitor platform health and make informed decisions.

**Acceptance Criteria:**

```
Given I am logged in as an admin and navigate to /admin
When the dashboard loads
Then I see cards for: Total Users, Active Users (last 30d), Total Astrologers (APPROVED count), Active Consultations (live count), Revenue Today (Coins recharged), Revenue MTD, Total Wallet Coins Issued, and Platform Commission Earned MTD

Given I view the Active Consultations card
When a new consultation starts
Then the count updates within 30 seconds (polling or Socket.io event)

Given I view the dashboard on any date
When the Revenue Today card is shown
Then it reflects only transactions with created_at >= today 00:00 UTC
```

**Out of scope:** Revenue charts and trend analysis (v2 analytics dashboard).
**Technical Notes:** GET /admin/stats; admin JWT role check middleware; active consultation count via DB query.
**Story Points:** 8
**Dependencies:** AUTH-001, INFRA-002
**Definition of Done:** All 8 KPI cards render with real data; admin role enforcement returns 403 for non-admins.

---

### STORY-ADMIN-002: User Management

**Persona:** As a platform admin,
**I want:** to search, view, and manage all registered users,
**So that:** I can handle support requests, suspend abusive accounts, and maintain platform integrity.

**Acceptance Criteria:**

```
Given I navigate to Admin → Users
When I search by name or email
Then GET /admin/users?search=X returns matching users with: name, email, phone (masked), join date, wallet balance, consultation count, and account status

Given I click on a user
When their detail panel opens
Then I see their full profile details, transaction history, consultation history, and current status (ACTIVE/SUSPENDED/DELETED)

Given I click "Suspend" on a user
When I confirm the action
Then users.status = SUSPENDED, any active consultations are ended (CHAT-006 disconnect flow), and the user cannot log in
And QA-009 scenario is satisfied
```

**Out of scope:** Bulk user actions.
**Technical Notes:** GET /admin/users; PUT /admin/users/:id; admin role required; ban during consultation triggers disconnect.
**Story Points:** 5
**Dependencies:** ADMIN-001, AUTH-001
**Definition of Done:** Search works; suspend sets status; active consultation ends; QA-009 passes.

---

### STORY-ADMIN-003: Astrologer Approval and Management

**Persona:** As a platform admin,
**I want:** to review pending astrologer applications and approve or reject them,
**So that:** only qualified and vetted astrologers appear on the platform.

**Acceptance Criteria:**

```
Given a new astrologer application has been submitted (ASTR-003)
When I navigate to Admin → Astrologers → Pending
Then I see a list of PENDING_APPROVAL applications with name, email, specialities, experience, and submission date

Given I click "Approve"
When PUT /admin/astrologers/:id/approve is called
Then astrologers.status = APPROVED
And the astrologer receives an email: "Congratulations! Your application has been approved."
And they appear in the public directory immediately

Given I click "Reject" with a rejection reason
When the rejection is submitted
Then astrologers.status = REJECTED
And the astrologer receives an email with the rejection reason
And QA-005 scenario is satisfied
```

**Story Points:** 5
**Dependencies:** ASTR-003, NOTIF-002
**Definition of Done:** Approve sets status; astrologer appears in directory; email sent; QA-005 passes.

---

### STORY-ADMIN-004: Transaction Monitoring and Manual Refund

**Persona:** As a platform admin,
**I want:** to view all wallet transactions across all users and initiate manual refunds,
**So that:** I can resolve disputes and correct billing errors.

**Acceptance Criteria:**

```
Given I navigate to Admin → Transactions
When the page loads
Then I see a paginated list of all wallet_transactions with: user name, type, amount, date, and reference (consultation_id if applicable)

Given I filter by type = REFUND
When the filter applies
Then only refund transactions are shown

Given I click "Issue Refund" for a user
When I enter an amount and reason and confirm
Then a REFUND wallet_transactions record is created and the user's wallet_balance is increased via Prisma.$transaction()
```

**Story Points:** 5
**Dependencies:** WALLET-003, ADMIN-001
**Definition of Done:** Transaction list renders; filter works; manual refund credits wallet.

---

### STORY-ADMIN-005: Content CRUD (Horoscope and Blog)

**Persona:** As a platform admin,
**I want:** to create, edit, and delete horoscope overrides and blog posts via an admin interface,
**So that:** the content team can manage editorial content without engineering intervention.

**Acceptance Criteria:**

```
Given I navigate to Admin → Content → Horoscopes
When I select a sign and date and click "Edit"
Then an inline editor allows me to override the AI-generated horoscope text
And on save, the horoscopes table is updated and the Redis cache key for that sign/date is invalidated

Given I navigate to Admin → Content → Blog
When I click "New Post"
Then a form allows me to enter: title, slug, body (rich text), category, tags, and publish status
And on save, the blog post is created and immediately accessible at GET /blog/:slug

Given I delete a blog post
When the delete is confirmed
Then the post is soft-deleted (deleted_at set) and no longer returned by GET /blog
```

**Story Points:** 5
**Dependencies:** HORO-001, CONTENT-001
**Definition of Done:** Horoscope override invalidates Redis cache; blog CRUD works; soft delete.

---

### STORY-ADMIN-006: Promo Code Management

**Persona:** As a platform admin,
**I want:** to create and manage promo codes that give users bonus Coins on recharge,
**So that:** we can run marketing campaigns to drive wallet recharge.

**Acceptance Criteria:**

```
Given I navigate to Admin → Promo Codes
When I click "Create Promo Code"
Then I can set: code string, bonus amount (fixed Coins or %), usage limit, per-user limit, and expiry date
And on save the promo_codes record is active immediately

Given a user enters a valid promo code at recharge
When they submit the code
Then if valid and not expired and usage limit not reached: bonus Coins are credited (type = PROMO_BONUS) and the code usage count is incremented atomically

Given the promo code has reached its usage limit
When a user submits the code
Then they see "This promo code has expired or reached its usage limit"
```

**Story Points:** 5
**Dependencies:** WALLET-002, ADMIN-001
**Definition of Done:** Promo code creation works; valid code credits bonus; limit enforced atomically.

---

### STORY-ADMIN-007: Platform Settings

**Persona:** As a platform admin,
**I want:** to manage platform-wide settings (commission rate, cashback rate, minimum payout, coin conversion rate) from the admin panel,
**So that:** I can adjust business parameters without a code deploy.

**Acceptance Criteria:**

```
Given I navigate to Admin → Settings
When the page loads
Then I see editable fields for: platform_commission_rate (%), cashback_threshold (Coins), cashback_rate (%), min_payout (Coins), coin_to_inr_rate

Given I update the platform_commission_rate
When I save
Then the new rate is stored in platform_settings table and applied to all future consultation earnings calculations
And existing closed consultations are not retroactively changed

Given I set an invalid commission rate (> 100% or negative)
When I save
Then I see "Commission rate must be between 0 and 100"
```

**Story Points:** 3
**Dependencies:** ADMIN-001, WALLET-004, WALLET-005
**Definition of Done:** Settings persist; new rates apply prospectively; validation enforced.

---

### STORY-ADMIN-008: Admin Role Assignment

**Persona:** As a super admin,
**I want:** to assign and revoke admin roles for other users,
**So that:** I can delegate administrative responsibilities without sharing credentials.

**Acceptance Criteria:**

```
Given I navigate to Admin → Team
When I search for a user by email and click "Make Admin"
Then users.role = ADMIN is set and the user gains access to all /admin/* routes

Given I revoke admin access from a user
When I click "Remove Admin"
Then users.role = USER is set and subsequent requests to /admin/* return 403

Given a non-admin user attempts to access /admin/*
When the JWT is validated
Then the admin middleware returns 403 with {"error": "INSUFFICIENT_PERMISSIONS"}
```

**Story Points:** 3
**Dependencies:** AUTH-001, ADMIN-001
**Definition of Done:** Role assignment works; non-admins get 403; role revocation immediate.

---

## Epic: MALL — AstroMall

**Epic Goal:** Users can browse astrological products (gemstones, yantras, books), add them to a cart, and complete a mock checkout. Order history is maintained.

---

### STORY-MALL-001: Product Catalogue

**Persona:** As a registered user,
**I want:** to browse a catalogue of astrology-related products organised by category,
**So that:** I can find products relevant to my astrological needs.

**Acceptance Criteria:**

```
Given I navigate to AstroMall
When the page loads
Then I see product cards organised by category (Gemstones, Yantras, Books, Rudraksha, Puja Items)
And each card shows: product image, name, price in Coins, brief description, and rating

Given I filter by a category
When the filter is applied
Then only products in that category are shown

Given I search for a product by name
When results load
Then matching products are shown regardless of category
```

**Story Points:** 5
**Dependencies:** INFRA-002 (seed products)
**Definition of Done:** Catalogue renders 25 seed products across 5 categories; filter and search work.

---

### STORY-MALL-002: Product Detail Page

**Persona:** As a registered user,
**I want:** to view the full details of a product before adding it to my cart,
**So that:** I can make an informed purchase decision.

**Acceptance Criteria:**

```
Given I click on a product card
When the detail page loads
Then I see: full-size image(s), name, price, detailed description (300+ words), category, ratings summary, and user reviews

Given I click "Add to Wishlist"
When logged in
Then the product is added to my wishlist (wishlist_items table) and the button changes to "Wishlisted"

Given I am not logged in and click "Add to Cart"
When the action is triggered
Then I am prompted: "Sign in to add items to your cart" with a login CTA
```

**Story Points:** 3
**Dependencies:** MALL-001, AUTH-001
**Definition of Done:** Detail page renders full product info; wishlist toggle works; login prompt for guests.

---

### STORY-MALL-003: Shopping Cart

**Persona:** As a registered user,
**I want:** to add products to a cart and manage quantities before checkout,
**So that:** I can purchase multiple items in a single order.

**Acceptance Criteria:**

```
Given I click "Add to Cart" on a product
When logged in
Then a cart_items record is created (or quantity incremented if product already in cart)
And the cart icon in the navigation updates to show the item count

Given I navigate to the cart
When the page loads
Then I see all cart items with: image, name, unit price, quantity selector, line total, and a remove button
And the cart total is shown with a breakdown

Given I increment the quantity of an item
When I update the quantity
Then the cart_items.quantity is updated and the total recalculates instantly
```

**Out of scope:** Cart persistence across devices without login.
**Technical Notes:** Cart stored in DB (cart_items table) per ADR-007 decision; no Redis TTL risk.
**Story Points:** 5
**Dependencies:** MALL-002, AUTH-001
**Definition of Done:** Cart CRUD works; quantity updates; total calculates.

---

### STORY-MALL-004: Mock Checkout

**Persona:** As a registered user with items in my cart,
**I want:** to complete a mock checkout and receive an order confirmation,
**So that:** I experience the full purchase flow without real payment.

**Acceptance Criteria:**

```
Given I proceed to checkout from the cart
When I review my order summary and click "Place Order"
Then if my wallet balance >= cart total: the Coin amount is deducted via Prisma.$transaction(), an orders record is created with status = CONFIRMED, cart_items are cleared, and I see "Order placed successfully! Order #XYZ"

Given my wallet balance < cart total
When I click "Place Order"
Then I see: "Insufficient wallet balance. You need X more Coins. Recharge now?" with a Recharge CTA
And no order is created

Given the order is placed
When I check my transaction ledger
Then a wallet_transactions record of type = MALL_PURCHASE exists for the order total
```

**Story Points:** 5
**Dependencies:** MALL-003, WALLET-002
**Definition of Done:** Checkout deducts coins; order created; cart cleared; insufficient balance handled.

---

### STORY-MALL-005: Order History

**Persona:** As a registered user,
**I want:** to view my AstroMall order history,
**So that:** I can track past purchases and reference my orders.

**Acceptance Criteria:**

```
Given I navigate to My Orders
When the page loads
Then I see a list of my orders sorted by date (newest first): order number, date, items count, total Coins, and status badge

Given I click on an order
When the detail page loads
Then I see: order number, date, all ordered items with quantities and prices, total, and order status

Given I have no orders
When I view My Orders
Then I see "No orders yet. Visit AstroMall to shop." with a CTA
```

**Story Points:** 2
**Dependencies:** MALL-004
**Definition of Done:** Order history renders; detail page shows all items; empty state shown.

---

### STORY-MALL-006: Wishlist

**Persona:** As a registered user,
**I want:** to maintain a wishlist of products I am interested in,
**So that:** I can save items for later without immediately purchasing.

**Acceptance Criteria:**

```
Given I have added products to my wishlist (MALL-002)
When I navigate to My Wishlist
Then I see all wishlisted products with: image, name, price, and "Add to Cart" button

Given I click "Add to Cart" from the wishlist
When the action completes
Then the product is added to my cart and remains in the wishlist (not auto-removed)

Given I click the heart icon on a wishlisted product
When toggled
Then it is removed from my wishlist and the heart icon changes to unfilled
```

**Story Points:** 3
**Dependencies:** MALL-002, MALL-003
**Definition of Done:** Wishlist renders; add to cart from wishlist works; remove from wishlist works.

---

## Epic: CONTENT — Blog & Tools

**Epic Goal:** Users can read blog posts and use utility tools including a numerology calculator, zodiac compatibility checker, and baby name generator.

---

### STORY-CONTENT-001: Blog Listing and Detail

**Persona:** As an anonymous visitor,
**I want:** to browse a blog with articles about astrology, Vedic wisdom, and product guides,
**So that:** I can learn and engage with the platform without needing to sign up.

**Acceptance Criteria:**

```
Given I navigate to /blog
When the page loads
Then I see a paginated list of published blog posts with: featured image, title, excerpt (first 150 chars), author, publish date, and read time estimate

Given I click on a blog post
When the detail page loads
Then I see the full article with rich text formatting, images, and a related posts section (3 posts, same category)

Given I search for a blog topic
When the search query is submitted
Then blog posts matching the title or body content are returned
```

**Story Points:** 5
**Dependencies:** ADMIN-005, INFRA-002
**Definition of Done:** Blog list renders; detail page renders; search works.

---

### STORY-CONTENT-002: Zodiac Compatibility Checker

**Persona:** As an anonymous visitor,
**I want:** to check the compatibility between two zodiac signs,
**So that:** I can quickly understand the relationship dynamic between myself and another person.

**Acceptance Criteria:**

```
Given I navigate to the Compatibility Checker
When I select two zodiac signs and click "Check Compatibility"
Then the result shows: overall compatibility score (out of 10), a compatibility narrative (80 words from seed data), and breakdowns for Love, Friendship, and Work

Given I select the same sign for both inputs
When the result renders
Then a self-compatibility result is shown (144 pairs cover same-sign combinations)

Given the result is shown
When I click "View Detailed Kundli Match"
Then I am directed to the Kundli Matching form (KUNDL-008) with a prompt to enter birth details for a deeper analysis
```

**Story Points:** 3
**Dependencies:** INFRA-002 (144 compatibility pairs seed)
**Definition of Done:** All 144 pairs return results; CTA to Kundli matching present.

---

### STORY-CONTENT-003: Numerology Calculator

**Persona:** As an anonymous visitor,
**I want:** to enter my name and date of birth and receive my numerology life path number and personality interpretation,
**So that:** I can explore numerology as an entry point to the platform.

**Acceptance Criteria:**

```
Given I navigate to the Numerology Calculator
When I enter my full name and date of birth and submit
Then the life path number is computed (sum of all DOB digits, reduced to 1–9 or 11, 22, 33)
And the name number (Chaldean or Pythagorean method) is computed and displayed
And a 200-word interpretation for each number is shown from the numerology content store

Given I enter a name with non-English characters
When the calculation runs
Then special characters are handled gracefully (mapped to their phonetic English equivalent)

Given the result is shown
When I am not logged in
Then a CTA "Get a detailed numerology reading from an astrologer" links to the Astrologer Directory
```

**Story Points:** 5
**Dependencies:** INFRA-002
**Definition of Done:** Life path and name numbers computed correctly; interpretations shown; CTA links to directory.

---

### STORY-CONTENT-004: Baby Name Generator

**Persona:** As a registered user,
**I want:** to generate astrologically auspicious baby name suggestions based on the baby's birth Nakshatra,
**So that:** I can choose a name aligned with Vedic tradition.

**Acceptance Criteria:**

```
Given I navigate to the Baby Name Generator
When I enter the baby's date, time, and place of birth and select gender
Then the Moon Nakshatra at birth is computed
And a list of 20 suggested names starting with the traditional syllables for that Nakshatra is shown (from nakshatras seed data)

Given the TOB is not available
When the form is submitted without TOB
Then I see: "Time of birth is needed to calculate the birth Nakshatra accurately. We'll use noon as a default — the Nakshatra may be approximate."
And the calculation proceeds with noon default

Given names are shown
When I click "Copy Names"
Then all names are copied to clipboard with a toast "Names copied to clipboard"
```

**Story Points:** 5
**Dependencies:** INFRA-002 (Nakshatra seed with syllables)
**Definition of Done:** Nakshatra computed; 20 names returned for that Nakshatra; TOB-absent handled.

---

### STORY-CONTENT-005: Panchang-Based Muhurat for Custom Date

**Persona:** As a registered user,
**I want:** to find an auspicious date within a date range for a specific activity,
**So that:** I can plan an important event (wedding, travel, business) with Vedic guidance.

**Acceptance Criteria:**

```
Given I select an activity type, date range (up to 30 days), and location
When I submit
Then the system computes Panchang for each date in the range and returns a ranked list of the top 5 most auspicious dates with their best Muhurat windows

Given no auspicious date exists in the range
When the result is returned
Then I see "No highly auspicious dates found in this range. Consider expanding the date range."

Given the computation is done
When I click on a recommended date
Then I am taken to the Muhurat Calculator (HORO-006) pre-filled with that date
```

**Story Points:** 5
**Dependencies:** HORO-005, HORO-006
**Definition of Done:** Date range scanning works; top 5 dates returned; links to Muhurat calculator.

---

## Epic: NOTIF — Notifications

**Epic Goal:** Users receive in-app bell notifications and transactional emails for key platform events. Astrologers receive alerts when a seeker is waiting.

---

### STORY-NOTIF-001: In-App Notification Bell

**Persona:** As a registered user,
**I want:** to see a notification bell in the navigation that alerts me to platform events,
**So that:** I am aware of important actions without constantly checking email.

**Acceptance Criteria:**

```
Given I am logged in and a notification is created for me
When the notification is delivered via Socket.io
Then the bell icon in the navigation shows an unread count badge that increments

Given I click the bell icon
When the notification panel opens
Then I see a list of my notifications sorted by date (newest first) with: icon, title, body, timestamp, and read/unread status

Given I click a notification
When it is clicked
Then it is marked as read (notifications.read_at set) and if it has a link, I am navigated there
```

**Story Points:** 5
**Dependencies:** AUTH-001, INFRA-004
**Definition of Done:** Bell badge increments on new notification; panel shows list; click marks read.

---

### STORY-NOTIF-002: Transactional Email Notifications

**Persona:** As a registered user,
**I want:** to receive transactional emails for key account events (registration, astrologer approval, session summary),
**So that:** I have a record of important platform activity in my inbox.

**Acceptance Criteria:**

```
Given I register a new account
When the registration is confirmed
Then within 60 seconds I receive a welcome email with: my name, a link to complete my profile, and a platform overview

Given an admin approves my astrologer application
When approval is processed
Then within 60 seconds I receive an approval email with next steps to set my availability

Given a consultation session ends
When the session is marked COMPLETED
Then within 5 minutes I receive a session summary email with: astrologer name, date, duration, coins spent, and a link to leave a review
```

**Out of scope:** Marketing emails; newsletter.
**Technical Notes:** Email dispatch via BullMQ email-dispatch queue; AWS SES or SendGrid; HTML email templates.
**Story Points:** 5
**Dependencies:** INFRA-004, AUTH-002, ASTR-003
**Definition of Done:** All 3 email types sent by BullMQ; correct content; delivered within stated SLA.

---

### STORY-NOTIF-003: Low Wallet Email Alert

**Persona:** As a registered user with a low wallet balance,
**I want:** to receive an email alert when my balance drops below a threshold,
**So that:** I can recharge before running out during a consultation.

**Acceptance Criteria:**

```
Given my wallet balance drops below 50 Coins
When any wallet deduction is processed
Then a BullMQ job dispatches a low wallet alert email: "Your AstroTalk wallet is running low. You have X Coins remaining. Recharge now."

Given I have already received a low wallet alert today
When my balance drops further
Then no second email is sent today (rate-limited to 1 per user per day via Redis key: low_wallet_alert:{userId}:{date})

Given I recharge and my balance exceeds 50 Coins
When the next deduction drops me below 50 again
Then the daily rate-limit resets at midnight and I can receive another alert the next day
```

**Story Points:** 3
**Dependencies:** WALLET-001, NOTIF-002
**Definition of Done:** Alert email sent on < 50 coins; rate-limited to 1/day; resets at midnight.

---

### STORY-NOTIF-004: Astrologer Online Alert

**Persona:** As a registered user,
**I want:** to receive an in-app notification when a specific astrologer I have bookmarked comes online,
**So that:** I can start a consultation immediately when my preferred astrologer is available.

**Acceptance Criteria:**

```
Given I have bookmarked an astrologer from their detail page
When that astrologer toggles their status to Online (ASTR-005)
Then I receive an in-app notification: "{Astrologer Name} is now online. Start a consultation!"

Given the notification is delivered
When I click it
Then I am taken directly to that astrologer's detail page with the "Start Consultation" CTA visible

Given I have bookmarked 5 astrologers and all 5 come online simultaneously
When all 5 status updates are processed
Then I receive 5 separate in-app notifications
```

**Story Points:** 3
**Dependencies:** ASTR-005, NOTIF-001
**Definition of Done:** Bookmark → online event → in-app notification → links to astrologer page.

---

### STORY-NOTIF-005: Admin Notification for New Astrologer Application

**Persona:** As a platform admin,
**I want:** to receive an in-app notification when a new astrologer submits an onboarding application,
**So that:** I can review and approve applications promptly.

**Acceptance Criteria:**

```
Given a new astrologer submits an onboarding application (ASTR-003)
When the application is saved
Then all users with role = ADMIN receive an in-app notification: "New astrologer application from {name}. Review now."

Given the admin clicks the notification
When navigated
Then they are taken directly to the astrologer's pending application in Admin → Astrologers → Pending

Given the application is subsequently approved or rejected
When the status changes
Then the notification is marked as actioned (visual indicator updated)
```

**Story Points:** 2
**Dependencies:** ASTR-003, ADMIN-003, NOTIF-001
**Definition of Done:** Admin receives notification on new application; click navigates to pending review.

---

## 17. Open Questions Log

| ID | Question | Status | Impact |
|----|----------|--------|--------|
| OQ-01 | Should Track B remain on Node.js (as mandated) or follow the Track A Laravel revision? Answered with assumption A1: Node.js stays. | **Assumed** | Stack for all subsequent epics |
| OQ-02 | What is the platform commission rate (%)? Assumed 20% but should be confirmed by PO. | **Open** | WALLET-005, ADMIN-007 |
| OQ-03 | Should the free session be 5 minutes as assumed (A9), or a different duration? | **Open** | CHAT-008 |
| OQ-04 | Is the Vedic corpus (zodiac sign descriptions, Nakshatra syllables, etc.) to be authored entirely by the Dev agent, or will PO provide source text? | **Open** | Seed data timeline in Sprint 0 |
| OQ-05 | Should the Kundli PDF use North Indian or South Indian chart style by default, or offer both? | **Open** | KUNDL-007 |
| OQ-06 | Is the Admin panel built as a separate React app or lazy-loaded admin routes in the main app? This is ADR-008 for the Architect to decide. | **For Architect** | ADR-008 |
| OQ-07 | Should anonymous Kundli generation (KUNDL-009) be available only once per guest session, or unlimited? | **Open** | KUNDL-009 scope |
| OQ-08 | What currencies should the wallet support? Assumed INR only (A4). Confirm before WALLET-002 implementation. | **Assumed** | WALLET epic |
| OQ-09 | Is the panchang-engine npm library the mandated choice for Panchang computation, or should the Architect evaluate alternatives? | **For Architect** | ADR (new — Architect to raise) |
| OQ-10 | Does the COMPARISON-REPORT.md (Sprint 7 deliverable) require real production deployment metrics, or lab/local measurements are acceptable? | **Open** | Sprint 7 scope |

---

## 18. Domain Glossary

All agents must use these definitions consistently across documents, stories, and code.

| Term | Definition | Used In |
|------|-----------|---------|
| **Kundli / Janam Kundali** | Vedic birth chart mapping planetary positions at the moment of birth. The core product artifact of the Kundli Engine. | KUNDL epic, Kundli engine |
| **Lagna / Ascendant** | Zodiac sign rising on the eastern horizon at birth. Changes every ~2 hours. Requires exact birth time (TOB) to calculate. | KUNDL-001, KUNDL-002 |
| **Nakshatra** | One of 27 lunar mansions in Vedic astrology. Each spans 13°20' of the ecliptic. The Moon's Nakshatra is the basis for Dasha calculation and baby names. | KUNDL-003, KUNDL-005, CONTENT-004 |
| **Dasha** | Planetary period system. Vimshottari Dasha spans 120 years across 9 planets in a fixed sequence. | KUNDL-005 |
| **Mahadasha** | The major planetary period within Vimshottari Dasha. One of 9 Grahas governs at any time. | KUNDL-005 |
| **Antardasha** | Sub-period within a Mahadasha. Each Mahadasha contains 9 Antardashas. | KUNDL-005 |
| **Panchang** | Hindu almanac: 5 daily elements — Tithi, Vara (weekday), Nakshatra, Yoga, Karana. Governs auspicious timing. | HORO-005, HORO-006, CONTENT-005 |
| **Tithi** | Lunar day. 30 Tithis per lunar month. Determines auspiciousness for activities. | HORO-005 |
| **Muhurat** | Auspicious time window for an activity, computed from Panchang elements. | HORO-006, CONTENT-005 |
| **Gun Milan / Ashta Koot** | 8-point Vedic compatibility scoring system for marriage matching. Maximum 36 points total. | KUNDL-008 |
| **Ayanamsa** | Angular difference between tropical and sidereal zodiacs. Lahiri Ayanamsa (~23.85°) is the standard for Vedic computation. Enforced via SIDM_LAHIRI in Swiss Ephemeris. | KUNDL-001, all ephemeris computation |
| **Graha** | Sanskrit for planet. The 9 Vedic Grahas are: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu (North Node), Ketu (South Node). Uranus/Neptune not used. | KUNDL-003, Planetary table |
| **Bhava** | One of 12 houses in a Kundli chart. Each governs a domain of life (e.g., Bhava 1 = Self, Bhava 7 = Partnership). | KUNDL-003 |
| **Rahu Kaal** | Inauspicious time period each day (~90 minutes). Varies by weekday and location. Shown on Panchang page. | HORO-005 |
| **Wallet Coins** | Platform currency. 1 Coin = ₹1 (configurable by admin). Used for per-minute consultation billing and AstroMall purchases. | WALLET epic, CHAT epic, MALL epic |
| **ContentService** | Backend service pattern: Redis cache-first → Claude API on miss → 3x exponential backoff retry → graceful fallback. Used for all AI-generated content. | KUNDL-004, HORO-001 |
| **Billing Tick** | BullMQ repeatable job that fires every 60 seconds per ACTIVE consultation. Deducts per-minute rate from seeker's wallet using SELECT FOR UPDATE. | CHAT-003, CHAT-004 |
| **BMAD** | Build–Measure–Analyze–Deploy. The AI agent framework used in Track B. Not a software package — a process methodology with 5 Claude personas. | This document |
| **SELECT FOR UPDATE** | PostgreSQL row-level lock used in all wallet deduction operations. Prevents race conditions in concurrent billing. Mandatory via Prisma.$transaction(). | CHAT-003, WALLET-002 |
| **Swiss Ephemeris** | Astronomical calculation library (node-swisseph). Authoritative source for planet longitudes, house cusps, and Ascendant. Claude API interprets; never computes. | KUNDL-001, KUNDL-002 |
| **Vimshottari Sequence** | Ketu (7y) → Venus (20y) → Sun (6y) → Moon (10y) → Mars (7y) → Rahu (18y) → Jupiter (16y) → Saturn (19y) → Mercury (17y). Hardcoded in shared/constants.ts. | KUNDL-005 |
| **has_used_free_session** | Boolean flag on the users table. True after the first free 5-minute consultation is used. Prevents second free session. | CHAT-008 |
| **P0 / P1 / P2** | Priority tiers. P0 = Sprint 1–3 (must-have). P1 = Sprint 4–6 (should-have). P2 = Sprint 7+ (nice-to-have). | All epics |

---

## Appendix: Story Count Summary

| Epic | Stories | Priority |
|------|---------|---------|
| INFRA | 4 | P0 |
| AUTH | 8 | P0 |
| ASTR | 7 | P0 |
| CHAT | 9 | P0 |
| WALLET | 7 | P0/P1 |
| KUNDL | 9 | P0/P1 |
| HORO | 8 | P0/P1 |
| ADMIN | 8 | P0/P1 |
| CONTENT | 5 | P1/P2 |
| MALL | 6 | P1/P2 |
| NOTIF | 5 | P1/P2 |
| **TOTAL** | **76** | |

---

*PRD.md — AstroTalk Replica Track B | BMAD Framework | PM Agent Output v1.0*
*Next step: PO (Arun) reviews and approves → Architect Agent is activated.*
