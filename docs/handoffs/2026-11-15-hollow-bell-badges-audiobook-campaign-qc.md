# JayTree Books — Books badges and old audiobook social URL QC
Date: 2026-11-15 (America/Chicago).
Base production main SHA: 8ba86a7034fa4578458a86f305f17b6201efa474.
Working branch: fix/hollow-bell-badges-audiobook-social-link-20261115.

## Completed
1. Matching Full Novel / Novella gold badges now overlay the two Hollow Bell covers in the Books shop and homepage six-book shelf. Changes are generated from existing edition metadata, not hand-edited temporary cards. Other books remain unchanged.
2. The legacy social URL https://JayTreeBooks.com/#audiobooks is explicitly routed by home-links.js to https://jaytreebooks.com/audiobooks.html, preserving Facebook/Instagram UTM query parameters and the other classic homepage hash bookmarks. Existing homepage section remains a non-JS fallback.
3. Found and fixed a preexisting narrow-phone overflow on Privacy and Terms pages using responsive CSS. No legal copy was altered.
4. Rebuilt books.html and home-v2.html using their actual generators. Preserved six published Vivian $1.99 products, the distinct Hollow Bell full novel/novella Payhip SKUs and all narrator samples.

## Quality control
- Chrome source-browser QC: 96/96 PASS at 320px, 390px, 768px, 1440px. Includes all key pages, gold badges, original redirect entry points, UTM preservation, same-page hashchange, unaffected #books and #challenge anchors, six selectable audiobook titles at desktop and phone widths, no horizontal overflow or missing visible local images.
- Existing Node tests: 56/56 PASS.
- Python catalog tests: 8/8 PASS; Python sitewide tests: 8/8 PASS; new focused book badge/social URL tests: 5/5 PASS.
- Both catalog/page generators report in-sync; 34 existing site pages were preserved.
- Verified screenshots: book_badges_1440_review.png and book_badges_390_review.png on authorized JayTree LAN.
- Browser receipt: book_badges_social_url_qc_20261115.json on authorized JayTree LAN.
- Commercial checkout was verified only as exact correct outgoing URLs, NOT as a completed paid order/settlement; actual GA4 reports and deep WCAG screen-reader audit remain separate gates.

## Deployment and rollback
This update is limited to the requested small visual and campaign-link fixes and incidental narrow-phone overflow correction. No source cover art, audiobook MP3 files, Payhip visibility, subscriber data, social posts, or application secrets were changed.
Before merge: recheck remote main SHA and source tests. After merge: verify GitHub Pages successful deployment and browser-check the exact public #audiobooks link, the Books badges and all 6 product/sample paths.
Rollback: revert only this hotfix merge commit and regenerate affected HTML pages. Preserve production masters and independent audio sales.
## Verified publication — same-day post-release supplement

PR #34 merged successfully into production main: squash source commit 6151370d371fa2a68b86aaf4d89eee6901180fa2. GitHub workflows for homepage normalization, canonical URLs and PWA completed successfully. Published GitHub Pages action: https://github.com/jaytreeranch/JayTreeBooks/actions/runs/43722057934 (success). Source was observed after normalization at main commit 26a195f9427b35fddbeb344acc80c3802965eb55; the public domain serves the new code.

Verified live site:
- Chrome public checks at 320, 390 and 1440: 69/69 PASS, including the exact old #audiobooks campaign link, UTM retention, narrow-phone page widths, correct highlighted cover edition badges and all six distinct Payhip/sample selections.
- 37/37 public routes HTTP 200, including the six book detail pages, narrator samples, first chapters and core static/SEO files.
- Full Novel and Novella labels visible on both Books and homepage covers, and the deployed home-links.js explicitly sends #audiobooks to /audiobooks.html.
- Google Analytics configuration, canonical sitemap routes and both hidden paths remain present in source, but receiving GA4 event records, actual subscriber creation and payment/settlement require separate authorized human/first-party testing. Automated product URLs were inspected, not charged.
- Live browsers did not click out to Amazon or Payhip and analytics calls were blocked during automated browser QC to avoid polluting marketing reports.
LAN post-release receipts: public_book_badges_social_url_qc_20261115.json, public_sitewide_content_qc_20261115.json, and public_book_badges_1440_review.png / public_book_badges_390_review.png.
Rollback: revert only merge 6151370d371fa2a68b86aaf4d89eee6901180fa2 or its specific files, then validate the public links, without touching audiobook masters or Payhip products.