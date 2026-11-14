# Audiobook Payhip two-title release — staging handoff (2026-11-14)

## Scope and current disposition

**STAGED; NOT DEPLOYED / NOT PUBLICLY LAUNCHED.** The website changes on `feature/audiobook-two-title-payhip-20261114` prepare two, and only two, approved direct-sale products for the limited-time **$1.99** promotion without an advertised end date. No public website changes were merged. The Payhip owner dashboard was not reliably available for the final live visibility changes; do not expose the website purchase CTA until both eligible products have confirmed **Visible** status.

- The Absconding — https://payhip.com/b/q3GfL
- The Hollow Year — https://payhip.com/b/Zf7tv
- **ACX clearance received after the initial staging audit:** ACX Support confirmed on 2026-11-14 that its projects for Second Draft, The Correction, The Hollow Bell, and The Hollow Bell: A Millbrook Falls Mystery were unclaimed/removed effective 2026-11-14; no ACX distribution agreement remains active and no direct-sale restriction is asserted. The source confirmation is preserved in private Gmail and SHA-bound on JayTree LAN. The four now have **checkout-testing hold**, not ACX contractual hold: do not publish until real Payhip buyer checkout, delivery, repeat downloads and hashes are verified.
- Existing older $5 The Correction product must remain untouched.

## Verified tests and source

The Payhip dashboard previously confirmed a seller-side $1.99 product for each of six editions, plus a separate legacy listing. Two eligible editions had authentic seller and buyer test-order emails (100% off, $0); two MP3 + two M4B customer downloads per eligible title were SHA-256-equal to their staged release masters. Both M4B containers passed chapter metadata inspection. Real payment charging was not tested. Both PayPal and Stripe were reported Connected by the live Payhip account. The four held titles' editors each showed MP3 + M4B attachments and Invisible status. These checks do not resolve ACX exclusivity.

Website source: `index.html`, `app.js`, `tests/audiobook_purchase_links.test.js`. Source code allowlists exactly two direct Payhip URLs; every other title retains coming-soon treatment. On the independent JT-DESKTOP checkout of this feature branch, `node --check app.js` passed and `node --test tests/audiobook_purchase_links.test.js` passed 4/4. Re-run after any edits and before release.

## Current blocker

The authenticated JT-DESKTOP Chrome Payhip editor ceased exposing its page accessibility tree upon navigating to the eligible product edit page. Reload did not restore the DOM. No verified **Visible** save occurred. A previously open Products tab also contained stale order/visibility values; treat it as **not authoritative** until a fresh live read completes. The safe last live prelaunch baseline had all six new products Hidden. The operator preserved the user session and the unpublished branch; no forced browser shutdown or bypass.

## Rollback, preservation, next actions

Private source masters, transaction evidence, exact file hashes and signed-off rights assertions remain on JayTree LAN; do not commit buyer identifiers, coupons, private files or keys. Before any public activation, verify fresh live Payhip seller state; use the existing baseline to restore Invisible in case of error. If site deployed in future, Git revert the audiobook CTA changes and verify live Pages reversion to coming soon.

1. Restore trusted authenticated Payhip editor access without closing unrelated user tabs; confirm two eligible product identities/files and set **Visible** individually, verifying a freshly loaded seller page plus anonymous buyer-facing view.
2. Merge this reviewed website feature branch only after both seller products are visibly purchasable and rerun website+security tests; verify GitHub main SHA, public site HTTP content and two correct CTA links.
3. Written ACX release is now documented. Keep the remaining four Invisible while completing independent owner-controlled checkout, receipt, MP3/M4B repeat-download/hash validation and individual SALE_READY, then authorize visibility changes.

No promotional expiration date was introduced. Real paid-card checkout and post-publication customer purchase are not certified.

## Post-clearance source QC addendum (2026-11-14)

After the ACX response, all 16 staged files (MP3, M4B, sample and cover for each of the four newly cleared editions) were independently SHA-256 compared to the source release matrix on JT-DESKTOP: **16/16 PASS**. M4B chapter counts: Second Draft 50; The Correction 37; The Hollow Bell novella 39; The Hollow Bell full novel 50. This does not prove the files uploaded to Payhip are customer-download identical; that requires separate live Payhip tests.

Payhip seller Chrome accessibility/document control remained unavailable even after guarded reload and switching existing tabs; attempting an alternative machine showed the account was not authenticated there. No authorized live public-listing toggle occurred. All six customer launches remain **unverified/not deployed**. Private, dated six-edition release matrix: `SIX_VIVIAN_POST_ACX_CLEAR_RELEASE_GATE_20261114_V3.json` on the established JayTree audiobook staging LAN path.
