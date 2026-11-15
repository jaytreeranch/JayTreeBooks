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

## Six-title Payhip checkout progress, evening November 14, 2026

**Development checkpoint, not a public launch.** The direct-sales website has been extended on this private feature branch to six exact, seller-verified Payhip product URLs. The separate Hollow Bell novella audiobook is now represented on the homepage, audio cards and book details. None of this website code is merged to public main. The offer remains limited-time **$1.99** with no advertised expiration.

The seller-side authorized desktop Chrome browser was temporarily usable when all three farm Windows sessions were Active. With ACX distribution clearance confirmed, four strictly product-scoped single-use 100%-off test coupons were created. The actual Payhip buyer checkout plus both seller and buyer emails now passed for **Second Draft, The Correction, and The Hollow Bell novella**. For Second Draft and The Correction, the complete buyer MP3 and M4B downloads independently matched source master SHA-256 and were preserved on JayTree LAN; **one copy per format was verified, repeat-download QC still pending**. The Hollow Bell novella has actual free checkout and emails but still needs both buyer-format downloads and hashes. The full Hollow Bell novel remains not tested through Payhip buyer checkout. The prior The Absconding and The Hollow Year buyer-flow tests remain independently verified. Live paid-card charging has never been tested.

**Safety / interruption:** The user RDP session on JT-DESKTOP and JT-GE78 switched to Disconnected again during testing. A fresh UI Automation document became unavailable and a screen check was black despite the machines and secure tunnels remaining online. No force-reconnection, browser termination, credential copying or unsafe direct API call was attempted. **The Hollow Bell novella was last VERIFIED UNLISTED (not publicly listed, but reachable to someone with the direct link)** and must be returned to **Invisible/Hidden** as the first seller action after trusted interactive access returns. The Correction and Second Draft were verified restored to Hidden; the other three new products remained Hidden at their latest trusted checks. Never claim all six are currently Hidden.

Website QC on the feature branch at source commit `94f535d9b25c77ede8a8996809971323eaf83631`: independently downloaded to JT-DESKTOP and executed `node --check app.js` **PASS**, plus `node --test tests/audiobook_purchase_links.test.js` **5/5 PASS**. Checks protect six exact links, dynamic book page plus homepage CTA, and the separate novella card. These are source regression tests, not public-store acceptance.

Private source evidence: `FOUR_ACX_CLEARED_PAYHIP_BUYER_QC_PROGRESS_20261114_V1.json` on the established `SixAudiobooksLaunchControl20261113` LAN staging directory; SHA-256 `81D298892F280724D1E21A8F89B7640ECEEE0F7607F78A9AC98907361CDFA9AB`. The receipt retains private order/coupon codes and exact buyer file hashes; do not copy those values into GitHub.

### Required continuation order

1. Verify Local Control hostname and Active Windows interactive session; reopen the existing authenticated Payhip seller tab. Immediately return the novella from Unlisted to Hidden and verify a fresh seller product list.
2. Complete the Hollow Bell novella full MP3/M4B buyer download/hash checks, then the full-novel free buyer checkout, receipts and both download/hash checks. Repeat buyer downloads for all four newly cleared editions as required by the pre-established release gate, documenting each exact SHA.
3. Verify limited coupons are exhausted/disabled, issue final four new private `SALE_READY` receipts, and verify all six exact seller products are Visible and genuinely buyer-accessible before merging this draft PR or enabling six public website checkout links. Verify public GitHub commit SHA and Pages live HTTP/CTA afterward. Keep the older $5 Correction listing untouched.
