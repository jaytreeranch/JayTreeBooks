# Downloadable cinematic storefront review

The verified website source is 3d70b454f818fd717295e2b900cdef6c2939f35c on design/multipage-storefront-review-20261114, draft PR #32. The GitHub remote returned the same SHA after push. This stage is for owner review. Production deployment requires separate approval.

## What to open

Extract JayTree_Books_Website_Preview.zip, then open index.html. On the farm, the extracted entry point is `\\JT-DESKTOP\JayTreeFarm\Projects\JayTreeBooksWebsiteRedesign_20261114\PortableReview_20261115\preview\index.html`. The ZIP, Windows Chrome screenshots, browser-qc.json and the executable QC script are in its parent folder.

The same ZIP was built in two environments and checked by SHA-256. Both returned dda8329c6379ad0ebed974f8d1052c287dc2618107fdc7d9eda05eee413b27b6 for 225796230 bytes. There are 162 entries, including 50 HTML files. All local HTML resource and link paths resolved. The archive includes the 21 playable audio excerpts. Checkout, hosted video and the Kit form use their existing internet destinations.

## Changes

The audiobook hero and selector use the approved lake, headphones, and separate tile and hero artwork for each edition from the approved preview. Official published covers remain on the Books, Samples and individual product pages. New releases can omit the optional audio_cover and audio_hero fields. The selected audiobook controls use catalog-derived product and sample paths, including separate Hollow Bell novel and novella entries.

Home now features the Second Draft rehearsal premise, a direct audiobook offer and a short published collection. The storefronts and editorial pages use the photographic setting. The Windows export makes root paths relative, routes historical homepage fragments, embeds the catalog for local search and strips external GA4 script tags. The release source preserves the existing production homepage and purchase-intent instrumentation.

## QC

- Generator checks passed for the storefront catalog and 34 sitewide pages. All 73 Node and 20 Python regressions passed.
- Headless Chrome on JT-DESKTOP loaded the extracted site using file URLs. All 92 responsive checks passed across 23 pages at 1440, 768, 390 and 320 CSS pixels. All 24 keyboard edition selections, six pointer selections, four search checks, three compact-menu checks and 21 audio playback checks passed.
- Screenshots were reviewed against the approved reference. Tablet CTA clipping, the overlapping sale badge, phone headphone spacing, stray literal newline text and narrow product-page heading overflow were corrected. Tablet and phone layouts use the purchase button for price.
- All six checkout URLs match the approved catalog. Direct HTTP checks returned 403 and fresh Chrome visits reached Payhip's Cloudflare challenge on all six. A successful live checkout, real payment, analytics ingestion, and subscriber delivery were not verified by this run.
- No public staging or live deployment. Hosted third-party video, formal screen-reader and field performance certification remain for release QA.

## Reproduce and continue

1. Run python scripts/build_download_preview.py PATH_TO_OUTPUT.zip. Extract the complete archive. On Windows the optional browser QC runner accepts the extracted directory and an output directory. It uses installed Chrome, requests and websocket-client.
2. Review the homepage and Audiobooks shelf, then the two Hollow Bell purchase and sample journeys. Compare the intended checkout in an ordinary buyer session and check the Kit flow before launch.
3. Reconcile current main, campaign anchor mappings, automated generators, canonical URLs, SEO and production analytics before seeking explicit approval for a merge. Rollback the preview by reverting its review-branch changes or rebuilding from c42ddaa61c9c1fc2fd40e8ba3825069953f75328. The previous live site does not require a rollback for this milestone.
