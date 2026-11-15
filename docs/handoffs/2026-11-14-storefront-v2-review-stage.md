# JayTree Books multi-page storefront — development stage and QC, 2026-11-14 CST

Branch: design/multipage-storefront-review-20261114 (protected review, NOT merged).
Main baseline: ea3ee60b90e880d5c28bbfb219dfe8662a81a76d (after the concurrently edited audiobook samples).
Status: INITIAL FOUR-PAGE CONCEPT BUILT AND QC'D, OWNER VISUAL REVIEW PENDING, NO PRODUCTION DEPLOY.

## Completed scope

- Four static concept HTML pages: home-v2.html, books.html, audiobooks.html and samples.html. New book cards and shopping links are present in HTML even when JavaScript is disabled.
- Responsive premium dark/gold storefront visual system: storefront-v2.css, official JayTree tree/open-book logo from icons/icon-192.png, existing six published covers, white-space hierarchy, clear CTA choices, mobile HTML details menu, visible focus and reduced-motion support.
- storefront-v2.js records outbound INTENT once by delegated data-track listeners. Audio buyers are sent to the six exact existing Payhip SKU links; book buyers to six exact Amazon listings.
- Canonical audio preview pages from the other chat are used as links only; includes separate Hollow Bell novella audio/book-6-sample.html. No sample media, manifests, Payhip products or original website code changed.
- Preview-only noindex,follow metadata and production-host-restricted GA4 JavaScript to avoid test traffic contaminating the real property.
- Brand conversion plan and release safety gates at docs/design/STOREFRONT_V2_NAVIGATION_AND_LAUNCH_PLAN.md.

## Source/QA evidence

- JayTree Local Control hostname_test verified JT-DESKTOP; GE75, GE78 identity checks also performed. Owner's tunnel access policy and project AGENTS.md read.
- Immutable feature branch assets copied on JT-DESKTOP LAN at F:\JayTreeFarmStorageV2\Projects\JayTreeBooksWebsiteRedesign_20261114\preview\.
- 11/11 Node static storefront tests PASS, 0 failures.
- Headless Chrome direct rendering: 10/10 views PASS at 1440x900, 390x844 and 320x720. All visible product covers plus official logo loaded; no page rendered wider than its viewport. Mobile details navigation contains six destinations.
- Early mobile QC caught and fixed a cover-stack overflow; subsequent QC 10/10 PASS.
- Six published audio sample HTML URLs HTTP 200 and contain Vivian/player text; six sample link mappings, six separate Payhip SKUs and six book-detail paths verified in staged code.
- Screenshot review gallery: \\JT-DESKTOP\JayTreeFarm\Projects\JayTreeBooksWebsiteRedesign_20261114\REVIEW_INDEX.html (SHA-256 F38F63DC8B6EB2D6ADECF33A85A3CF8A506455E591A6CB36D8B97E823F158784 at gallery creation). Gallery has actual headless Chrome screenshots, no generated cover substitutions.
- Additional LAN QA receipts: browser_qc.json, storefront_links_qc.json, source_manifest.json, screenshots, and scripts browser_qc.py/sync_review_source.py/link_integrity_qc.py.
- No production Pages merge, no direct payment tests and no claim of full WCAG or full Core Web Vitals certification.

## Open / exact next steps

1. Owner reviews aesthetic and hierarchy in LAN gallery or design PR. Confirm final site menu and whether challenge, newsletter, reading guides, trailers and series information deserve a dedicated landing page or short home teaser.
2. Keep current production homepage and book detail pages unchanged while the review branch is open. Prepare six enhanced individual book sales pages and a safe mapping for old homepage section anchors, canonical SEO metadata and existing campaign links.
3. Confirm latest production main and final Vivian audio sample hashes from audio team's handoff before any future merge. No audio binaries or sample routes should be rewritten in this design PR.
4. Add end-to-end keyboard/zoom/contrast accessibility and seller redirect tests. Preserve GA4 intent events with the existing tracking.js wrapper, Kit signup, correct Payhip product identity and original Kindle Unlimited rules.
5. Only with owner review and launch authorization: merge coordinated redesign, watch GitHub Actions including legacy Reader Growth generator that still has obsolete coming-soon assumptions, inspect Pages build/deploy receipt, run public smoke suite, log production SHA.
6. If any buyer path or core SEO content is damaged, revert the website-specific merge and preserve six current approved Payhip product listings, their $1.99 prices and full audio masters.

## Reconciliation rule

Do not infer that the other chat's web/sample work must be repeated. Current main already has the sample updates and sixth novella sample page. The design prototype is based on that state and only creates new HTML/CSS/JS/tests/docs. Compare main at release time; in a conflict, rebase/reconcile only the new concept pages and preserve audio edits verbatim.

## Saved GitHub review PR

- Draft PR #32: https://github.com/jaytreeranch/JayTreeBooks/pull/32
- Review-only branch: design/multipage-storefront-review-20261114; owner explicitly requested not to merge the redesign into main yet.
- The original design scratch branch design/multipage-storefront-20261114 is superseded by this current-main-based review branch. Do not use the scratch branch for a production merge.
- All six preview destinations were independently verified against public HTTPS after the other chat completed its sample work. No audio files were touched.

## November 14 — Follow-up interactive hero and future-book publishing milestone (review branch)

- The six small cover thumbnails are real buttons (not links away). Selecting any cover replaces the featured book cover inside headphone framing, title, author/story hook, linked detail page and both selected real Payhip/preview destinations. It scrolls back to the featured display, is keyboard-activatable and keeps exactly one aria-pressed=true selection. Tested at 1440px, 390px and 320px.
- Buyer URL identity remains tied to the same HTML product card; The Hollow Bell full novel and novella have separate SKUs and different approved preview routes. All six Vivian editions are available now; alternative full-length narrators are coming soon.
- Added data/storefront-catalog.json (single source of truth), scripts/build_storefront_catalog.py (static catalog generator with --check / --write), scripts/new_storefront_title.py (safe future-title draft scaffold), tests/test_storefront_catalog.py (independent release-state QC), and docs/design/ADDING_NEW_BOOKS_TO_STOREFRONT.md.
- Generator updates Books, Audiobooks and Samples pages, selection metadata and supported catalog counts. New titles default coming_soon and carry **no fake checkout**; changing to published + audiobook available requires real seller/sample info. Featured audiobook initial state is derived from the catalog. Mixed prices/narrator disclosure assumptions are rejected pending explicit marketing review.
- **Tests:** 13/13 Node PASS, 8/8 Python PASS, catalog generator --check PASS against downloaded authoritative GitHub branch, helper dry-run preserved manifest checksum, Chrome **18/18 cover selections PASS** (six titles × desktop/390px/320px), no horizontal scrolling or broken cover images.
- During QC, remote source punctuation was damaged by text transfer; corrected with escaped-JSON ASCII transport, restored exact Unicode and verified --check on the **remote branch**, not merely a local file.
- **Important visual follow-up:** Current branch still uses SVG lake/headphones; owner-approved photorealistic generated images have been prepared separately in ChatGPT artifacts, but are **not yet on GitHub or LAN**. Import those assets and visually certify before claiming the screenshot style is achieved.
- Exact LAN evidence: F:\JayTreeFarmStorageV2\Projects\JayTreeBooksWebsiteRedesign_20261114\featured_selector_browser_qc.json and audiobook-selected-novella-{1440,390}.png. [Engineering handoff](2026-11-14-interactive-audiobook-and-catalog-growth.md).
- Not merged or deployed; PR #32 remains draft. Next: approved image integration, full-site redesign consistency, new title details/sitemap automation, accessibility/SEO/performance/commerce release QC and owner approval. Rollback: abandon/revert review branch, leaving live website, Payhip sellers, original masters and sample media untouched.
