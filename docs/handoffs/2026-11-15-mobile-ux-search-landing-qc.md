# JayTree Books: navigation, mobile conversion and organic search ? November 15, 2026

## User goal and release scope
User approved immediate quality improvements followed by Google search visibility review, with an ambition to reach page 1 for 'psychological mystery books' and 'new mystery book'. Work began from production commit df2260b4ff2a785db93cbacdb20ffb5132b1e70c, on feature branch fix/mobile-navigation-seo-20261115. Preserve all six sale-ready Payhip SKUs, site samples, live GA4, approved social cards, PWA and hidden JayTree paths.

## Implemented (development stage, publication pending)
- 15 modernized public pages carried both redesigned and legacy headers. Durable source-generator correction removes only replaced legacy header, preserving one semantic navigation landmark. It adds focusable 'Skip to main content' and a matching main#main to modernized legacy, audio and chapter pages. No private callback pages are opted into analytics.
- Home now links directly to both topical SEO hubs (psychological mysteries and new mystery books) without adding a new site-wide menu or duplicate product shelves.
- Both topical search pages: small-screen h1 sizing and overflow wrapping corrected after real Chrome found scrollWidth=362/399 at a 320px device width; follow-up isolate confirmed both now fit within 320px. Added intrinsic book cover dimensions to prevent avoidable layout jumps, plus a clearly named path to free samples and the six-authorized-audiobook sale shop.
- Added early preload for the existing optimized Second Draft home hero image (also marked fetchpriority=high), leaving other covers lazy loaded. Existing external seller and narrator asset URLs are unchanged.
- Durable tests under tests/test_single_navigation.py and tests/test_search_landing_quality.py validate header uniqueness, navigation, semantic landmarks, book-list structured data, canonicals, image dimensions, mobile CSS and the two target inbound home links.

## Current SEO baseline and limitations
- The two pages already have exact-intent titles, descriptive original book copy, canonical tags, CollectionPage/BreadcrumbList/ItemList markup, crawlable internal links, and are present in the site's sitemap. General public web searches surfaced both; this is evidence of discovery by a search engine, not a proven Google ranking.
- Google Search Console/GSC Wizard reports are subscription-blocked; Windsor.ai GA4/search-console data reads are blocked by connector count on Free. Therefore we have NO defensible verified ranking number, Google average position, click volume, CTR or indexed coverage. Do not guess or claim page-one ranking.
- Google's public PageSpeed API returned HTTP 429; do not invent performance or Core Web Vitals results. A local Chrome visual/layout test is not equivalent to field LCP/INP/CLS.
- Generic result sets for these terms include high-authority Goodreads, Penguin Random House, Book Riot, publisher and bestseller content, making generic broad keyword page-one goals highly competitive. Search results vary by location, user, date and device.
- Do not call books newly released in 2026 unless a real publication date is separately verified. Do not add misleading reviews, fake author awards, mass-generated near-duplicate pages, bought links or keyword stuffing.

## Quality control
- Static source generator must run: python scripts/build_sitewide_preview.py --check.
- Storefront catalog --check and social preview metadata --check must pass after future changes.
- Python and Node regression suites must pass, including public commercial links.
- Chrome at 320, 390 and 1440 widths for home, both SEO hubs, Privacy/Terms, case files, audiobook store, novella preview and book detail, with zero horizontal overflow or missing target navigation. Store QC receipts under LAN Projects/JayTreeBooksWebsiteRedesign_20261114/UX_SEO_20261115. No user purchase or subscription events are generated for QC.

## First-page SEO growth plan (not a guarantee)
1. Restore authorized first-party Search Console reporting. For exact queries 'psychological mystery books' and 'new mystery book', record a 28-day baseline split by US vs global and mobile vs desktop: impressions, clicks, CTR, average position, landing page URL, and 7/28-day movement. Inspect site and both hubs for Google indexing/canonical selections. Use correct domain property and existing sitemap.
2. Build topical authority without filler. Expand original, author-specific mystery reading guides only where they answer questions the current hubs do not, e.g., altered-record psychological mysteries vs unreliable-memory mysteries, psychological thriller vs psychological mystery, and independent small-town cold case mysteries; demonstrate the books' distinctive mechanisms, accurate bylines, snippets and first chapters.
3. Earn relevant editorial links and genuine reader mentions through independent mystery reviewers, genre newsletters, writing interviews, podcasts and book-community collaboration. Keep link-building voluntary, editorial and high-quality; no paid placement disguised as organic editorial coverage.
4. Review Search Console weekly. Prioritize high-impression queries with below-page-one positions, compare page-level CTR, correct intent and improve links/snippets. Keep two main hubs as canonical topic owners, avoid competing new pages using the same phrase.
5. Targets: page-one (average US position <=10 as one directional indicator, not a guaranteed single-SERP result) for exact phrases; secondary goals include free-sample engagement, audiobook store clicks, verified subscriber conversions, and independently documented Payhip purchases.

## Release status / rollback / next exact steps
SOURCE STAGED; do not claim live until PR CI, GitHub Pages and public QA receipts pass. Review feature branch diff against main; commit, push, open PR, verify required checks, merge without force-push, verify Pages; check all changed public pages after publication. Rollback: revert the targeted UX/SEO PR while preserving the preceding live GA4 repair and unrelated later commits; rerun generator and public QA. Analytics positioning still requires restoration of first-party GSC access, not speculative ranking.
