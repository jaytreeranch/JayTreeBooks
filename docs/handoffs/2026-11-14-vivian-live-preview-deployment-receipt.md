# Vivian audiobook samples — final public deployment QC, November 14, 2026 CST

## Verified LIVE
GitHub PR 31: https://github.com/jaytreeranch/JayTreeBooks/pull/31
Squash merge: a16cc39415670b5140389c268e08ce9cb5517831
Post-automation deployed source: dba6bd8e45f17818e99d2bc8e4198136c2eccf09
GitHub Pages run 43674595906: SUCCESS
All six public Vivian audiobook sample MP3s: HTTP 200, SHA-256 byte-identical to certified sale-preview files. Six public sample pages: HTTP 200 with the correct edition-specific Payhip $1.99 links. Newly added Hollow Bell novella sample route is live.
Postautomation regression: 57/57 Node PASS, 4/4 Python sample tests PASS, JS syntax PASS. Previous site UX, tracking, PWA and SEO generator improvements preserved. Full masters, Payhip products, pricing, visibility, buyer records and alternate narrator demos were not changed.

## Evidence
Independent LAN receipt:
F:\JayTreeFarmStorageV2\QCReceipts\AudiobookSampleAudit_20261114\VIVIAN_LIVE_PUBLIC_HASH_AND_PAGE_QC_20261114.json
Receipt SHA-256: 8939B8541BB3F78D7A60A43C6D3975B4C9D6993C95B061E39BC3BEB044AE105A
Earlier October excerpt scripts matched final manuscripts in all six editions (five 100% six-gram overlap, The Absconding 99.6%). Old public Vivian MP3 audio differed from certified final previews; website now serves the exact certified audio.

## Scope, known issues and rollback
All website source and live deployment work on this workstream has stopped to avoid interference with the owner's planned visual redesign. Only this documentation checkpoint is pending on a separate docs branch. NO MORE LIVE WEBPAGE CHANGES in this workstream.
Inherited Build/Validate Reader Growth CI still has outdated five-book and audiobook-coming-soon assumptions; this is separate maintenance and did not prevent successful Pages deployment. Nonzero paid Payhip transaction/payout not tested.
For a preview-specific issue, revert only PR 31, keep the previous visual/UX fixes and six visible $1.99 Payhip listings, and recheck Pages and MP3 URLs.

## Next workstream
The mystery-themed social artwork Option A was approved, but its exact original file has not been verified present on the JayTree LAN. Do not invent an attachment or claim the promo has posted. Social promotion is independent of the owner's website redesign. Next social action after exact creative transfer: publish via existing poster, log live platform URLs and campaign attribution.
