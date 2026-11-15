# JayTree Books — Full Website Journey & Audiobook Commercial QC
**Date:** 2026-11-14 (America/Chicago)  
**Repository:** `jaytreeranch/JayTreeBooks`  
**Production:** `https://jaytreebooks.com/`, GitHub Pages, `main`  
**Development remediation branch:** `fix/website-novella-qc-20261114`  
**Review status:** AUDITED, HIGH-PRIORITY PATCHES STAGED AND TESTED, **NOT DEPLOYED**

## Executive outcome

The current website serves six independently linked Vivian audiobook offers at $1.99. Historical certified seller and owner test receipts documented in `docs/CURRENT_HANDOFF.md` show six products visible, $0 owner-controlled purchase and MP3/M4B delivery tests, ACX clearance, and no confirmed nonzero payment/payout. In this new session we independently verified public HTTP, all six website purchase URLs, and rendered browser paths, but **did not log into the seller dashboard or execute a nonzero payment**.

The strongest technical finding was missing `audiobook_payhip` event tracking on the Hollow Bell novella page. A second commercial problem was that all five narrator-comparison sample pages still said the full audiobooks were in production and had no direct purchase offer. Their existing audio script and footer also registered overlapping click handlers, risking duplicate GA4 events. All are repaired **only on the development branch** and tested there. A fixed PWA install button obscured purchases, and outdated novella meta descriptions could mislead search/social visitors; both patched on branch.

### Verified public-site checks

| Area | Evidence / result | Gate |
| --- | --- | --- |
| Sitemap pages | 26/26 returned HTTP 200 | PASS |
| Additional same-origin internal paths/assets | 28/28 returned successful HTTP responses | PASS |
| Direct Payhip links | Homepage six approved unique URLs; six static book pages each contain their own correct URL, price $1.99 and MP3/M4B copy | PASS (website links only) |
| Canonical host | HTTPS apex 200; www redirects to apex | PASS |
| Published narrator preview files | 20/20 MP3 HEAD checks HTTP 200, with `audio/mp3` content type | PASS (reachability, not playback/QC of audio content) |
| First-chapter paths | Spot-checked chapter one for Second Draft and Hollow Bell, HTTP 200, with continuing reading links | PASS (sampled) |
| Privacy / terms | Both pages HTTP 200, existing Google Analytics, Kit and third-party service language | PASS for reachability; legal copy needs review |
| Mobile viewport | Chrome emulated 390×844: homepage, novella and menu; no horizontal overflow; menu opens and sets `aria-expanded` | PASS for sampled layout |
| Desktop viewport | Chrome 1365×900, no horizontal overflow | PASS for sampled layout |
| Mobile reader purchase journey | Audiobook section starts roughly 13,241px down a 19,296px-high homepage; accessible by header menu anchor, not directly featured in hero | CONVERSION FRICTION |
| Install CTA | Fixed bottom-right install button overlays content/CTA in mobile screenshots | FAIL UX; branch patch |
| Analytics click intent | Chrome `window.dataLayer` clicked homepage Payhip CTA 0→1; Correction static page 0→1; Hollow Bell novella static page 0→0 | FAIL for novella in live production |
| Branch novella analytics | Same test on locally downloaded review branch novella: 0→1 | PASS (development only) |
| Branch sample purchase intent | Same click test on the patched Second Draft narrator sample page: 0→1 | PASS (development only) |
| Source regression tests | 24/24 Node tests PASS, 0 failures; `node --check app.js`, `pwa.js`, `audio/audiobook-experience.js` PASS | PASS (development only) |
| Search impressions, GA4 sessions, real sales conversion | GSC Wizard trial/subscription expired; Windsor.ai read requests blocked by plan/account limit | BLOCKED — no real traffic metrics asserted |
| Nonzero paid order, settlement and Payhip-to-GA4 purchase event | No paid test or settlement proof in existing launch record; not attempted here | NOT VERIFIED |
| Lighthouse, automated accessibility audit, third-party checkout live browser | Not performed in this session; no performance score or WCAG certification claimed | OPEN |

### Sales links — preserve these six identities

| Edition | Direct Payhip offer |
| --- | --- |
| The Absconding | https://payhip.com/b/q3GfL |
| The Hollow Year | https://payhip.com/b/Zf7tv |
| Second Draft | https://payhip.com/b/GejHn |
| The Correction — Vivian | https://payhip.com/b/OPaGw |
| The Hollow Bell novella | https://payhip.com/b/EWc5q |
| The Hollow Bell full novel | https://payhip.com/b/0BeoF |

Do not change the unrelated older $5 Correction Payhip SKU, currently recorded Hidden in seller receipts. Payhip direct anonymous HTTP may return 403 anti-automation; no anonymous crawler response was treated as seller visibility evidence.

## Journey and design observations

1. **Homepage discovery → sale:** Brand/color palette is coherent (dark mystery with warm gold), and six crawlable HTML book cards are available without JavaScript. The first mobile screen presents four reading/trailer/book actions but no $1.99 audiobook path. The six-book sales section is deep below several other campaigns, even though the menu links directly to `#audiobooks`. Recommend a visible first-screen audiobook offer with clearly identified Vivian format, followed by an optional dedicated `/audiobooks.html` landing page. The latter currently returns 404 but is **not** a broken link on the site: the live navigation uses an in-page anchor.
2. **Book detail → checkout:** All six independent static book pages show the correct book-specific Payhip link, digital MP3 and chaptered M4B, synthetic-voice disclosure and no artificial promotional end date. Hollow Bell novella correctly differentiates the shorter edition from the full novel. Purchase CTAs are safe external links (`rel=noopener noreferrer`).
3. **Audio sample → checkout:** The five existing audio sample pages contain 4 preview voices per novel. Before patching, all said Classic audiobooks were still in production and did not link directly to live sale. Updated on branch to explain only the complete Vivian edition is for sale, keep other voices preview-only, retain Immersive as genuinely coming soon, and provide top/bottom direct $1.99 CTAs. Existing `audiobook-experience.js` tracks narrator starts/completions; removed redundant footer `data-track` binding that risked double events.
4. **Novella audio discovery:** The novella book page offers the standalone audiobook but has no corresponding narrator comparison/sound preview. A verified novella-specific Vivian sample is a potential future conversion enhancement; do not repurpose unrelated or unapproved source audio.
5. **Read/listen follow-through:** Chapter pages have Amazon and return-to-book controls; narration preview pages have four audio players that load metadata. Future work: review whether current four-voice section needs clearer "preview only" messaging at the homepage entry point and provide a clear direct purchase CTA on every audiobook sample.
6. **Mobile PWA overlay:** The sticky `Install App` button obscured call-to-action content in the homepage and novella live screenshots. Branch moves button to footer or end of body with `position:static` without disabling install functionality. Screenshots verify original impact; branch static tests verify fix, though full patched visual screenshot is still desirable.
7. **Accessibility:** Sampled pages have H1, meta viewport, alt text and visible keyboard focus styling. Mobile menu works; novella Escape closing fixed on branch. No full WCAG 2.2 color-contrast, screen-reader, keyboard trap, zoom-to-400%, or automated axe assessment was completed. Tiny uppercase CTA labels deserve review.
8. **Security/commerce trust:** HTTPS, canonical redirects, third-party safe link attributes, and `strict-origin-when-cross-origin` meta observed. Response checks did not show `Content-Security-Policy` or `Strict-Transport-Security` headers; GitHub Pages hosting constraints require a deployment-architecture review before changing response headers. The existing privacy/terms pages lack explicit Payhip/direct audiobook sale disclosures and applicable support/fulfillment/refund references; review with the owner and appropriate legal/compliance guidance before changing policy text. Do not invent refund promises.
9. **SEO:** Distinct titles/canonical/meta descriptions across 26 sitemap pages and six crawlable catalog cards; novella static metadata stale despite live sale (patched). Search Console indexed impressions, rankings and CTR could not be verified due both reporting connector restrictions. Dynamic Mini-Series anchor flagged by static parser is correctly created on loaded pages and works with JavaScript; it is not a live broken navigation link.

## Exact changes staged in development branch (not deployed)

- `books/the-hollow-bell-novella.html`: current sale metadata; delegated `data-track` click dispatch; Escape closes menu; one PWA script, not two.
- `audio/book-{1..5}-sample.html`: correct live Vivian pricing, preview-only alternate narrator wording, two book-specific Payhip CTAs, remove duplicated outbound click listeners; preserve four existing samples and immersive coming-soon.
- `pwa.js`, `pwa.css`: footer/end-of-page inline install affordance instead of fixed overlay.
- `tests/novella_sale_telemetry.test.js`, `tests/audiobook_sample_sales_flow.test.js`: new regression coverage, together with existing purchase tests total **24 PASS**.

### Current priority backlog

**P0 — Review and deploy the tested branch safely:** confirm current main has not advanced incompatibly; review PR/patch; run 24 tests on final head, check screenshot and first-screen CTA; merge only with production authorization; verify GitHub Pages receipt and all pages + event counts after cache refresh. Rollback a faulty site change by reverting the affected main commit; leave all six certified Payhip products Visible unless a real buyer failure is confirmed.

**P1 — Proper confirmed-sale telemetry:** audit actual completed orders from Payhip using approved server-side or authorized webhook reconciliation, dedupe on transaction ID, emit GA4 `purchase` only on confirmed payment, never on click or $0 test. Avoid exposing order/buyer identifiers in GitHub or browser logs. Current `audiobook_payhip` measures **outbound intent only**. `case_files_signup_submit` may represent a form attempt; count `sign_up` only from verified Kit confirmation.

**P1 — Restore real analytics:** GSC Wizard reports `payment_required`; Windsor.ai reports 5 connected accounts on Free plan (1 allowed) and refuses all data reads, including GA4 property 549202437 and Search Console `sc-domain:jaytreebooks.com`. Do not disconnect users' channels automatically. Once access resumes compare acquisition source, page exits, sample-play → sale-click funnel, and real Payhip completed orders.

**P1 — Conversion and content design:** Surface six audiobooks closer to the top of homepage, make a lightweight dedicated audiobook landing/catalog page and links on relevant book/sample pages, show duration, formats, the Vivian narrator and download method before handoff, make voice-preview-only disclosures prominent. Maintain unique-mechanism-first positioning. Avoid confusing the novella and full-length edition.

**P1 — Real-money settlement smoke test:** Only with explicit informed owner approval for the actual charge, one small nonzero order and processor/payout reconciliation; prior $0 owner checkout and hash verified digital fulfillment, not real-money settlement.

**P2 — Confidence/build:** repair prelaunch Reader Growth Site CI tests that still expect five books or "Coming Soon" while preserving six live offers; run Lighthouse/LCP/CLS/INP and 320/375/390/768/1440 widths, screen reader and high-zoom checks; validate GSC performance once available; review HSTS/CSP hosting options and Payhip disclosures.

## Evidence, storage and continuity

**Verified machine:** JT-DESKTOP via native JayTree Local Control `hostname_test` PASS. GE75 and GE78 tunnels also passed initial identity check; they were not needed for this website job.

**Private/review evidence (LAN only):** `\\JT-DESKTOP\JayTreeFarm\Projects\JayTreeBooksWebsiteAudit_20261114\`
- `website_qc_live_http_20261114.json` and `site_audit.py`
- `website_qc_chrome_metrics_20261114.json` and mobile/desktop screenshots
- `website_qc_tracking_clicks_20261114.json` (live) vs `website_qc_tracking_branch_20261114.json` (local branch)
- `website_qc_audio_sample_branch_click_20261114.json`
- `site_detail_checks_20261114.json` — public privacy/terms/preview reachability
- `source-qc/` — source fetched from GitHub review branch at the tested checkpoint
- `QC_REPORT_20261114.md` and `QC_STAGE_LOG_20261114.md`

**Source preservation:** GitHub feature branch `fix/website-novella-qc-20261114`; review via `https://github.com/jaytreeranch/JayTreeBooks/tree/fix/website-novella-qc-20261114`. Confirm its **remote head SHA** in the final handoff, then do not claim live deployment without an independently successful Pages run.

**Next exact action:** Review / optionally extend branch with hero audiobook offer and legal copy after approval; run the tests again; if authorized merge, independently verify the six live book CTAs, five narrator sample pages, novella GA4 click 0→1 and non-floating install affordance, then record public production receipt. Separate seller/paid transaction workstream from website UI review.
