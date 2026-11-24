## 2026-11-24 - Historical checkout receipts 6/6, shop DNS preflight verified

Merchant/Payhip/GoDaddy admin access and current checkout verification pending. No new charges or DNS changes. See docs/handoffs/2026-11-24-shopping-checkout-dns-evidence.md.

---
## 2026-11-24 - Six offline Shopping previews, QC 5/5 PASS

Private LAN previews only; checkout verification and Merchant Center access still blocked. No live changes. See docs/handoffs/2026-11-24-shopping-offline-preview.md.

---
## 2026-11-24 - Free Shopping candidate audit (not submitted)

Six candidate audiobooks documented; checkout and Merchant Center authentication pending. No production changes or paid services. See docs/handoffs/2026-11-24-free-shopping-readiness.md.

---
## November 15, 2026 â€” Cinematic storefront published and verified

PR #32 merged as c1f5f0489ca324af094e856bdae5d66587e0bc22 after the release candidate 100b0bfac8e48881c032f6c3e66d1deebdaeb76a passed all 93 source regressions, the campaign checks and the actual Pages build. GitHub Pages deployed production main 603c5499154196da19bf06abd64e1dee585a8e90 ([deployment](https://github.com/jaytreeranch/JayTreeBooks/actions/runs/43711452197)). The custom domain passed 162 Windows Chrome checks across 320, 390, 768 and 1440 pixels before and again after publication. Eight public routes returned 200 with the expected content.

The original /#audiobooks sale link and standalone /audiobooks.html shop work. All six title selections resolve to their distinct Payhip and sample destinations. All 21 excerpts played. The series heading, complete Samples cover artwork, News animated-series/reader-guide art and both hidden paths passed live checks. Automated Payhip product requests returned 403; no charge or settlement was verified. The final PWA validator follows the homepage include and checked all 47 source pages locally.

LAN evidence: JayTreeBooksWebsiteRedesign_20261114/PortableReview_20261115/EditorialUpdate/public-release-qc under the JayTreeFarm Projects share. browser-qc.json SHA-256 4cfcef224932e9699f779e04a04d084527d63d902743a49b8f8a3ecd03fe6796. Roll back the redesign by reverting merge c1f5f048 with mainline parent 1, then regenerate the sitemap and verify the custom domain. No further website publication step is pending. A human checkout would verify Payhip's separate purchase flow.

## November 15, 2026 â€” Authorized storefront release candidate

Reconciled production 0218ac82985d649c33600503252c5eaf1933d014 and editorial fix c113f58427752da6f6e31886d78d16118d180c56. All 161 Windows browser checks passed for the editorial build. The existing /#audiobooks entry opens the sale section, with the full shop at /audiobooks.html. The Pages build maps the previous homepage to /classic.html. Gate publication on the rendered Pages build and source regressions. After merge verify the custom domain, links and both hidden gestures. Rollback by reverting the PR merge on main.

## November 14, 2026 (Central) â€” Downloadable cinematic storefront

Verified source 3d70b454f818fd717295e2b900cdef6c2939f35c on draft PR #32. The complete ZIP opens directly on Windows, with the owner-approved photographic audiobook showcase, six distinct product selections and 21 locally playable excerpts. All 93 source regressions and 150 Windows browser checks passed. Payhip challenged automated access. Checkout settlement and production launch remain open. [Evidence, archive hash, rollback and next steps](handoffs/2026-11-15-downloadable-cinematic-storefront.md).

## 2026-11-14 audiobook social sale image/video DELIVERY-ONLY

Approved Option A creative staged as three static media assets on isolated branch release/audiobook199-social-delivery-only-20261114; website HTML/CSS/JS and audiobook checkout pages UNCHANGED. Direct public URLs must be verified after merge. Details: docs/handoffs/2026-11-14-audiobook199-public-media-only.md. Social publication is performed independently through existing Social Poster and must have seven provider receipts before claiming success.

---

## November 14, 2026 ? Website integration of certified Vivian previews

Reconciled approved preview audio with the previously completed website QC release on main f01b7940. Changed five Vivian MP3 website samples to certified full-edition excerpts; created sixth Hollow Bell novella audio player; corrected on-page narrator labeling and preserved six $1.99 Payhip URLs. Additional Python sample QC 4/4 PASS, **57/57 Node suite PASS**, JS/Python compilation PASS, six release SHA hashes PASS. Staging on `fix/vivian-final-samples-merged-20261114`; live deployment pending. Original current main and Payhip seller listings unchanged. See [handoff](handoffs/2026-11-14-vivian-final-website-preview-parity.md).

## November 13, 2026 - Owner approved scored upcoming novels video, new thumbnail hosted for TikTok-first seven-platform posting
Video SHA a599f891dc2912b62ab036234631ec2e5428cdb3c19d42a3ee292f28413e3446, cover SHA 7b92379c8cf64ff3a59b56b6680aaf7a61927778535c9ef7fe2e4e76d3b56e11. Staging only; verify Pages HTTP 200 and exact SHA before live Social Poster delivery. TikTok FIRST; six other official destinations later; no post claimed. See docs/handoffs/2026-11-13-scored-upcoming-novels-native-social-delivery.md.

---
## 2026-11-12 Î“Ã‡Ã¶ Hollow Bell novella catalog released and independently certified

**Production source remote `a33f120b81ab03d40a265bc5d614d7ff4bccbd1d`**, Pages run **43315324589 SUCCESS**. Public homepage HTTP 200; six crawlable book cards; correct novels/KU versus novella/Amazon banner and meta; old all-titles KU claim absent. New novella permalink HTTP 200 with distinct Kindle/paperback/hardcover ASINs, cross-linked full novel and mystery hub; optimized cover HTTP 200; sitemap HTTP 200 with 26 URLs. Audiobook is explicitly **Coming Soon**, no checkout or sample. Node regression 9/9 PASS, Python six scripts compile PASS, Reader Growth run 43315069298 PASS, SEO run 43315069382 PASS, PWA run 43315211519 PASS. Verified LAN QC receipt at `F:\JayTreeFarmStorageV2\Projects\JayTreeBooks-Novella-QC-20261112\QC_RECEIPT_20261112.md`. Rollback: selective non-force revert via GitHub main; no private assets published. Next: await audiobook SALE_READY and then implement real sample/direct checkout; confirm KU before any novella KU claim. Docs-only handoff commit will have a newer SHA than source release.

## 2026-11-12 Î“Ã‡Ã¶ Fix inherited KU banner after novella catalog release
Reader Growth workflow 43314424712 PASSED; bot asset commit ae94b17365b614697309cbffd3c4df1c84107b85. Corrected misleading all-titles KU wording and retained 5 novels + novella meta via durable SEO scripts. Added workflow assertions and regression; production follow-up pending.

## 2026-11-12 Î“Ã‡Ã¶ Correct stale audiobook anchor assertion
Build Reader Growth action 43314086713 failed final validation on `#listen` (actual `#audiobook`); patched workflow and appended regression; verify rerun and published site. Base 1b27f62a707e6e43a9cc6a4038eff76bc0505e05.

## 2026-11-12 Î“Ã‡Ã¶ Novella six-title automation preservation
Live listing and image verified HTTP 200; source Node tests 6/6 and Python compile PASS. Fixed audiobook generator, QC optional chapter/audio, SEO 26-item sitemap, workflow validators and distinct Amazon ASIN preservation. Base 6e23e6917c3d581d7d3b497c5445dd9daeccebba; workflow and new SHA verification pending.

## 2026-11-12 Î“Ã‡Ã¶ Novella generator compatibility
Post-push tests PASS 5/5; remote source commit 71bad26b377d8218d5409ffbcec3dc7d1330b18f verified. Auxiliary reader-growth and audio-SEO workflows exposed legacy assumptions; patched generator to skip unpublished novella samples and preserve editorial pages/sitemap, and patched audio SEO breadcrumbs. Pages hosting still pending at diagnostic time. Re-verify follow-up commit and all workflows.

## 2026-11-12 Î“Ã‡Ã¶ Hollow Bell novella website listing
Owner-approved update: six distinct homepage cards (five novels + novella), new novella SEO/purchase page, dynamic catalog, gated audiobook coming-soon, novel cross-link, sitemap and tests. Base main 0751729adb8327445850155da1cd83fbdfdd9224. Remote push, test execution and Pages verification pending at source preparation. Rollback by additive revert commit; preserve original novels and media.

# November8 approved V6 public delivery

Verified November8 from GE78: direct HTTPS HTTP200, zero redirects, 20,768,108 bytes, SHA256 211b150ccb1e7487faa9e1dd9fdd4c31bafb61f6a6341bc23c27f531e9219897. Published delivery source commit3fc4298e6fa1f3b61f834fa028256c2e842495da matches GitHub main. This verifies hosting, not a TikTok post.

## Nov 13, 2026 â€” Instagram-only compatible delivery after first Reel container failed
The scored V6 reel was successfully posted to TikTok FIRST, Facebook Page, YouTube, X, Bluesky and Threads; Instagram media container 17912531781590536 failed with Meta processing error 2207077 BEFORE publishing. Original approved and already-hosted vertical file remains byte-identical. Created one delivery-only variant by stream-copying all 653 H264 source video frames bit-for-bit while encoding existing scored stereo AAC to Instagram-appropriate 128 kbps. The owner-approved soundtrack, visuals, captions and ending are otherwise preserved. Exact derivative delivery: media/delivery/upcoming-novels-native-scored-20261113-instagram-aac128.mp4, SHA256 22f433fcd795d4f27ceb585f2a6cf7b22a4bac1036be76656ccB4AA40FD4EC4B (26,601,198 bytes); source V6 master SHA a599f891dc2912b62ab036234631ec2e5428cdb3c19d42a3ee292f28413e3446. Verify new Pages 200/no redirect and full remote SHA BEFORE a targeted Instagram-only retry. Do not repost the already-successful six destinations.
