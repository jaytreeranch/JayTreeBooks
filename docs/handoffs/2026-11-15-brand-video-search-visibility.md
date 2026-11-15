# JayTree Books — Brand identity, video search and visibility handoff

Date: November 15, 2026 (America/Chicago)
Host: JT-DESKTOP via verified JayTree Local Control tunnel.
Base source: origin/main 241345a4346e2e0bb659302f23e7052ff015dcd8.
Working branch: seo/brand-video-search-20261115.
Publication status: STAGED / NOT DEPLOYED. No Payhip, customer sale, audio master or production media changes.
Repository: https://github.com/jaytreeranch/JayTreeBooks

## Verified findings

Production redesign already includes Organization with eight sameAs profile/identity links. No duplicate Organization object should be added. The published trailer schema on animated-series.html contained a YouTube watch-page link in contentUrl; corrected in this branch.

Existing OpenSEO project and manual US mobile depth-50 rank tracker have only two genre keywords and no completed ranking check. OpenSEO GSC is not connected, while GSC Wizard refused API reads due expired subscription. No current ranking position or improvement can be certified.

## Changes

- index.html and home-v2.html: clarify alternateName while preserving all existing social identity links.
- animated-series.html: remove invalid YouTube watch-page contentUrl; retain real embedUrl, add creator and canonical video attribution.
- upcoming-novels-teaser.html: dedicated approved-video watch page with VideoObject, actual previously released MP4 URL, video-specific metadata, stable approved thumb, captions, host-scoped GTM/GA4, existing upcoming.js playback progression telemetry.
- upcoming-books.html: link to the watch page without moving or altering the approved on-page video.
- sitemap.xml and scripts/seo_content_cleanup.py: keep watch route indexed through regeneration.
- scripts/apply_entity_seo.py and scripts/seo_content_cleanup.py: preserve brand alias when publisher entity is processed.
- scripts/apply_brand_video_seo_patch.py: reproducible, idempotent patch for regenerated content.
- scripts/report_search_visibility.py and tests/test_brand_video_search.py: local first-party Search Console CSV grouping and seven source/analytics regression cases.
- tests/tracking_page_coverage.test.js: expand GA4 route-coverage assertion from 35 to 36.
- docs/SEARCH_VISIBILITY_RUNBOOK.md: data access, limitations, baseline and no-credit reporting route.

## Quality gates

New Python SEO/tracker regressions: 7 PASS, 0 FAIL.
Existing Node website tests: 78 PASS, 0 FAIL.
Python AST syntax: 4 PASS.
Sitemap route count: 36; includes dedicated watch page with known analytics ID.
Real production publication, live HTTP checks for the new route, Google recrawl, Search Console ingestion, Google ranking baseline: PENDING / NOT VERIFIED.

## Rollback

The isolated branch can be discarded without affecting current production. For a separately approved future merge, revert only this branch's SEO-specific changes using a new non-force commit, refresh sitemap and verify website routes and GA4. Do not touch customer checkout, social posts, Pages settings or media masters. Never force-push.

## Next three actions

1. Verify complete site generator and regression QC, commit and push this safe development branch, and verify GitHub remote branch SHA.
2. Obtain production publication approval for the SEO change; then run the existing GitHub Pages release process and independently test the new route and schema.
3. Connect first-party Google Search Console for real brand-vs-genre baseline, or use the documented owner-exported CSV. Check OpenSEO credit estimate before any optional rank check.

Verified source/checkpoint commit: 4ea5a376e5cd6d2a2ef22b0a478f4c106b8129d4. GitHub refs/heads/seo/brand-video-search-20261115 returned the identical full SHA through git ls-remote. Source commit pushed successfully and worktree clean. This subsequent documentation addendum receives its own commit; record its final SHA in the independent LAN receipt.
