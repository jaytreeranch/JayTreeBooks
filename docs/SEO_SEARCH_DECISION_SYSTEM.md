# JayTree Books SEO Search Decision System

Updated: 2026-09-24

## Purpose

Use live Google Search Console and GA4 evidence to decide what to change, what to preserve, and what to monitor. The machine-readable snapshot is `data/seo-search-baseline.json`. Refresh decisions from live data rather than treating this baseline as permanent.

## Current baseline

Search Console, 2026-08-25 through 2026-09-21: **16 clicks, 80 impressions, 20.0% CTR, average position 5.48**. The prior 28-day comparison is not yet available in Windsor.

GA4, 2026-08-27 through 2026-09-23: **165 sessions, 87 users, 102 engaged sessions, 61.82% engagement rate**. Organic Search contributed **30 sessions (18.18%)**, **13 engaged sessions (43.33% engagement)**, and **17 tracked reader actions**.

Search Console privacy/anonymization means visible query rows may not add up to total clicks or impressions. Page-level and property-level totals should be treated as more complete at low traffic volume.

## Current page priorities

| Page / query | Evidence | Decision |
| --- | --- | --- |
| Homepage | 67 impressions, 14 clicks, 20.9% CTR, position 2.48 | Preserve as the authority hub. Do not churn title/meta without a clear decline. |
| The Correction | 3 impressions, 2 clicks, 66.7% CTR, position 2.67 | Use as a benchmark; protect the current mechanism/snippet. |
| Second Draft | 4 impressions, 0 clicks, position 8.0 | Page-one opportunity. Improve mechanism consistency, internal support, and snippet clarity before expanding content. |
| “the hollow bell” query | 4 impressions, position 7.25 | Exact-title opportunity. Preserve title identity and reinforce book/audio/chapter/video relationships. |
| The Hollow Bell page | 6 impressions, position 19.17 | Strengthen supporting entities/internal links; do not keyword-stuff. |
| The Hollow Year page | 5 impressions, position 17.6 | Strengthen supporting entities/internal links and unique erased-memory mechanism. |
| The Correction audio sample | 1 impression, position 3 | Keep audio pages indexable and expand AudioObject strategy to all five titles. |
| Social Poster utility page | 6 impressions, position 7 | `noindex,follow` applied 2026-09-24; monitor until it disappears. |
| Legacy `book.html` | GA4 recorded a landing session | Redirect installed; monitor until legacy landings reach zero. |

## Weekly decision rules

- **Positions 1–4 with healthy CTR:** protect winners. Avoid unnecessary title/meta rewrites.
- **Positions 1–10 with impressions but weak CTR:** improve snippet/search-intent alignment first.
- **Positions 5–20:** strengthen internal links, distinct-mechanism copy, genre hubs, and Book/Chapter/Audio/Video entity relationships.
- **Positions worse than 20:** improve relevance and architecture before optimizing CTR.
- **Utility/legacy URLs:** noindex or redirect as appropriate, then verify Search Console/GA4 decay.
- **Evidence window:** use the latest complete 28 days and compare with the previous 28 days when available. Do not overreact to tiny samples.

## Monday scorecard

The Monday JayTree Books agenda should pull current Windsor Search Console and GA4 data and report: Search Console clicks, impressions, CTR and average position; GA4 sessions, Organic Search sessions/share, organic engagement and tracked reader actions; top queries and landing pages; title/page movement; technical/indexing cleanup; and exactly which SEO action is justified by the evidence.
