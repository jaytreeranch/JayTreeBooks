# Upcoming novels promotion — release receipt

2026-11-09, checked 19:44 UTC.

Owner approved images/preview and public website update; narrator and subtitles selected for proposed 30-second teaser. Script/production approval remains pending. No video generated or posted.

## Verified production
- Source release commit: 422612d61f89604fd12e81a2ec5436c93aef79d7, main, remote SHA verified after publication.
- Existing social-image automation followed with 8a1077ae5f383168f33ead940ced7257c49f2f11; promotion files verified retained.
- GitHub Pages run 42685480695: build, deploy and report-build-status all SUCCESS.
- Live https://jaytreebooks.com/upcoming-books.html opened in browser with all three novel cards; every new illustration and all five published covers loaded.
- The Correction first-chapter CTA opened the correct existing first-chapter page.
- Mobile 390px: no horizontal overflow, navigation and cards readable.
- Homepage source retains navigation, promo section, styles and tracking script.
- Browser review identified oversized opening typography and anchor offset; this checkpoint reduces headline size and adds scroll margin. Follow-up live visual check required after this commit deploys.

## Tracking and checks
- GA4 G-PHE2JVV5P6 retained. New landing page and homepage use upcoming.js with existing tracking.js for UTM attribution.
- Six Node behavioral tests PASS, including background-tab activation, once-per-load impressions, click intent and safe missing analytics.
- Static validation PASS: 38 landing references, five existing sample links, three novel cards, six optimized images, correct GA4 ID and valid sitemap.
- Reporting connector refused access because GSC Wizard subscription is inactive. Browser sandbox does not expose the live analytics runtime/network for collection inspection. Therefore actual GA4 server receipt and visitor totals are NOT VERIFIED. This is not a claim that the site's existing GA tag is broken.
- Local tests are suppressed from production analytics; live test URL used promo_test=1 and must be excluded from launch counts.
- Two pre-existing maintenance workflows failed in apply_audio_seo.py on missing audio-breadcrumbs in the five audio pages. They did not commit their work; independent Pages deployment succeeded. Repair those separately, without replacing the current website using older generators.

## Files and rollback
Added upcoming-books.html, upcoming.css, upcoming.js and six sanitized WebP assets; modified index.html and sitemap.xml; added event tests and analytics/spec/plan docs. Approved PNG originals remain in the owner's private workspace. Only optimized public assets are in Git.

Rollback by a new commit restoring only the changed homepage/sitemap and removing their promotion integration. Baseline source: 112b93b3f0eac88c7e68178914e16f907bb1cd57. Never reset or force-push over later automation or unrelated owner changes. Preserve media and previous source history.

Next: verify the small visual polish deployment, then review the teaser script and voice choice before paid video production. Do not publish a video without owner review.
