# Five-novel Vivian audiobook direct-sale storefront — private feature branch

Checkpoint: November 8, 2026. This is an additive, non-deployed feature branch for **direct sales on JayTreeBooks.com**. No real checkout is offered, no product has been published, and no audiobook master is stored in public GitHub or Pages.

## User scope

Five primary novels: *Second Draft*, *The Correction*, *The Hollow Year*, *The Absconding* and *The Hollow Bell*. The separate *Hollow Bell* novella can be included later as a bonus product, but it does not count toward the five novels. First narrator is Vivian (Narrator D).

## Implemented

- `audiobooks/index.html`: new attractive, mobile-responsive five-book collection page. It uses existing published website cover assets and existing narrator-sample / first-chapter links rather than unreviewed or cloud-placeholder audio.
- `tests/test_audiobooks_private_storefront.py`: 7 safety/accessibility tests. **7/7 actual GE78 Python regression tests PASS** on November 8. Checks five accurate novels, five images with alt text, correct legacy sample links, no payment/download URL, no checkout button, noindex, and no false claim of live purchasing.
- Private site source audit on authorized LAN; HTML SHA256 (of Windows UTF8 staged copy) `fff8c96fd376d24157b0cefd97e26037b7917a9a279c544282f38b6847d3f0a9`. Public repository commit hash must be independently verified after latest handoff.
- The production site `main` branch, live navigation, customer data, checkout provider, payment settings, and published audio previews are **unchanged**.

## Release architecture and security

Do not attach the hundreds-of-megabytes customer M4B/MP3 files directly to a public GitHub Pages asset path. Use a secure **per-order delivery entitlement** through a suitable payment + digital fulfillment provider, with private files, expiry/revocation, download handling, receipts and support. No checkout links, pricing, keys, customer lists or provider credentials have been invented.

The private audiobook project keeps five-novel direct-sale draft catalog with every product `sale_ready=false`, `publish_allowed=false`. Progress: *Second Draft* is technically mastered in v5, *Correction* and *Hollow Year* gain-adjusted v5 encode jobs are active or awaiting QC, *Absconding* and *Hollow Bell* need remaining Vivian sections. The companion novella has technical v4 candidates.

## Exact next actions

1. Audit secure direct-download provider availability and authorized existing store integration; do not invent Payhip product URLs or claim checkout active.
2. Package each first-narrator edition with real approved cover, M4B, MP3 and sample. Verify all file checksums, chapter boundaries, complete decoding, source/content QC, acceptable levels, and ownership/licensing.
3. After explicit per-title SALE_READY, attach payment-product mapping in a non-secret config on this feature branch, test sandbox checkout and signed/authorized file delivery, then merge/site-deploy with approved release and live QA.
4. Keep title-level status factual. Do not weaken historic chapter FAIL holds or treat deferred owner listening as approval.

Rollback: delete or close feature branch only. Do not change public `main` or paid product delivery records.