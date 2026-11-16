# JayTree Books - targeted genre-hub internal links release (2026-11-16)

## Purpose and authority
Owner approved targeted SEO internal linking, full QC, then publication without disturbing the existing cinematic storefront. Primary SERP goals remain psychological mystery books and new mystery book. Isolated source branch feat/genre-internal-links-20261116 is cut from remotely verified production main SHA 9a2eccd508f901c2d2384cc01562d6149e45bdbe. No paid SEO service is used.

## Implementation - limited scope
- books.html: compact editorial discovery section before the catalog, natural entry links to both existing genre pages, reading-guides cross-link.
- audiobooks.html: short discovery section after existing audiobook shopping collection, links to both genre hubs. Purchase offers remain in their approved position.
- guides/psychological-mystery-stories.html: in-body contextual link to the indexed psychological mystery hub.
- guides/supernatural-suspense.html: in-body contextual link to new-mystery books hub.
- storefront-v2.css: scoped cinematic night/gold styling and responsive one-column mobile layout.
- tests/test_genre_discovery_links.py: guards route destinations, existing catalog/metadata identity and mobile CSS.
- Five novel book pages already contain appropriate genre context links and footers; left intact. No new genre page or duplicate heading. No changes to purchase links, Payhip, GA4, approved art, social previews, chapters, story claims, easter eggs or legal pages.

## Verified pre-release QC
- Full Python: 50/50 PASS; Node: 61/61 PASS.
- python scripts/build_storefront_catalog.py --check: PASS, all six books and six audiobooks generated in sync.
- Actual isolated headless Chromium localhost: 16/16 page/viewport checks PASS across Books, Audiobooks and two reading guides at 320/390/768/1440 px; no horizontal overflow, links visible, phone discovery cards stacked; isolated screenshots and test output in D:\Projects\JayTreeSeoLinks_20261116_QC.
- New genre links resolve to existing HTML destinations, with no changes to book checkout destination URLs.
- Google Indexing API is NOT authorized for ordinary book pages; GSC OAuth is read-only. Human Google Search Console URL Inspection -> Request indexing is still needed for /mystery-books.html, /books.html, /audiobooks.html after live deployment. Requesting indexing is not a guarantee and has not been executed or claimed here.

## Release, next steps and rollback
Development and local QC PASS; publication pending separately verified GitHub PR merge, GitHub Pages Actions, and live-page QC. Owner authorized publish after QC. Recheck main SHA before merge and avoid other concurrent publisher conflicts. The original full website redesign and book conversion flows must remain intact.
Source branch: feat/genre-internal-links-20261116.
Rollback: revert the isolated link-section commit/PR if production regression; no private data or credentials in this branch.
Next: commit/push feature, independently verify remote SHA, open/merge PR only on green source gates, inspect production Pages deployment, verify public HTML/links, and update private LAN stage log + final source handoff.