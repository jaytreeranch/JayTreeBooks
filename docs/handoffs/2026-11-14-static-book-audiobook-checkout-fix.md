# Six audiobook static book-page checkout correction — November 14, 2026

## Why this follow-up exists

The first six-title website launch was merged to GitHub main at `e3576b343279b16b5966cc68241c03bd1b94ab18`. After GitHub Pages refreshed, both `https://jaytreebooks.com/` and `https://www.jaytreebooks.com/`, plus the deployed `app.js`, independently returned HTTP 200 with **exactly the six correct Payhip URLs**. The host was confirmed GitHub Pages (`Server: GitHub.com`, varnish CDN), and the prior 600-second cache explained the delay. A separate concurrent SEO change moved main to `0d447613a8c59dbbdcae549976a67c923c85f727`; this source branch was based on that newer main rather than overwriting it.

A further live audit found that the **six static `books/*.html` pages** did not use `app.js` to render the audiobook purchase CTAs; those pages still displayed “Audiobook — Coming Soon,” even though all six releases were commercially certified and their Payhip listings were Visible. This follow-up resolves that production inconsistency.

## Exact changes

These existing standalone detail pages now offer the limited-time **$1.99** audiobook with its correct Payhip link, MP3 and chaptered M4B format description, and disclosure that the narrator is a digitally generated JayTree Books voice:

| Static detail page | Direct-sale URL |
| --- | --- |
| `books/the-absconding.html` | https://payhip.com/b/q3GfL |
| `books/the-hollow-year.html` | https://payhip.com/b/Zf7tv |
| `books/second-draft.html` | https://payhip.com/b/GejHn |
| `books/the-correction.html` | https://payhip.com/b/OPaGw |
| `books/the-hollow-bell.html` | https://payhip.com/b/0BeoF |
| `books/the-hollow-bell-novella.html` | https://payhip.com/b/EWc5q |

Each CTA uses safe external link attributes (`target="_blank" rel="noopener noreferrer"`), and the existing `data-track="audiobook_payhip"` analytics marker. The promo has **no expiry date** in copy. The older unrelated $5 Correction Payhip product was untouched.

New `tests/audiobook_static_book_pages.test.js` protects all six static book pages, verifies their unique sale link and absence of stale “coming soon” audiobook copy, plus format/price/narrator text.

## Verification and gates

- Source branch: `fix/audiobook-six-static-book-pages-20261114`; all code/docs changes committed and pushed through the authenticated GitHub connector.
- Independently fetched an immutable source commit to JT-DESKTOP LAN storage at `F:\JayTreeFarmStorageV2\Staging\SixAudiobooksLaunchControl20261113\STATIC_BOOK_RELEASE_QC_20261114`.
- `node --check app.js`: **PASS**.
- `node --test tests/audiobook_purchase_links.test.js tests/audiobook_static_book_pages.test.js`: **12 PASS / 0 FAIL**.
- Original six Payhip products had real $0 owner-controlled purchases with receipt and repeated customer MP3/M4B SHA matches, then seller-verified Visible at $1.99. Private aggregate receipt: `SIX_VIVIAN_PAYHIP_LIVE_VISIBLE_GATE_20261114_V1.json`, SHA `D4F034C5EA07FA6521D3A823AF206250DB2B359BDBBF255CFC95027F7FAD6735`. All large assets and buyer details stay on LAN.
- The live homepage is already serving all six purchase links. **This document is authored before deploying the six static detail-page fixes**; verify those separately after merge. A real nonzero card charge/payout was not tested.

## Remaining publication / acceptance

1. Review the PR based on the latest main; ensure 0 commits behind and no unrelated files. Re-run tests on its actual final head.
2. Merge to main, verify the exact new main remote SHA and GitHub Pages production refresh. Check all **six independent `https://jaytreebooks.com/books/<slug>.html`** pages return HTTP 200 and contain exactly their respective Payhip URL and no stale audiobook coming-soon text.
3. Write production HTTP/QC receipt and update LAN stage log/current handoff. Do not claim the static detail pages are live until those HTTP checks pass.

Rollback: revert the static page correction merge if any public page breaks and verify production reversion; do not remove the original first six-title homepage launch. For any Payhip buyer issue, make the affected product Invisible and investigate while preserving original masters, QC copies and receipts.
