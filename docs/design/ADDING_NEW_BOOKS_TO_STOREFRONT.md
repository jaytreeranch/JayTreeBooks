# Add new JayTree Books titles to the redesigned storefront

**Status:** This is review-only work on design/multipage-storefront-review-20261114 (draft PR #32). Do not merge into main without whole-site release approval.

## One central catalog

The v2 website uses data/storefront-catalog.json for the Books, Audiobooks and Samples sections. Run scripts/build_storefront_catalog.py to create search-crawlable HTML product cards automatically, not JavaScript-only catalog tiles. When a seventh book is added, the storefront can grow without manually copying six card templates.

Each available audiobook card is selectable: clicking its cover updates the featured cover, title, description, real Payhip button, and correct audio sample link. The initial featured audiobook is chosen by the featured_audiobook field.

## Stage a new book while writing

A JayTree agent may run:

    python scripts/new_storefront_title.py --title "Working Title" --tagline "Unique mystery mechanism" --description "Short compelling hook" --write

This stages the title as coming_soon, with no purchase URLs. Add --audiobook-coming-soon only when a future audiobook edition is genuinely planned. There are no fabricated launch dates, sample files, checkout products, or prices. Editing the JSON directly is equally supported.

## Make the book purchasable

When the actual book edition is published, add its approved official cover, a real Amazon URL, a verified individual book details page at books/<slug>.html and optional first chapter. Change book_status from coming_soon to published. Confirm Kindle Unlimited eligibility before enabling the badge.

The generator deliberately preserves the six existing bespoke book details pages. A new title's individual detail page, metadata and sitemap entry require an editorial/release gate.

## Release the audiobook separately

After narration, rights, exact sample, digital files, Payhip checkout and fulfillment are approved, change audiobook_status to available. Supply its actual payhip_url, sample_page, narrator (currently Vivian) and audiobook_price_usd. Regenerate the cards.

An unapproved audiobook cannot acquire a Buy link: validation requires a published book, exact seller domain, sample path, narrator and price; duplicate Payhip links are rejected. The current sitewide promotional banner assumes all available audiobooks have the same price and Vivian narration; a different price or narrator requires reviewing marketing copy and validation *before* publication.

## Build and QC (agents use the existing JayTree tunnel)

    python scripts/build_storefront_catalog.py --write
    python scripts/build_storefront_catalog.py --check
    node --test tests/storefront_v2.test.js
    python -m unittest discover -s tests -p test_storefront_catalog.py -v

The generator is idempotent. Future-book tests prove that upcoming titles do not create fake buy buttons, and that a separately simulated seventh published audiobook updates all three catalogs, the featured hero, and relevant counts.

Before release, review the individual product page, metadata, search sitemap, full-novel/novella distinction, preview playback, correct Amazon and Payhip links, mobile and keyboard controls, tracking, and fresh deployed GitHub Pages receipt. No merge or production deploy is authorized by generating the cards alone.

## Preservation

Keep all original book and audio assets in their authoritative locations. Never overwrite the audio team's approved samples or Payhip sale-ready masters. Future title release is independent of the current redesign and should receive its own reviewed PR, verified remote SHA, QC record and rollback plan.

See docs/design/STOREFRONT_V2_NAVIGATION_AND_LAUNCH_PLAN.md and docs/handoffs/2026-11-14-storefront-v2-review-stage.md for navigation and continuity.
