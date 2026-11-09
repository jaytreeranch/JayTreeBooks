# Upcoming novel campaign — analytics guide

Published campaign ID: upcoming_novels_202611. GA4 measurement ID: G-PHE2JVV5P6. Shareable landing URL: https://jaytreebooks.com/upcoming-books.html

## Measure visits
In Google Analytics Reports > Engagement > Pages and screens, filter Page path to /upcoming-books.html. Views are page views, not unique people. Active users measures tracked visitors, subject to browser/privacy limits. Use landing-page reports for entry sessions and acquisition reports for referrers. Do not sum homepage exposure events and landing visits as people.

## Events
- upcoming_promo_view: one per page load on the landing page, or first 35%-visible homepage campaign section. placement separates landing/homepage.
- upcoming_book_view: first 35%-visible individual upcoming card per page load. book identifies the title.
- upcoming_promo_click: homepage link to upcoming page.
- upcoming_notify_click: click toward newsletter page; NOT a confirmed subscription.
- upcoming_collection_click: click toward current collection.
- upcoming_chapter_click: one of the five available first chapters selected. Existing chapter and derived reader_start events remain available.
- upcoming_existing_book_click: click toward one of the five published book pages.

All custom events carry promo_id, placement and promo_path. Relevant events also carry book/link_url. Existing tracking.js preserves inbound UTM attribution. Register custom event-scoped dimensions promo_id, placement and book in GA4 Admin if not already available; collection does not require that registration, but custom breakdowns do. Basic page visits and event-name counts work without them. No new analytics vendor or personal fields introduced.

## Share links
Use https://jaytreebooks.com/upcoming-books.html?utm_source=youtube&utm_medium=video&utm_campaign=upcoming_novels_202611&utm_content=cinematic_teaser for a future authorized YouTube promotion. Change source/medium/content to match the actual channel. Do not apply internal UTMs to site navigation.

## Verification limits
Six local behavioral tests PASS; HTML/assets/link destinations and configured GA4 ID checked. Live browser collection/request confirmation and deployed-page checks must be recorded in release receipts. GSC Wizard reporting connector refused reads because no active subscription; this is separate from the site's Google Analytics tag. No visitor total or confirmed GA4 server-side receipt is claimed from a local test. A test visit tagged promo_test=1 sends debug_mode and promo_test=true; exclude it when interpreting launch counts.


## Approved native teaser

upcoming_video_start counts one first play per page load. upcoming_video_progress reports once each for 25, 50 and 75 percent of unique played-time ranges. upcoming_video_complete requires playback ended and at least 90 percent actually viewed; seeking alone does not qualify. upcoming_video_error reports the browser media error code. Parameters include video_id, video_title, video_duration and video_percent where applicable. These are viewing metrics, not purchases or subscriptions. Eight behavioral tests PASS. Live Analytics receipt remains unverified.
