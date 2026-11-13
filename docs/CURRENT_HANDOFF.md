## November 13, 2026 - Owner approved scored upcoming novels video, new thumbnail hosted for TikTok-first seven-platform posting
Video SHA a599f891dc2912b62ab036234631ec2e5428cdb3c19d42a3ee292f28413e3446, cover SHA 7b92379c8cf64ff3a59b56b6680aaf7a61927778535c9ef7fe2e4e76d3b56e11. Staging only; verify Pages HTTP 200 and exact SHA before live Social Poster delivery. TikTok FIRST; six other official destinations later; no post claimed. See docs/handoffs/2026-11-13-scored-upcoming-novels-native-social-delivery.md.

---
# JayTreeBooks ΓÇö Current verified release handoff (2026-11-12)

**Stage: PUBLISHED + VERIFIED ΓÇö The Hollow Bell novella website catalog.**
- Canonical production repository: `jaytreeranch/JayTreeBooks`, branch `main`.
- **Verified remote production source SHA:** `a33f120b81ab03d40a265bc5d614d7ff4bccbd1d`.
- GitHub Pages: workflow run **43315324589** on exact source `a33f120b81ab03d40a265bc5d614d7ff4bccbd1d` completed **SUCCESS**, including build, upload, deployment.
- Independent live verification (JT-DESKTOP through authorized Local Control): `https://jaytreebooks.com/` HTTP 200, **six server-rendered book cards** (five novels + one novella); corrected banner ΓÇ£Five novels on Kindle Unlimited. Plus a novella on Amazon.ΓÇ¥ visible; false all-titles KU claim absent; updated homepage meta description about five novels and novella visible.
- Novella permalink: `https://jaytreebooks.com/books/the-hollow-bell-novella.html` HTTP 200; standalone cover, SEO, structured data and separate Amazon buttons for Kindle ASIN `B0HD2H8586`, paperback `B0HD2KL44Q`, hardcover `B0HFT5VDRL`; no unverified novella KU promise. The full novel's existing page crosslinks; mystery hub crosslinks; no false sequel claim.
- Optimized novella cover `https://jaytreebooks.com/images/optimized/the-hollow-bell-novella.webp` HTTP 200 (180,854 bytes). Original novella image also HTTP 200. `https://jaytreebooks.com/sitemap.xml` HTTP 200 with **26 URLs**, including novella page.
- Audiobook: **COMING SOON / NOT SALE_READY**; no pay, direct download, or novella preview CTA. Mailing-list release updates enabled. User authorization covers website book promotion, not release of unapproved audio.
- QC: Node regression **9 PASS / 0 FAIL**, including six static/dynamic catalog links, Amazon ASINs, pending audiobook gates, no novella KU claim, sitemap and automation compatibility; `node --check app.js`, `node --check config.js` PASS on earlier source, Python `py_compile` across six site/SEO/QC generator scripts PASS. Build Reader Growth Site run **43315069298 SUCCESS**, SEO Content Cleanup **43315069382 SUCCESS**, PWA run **43315211519 SUCCESS**. Both durable scripts and compiled outputs validated, no failing site publication gate at final check.
- Verified LAN QC receipt: `F:\JayTreeFarmStorageV2\Projects\JayTreeBooks-Novella-QC-20261112\QC_RECEIPT_20261112.md`. LAN receipt first saved SHA-256 `44331F241673E7665AB7B762E787AF79308568DB987D853D2384BAA34A1675F5`; receipt amended with this final evidence after successful deploy, see current LAN hash.
- Source changes include website pages, `config.js`, `data/books.json`, `app.js`, `scripts/*`, `tests/hollow-bell-novella.test.cjs`, SEO sitemap, workflow compatibility, and handoff. Original novels, audio media, games and video productions preserved. No publication of audiobook was made.
- **Rollback:** Revert novella-specific source/docs and compatible workflow changes via a new non-force commit after preserving exact Amazon and cross-links; never rewrite unrelated production assets. GitHub history permits reverting source; separate public download media unaffected.
- **Next exact actions:** (1) When audiobook is independently approved `SALE_READY`, upload approved sample and direct checkout, switch novella status and validate purchase end-to-end. (2) Only advertise novella Kindle Unlimited if verified on Amazon. (3) Keep routine weekly website monitoring, with no immediate release blocker.
- This handoff documentation commit is created after the verified production source SHA above; a docs-only new SHA does **not** alter the published website assets. Verify its remote SHA separately before claiming continuity fully saved.

## Homepage KU messaging for five novels plus novella ΓÇö November 12, 2026

After reader-growth workflow 43314424712 passed, generating remote bot commit `ae94b17365b614697309cbffd3c4df1c84107b85` and a 26-page sitemap, independent tests of generated source exposed old site scripts overriding homepage metadata and maintaining misleading claim that every current title participates in Kindle Unlimited (the novella's enrollment is unverified). Corrected static homepage, persistent SEO/site builders, workflow assertions and regression. All five novels retain existing KU flags; novella directs readers to separate Amazon listing with no KU assertion. Kindle/print ASINs and audiobook sale gate unchanged. QC, workflow rerun and latest Pages publication pending for this checkpoint. Rollback via non-force selective revert. Next: Node regression, Python compile, Actions results, independent live site verification, and final SHA.

## Reader growth workflow validation correction ΓÇö November 12, 2026

Remote main at milestone start: `1b27f62a707e6e43a9cc6a4038eff76bc0505e05`. After six-title compatibility patch, reader-growth action run 43314086713 completed generator, audiobook, QC, SEO, and related steps successfully; its final validation failed because of a stale assertion requiring `books/${b.slug}.html#listen` in app.js despite the existing correct dynamic anchor `#audiobook`. This commit fixes the assertion and adds regression. Previous tests: 7/7 Node and Python compile PASS on JT-DESKTOP; workflow/Pages checks for the new source PENDING. No changes to public novella copy, artwork, sales gates, or Amazon links. Rollback: use new non-force revert commit. Next: verify workflow, live site and remote SHA; record final receipts.

## Novella six-title automation fix ΓÇö November 12, 2026

The source release `71bad26b377d8218d5409ffbcec3dc7d1330b18f` passed live production HTTP checks on JT-DESKTOP: the novella page, home (six cards), cover, crosslinks, sitemap, Amazon ASIN, and gated audiobook. Node regression 6/6 PASS; Python syntax PASS. Compatibility patch `786eb53a639c6907422fc11fc49058e5e562a64a` fixed the generator's missing novella chapter and audio SEO breadcrumb logic. Reader growth rerun 43313261774 then failed on old `add_audiobook_coming_soon.py`; the reader-growth generator itself completed for six books. Audio SEO successful run moved main to `6e23e6917c3d581d7d3b497c5445dd9daeccebba` and regenerated a 25-item sitemap without the novella.

This checkpoint adds explicit novella audiobook skip, guards chapters/audio in QC, preserves the editorial sitemap, updates SEO sitemap to 26 URLs, teaches reader-growth validation five novels PLUS novella, and prevents its Amazon rewrite from turning novella print formats or novel cross-promotions into the wrong ASIN. Kindle/print are Amazon-only; novella audiobook remains COMING SOON, direct sales blocked until SALE_READY. Tests/deployment on this final change remain pending. Rollback via new non-force revert commit of novella-scoped changes. Next: verify new main SHA; run Node/Python QC; ensure reader-growth/SEO workflows pass; verify live permalink, homepage, cover and sitemap.

## Novella compatibility remediation ΓÇö November 12, 2026

After production source commit `71bad26b377d8218d5409ffbcec3dc7d1330b18f` was pushed, independent QC on JT-DESKTOP PASSED: 5/5 Node regression tests, `node --check` on `app.js` and `config.js`; remote main verified. Initial live HTTP still showed old version while Pages run 43312717047 was IN_PROGRESS (the old version returned 404 for the new novella page). Two auxiliary workflows failed: reader-growth job 43312718338 due `KeyError: 'chapter'` for the novella, audio SEO job 43312718440 because it expected the retired `audio-card` markup on narrator preview pages.

This remediation makes reader-growth generator chapter/sitemap logic optional for a book with no chapter, preserves all hand-reviewed book pages and existing editorial sitemap, and updates audio SEO breadcrumb insertion for current narrator pages. No audiobook release or other asset modified. Added regression for these safeguards. QC and live Pages for this new follow-up commit PENDING, must re-run and verify before declaring website deployed. Rollback: revert only the novella release and this compatibility remediation through a new commit; do not force-push. Next: run tests and Python syntax, check the new Pages workflow and https://jaytreebooks.com/books/the-hollow-bell-novella.html, confirm its image and Amazon link, then document final verified SHA/deployment.

## Hollow Bell novella catalog release ΓÇö November 12, 2026

Owner approved adding the already-published novella to the JayTree Books website (replaces the earlier marketing exclusion for this title only). Added a distinct static homepage card, separate SEO/Book structured-data page, Kindle/paperback/hardcover Amazon CTAs based on known separate ASINs, dynamic catalog entry, audiobook coming-soon and mailing-list CTA, full-novel cross-links, mystery hub discovery, sitemap, and regression tests. Reused existing repo cover `images/the-hollow-bell-novella.png`; no new image/audio was generated.

**Sale gates:** novella ebook/print formats link to Amazon; audiobook remains COMING SOON, with no purchase/sample until certified SALE_READY. No novella KU promise because current enrollment was not rechecked. Full-length novel and existing audiobook samples remain separate.

Base: `0751729adb8327445850155da1cd83fbdfdd9224` on `main`. QC: source assertions before commit PASS; Node tests and live public Pages/HTTP checks PENDING until deployment. Publication authorized by owner for this website catalog change only. Rollback: revert only the novella catalog/page/cross-links/sitemap/test changes from this milestone using a new, non-force commit. Next: verify main remote SHA, run `node --test tests/hollow-bell-novella.test.cjs`, inspect GitHub Pages workflow and public permalink/cover/homepage, then update this handoff with evidence.

## Cinematic teaser hosting recovery ΓÇö November 9, 2026, 20:52 UTC

Owner reconfirmed website publication and asked whether to use social media instead. Recommendation: use both, with the website as the permanent promotion destination. No social posts submitted.

Verified remote video source: 266eeadbdaa9cf877edd653e4abb8e4da04c1cbe on main. Eight tracking behavior tests PASS; player/caption static validation PASS. The public landing page still lacks the player. Pages run 42691669838 attempts 1 and 2 failed after the hosting action's 10-minute timeout (syncing_files, then finished_file_sync). Fresh full build 42696581260 passed, but deployment immediately returned "Deployment cancelled" while reusing pages_build_version/ID 266eeadbdaa9cf877edd653e4abb8e4da04c1cbe.

This documentation checkpoint creates a fresh revision for the existing approved website; no artwork, video, tracking or published-book content changed. Next: inspect this revision's Pages run, then verify https://jaytreebooks.com/upcoming-books.html#cinematic-teaser in browser including playback. Publication remains PENDING until verified. Do not repeatedly submit the canceled old revision. If fresh revision also fails, preserve evidence and escalate the hosting failure; do not migrate hosting or change DNS without a reviewed plan.

Approved video: https://github.com/jaytreeranch/JayTreeBooks/releases/download/upcoming-novels-teaser-20261109/JayTree_Upcoming_Novels_Cinematic_Teaser_v1.mp4 ΓÇö 27.2s, 19,665,280 bytes; SHA256 870c7f7de906473a874082ec908b60b5a900972d4031564db81dbbe0c1f4d184. No new generation or purchase. GA4 reporting/actual ingestion remains unverified. Preserve Video Studio production HOLD and other chats' repairs. Social handoff remains for seven connected platforms including both Facebook names, JayTreeBooks and JayTreeBook.

Rollback: no content rollback is required for this documentation-only checkpoint. Video rollback, if requested, must remove only the cinematic-teaser section and video-specific instrumentation in a new commit, preserving the live three-novel promotion.

## Approved cinematic teaser publication ΓÇö November 9, 2026

Owner approved the finished teaser for the website. Public approved asset is https://github.com/jaytreeranch/JayTreeBooks/releases/download/upcoming-novels-teaser-20261109/JayTree_Upcoming_Novels_Cinematic_Teaser_v1.mp4. HTTP 200, 19,665,280 bytes, SHA256 870c7f7de906473a874082ec908b60b5a900972d4031564db81dbbe0c1f4d184 verified; byte-identical to approved export, 27.2 seconds. No new generation, re-encoding or subscription.

Added native controls/playsinline video on upcoming-books.html, preload=none and existing approved poster; same-origin English VTT captions plus fallback direct link. Updated script/style versions to avoid stale caches. Added video-start, watched 25/50/75% and completion events. Progress uses actually played time ranges rather than seek position; completion requires ended with at least 90% watched. Eight tests PASS (existing six plus two video behavior tests). Website deployment/player playback PENDING at this checkpoint. GA4 server ingestion remains unverified due reporting access limitations.

Owner also requested a handoff prompt for the existing seven-platform social poster, including both JayTreeBooks and JayTreeBook on Facebook. No social posts were submitted in this chat. Verify exact account IDs; if JayTreeBook is unavailable, provide the manual posting package without blocking other connected accounts. Keep Video Studio repairs and global production settings untouched. Rollback: remove only cinematic-teaser section and video-specific events using a new commit; preserve three-novel promo and existing published books.

## Final verification ΓÇö November 9, 2026, 20:06 UTC

Public promotion COMPLETE: https://jaytreebooks.com/upcoming-books.html. Latest website source commit 4b020d9cf460ed7c996ee11e831f88db462ee572 verified on main. GitHub Pages run 42687869864 SUCCESS; final desktop styling and 390px phone layout verified in browser, no horizontal overflow. Homepage mobile menu's Upcoming Novels link reaches the correct landing page. Three novel illustrations and all five current covers load; The Correction first-chapter link verified by navigation. Six event behavior tests and static validation PASS. Actual GA4 ingestion/live visitor counts remain unverified because reporting access is subscription-blocked; see analytics guide. No claim of new signups or sales.

Cinematic teaser PRIVATE REVIEW export completed locally: 27.200 seconds, 1920x1080 H.264/AAC, 30fps, SHA256 870c7f7de906473a874082ec908b60b5a900972d4031564db81dbbe0c1f4d184. Narration and three story scenes generated after owner approved script/voice choice; one reading-room background generation failed. Owner then required further generation to be free. NO replacement call was submitted; closing was authored locally with the five published covers. Final decode PASS; visual and caption/timing review PASS; voice still needs owner listening review. Video is in the owner's private Cinematic Teaser workspace and is NOT published. Video Studio inspected only: live connection reports can_start=false/publish_allowed=false; ongoing repairs untouched.

Next action: owner reviews finished teaser and decides whether to publish it. Do not add it to the website or social media without that approval. Source artifacts, subtitle sidecar, edit ledger and original files preserved privately. No further website code change is pending for the promo launch.

## November 9 upcoming promotion ΓÇö LIVE

The approved three-novel promotion is live at https://jaytreebooks.com/upcoming-books.html and linked from the homepage. Source commit 422612d61f89604fd12e81a2ec5436c93aef79d7 and automated follow-up 8a1077ae5f383168f33ead940ced7257c49f2f11 verified remotely; Pages run 42685480695 succeeded. All eight artwork/cover images load; first-chapter navigation works; mobile has no overflow. Six tracking tests PASS. Actual GA4 server receipt/reporting is not verified because reporting access is subscription-blocked and browser runtime/network inspection is unavailable. See handoffs/2026-11-09-upcoming-promo.md and UPCOMING_PROMO_ANALYTICS.md. This checkpoint includes a small headline/anchor polish; verify after deploy. The cinematic teaser is awaiting script approval; no video generation or posting performed.

## November 9 upcoming-novels promotion
Owner approved the three concept images, preview and website publication. Implemented upcoming-books.html, homepage/nav teaser, six optimized images, spoiler-free hooks, five published first-chapter links and GA4 promo instrumentation. Six behavioral tests PASS; 38 landing references and five sample links PASS; JavaScript syntax and sitemap PASS. Base remote main verified at 112b93b3f0eac88c7e68178914e16f907bb1cd57. Publishing and live visual/analytics receipt PENDING at this checkpoint. See docs/UPCOMING_PROMO_ANALYTICS.md. Rollback: restore only index.html and sitemap.xml from base, remove upcoming page/nav integration with a new commit; never force-push. No paid video generated or social post sent. Next: publish atomic source/assets update, verify Pages and live browser, then record receipt.

## November 8 V6 public delivery
See handoffs/2026-11-08-v6-public-delivery.md. Exact approved master copy hash PASS; public HTTP/hash check pending Pages deployment.

# JayTreeBooks ΓÇö CURRENT HANDOFF

**Status at 2026-10-31: DOCUMENTATION BOOTSTRAP ONLY ΓÇö PROJECT STATE NOT AUDITED.**

## Where to resume
- Repository: `jaytreeranch/JayTreeBooks`
- Default branch at bootstrap: `main`
- Instructions: `AGENTS.md`
- Standing policy: [JayTree Development Continuity](https://github.com/jaytreeranch/JayTreeLLC/blob/main/docs/JAYTREE_DEVELOPMENT_CONTINUITY_POLICY.md); the authenticated private operational policy is in `jaytreeranch/JayTree-Video-Studio/docs/JAYTREE_DEVELOPMENT_CONTINUITY_POLICY.md`.
- Last verified implementation branch/remote SHA: **NOT YET RECONCILED**
- Live app/deployment/queue: **NOT INSPECTED**
- Tests/QA: **NOT RUN as part of this documentation bootstrap**
- Production/publishing: **NOT MODIFIED by bootstrap**
- Parallel work/owner approvals: **CHECK BEFORE WORK**
- Backup/rollback: **CHECK EXISTING REPO AND LIVE HOST BEFORE CHANGING**

## Next exact actions
1. Read `AGENTS.md`, repository README and existing project-specific status documents. Discover recent commits/PRs and active development branches. Check live project through the existing authorized connection.
2. Record the actual stage, branch, verified remote SHA, source location, tests, deployment, blockers, rollback, next task in this file, then commit/push and verify again.
3. Append every coherent stage under `docs/handoffs/`. Never present the bootstrap as verified app status.

## Mandatory per-stage handoff fields
UTC timestamp; task/stage; affected source/tests/docs; verified remote commit SHA and branch; actual tests PASS/FAIL/BLOCKED; artifact hashes and safe storage; deployment/prod state; pending decisions; security gates; rollback; exact next action. Update this file and push it with every stage.

Verified November8 from GE78: direct HTTPS HTTP200, zero redirects, 20,768,108 bytes, SHA256 211b150ccb1e7487faa9e1dd9fdd4c31bafb61f6a6341bc23c27f531e9219897. Published delivery source commit3fc4298e6fa1f3b61f834fa028256c2e842495da matches GitHub main. This verifies hosting, not a TikTok post.

## Nov 13, 2026 — Instagram-only compatible delivery after first Reel container failed
The scored V6 reel was successfully posted to TikTok FIRST, Facebook Page, YouTube, X, Bluesky and Threads; Instagram media container 17912531781590536 failed with Meta processing error 2207077 BEFORE publishing. Original approved and already-hosted vertical file remains byte-identical. Created one delivery-only variant by stream-copying all 653 H264 source video frames bit-for-bit while encoding existing scored stereo AAC to Instagram-appropriate 128 kbps. The owner-approved soundtrack, visuals, captions and ending are otherwise preserved. Exact derivative delivery: media/delivery/upcoming-novels-native-scored-20261113-instagram-aac128.mp4, SHA256 22f433fcd795d4f27ceb585f2a6cf7b22a4bac1036be76656ccB4AA40FD4EC4B (26,601,198 bytes); source V6 master SHA a599f891dc2912b62ab036234631ec2e5428cdb3c19d42a3ee292f28413e3446. Verify new Pages 200/no redirect and full remote SHA BEFORE a targeted Instagram-only retry. Do not repost the already-successful six destinations.