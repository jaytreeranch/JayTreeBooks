# JayTreeBooks website and public media staging — stage log

## November 3, 2026 — Private Hollow Bell V6 GitHub Release

Authorized user has approved The Hollow Bell — Beneath the Ice V6 creative master and cover and requires first real social post before further books. The existing website deliberately excludes media/social/video from public GitHub Pages via _config.yml, so older MP4 links from the Pages domain return 404. Existing public GitHub Release MP4 returned HTTP 206 and was selected as the already-tested distribution mechanism.

Using existing GE78 Git Credential Manager authorization transiently in memory, created a **PRIVATE DRAFT** GitHub Release in this repository: release ID 433067322, tag hollow-bell-beneath-the-ice-v6-20261101. Server-reported digests match original owner-approved MP4 SHA256 211b150ccb1e7487faa9e1dd9fdd4c31bafb61f6a6341bc23c27f531e9219897, size 20,768,108 bytes and portrait JPEG SHA256 7b959cb19ccaf2fb232ab082d9d7e95d11ae8ede0bf73503c36cdf808c6b3c1e, size 638,324 bytes. Anonymous release-tag API 404 confirms draft is not public. Authoritative local media on LAN is unchanged; no large source file was committed to git. Independent LAN stage receipt SHA 31d6410de79685f101722ee5fe52669e4bfdcefdea282f38f078b191ab32d622.

Social Poster independent feature branch has a disabled staged-asset pointer to this private draft and private-stage gate with 12 tests PASS, full 104-test source suite PASS. Live Social Poster production main is untouched. No public video release, social posting, changes to YouTube token or other book production.

Next: commercial rights and signed release for exact V6 soundtrack/voice/bell/visual/cover sources, correct official book-channel/remote duplicate proof, turn private release public only when permitted, verify public bytes and URLs, and use existing Social Poster publisher for one verified first post. Full documentation docs/handoffs/2026-11-03-hollow-bell-v6-private-release-staging.md. Rollback: keep draft private and preserve original LAN assets; discard only feature documentation with owner permission. Follow AGENTS.md continuity and verify remote branch commit SHA after final push.
