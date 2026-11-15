# Six Vivian audiobook direct-sale release — November 14, 2026

## Production decision

**All six separate Vivian-narrated audiobook editions are privately SALE_READY and all six Payhip $1.99 products were verified VISIBLE in the authenticated seller dashboard.** The website deployment is a separate gate and remains pending until the GitHub Pages source is merged and verified live.

ACX Support confirmed in writing on November 14, 2026, that the four formerly affected ACX projects were unclaimed/removed effective November 14, no ACX distribution agreements remain active, and ACX asserts no restriction on independent direct sales. Original source email and SHA-bound clearance evidence are retained privately on JayTree LAN. Do not publish the private buyer or coupon tokens to GitHub.

## Exact live Payhip products

| Edition | Seller-verified public product URL |
| --- | --- |
| The Absconding | https://payhip.com/b/q3GfL |
| The Hollow Year | https://payhip.com/b/Zf7tv |
| Second Draft | https://payhip.com/b/GejHn |
| The Correction (Vivian) | https://payhip.com/b/OPaGw |
| The Hollow Bell (Novella) | https://payhip.com/b/EWc5q |
| The Hollow Bell: A Millbrook Falls Mystery (Full Novel) | https://payhip.com/b/0BeoF |

All six new products are $1.99 and use Payhip's **Visible — Everyone can see this product** configuration. The older, separate $5 *The Correction* product remains **Hidden**, untouched.

## Completed release gates

- Source package SHA validation for MP3, chaptered M4B, preview and cover; all master files matched their edition manifest.
- Six genuine owner-controlled Payhip 100%-discount buyer checkouts and buyer/seller confirmation emails verified, without charging a credit card.
- First **and second** customer-downloaded MP3 and M4B for each of all six editions SHA-256 identical to source release masters; 24 buyer-format copies checked across six editions.
- Six edition-specific private `SALE_READY_BUT_NOT_PUBLIC` receipts and an aggregate Payhip Visible gate receipt on JayTree LAN, verified by SHA-256.
- Payhip PayPal and Stripe integrations showed Connected at account level. Actual nonzero card charge and payout were **not** tested.
- All four new 100%-discount test coupons were verified exhausted at 1/1 redemption each; previously issued discounts are not publicly available.
- GitHub six-title $1.99 website CTAs staged on this feature branch, including separate Hollow Bell novella audio card and direct-book link. No advertised promotion end date.
- JT-DESKTOP ran `node --check app.js` PASS and `node --test tests/audiobook_purchase_links.test.js` **5/5 PASS**.

## Browser and download QC findings

The original seller browser session on JT-DESKTOP was reused; no additional Payhip tabs were opened in the final production phase. UI control was attempted only when the authorized Windows session was Active. Earlier disconnected Windows sessions were **not** mistaken for computers being offline.

Parallel repeat-download stress requests caused several Chrome **Failed — Network error** entries, and one full novel repeat MP3 attempt failed. Sequential retries succeeded and all 24 expected buyer-copy checks ultimately matched the masters. **Do not retry large downloads concurrently** or assume UI download requests are successful without checking both completion and SHA. Partial `.crdownload` failures are not release media and are not in the authoritative deliverables.

## GitHub and launch continuation

Feature branch: `feature/audiobook-two-title-payhip-20261114`; draft PR #26 at https://github.com/jaytreeranch/JayTreeBooks/pull/26. At this checkpoint, Payhip visibility is complete, website code is not yet merged; public site must not be claimed updated until GitHub Pages responds with six CTAs.

1. Rerun tests on the exact PR head; ensure comparison to `main` is ahead-only and PR contains only the expected changes.
2. Mark PR ready and squash-merge to `main`; verify exact remote SHA.
3. Verify the public JayTreeBooks homepage includes six $1.99 purchase CTA URLs, plus separate novella card and book pages. The public release must not advertise an expiration date.
4. Save final public-site HTTP/links QC receipt on JayTree LAN; update current handoff and stage log with merge SHA, pages verification, blockers, and rollback.

Rollback: for any buyer-facing failure, revert the exact website CTA merge and verify live Pages. If needed, return the six new Payhip products to Invisible and verify; preserve original packages and test orders. The separate $5 legacy Correction listing must remain untouched.
