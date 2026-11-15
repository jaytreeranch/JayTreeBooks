# JayTree Books brand and genre search visibility

This monitoring workstream separates branded discovery from genre discovery. Never present manually checked Google results, Search Console average positions or a paid SERP tracker position as interchangeable.

## Current verified access (November 15, 2026)

- The existing OpenSEO project is JayTree Books, domain jaytreebooks.com.
- The existing OpenSEO manual US English mobile rank tracker has depth 50 and two target keywords: psychological mystery books and new mystery book.
- That tracker has not completed a check. It has no ranking baseline yet; no credits were spent in this workstream.
- OpenSEO first-party Google Search Console is NOT CONNECTED. Its connection screen is https://app.openseo.so/p/4b21e1ca-15a3-414b-8904-b21c3d53451d/search-performance
- The separate GSC Wizard connection refused data access because its trial/subscription ended. Do not claim live first-party Google rank metrics until a working Google Search Console connection is verified.

## Two reporting views

1. Brand: JayTree Books; JayTreeBooks; JayTreeBooks.com, including longer searches with the brand phrase.
2. Genre: psychological mystery books; psychological mystery book; psychological mystery thriller; new mystery book; new mystery books; mystery thriller books. Other unbranded queries remain a separate group.
3. For individual target phrases, record impressions, clicks, click-through rate and Search Console average position, with change from an equivalent previous period.

## Free first-party data route (no OpenSEO credits)

Open the official Google Search Console property for jaytreebooks.com with an owner-authorized account. Use Performance > Search results > Search type: Web > Date. Use the same country, device and date-window length for each comparison. Export Queries as CSV. The exporter accepts either Query or Top queries and Clicks, Impressions, CTR, Position column names.

Run on an authorized local PC using the existing script, replacing the example paths with genuine owner-exported CSVs:

python scripts/report_search_visibility.py C:/Private/current-queries.csv --previous C:/Private/prior-queries.csv --period 2026-11-01..2026-11-14 --out F:/JayTreeFarmStorageV2/CampaignAnalytics/SearchVisibility/visibility_2026-11-14.json

Store exported CSV and JSON privately on JayTree LAN, not in GitHub. The script never calls an external API and does not schedule checks. An absent phrase is UNOBSERVED, not position zero. Search Console metrics describe impressions and average placement, not an invariant Google results page. The first valid export establishes the baseline; do not fabricate earlier positions.

## Rank tracker (optional separate comparison)

Existing OpenSEO tracker: https://app.openseo.so/p/4b21e1ca-15a3-414b-8904-b21c3d53451d/rank-tracking/7bb8eaaa-b368-4c6f-afd4-ae3188615131

Its two original genre keywords are preserved. Any first SERP check or new keywords could use credits; estimate costs and get explicit owner approval before running it. Keep US mobile and search depth 50 consistent. A not-found result only means no listing in the checked results; it is not proof of ranking 51+.

## After publication

Inspect https://jaytreebooks.com/ and the new watch page with Google Search Console URL Inspection. Review video indexing, the video rich results report, VideoObject validity, the site sitemap and social brand queries. Google decides the displayed result, and snippets for unrelated Instagram reels cannot be forcibly controlled from this site.

## Goals

Brand: official website and official social destinations should be the clearly identifiable results for JayTree Books.

Genre: improve sustained visibility for psychological mystery books and new mystery book; aim for top 50 first, then top 10. Do not claim progress until identical tracked markets and data windows can be compared.
