# JayTree Books — Multi-page storefront redesign and release map

Status: CONCEPT IMPLEMENTED ON ISOLATED REVIEW BRANCH. Not merged, not published, and not authorized to replace the current homepage.
Date: November 14, 2026 (CST)
Branch: design/multipage-storefront-review-20261114
Repository: jaytreeranch/JayTreeBooks
Base: ea3ee60b90e880d5c28bbfb219dfe8662a81a76d (includes independently completed Vivian sample work).

## Product goal

Convert the existing very long author/brand homepage into a premium mystery-fiction **navigation hub** with two clearly differentiated shops. Keep purchases fast, preserve distinct editions, and ensure the final published Vivian samples and existing buyer fulfillment remain authoritative.

### Brand language

Mystery mechanism first, never generic thriller hype. Retain JayTree's official gold tree-and-book mark, six real cover artworks, dark navy/charcoal, muted gold, warm cream typography, cinematic fog-inspired gradients. Do not use concept/mockup covers as actual editions. Emphasize readability and sufficient spacing over excessive parallax/video effects.

### Proposed visitor map

    Homepage (/)
    ├── Shop Books (/books.html)
    │   ├── Five published novels (Kindle Unlimited and Amazon format options)
    │   └── The Hollow Bell novella (separate shorter edition; not a sequel)
    │       └── Existing individual /books/{slug}.html product pages (preserve SEO URLs)
    ├── Shop Audiobooks (/audiobooks.html)
    │   ├── Six full Vivian editions — $1.99 each, MP3 + chaptered M4B
    │   ├── One-click existing Payhip checkout per edition
    │   └── Hear samples (approved /audio/book-N-sample.html pages, including novella #6)
    ├── Try Samples (/samples.html)
    │   ├── Read existing first chapters
    │   └── Hear verified Vivian previews / existing other narrator samples
    ├── The mystery universe / future books (/upcoming-books.html and existing series pages)
    ├── Mystery Challenge / JayTree Case Files (migrate existing dedicated experience)
    ├── Videos, animated series and trailers (preserve pages, embeds and tracking)
    └── About, Reading Guides, Privacy, Terms, email and social destinations

Do not remove the current #books, #audiobooks, #case-files, #challenge or #youtube deep-link experiences until corresponding replacement anchors/landing destinations are implemented and tested. Redirect or retain any evergreen content with meaningful search performance. The new homepage should be concise, but should not orphan long-form material.

## Working preview routes (not live)

- /home-v2.html — shorter premium brand homepage with immediate Book/Audiobook buttons, 3 paths, featured audiobook offer and supporting news destinations.
- /books.html — six-book crawlable HTML catalog; real covers, original Amazon editions, Kindle Unlimited badges on five novels, honest novella separation and reading samples.
- /audiobooks.html — six separate real Vivian $1.99 Payhip CTAs, six preview links, MP3/M4B buyer info and an explicit note only alternative full narrator editions are coming soon.
- /samples.html — focused six-edition preview index, using EXISTING approved preview routes; no audio assets or sample source files changed in this project.
- /storefront-v2.css — namespaced responsive design system using sf- classes and official brand icon to avoid production stylesheet contamination.
- /storefront-v2.js — one delegated outbound intent event handler; no false GA4 purchase event; preview hosts intentionally do not send GA4 events to the production property.
- /tests/storefront_v2.test.js — 11 static Node regression assertions.

All four pages are intentionally marked noindex,follow in review. Do not deploy a page with production canonical/index metadata until its route has been approved.

## Conversion paths

Book buyer: Homepage > Books > book details or first chapter > correct Amazon listing.
Audiobook buyer: Homepage > Audiobooks > title > optional audio preview > exact direct Payhip offer. No internal cart/payment form invented.
Undecided visitor: Homepage > Samples > first chapter or final Vivian voice preview > book and/or Payhip.
Audiobook narrator policy: Vivian **full editions available NOW** for all six. Other full-length narrator editions **coming soon**; comparison excerpts may be available already. Immersive is a separate work in development, not a reason to label the complete audiobook pending.

### Exact preserved seller identities

- Second Draft — https://payhip.com/b/GejHn
- The Hollow Year — https://payhip.com/b/Zf7tv
- The Hollow Bell full novel — https://payhip.com/b/0BeoF
- The Hollow Bell novella — https://payhip.com/b/EWc5q
- The Absconding — https://payhip.com/b/q3GfL
- The Correction — https://payhip.com/b/OPaGw

All external sellers preserve target=_blank, rel=noopener noreferrer where present, and data-track purchase-intent hooks. Do not treat an outbound link click as a confirmed payment; use only verified seller order or webhook events to record purchases. The previous alternate $5 Correction Payhip SKU is unrelated and must remain Hidden.

## Migration/launch gates (not yet passed)

0. **Concurrent-work protection:** Current main contains the other chat's latest Vivian sample work, including the dedicated book-6-sample.html. Do not edit/replace any audio source binary or approved preview page. Recompare main with the feature branch immediately before the eventual merge.
1. **Design review:** Owner reviews screenshots / pages. Decide which existing Challenge, YouTube, reading guides, newsletter and social content goes to dedicated pages or short homepage gateways.
2. **Finish production content:** Upgrade six existing /books/{slug}.html product-detail layouts with easy Amazon/eBook/print/audiobook/sample choices, without changing canonical identities. Create or preserve the standalone challenge/videos/reading guides routes as needed.
3. **SEO & deep links:** Retain canonical book links, metadata, schema, sitemap, existing crawlable book cards, social OG images, audio product copy, #legacy anchors and user attribution. Mark new indexable routes only after approval. Preserve existing Google Analytics configuration, Kit signup and Payhip links.
4. **UX / accessibility certification:** Test 320/390/768/1440px, keyboard menu and focus, 200–400% zoom, images, semantic H1, 44px touch targets, screen-reader check, reduced-motion behavior, LCP/CLS/INP and external checkout flow.
5. **Commercial certification:** Reverify six authentic final Vivian preview media hashes against audio team's handoff, approved seller SKUs/visibility, sample playback, checkout redirection, analytics intent once per click, cross-device/UTM links, and buyer downloads. Real-money settlement remains a separately owner-approved test; never invent proof.
6. **Release:** Do not merge this branch to main until explicit review approval and a passed coordinated release gate. Record expected SHA, use draft PR, merge only reviewed code, verify Pages deployment and public HTML/JS/CSS/links, then monitor. Roll back website-only changes if broken; do not hide live Payhip products.

## Evidence and current state

- Desktop/phone browser review screenshots and portable review gallery:
  \\JT-DESKTOP\JayTreeFarm\Projects\JayTreeBooksWebsiteRedesign_20261114\REVIEW_INDEX.html
- 11/11 targeted Node tests passed on immutable downloaded GitHub feature source.
- 10/10 Chrome viewport checks passed, across four desktop and mobile pages plus 320px narrow-phone home/audio tests. No horizontal overflow or broken cover/logo images.
- Six of six existing sample HTML pages responded HTTP 200 when checked against public jaytreebooks.com.
- All six Amazon product links, all six distinct Payhip destinations and six audiobook sample routes verified in the new static HTML.
- Full WCAG and paid settlement certification NOT performed. Current production homepage has not been changed. Portable review folder is for visual review; external sample/book links are live site routes and not duplicated offline.
