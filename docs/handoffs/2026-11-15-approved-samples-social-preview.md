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