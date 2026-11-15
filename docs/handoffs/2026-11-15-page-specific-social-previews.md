# JayTree social-share preview release — November 15, 2026

Feature branch: fix/page-specific-social-previews-20261115
Production main starting SHA: 26a195f9427b35fddbeb344acc80c3802965eb55
User explicitly authorized production publication.

## Changes

Generated 24 unique 1200x630 optimized JPEG social cards from official JayTree existing imagery. Assigned to 25 page heads: Homepage and Home v2 (one shared home image), Books, Audiobooks, Samples, Series, News, Experiences, About, Upcoming, Reader Guides, Case Files, Animated Series, six genre discovery pages and six individual books.

The Audiobooks share image now represents the true page: cinematic lake and manor, actual bronze/black headphones, Second Draft official book cover and $1.99 offer, replacing the unrelated generic Mystery Challenge image.

Every card has absolute HTTPS og:image, og:image:secure_url, og:image:type, og:image:width and height, descriptive alt text, and matching X/Twitter card, title, description and image. Original OG titles/descriptions, canonicals, six Payhip product links, samples, newsletter, GA4 and hidden pages are retained.

Metadata is generated with scripts/apply_social_previews.py and used by scripts/build_sitewide_preview.py. The SEO cleanup automation reapplies and verifies page-specific social previews after its existing content writers. The manual offline image composer is scripts/build_social_art.py (Pillow needed only on desktop).

## QA

- 73 of 73 existing Node tests PASS.
- 31 of 31 Python tests PASS, including six social-image suite checks.
- 25 of 25 preview page tags in sync; image files are proper JPEG 1200x630, distinct where required.
- 34 site pages in sync; six-book catalog generator in sync.
- SEO maintenance run twice, with postwriter social metadata regeneration and final --check PASS.
- Original purchase URLs and samples unchanged; no payment was made or buyer fulfillment simulated.
- LAN evidence: F:\JayTreeFarmStorageV2\Projects\JayTreeBooksWebsiteRedesign_20261114\SOCIAL_SHARE_PREVIEWS_QC_20261115.json

## Final release gates and rollback

Commit and push feature source with verified remote SHA; obtain PR QC; merge approved fix; verify Pages success and bot HTTP/HTTPS OG metadata for all pages plus 200 image/jpeg for each; verify exact public https://jaytreebooks.com/audiobooks.html and 1200x630 response. Do not claim a Facebook cache refresh without a provider receipt.

The old /#audiobooks hash link still navigates visitors to the audiobook store, but a fragment cannot have its own social image. Use the direct page URL for the correct preview.

Rollback: revert the website-only release commit and restore previous social metadata/assets. Do not touch Payhip products, books or audio masters.

Status before live deployment: SOURCE READY; PUBLICATION PENDING.
