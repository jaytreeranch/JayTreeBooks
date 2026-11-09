# Upcoming novels promotion implementation plan

**Goal:** Publish the owner-approved three-novel promotion and measure reader interest.

**Architecture:** Extend the existing static website with one landing page and a shared promo-only stylesheet/event script. Reuse current site styles, GA4 and existing publication links. Upload one atomic Git tree after local verification, with a compare-and-swap branch update.

**Spec:** UPCOMING_PROMO_SPEC.md

- [ ] Add behavioral event tests for once-per-load visibility, click attribution, local-traffic suppression and missing analytics.
- [ ] Implement upcoming-books.html, upcoming.css and upcoming.js; integrate homepage teaser/navigation and five first-chapter cards; optimize approved art to WebP.
- [ ] Validate links, readable desktop/mobile layouts, event behavior and GA4 configuration. Reporting connector is subscription-blocked; verify instrumentation separately and disclose reporting limit.
- [ ] Publish assets/source/docs atomically on authorized main; verify remote SHA, Pages completion and live page/assets; record exact receipts and rollback.

Constraints: no invented release dates, no future-book samples claimed available, no completed-signup or purchase claims from clicks, preserve existing scripts/campaigns and all prior handoff content. Local preview is isolated in this workspace because shell networking and local GitHub credentials are unavailable; connected GitHub API remains functional.
