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
