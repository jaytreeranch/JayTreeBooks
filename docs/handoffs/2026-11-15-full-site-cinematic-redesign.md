# Full-site cinematic redesign — 2026-11-15 UTC

Review branch: design/multipage-storefront-review-20261114. Draft PR #32: https://github.com/jaytreeranch/JayTreeBooks/pull/32
Status: DEVELOPMENT REVIEW ONLY; NOT merged into main or publicly deployed.

## Completed source
- Applied coordinated premium midnight/navy/gold styling across 34 pages with cinematic-site-v2.css and cinematic-site-v2.js, generated idempotently by scripts/build_sitewide_preview.py.
- Shorter Home home-v2.html, Books, Audiobooks, Samples, new Series series-v2.html, News news-v2.html and Experiences experiences-v2.html pages. Responsive seven-link navigation and searchable titles keep the two Hollow Bell editions distinct.
- Preserved full content, SEO canonical URLs, KU messaging, trailers, reading guides, related books and original audio sales CTA in all six book detail pages. Added a near-top format/sale bar pointing to the identical correct title-specific Payhip product.
- Preserved all six approved Vivian narrator sample pages, five first chapters, Kit subscription, Challenge links, video experiences, existing About/Upcoming/discovery pages, Privacy and Terms. Common navigation styling only; no original audio media was touched.
- Original production index.html remains untouched. New home URL home-v2.html is a design prototype. The six available Vivian audiobooks remain $1.99 each; alternative full-length narrator editions are the only narrators coming soon.
- Central JSON catalog and safe future-book release scripts remain intact.

## Verified QC
- JT-DESKTOP Local Control hostname_test PASS; AGENTS.md, current handoffs and standing local tunnel policy followed.
- 34/34 generated pages in sync, generator --check PASS.
- 38/38 responsive Chrome viewport tests PASS (1440 desktop, 390 and 320 phone as relevant), no broken local image assets or horizontal scroll.
- 18/18 real thumbnail selection checks PASS across six titles and three widths, maintaining correct selected details, Payhip SKU, final audio sample and aria-pressed.
- 5/5 Chrome search/mobile navigation checks PASS; searching Hollow Bell finds correct distinct full novel and novella pages.
- Node storefront tests 16/16 PASS; Python central catalog tests 8/8 PASS; Python sitewide tests 8/8 PASS; historic audiobook commerce and narrator tests 40/40 PASS.
- Visual evidence: authorized LAN F:\JayTreeFarmStorageV2\Projects\JayTreeBooksWebsiteRedesign_20261114\FULL_SITE_REDESIGN_REVIEW.html (14 desktop/mobile pairs), gallery SHA256 1CA7FAA7C2A42A6EA7CA1EE548BF8C6E50F7F411C6E1079D6E8208537CE1ED45. Receipts full_site_browser_qc.json, sitewide_featured_selector_qc.json, sitewide_navigation_search_qc.json, site-*.png.

## Not yet complete / release blockers
1. Owner-approved photorealistic lake and gold-black headphones PNG/WEBP art remain in separate ChatGPT conversation assets; not imported into LAN or GitHub. The current sitewide imagery is still an SVG approximation. Do not claim exact visual parity.
2. Before replacing production index.html, preserve/migrate #books, #audiobooks, #challenge, #case-files, #youtube, #about and other historical anchors; keep canonical/OG/schema/sitemap, Kit and GA4 tracking, and account for legacy GitHub workflow generators.
3. Full screen-reader WCAG, zoom/contrast, LCP/CLS/INP, real Search Console/GA4 and real-money Payhip settlement not certified. No paid transaction performed.
4. Pre-existing typography corruption in some older content was preserved rather than editorially rewritten. Review separately before launch.
5. Reconfirm exact audiobook sample SHA/rights from the authoritative audiobook team as part of final coordinated launch.

## Next
Import and certify the two approved cinematic photo layers, owner-review fourteen page pairs, fix legacy encoding / SEO migration with source review, run full accessibility/performance/seller QC, reconcile current main and obtain distinct owner production launch approval. Never merge PR #32 until expressly authorized. Rollback: close/revert review branch; live main, Payhip listings and private audio masters untouched.
