# November 3, 2026 — Hollow Bell V6 private GitHub Release staging

Owner priority: publish approved The Hollow Bell — Beneath the Ice V6 FIRST, verify actual social post URL, only then produce daily book videos.

## Existing delivery service diagnosis
The website's _config.yml intentionally EXCLUDES media/social/video from GitHub Pages. Confirmed ranged GET to old JayTreeBooks.com MP4 paths HTTP 404; JPG image from the same site served 206. An existing public GitHub Release with 178707443-byte Hollow Bell official trailer served HTTP 206 and was verified as working. Reused this same distribution service, with no new host or editor.

## PRIVATE draft release staged and verified
- Repo: jaytreeranch/JayTreeBooks.
- Draft tag: hollow-bell-beneath-the-ice-v6-20261101.
- GitHub Release ID: 433067322. Draft=true, unauthenticated REST tag lookup 404; not publicly visible.
- Original owner-approved MP4 asset 2026-11-01_the-hollow-bell.mp4, 20,768,108 bytes, GitHub server digest SHA256 211b150ccb1e7487faa9e1dd9fdd4c31bafb61f6a6341bc23c27f531e9219897.
- Original approved cover The_Hollow_Bell_Beneath_the_Ice_V6_APPROVED_REEL_COVER_1080x1920.jpg, 638,324 bytes, server digest SHA256 7b959cb19ccaf2fb232ab082d9d7e95d11ae8ede0bf73503c36cdf808c6b3c1e.
- Assets remained in original JayTree LAN as source of truth; no large media committed into website Git history.
- GE78 existing Git Credential Manager credential was used transiently in memory for GitHub CLI, not printed, not logged and not stored. Draft creation/upload verified via authenticated GitHub Release API. Initial immediate read-back disagreed about the filename; confirmed original basename through API, no re-upload or overwrite.
- LAN private stage receipt: \JT-DESKTOP\JayTreeFarm\Promos\DailyBookCampaign_20261101\ReleaseAudits\NOV03_HOLLOW_BELL_V6_PRIVATE_GITHUB_RELEASE_STAGE_QC.json. SHA256 31d6410de79685f101722ee5fe52669e4bfdcefdea282f38f078b191ab32d622.

## Code and QC
On separate Social Poster feature/hollow-bell-v6-release-admission-20261102, source-only asset now references private draft but stays ready=false, status=awaiting_release, media_url blank, gate HOLD. Added private draft release QC and 12 tests PASS, whole Social Poster suite 104 PASS (one known nonfatal anyio warning); actual LAN stage gate receipt SHA FA6C3E64D3C50598AEB4AAB84EAC91ADA5A2D63C5EA85130DB61C7808190DCF8, publishing_allowed=false.

## Outstanding before making public
1. Independent source rights and signed Studio V6 release for music, bell recording, narrator reference/voice, visuals, cover/endcard. The owner's creative approval exists; it is NOT a substitute for independent commercial-rights evidence.
2. Verify correct authorized JayTree Books YouTube/other publisher account and private/unlisted duplicate status. Existing youtube.upload token was present; youtube.readonly query 403, so do NOT reset/reconnect the working upload token without need.
3. ONLY after clearance, publish draft release and verify public HTTP video/JPG URLs and bytes, configure approved exact V6 media URL and cover in Social Poster, perform protected dry-run and live single-platform upload with proof of provider ID, URL and durable ledger. No other book videos yet.

Rollback: preserve private draft until owner explicitly authorizes deletion, preserve LAN masters, main publishing infrastructure, existing creds and all other release assets. No website main code or deployed website modified by this staging step.
