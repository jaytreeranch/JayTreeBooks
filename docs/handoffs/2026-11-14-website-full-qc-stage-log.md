# JayTreeBooks website QC stage log — 2026-11-14

Status: REVIEW BRANCH TESTED — NOT MERGED / NOT DEPLOYED. This is not a live production fix receipt.

## Steps verified
1. JT-DESKTOP, JT-GE75, JT-GE78 native tunnel hostname tests PASS. Read mandatory `AGENTS.md`, `docs/CURRENT_HANDOFF.md`, and LAN control policy. Production source main at initial audit: `6f63aee0c56cf899f02bd23db700b26f15d813f9`.
2. Public HTTP: 26/26 sitemap URLs 200; 28/28 additional same-origin navigation/assets successful; 20/20 narrator MP3 HEAD 200; privacy, terms, chapter samples accessible. Six Payhip links correct, edition-specific; no seller login or paid orders repeated.
3. Chrome mobile and desktop rendered QC: 390px / 1365px, no sideways overflow, mobile menu opens. Mobile homepage 19,296px document; audiobook section ~13,241px down. Fixed Install App overlays content on live production.
4. Live synthetic click events (no actual outbound navigation): homepage 0→1, regular Correction detail 0→1, novella 0→0 `audiobook_payhip`. Browser event defect confirmed.
5. GitHub development branch created. Novella metadata, PWA duplication, Escape menu and click handler fixed. Five existing narrator comparison sample pages had outdated in-production sales copy, missing Payhip CTAs, duplicated click handlers; corrected all five. PWA install button moved out of fixed sales overlay into footer/end-body.
6. Local branch browser click checks: novella 0→1, first audio sample 0→1. Source downloaded from GitHub review branch to LAN. Node regression suite: **24/24 PASS**, JS syntax checks PASS.
7. Commercial boundary: seller visible and $0 delivery tests documented in previous production handoff; current audit did not conduct seller login, nonzero payment, or payout reconciliation. Current live buyer actions unaffected; no Payhip visibility changes.
8. Reporting boundary: GSC Wizard subscription required; Windsor.ai refuses all reads because Free plan 1-account cap vs 5 connected accounts. No GA4/GSC behavioral metrics represented as verified.

## Change list
- `books/the-hollow-bell-novella.html` — tracking, menu, SEO descriptions, one PWA script
- `audio/book-{1..5}-sample.html` — correctly disclosed $1.99 Vivian edition, sale links, remove duplicate event listeners
- `pwa.js` and `pwa.css` — install prompt stops covering purchase actions
- `tests/novella_sale_telemetry.test.js`
- `tests/audiobook_sample_sales_flow.test.js`
- `docs/handoffs/2026-11-14-website-full-qc-audiobook-journeys.md` — thorough report
- `docs/CURRENT_HANDOFF.md` — continuity pointer

## Remaining / exact next steps
- Review this feature branch against moving main, consider staged PR. No production deploy has been authorized in this audit.
- Add/remove no products; leave six $1.99 Vivian listings untouched and older $5 Correction listing hidden.
- Once owner approves rollout, rerun tests, merge carefully, verify Pages deployment and six static links + 5 sample pages in public HTTP, then browser-check novella click count exactly one and install prompt no longer overlays page.
- Review Payhip privacy/terms disclosures (no unapproved legal promises), home-first-screen $1.99 promo, dedicated audiobook hub, Core Web Vitals, WCAG tests.
- Analytics restore and paid settlement are separate operator-approved workstreams.

## Rollback
Revert only site source changes on main if a buyer-facing regression is found, preserve good six-product Payhip sales; original master packages and private buyer receipts remain on JayTree LAN. Do not revert unrelated concurrent production work.

## Evidence
`\\JT-DESKTOP\JayTreeFarm\Projects\JayTreeBooksWebsiteAudit_20261114\` contains immutable generated receipts/screenshots and scripts. Before declaring fully preserved, verify remote feature head SHA, this stage log and the LAN report paths/checksums.
