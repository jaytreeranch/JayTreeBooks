# Owner-approved Samples social preview — November 15, 2026

Status: requested change implemented locally, owner-authorized publication subject to deployment QC.

## Source and exact artwork preservation

The owner uploaded JayTree Books_ Mystery in Every Page.png, located at C:\Users\aguil\Downloads\JayTree Books_ Mystery in Every Page.png on JT-GE78. The input is a 1731x909 PNG, SHA-256 12FBD91162852B868BC77F5A6B445998AA9E6A237CBB251BDEA9A83C68B371C0. Its byte-for-byte backup was verified at \\JT-DESKTOP\JayTreeFarm\Projects\JayTreeBooksWebsiteRedesign_20261114\ApprovedSocialArt\JayTree_Books_Samples_OwnerApproved_Original.png.

The versioned social asset images/social/previews/samples-approved-20261115.jpg was resized directly from this original without regeneration or changes to words/artwork. Optimized JPEG 1200x630, 228311 bytes, SHA-256 B62959DFC89E7BE34FF4D89AA87FD78E92F5CC832310D877FC9828062367874B.

## Technical changes

scripts/apply_social_previews.py maps Samples to the new versioned file with accurate alt wording. samples.html carries the correct og:image and twitter:image URL and keeps the existing title, canonical URL, six sample links, six audio offers, analytics, book details and other website metadata. Existing samples.jpg remains unused and unmodified. The manual generic image generator does not know or overwrite the unique approved filename, so future runs cannot erase this owner's approved image. Other page previews remain unchanged.

The unique image URL helps social networks fetch new image bytes when they next scrape Samples; Facebook can separately cache the page HTML. Do not claim Facebook cache invalidation without a provider receipt.

## QC and rollback

Source copied from JT-GE78 to JayTree LAN and SHA-256 verified. 1200x630 optimized JPEG source/output checks PASS.
Python complete test suite: 36/36 PASS. JavaScript suite: exit 0. Sitewide source generation: 34/34 sync. Social metadata updater: 25/25 sync. Catalog generator: 6/6 book records sync.
Source branch: fix/approved-samples-social-art-20261115; merge, Pages deployment and public crawler response still require separate verification.
Rollback: revert the Samples-specific release commit, preserving the JPEG and source PNG in LAN; prior Samples social metadata and all website purchase/audio functions can be restored without touching Payhip or official book/audio assets.

## Verified production release receipt

- Owner-provided Samples preview merged into production main via PR #36, source squash commit c65739c981ecbcf51f449fbac6927410a87dc5bb.
- GitHub Validate Reader Growth Site action 43729499687 COMPLETED SUCCESS, and GitHub Pages action 43729663535 COMPLETED SUCCESS for this release.
- LIVE https://jaytreebooks.com/samples.html returned HTTP 200 with Open Graph and Twitter image https://jaytreebooks.com/images/social/previews/samples-approved-20261115.jpg.
- The public JPG returned HTTP 200, image/jpeg. Its SHA-256 is b62959dfc89e7be34ff4d89aa87fd78e92f5cc832310d877fc9828062367874b, exactly matching the approved committed image, dimensions 1200x630.
- All six sample cards remain in the published Samples HTML. The other main section social previews were not changed in this targeted release.
- LAN public receipt: F:\JayTreeFarmStorageV2\Projects\JayTreeBooksWebsiteRedesign_20261114\PUBLIC_SAMPLES_APPROVED_SOCIAL_QC_20261115.json.
- META PROVIDER CACHE NOT VERIFIED. Facebook may require re-scraping the exact Samples URL. Do not claim cache purge or a real transaction.
- Rollback: revert source release c65739c981ecbcf51f449fbac6927410a87dc5bb (or restore the old samples.jpg mapping) without touching book covers, Payhip, audiobooks, source PNG or other page-specific previews.
