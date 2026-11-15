# Standalone interactive audiobook HTML preview — November 15, 2026 UTC

Status: OWNER VISUAL REVIEW ONLY, NOT DEPLOYED. Draft PR #32 remains unmerged.

## Delivered to owner in ChatGPT

- File: `JayTree_Audiobooks_Interactive_Preview.html` (single self-contained HTML, ~858 KiB)
- SHA-256: `c7df68ce227032a1b07f8fd839010fbfab2e7045a20b5f70e9463a3ba363c547`
- Independently created from the owner's approved cinematic lake and transparent headphones artwork plus crops of the *owner-supplied reference mockup* for visual-only covers.
- No external image folder or server required to open the file. Buy/Listen links connect to live external Payhip and jaytreebooks.com targets and therefore need an internet connection.
- Official production cover files must replace the screenshot-derived visual placeholders before a real deployment. The stand-alone preview is NOT a source of approved cover assets.

## Interaction QC

- Playwright Chromium set_content tests: all six card selections correctly changed featured cover, title, description, Payhip destination, sample URL and unique highlighted aria-pressed thumbnail at widths 1536, 390 and 320 pixels.
- 18/18 selection assertions PASS; no horizontal overflow and no broken images at these sizes.
- Sale links correspond to the existing six exact Payhip SKUs: GejHn, Zf7tv, 0BeoF (full novel), EWc5q (novella), q3GfL, OPaGw.
- Samples point to approved live routes: book-1, book-2, book-3, book-6, book-4, book-5 respectively.
- The six actual audiobook products are Vivian editions available now for $1.99; full alternative narrator editions are coming soon.
- External checkout payment/fulfillment not tested; button destination verified. No transaction was created.

## Caveats and next steps

This artifact illustrates the Audiobooks page only; the entire site redesign still includes Home, Books, Samples, individual book pages, series, newsletter, Challenge, search/SEO and accessibility QC.

The self-contained preview was delivered as a ChatGPT downloadable artifact; don't infer the standalone binary is stored in this GitHub repository. The implementation branch remains the source of website functionality, and the prior handoff documents the staged source. The preview itself is a separate review artifact. Future owner approval is required before importing artwork into production pages or merging PR #32.

Rollback: close the development PR; no change to main, live Payhip products or audiobook masters.
