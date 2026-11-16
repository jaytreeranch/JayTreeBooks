# Google Search Console: owner requested indexing of three JayTree Books pages

Date: 2026-11-16, America/Chicago.
Authorization: Owner explicitly stated "all three submitted" after requesting indexing through the official Google Search Console URL Inspection interface.
This is an **owner-reported UI action**, not an independently verified submission receipt: the official Google read-only URL Inspection API cannot enumerate individual indexing request events.

## Submitted page URLs
1. https://jaytreebooks.com/mystery-books.html
2. https://jaytreebooks.com/books.html
3. https://jaytreebooks.com/audiobooks.html

## Independent post-submission Google status verification
JT-GE78 hostname_test passed; current user's approved Windows DPAPI Google OAuth vault was used solely with official Search Console read-only permission. Google domain access passed. Three URL Inspection API reads succeeded, stored privately on JayTree LAN.
- New Mystery Books: **Crawled - currently not indexed**; last crawl reported 2026-11-16T16:55:23Z.
- Books storefront: **Crawled - currently not indexed**; last crawl reported 2026-11-16T16:55:23Z.
- Audiobooks: **Discovered - currently not indexed**; no last crawl timestamp.
- Both of the first two pages had previously been "URL unknown to Google"; this is confirmed progress in discovery and crawl, but no Google indexing acceptance yet. Owner's Request indexing does not guarantee indexing.
- No repeated requests or third-party paid API usage. No changes to website, Search Console scope, protected farm scheduler, current GA4, sales funnels or any credentials.
- Detailed official API evidence PRIVATE: \\JT-DESKTOP\JayTreeFarm\Projects\JayTreeBooksWebsiteRedesign_20261114\SEO_LINKS_20261116\GSC_AFTER_OWNER_INDEX_REQUESTS_20261116.json; SHA256 E8353CE2FDB89A735DC02F64C1EAE91FF448AF2AC28F695143DDAB7A311CC88A.
- Private current stage log updated in the same folder. Any older dated "not submitted" statements are historical pre-owner-approval observations, not present-tense state.

## Next step and decision rule
Do not request indexing for the same URLs repeatedly now. Allow normal Google crawling and periodically recheck their **indexingState/coverageState** using the owner-controlled direct Google OAuth. If they remain not indexed after a reasonable period, inspect index coverage, duplication/canonical selection, content value, and internal-link routes rather than guessing that a request failed. Maintain the two exact target keywords psychological mystery books and new mystery book. The collector has not yet been enabled for unattended weekly runs because a protected Production Manager scheduler must have one verified authority.
Rollback: no website or API writes occurred here; revert documentation only if owner later corrects the submission report. Preserve the private historical receipts.