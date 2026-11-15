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

## Post-merge production verification — 2026-11-15
- PR #37 merged to main as `13ce2f3479a3103a5db67b75a76754757f74b01a`; a later SEO maintenance commit `9c87cc3996ff7d31109f8a5ff83d9fde02fb06ef` preserved the tracking changes.
- GitHub Pages deployment run `43740737481` completed **SUCCESS** at the custom domain.
- **35/35 live sitemap routes returned HTTP 200** and carried the expected GA4 config plus shared tracking helper, audited in two independent parity partitions via GE75 and GE78. **10/10 target public pages HTTP 200** via JT-DESKTOP with expected new scripts and events; unverified thank-you signup conversion removed.
- Local source regression **5/5 PASS** and **18/18 inline script Node parsing PASS**, PR validation workflow `43740310488` **SUCCESS**.
- **Final analytics truth limitation**: GA4 Data API traffic/event report cannot currently be read. GSC Wizard access requires subscription, Windsor.ai reports 5 connected sources versus 1 on its Free plan. Do not report real pageview or conversion ingestion verified. Kit subscription confirmation and Payhip purchase events not retested in this release.
- This is a tracking-only source change; zero Payhip catalog, pricing, audio master, social media or private OAuth modifications.
- **Rollback**: selective restoration of the 14-file PR #37 change-set, preserving subsequent SEO/PWA automation commits. Re-run 35 route checks after rollback.
- **Next actions**: restore a GA4 read connection (one provider); inspect last-day `page_view`, `audio_sample_play`, `audio_sample_complete`, `audiobook_payhip`, `campaign_landing`, newsletter `generate_lead`; separately verify Kit subscriber success and genuine Payhip purchase before claiming `sign_up` or `purchase`. Watch whether subsequent SEO/PWA generators preserve code.
