# November 14, 2026 — Vivian website sample parity

## Production baseline verified
All six Vivian-narrated audiobook editions are presently Visible at USD $1.99 in Payhip. November 14, 20:48 CST live seller recheck, six SALE_READY receipts, 24 buyer MP3/M4B copies SHA-matched, six live public website CTAs HTTP 200. Nonzero card charge/payout not tested. ACX written clearance archived privately.

## Finding
The October 3 sample excerpt text matches the locked October 22 final manuscripts at 100% six-gram sequence overlap for 5/6 editions, and 99.6% for The Absconding. The old public Vivian MP3 file first-60s content differs acoustically from the certified Payhip sale preview recordings for all five website sample pages (best normalized crosscorrelation 0.048-0.061). Transcript/voice equivalence of the historical MP3 was NOT verified. Full Hollow Bell final book begins with a prologue; historical excerpt was Chapter One.

## Staged website remediation, NO production deploy
- Replaced five existing public Vivian sample binaries with identical copies of the five approved final Payhip preview MP3s.
- Added sixth certified novella Vivian preview binary and /audio/book-6-sample.html with $1.99 correct SKU.
- Fixed five pages' preview descriptions: sold Vivian excerpt is exact preview, alternate archived voices are not purchasable full editions.
- Updated app.js and config.js six-card routing, preserved seller links, added cache bust query for Vivian players.
- Added fail-safe to scripts/build_audiobook_pages.py to prevent legacy generator from clobbering sale-ready pages.
- scripts/refresh_vivian_sale_previews.py validates all source SHA-256 manifest values before copying. Local release manifest/master files stay LAN-only.
- tests/test_vivian_release_previews.py tests six hashes, audio paths, $1.99 links, alternate voice copy and novella.

## QC and next steps
6/6 certified preview SHA-256 PASS. 4/4 new Python tests PASS, 5/5 existing Node purchase URL tests PASS, node --check app.js PASS, Python compilation PASS, git diff --check PASS. Local clone source base was GitHub main 971b9ae38f86dcca23baa725b38db58c338e92a9. Branch fix/vivian-final-samples-20261114. Feature branch remains **UNMERGED and NOT LIVE**; exact remote commit SHA to be verified separately.

1. Finish branch push, verify remote SHA, and open draft PR; review mobile and desktop preview players in PR.
2. Coordinate merge with other website QC work; check GitHub Pages deployed SHA, live 200 + media and all six Payhip URLs after merging.
3. Launch previously approved mystery graphic Option A with UTM and publish platform URL receipts. No social post made by this audiobook site QC.

Rollback: revert only this isolated preview/file/link patch; never change Payhip product visibility and preserve private full audio masters. Source and audio comparison receipts remain at \\JT-DESKTOP\JayTreeFarm\QCReceipts\AudiobookSampleAudit_20261114.
