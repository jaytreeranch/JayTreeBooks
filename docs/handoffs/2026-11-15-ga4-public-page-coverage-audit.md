# JayTree Books — GA4 page and funnel audit (2026-11-15)

## Scope and baseline
Authorized website review and tracking coverage QC on the live https://jaytreebooks.com/ site. Production GA4 property 549202437; measurement ID G-PHE2JVV5P6.

- Live-read sitemap: 35/35 routes HTTP 200 with one expected GA4 measurement ID and gtag config present.
- Seven pages had the base GA4 page tag but lacked /tracking.js: six audiobook preview pages and case-files.html.
- Privacy and Terms were publicly accessible HTTP 200 but had no GA4 measurement ID. Social Poster, TikTok OAuth callback, and X preview test intentionally carry NO GA4.
- GA4 reporting/ingestion cannot be independently read: GSC Wizard says subscription_required and Windsor.ai says free-plan connector limit exceeded (five connected accounts vs one included). This is an account-access issue, NOT evidence of an offline website. Never report GA4 collection as verified.
- Historic main handoff documents earlier live automated browser QC and 6 paid-order/fulfillment receipts; no new Payhip checkout occurred in this audit.

## Changes (feature branch, not automatically live)
- Added production-host-scoped GA4 initialization to privacy.html and terms.html; both include existing /tracking.js helper.
- Included /tracking.js on case-files.html, and all six audio sample pages, preserving existing static GA4 and outbound purchase links.
- Added one-play and one-complete events to Hollow Bell novella preview. The other five already have first-play and completion events.
- Changed unverified case-files-thanks.html event from misleading case_files_signup_complete to case_files_signup_receipt_view. This event is NOT a confirmed newsletter sign_up; Kit confirmation should be the only source of a verified signup.
- Updated retired audiobook page generator to include /tracking.js if ever deliberately re-enabled (it still early-exits on certified Vivian release pages).
- Added tests/tracking_page_coverage.test.js to check 35 sitemap pages, legal pages, six previews, meaningful signup distinction, private-page exclusions, and generator resilience.

## Checks and artifacts
- Source exported from exact GitHub branch SHA 5fa87040f16b451abe1455e0b48465d664ec995f (verified git fetch) as 45-file text-only archive on the JayTree LAN.
- New Node tracking coverage suite: 5/5 PASS, exit code 0. First run failed due to QA export lacking sitemap.xml, fixed the QC archive input and re-ran to PASS; no production defect was inferred.
- LAN QC folder: F:\\JayTreeFarmStorageV2\\Projects\\JayTreeBooksWebsiteRedesign_20261114\\GA4_QC_20261115.
- Checks confirm source configuration/events, not GA4 backend reception, real Payhip settlement, Kit subscriber API outcome, or social attribution numbers.

## Release gate, rollback, next actions
Production stays unchanged until deployment authorization/independent release QC is satisfied.
1. Run existing site/browser and generator-regression checks on current GitHub feature source, with extra attention to six Payhip links, UI, sample events and landing redirect.
2. Review PR and merge to main only if safe against concurrent website edits, then verify GitHub Pages successful deployment and live routes. Recheck analytics tag, privacy/terms, novella audio first-play events, and no false signup event.
3. To fully certify analytics recording, restore *one* read path to GA4 (GSC Wizard subscription or Windsor.ai account allowance), then inspect page_path and event_name for page_view, audiobook_payhip, audio_sample_play, audio_sample_complete, campaign_landing and generate_lead. Never fabricate numbers or count a Payhip outbound click as purchase. Tag Assistant/DebugView or consent-aware browser network verification may supplement.
4. Rollback is a revert of this analytics-only PR; preserve the website and production media.

Status: DEVELOPMENT SOURCE UPDATED; NODE TRACKING QC PASS; PRODUCTION DEPLOYMENT AND GA4 INGESTION NOT YET VERIFIED.
