# Post-deployment generator repair — Vivian narrator wording release (November 14, 2026 CST)

## Why this follow-up was necessary

- Website/narrator release from PR #29 was squash-merged on GitHub main at `0fcb08146aa2b62d179a5aea041ff276a8418038`.
- Automatic post-merge workflows advanced main to `971b9ae38f86dcca23baa725b38db58c338e92a9`. GitHub Pages deployment **run 43672594033 SUCCESS** at that main SHA. Public owner-controlled HTTP checks **14/14 PASS** after earlier CDN cache expiry: homepage, mystery-books page, deployed app.js, six static book pages, and five narrator sample pages. Verified receipt `VIVIAN_NARRATOR_PUBLIC_LIVE_QC_20261114.json` SHA-256 `28DA2F08CC856BC407315B70ACD428889882FFC4D86A96FDCDF5D23463853851`, on the JayTree LAN.
- The **Build Reader Growth Site** workflow at merge SHA `0fcb081...` failed due **stale pre-launch "Coming Soon" assertions**. Its failure did not prevent the succeeding GitHub Pages deployment; it remains an **OPEN CI MAINTENANCE** issue. Do NOT let it restore obsolete full-audiobook coming-soon copy.
- A successful **SEO Content Cleanup** automation commit `1685bf4d904df6b86450061636d332a221284062` silently reinserted redundant `data-track` click handlers into five narrator pages, risking doubled `audiobook_payhip` intent events.
- A successful **Apply JayTree PWA** automation commit `971b9ae38f86dcca23baa725b38db58c338e92a9` restored the floating Install App button after our code-level fix, again obscuring mobile purchase content.
- Rechecking the **actual deployed main** at that state revealed **5 failing regression tests**, correctly identifying regenerated click-handler duplication. PWA overlay was independently observed from source. This is not an audiobook delivery or seller listing failure.

## Permanent generator and file fixes

On branch `fix/pwa-generator-overlay-20261114`:

1. `scripts/apply_pwa.py`: authoritative PWA_JS template now attaches install control to footer/end of body; PWA_CSS uses static rather than fixed position. Generated `pwa.js` and `pwa.css` contain matching code, so future successful PWA runs will preserve the non-obstructive behavior.
2. `scripts/apply_audio_seo.py`: authoritative audio SEO tracking block now leaves outbound `data-track` clicks to existing `audio/audiobook-experience.js`. It retains audio playback instrumentation but does not register a second click listener.
3. `audio/book-{1..5}-sample.html`: removed redundant `data-track` event bindings reinserted by the automation. Existing six-book $1.99 Vivian links, alternate narrator coming-soon badges and preview audio sources remain unchanged.
4. `tests/audiobook_sample_sales_flow.test.js`: added generation-drift test that validates `PWA_JS` and `PWA_CSS` raw templates match shipped `pwa.js` and `pwa.css`, plus an audio SEO generator invariant against any `data-track` rebinding.

**QA:** Source downloaded from remote repair branch onto JT-DESKTOP authorized LAN; **40/40 tests PASS**. `node --check pwa.js` PASS. Source QA workspace: `F:\JayTreeFarmStorageV2\Projects\JayTreeBooksWebsiteAudit_20261114\source-qc-pwa-generator`. Build/paid checkout not repeated; no Payhip product, price, visibility or source-master change.

## Next production action

Review PR, confirm branch is current with main, rerun 40 tests, squash merge with expected head SHA, allow GitHub automation to run, then independently verify no reinsertion of redundant listeners, footer-based PWA control in public `pwa.js`/`pwa.css`, continued **14/14** narrator copy HTTP checks and a successful GitHub Pages deployment. If automation reintroduces a bug, identify and update the authoritative generator **before** another rollout; do not repeatedly patch generated files alone. Record final production SHA and receipt.

**Rollback:** Revert only the website-specific repair if necessary; preserve original six Payhip Vivian listing statuses and older unrelated hidden $5 Correction SKU. Existing audio delivery and ACX rights receipts remain private on LAN. Nonzero card charge, processor settlement, full WCAG and GA4/GSC reporting remain unverified (separate scopes).

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
