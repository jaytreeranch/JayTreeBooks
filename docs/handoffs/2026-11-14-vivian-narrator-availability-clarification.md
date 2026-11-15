# Vivian audiobook availability versus alternative narrator editions — 2026-11-14

## Owner direction

The owner explicitly clarified: **all six complete audiobook editions are available NOW with Vivian narration**, while **alternative full-length narrators are coming soon**. Existing other-voice chapter samples may be heard today; none is offered as a second complete edition. Do not describe published audiobooks, any of the six products, or the full Hollow Bell novella audiobook as 'coming soon'. Preserve the immersive edition as a separate in-development experience.

## Exact website changes

- `index.html`: audiobook heading now says Vivian is available; body text and the six-product $1.99 callout distinguish future narrators.
- `app.js`: all dynamic audiobook cards/callouts make Vivian immediate and alternatives future; a previously unreleased generic `Full Audiobook — Coming Soon` fallback is removed; the alternate-free novella detail no longer falsely says 'Audiobook Coming Soon', and its missing sample URL is no longer rendered as a broken link.
- `mystery-books.html`: corrected Hollow Bell novella audiobook 'coming soon' text to Vivian available now at $1.99, other narrators coming soon.
- `books/{second-draft,the-hollow-year,the-hollow-bell,the-hollow-bell-novella,the-absconding,the-correction}.html`: added the same distinction next to the $1.99 Payhip CTA. Novel-page reader follow-up copy now points to alternate-narrator release alerts, rather than generic audiobook release news.
- `audio/book-{1..5}-sample.html`: every narrator comparison page states complete Vivian availability, the three non-Vivian narrator cards carry specific 'Alternative full-length narration coming soon' badges while keeping playable Chapter One previews, and the footer preserves a direct Vivian $1.99 purchase button. The distinct Immersive project is identified 'In Development' rather than as the whole audiobook coming soon.
- `tests/audiobook_purchase_links.test.js`, `tests/audiobook_sample_sales_flow.test.js`, `tests/vivian_available_alt_narrators_coming_soon.test.js`: updated plus dedicated regression coverage against generic full-audiobook 'coming soon' language, six distinct product links, five audio pages with 3 alternate cards each, novella dynamic fallback and misleading release-news language. Existing narrator, tracking and Payhip tests retained.

## QC and preserved commerce

**PASS — 38 of 38 Node regression tests**, zero failures. `node --check app.js`, `node --check pwa.js`, `node --check audio/audiobook-experience.js` passed. JT-DESKTOP hostname verified using authorized JayTree Local Control. Static/JS review source obtained from remote GitHub branch and executed from established LAN QC workspace, under `F:\JayTreeFarmStorageV2\Projects\JayTreeBooksWebsiteAudit_20261114\source-qc`.

The six certified Vivian Payhip URLs remain unchanged and correctly edition-specific. No product state, charge, payout, buyer data, coupons, or original audio master files were changed. No claim is made about a new nonzero Payhip settlement. A local headless Chrome screenshot was captured, but the richer follow-up CDP browser interaction timed out; therefore do not call full browser/visual certification complete.

**Pre-publish state:** This content correction was added to the existing website QC review branch `fix/website-novella-qc-20261114`, draft PR #29. At this document revision production is still the pre-merge site. Only describe the wording as publicly live after a successful main merge, GitHub Pages deploy and actual production HTTP content inspection.

## Release gate, rollback and next executable action

1. Verify head is current with main, review the PR's file changes, and rerun the 38 regressions on the exact final source SHA.
2. When production rollout is authorized, merge with a locked expected head SHA, verify exact main SHA and successful GitHub Pages workflow. Audit homepage, the mystery-book hub, six book detail pages, five sample pages, deployed `app.js` and original six Payhip URLs. Confirm only alternate narrator full editions are coming soon, and the released Vivian audiobooks are not advertised as pending.
3. Update live receipt and `docs/CURRENT_HANDOFF.md`, with actual outcome and GitHub remote SHA. In a buyer-facing regression, revert the site merge without hiding verified six Payhip listings or touching the hidden legacy $5 Correction listing. The project must not claim a real-money transaction was tested.

**Private/LAN evidence:** `\\JT-DESKTOP\JayTreeFarm\Projects\JayTreeBooksWebsiteAudit_20261114\` and the earlier commercial SALE_READY receipts under LAN `Staging\SixAudiobooksLaunchControl20261113`.

## Final public release certification — 2026-11-14, after automatic workflows

**PASS: Vivian audiobook availability and alternative narrator messaging are LIVE.**
- Main production source after PR #29, PR #30 and automatic SEO normalization: `c8e3bc5865924b67377ad309f55003922c49ddff`.
- GitHub Pages build/deployment run **43673295167** completed **SUCCESS**, including build, report-build-status and deploy steps, on the source SHA above.
- JT-DESKTOP owner-controlled live HTTPS acceptance: **16/16 PASS**, HTTP 200 and exact current language, checking homepage, mystery-book hub, app.js, pwa.js, pwa.css, six static book pages and five narrator comparison pages.
- All six distinct $1.99 Vivian Payhip purchase URLs remain present and unmodified; five narrator pages each carry three alternative narrator coming-soon badges with their playable previews. The full audiobook is explicitly available now; no generic 'audiobook coming soon' promotion remains on those routes.
- Live `pwa.js` places Install App in footer/end-of-body (not floating over purchase buttons); `pwa.css` gives it static positioning. Live narrator sample pages have no duplicate `data-track` event-binding loop.
- Directly downloaded actual post-automation remote main source and ran **40/40 Node tests PASS** and JS syntax PASS; authoritative PWA and audio SEO generators now preserve these behaviors on future successful runs.
- Verified LAN receipt: `F:\JayTreeFarmStorageV2\Projects\JayTreeBooksWebsiteAudit_20261114\VIVIAN_FINAL_PUBLIC_POST_GENERATOR_QC_20261114.json`, SHA-256 `FF0D5209BC20DC0C80156311D5C1566F4B5B21957C23A3BC5E1E27069BB4559F`.
- **Unrelated open maintenance:** Legacy Build Reader Growth Site workflow still fails because its validator/generator expects pre-launch generic audiobook Coming Soon text. Do not reverse the release copy to satisfy it. GA4/Google Search Console reporting access restrictions, a real-money checkout/payout, full WCAG test remain separate open checks.

**Rollback:** Revert a faulty website repair commit while retaining six correctly visible Payhip products and their certified masters. Do not touch the unrelated older Hidden $5 Correction listing.
