# Six Vivian audiobook storefront — evening recheck (November 14, 2026)

## Outcome
**PASS: All six JayTree Books Vivian-narrated audiobooks remain publicly listed for sale through the existing Payhip products at USD $1.99 each.** The owner expressly requested that all six be on sale. No new Payhip products were created or new Payhip Chrome tabs opened during this recheck.

The approved ACX clearance email from Franco dated November 14 confirms the four affected ACX projects were unclaimed, no agreements remain active, and ACX asserts no restriction on separately produced direct sales. The original ACX email and associated private evidence remain on JayTree LAN.

## Current independent checks
- JT-DESKTOP Local Control tunnel `hostname_test` PASS; the active Windows session and existing authenticated Chrome seller `Products - Payhip` tab were reused.
- Payhip seller product list inspected live: **six of six new Vivian audiobooks VISIBLE at $1.99**. The older, unrelated $5 The Correction product remained Hidden.
- Live HTTPS requests made directly from JT-DESKTOP to `https://jaytreebooks.com/`, `https://www.jaytreebooks.com/` and `/app.js`: each HTTP 200, all six exact Payhip URLs present. All six `/books/<slug>.html` pages: HTTP 200, each exact single correct edition purchase URL, $1.99, MP3 and chaptered M4B, with no obsolete audiobook Coming Soon copy. No promotional expiry date imposed.
- The six previously issued private `SALE_READY` receipts, real $0 owner-controlled checkout orders and buyer/seller emails, four original/repeat MP3 and M4B SHA-matched downloaded copies per edition, written ACX clearance, and completed public HTTP acceptance remain documented on LAN.
- Attempts to fetch Payhip product pages without a browser session via HTTP returned 403 anti-automation responses; **this was not mistaken for a missing product**, since the authenticated seller showed all six Visible. A fresh nonzero paid-card charge and processor payout have **not** been tested.
- Existing remote `main` at this checkpoint: `38d2a4015daf2db48aded9bbf9fb545b364ac341`. No storefront media or website code changed during this recheck.

## Exact public checkout URLs
| Audiobook | Payhip product |
| --- | --- |
| The Absconding | https://payhip.com/b/q3GfL |
| The Hollow Year | https://payhip.com/b/Zf7tv |
| Second Draft | https://payhip.com/b/GejHn |
| The Correction (Vivian) | https://payhip.com/b/OPaGw |
| The Hollow Bell novella | https://payhip.com/b/EWc5q |
| The Hollow Bell full novel | https://payhip.com/b/0BeoF |

## Evidence, rollback, and continuation
Private receipt: `F:\JayTreeFarmStorageV2\Staging\SixAudiobooksLaunchControl20261113\SIX_VIVIAN_LIVE_STORE_RECHECK_20261114_204830.json`, SHA256 `4F65A259DDCA7E8D74ACAD927F1452AC6AFB287AC8B3DD215D4923A7AE352E92`. The same LAN location has updated current handoff and stage log, plus six release certificates and prior buyer download/hash evidence. Keep coupons, buyer identifiers, source audio and other private data exclusively on LAN.

**Sales launch status:** live. The only commerce limitation is that a real nonzero payment and payout were not yet tested. Follow-up priority: owner-approved marketing content for the limited-time $1.99 sale, then a nonzero-value checkout/payout reconciliation if economically appropriate. Do not repeat $0 test orders or hide live listings without a genuine buyer-facing failure.

**Rollback:** If a listing's buyer journey fails, temporarily switch *that new audiobook edition* to Invisible and remove or revert the specific website CTA; verify public Pages. Preserve the other five offerings and unrelated legacy $5 Correction listing.
