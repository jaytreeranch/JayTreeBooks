# Interactive audiobook hero and scalable book catalog — JayTree Books

Date: November 14, 2026 (CST)
Branch: design/multipage-storefront-review-20261114
Pull request: https://github.com/jaytreeranch/JayTreeBooks/pull/32
Status: DEVELOPMENT REVIEW ONLY — NOT MERGED OR PUBLISHED

## Owner-approved behavior

The supplied premium audiobook reference remains the desired visual specification. When a visitor selects any of the six small book covers, it **does not navigate away**: it replaces the top featured cover (inside the headphone framing), title, exact story description, book-detail link, selected title identifier, Payhip Buy button and Listen to Sample destination. It scrolls the selected feature into view, preserves keyboard access, exposes exactly one aria-pressed=true cover, and avoids animation when reduced motion is requested.

No checkout destination was invented. Original six Vivian Payhip links and six approved audio sample paths, including the separate The Hollow Bell full novel and novella, remain distinct and unchanged. Vivian is the only fully released narrator; future alternative full-length narrators are not represented as purchasable.

## New title workflow

The source of truth for the four-page redesign is data/storefront-catalog.json.

- scripts/new_storefront_title.py stages new books as coming_soon / no Payhip link, dry-run by default.
- scripts/build_storefront_catalog.py --write updates static, crawlable Books, Audiobooks and Samples cards, plus supported current-collection counts.
- The generator performs idempotent --check verification, preserves manually maintained original book detail pages and rejects accidental publication without actual seller/sample data.
- Published book and audiobook states are independent. An unreleased book has no buy button; an audiobook cannot be marked available before real publishing/sample/Payhip info exists.
- The featured_audiobook field chooses the initial featured item without hand-editing hero HTML. A newly released seventh audiobook can be added through the JSON and automatically selected.
- Additional audiobook prices or narrator editions beyond the currently approved uniform Vivian $1.99 promotional claim require explicit copy/QA review. The generator rejects silent mixed-price or mixed-narrator changes.
- New individual book detail pages and sitemap/SEO additions remain an explicit release gate; the generator does not overwrite the current six curated product pages.

Usage: docs/design/ADDING_NEW_BOOKS_TO_STOREFRONT.md.

## Verified QC

- 13/13 Node storefront tests PASS; no JS syntax failures.
- 8/8 Python release-state and generator tests PASS, including a simulated seventh released audiobook, first-feature switching, pending-release exclusion, URL safety, duplicate SKU safety, price safety and regeneration idempotence.
- Remote GitHub-generated pages downloaded and --check confirmed in sync after fixing UTF-8 punctuation preservation.
- Chrome DevTools browser test: **18/18 real selections PASS** (6 books at 1440px desktop, 390px and 320px phones). Actual click updates featured title, description, cover, book detail, distinct Payhip and sample links, exactly one selected thumbnail and scrolls to feature; no horizontal overflow or broken cover images.
- New-title helper dry-run passed without modifying catalog SHA-256.
- Screenshots: audiobook-selected-novella-1440.png and audiobook-selected-novella-390.png on authorized JayTree LAN.
- No real Payhip charge/settlement was attempted in this workstream. Browsing purchase destinations verified as HTTPS links, not payment completion.
- Existing final audio sample binaries, GitHub main, Payhip listings and production website were not modified.

## Remaining visual asset integration

The current branch renders a custom SVG lake/environment and inline headphone SVG in the working page. The owner separately approved more photographic cinematic lake and transparent gold/black headphone artwork in this conversation. Those approved generated bitmap assets were optimized in the conversation workspace but **have not yet been imported to the JayTree LAN or GitHub review branch**. Do not claim the current site image matches the approved renders perfectly. Import each as independent, optimized source artwork, verify layering with real covers across viewports, then ask for visual signoff. No flattening of the page into a mockup image.

## Next actions, rollback, continuity

1. Transfer individually approved cinematic background and headphone layer to LAN/GitHub review branch and replace SVG approximation; test transparent composition, official cover switching, visibility and performance.
2. Apply the same consistent sitewide cinematic visual system to short homepage, Books, Samples and individual book/series pages; preserve Challenge, newsletters, reading guides, videos and legacy anchor links.
3. Implement audited new-title detail-page/sitemap release step, and verify add-a-new-title workflow with actual private test content.
4. Test keyboard/zoom/screenreader, Core Web Vitals, tracking counts, sample playback and buyer redirects before owner authorizes merge.
5. **Do not merge draft PR #32 into main without separate owner authorization.** Rollback for this milestone is simply to close/revert the draft branch; production sales stay untouched.

Private LAN QC location: F:\JayTreeFarmStorageV2\Projects\JayTreeBooksWebsiteRedesign_20261114\
