# JayTree Books - first LIVE Google Search Console collection (2026-11-16)

## Goal
Complete the owner-approved, no-paid-vendor first-party Google Search Console integration for the exact primary phrases: psychological mystery books and new mystery book. Keep the offline reports private to JayTree LAN.

## Live results, with evidence
- Verified JT-GE78 via its authorized JayTree Local Control hostname_test. Existing standalone code is on feature branch feat/free-gsc-weekly-tracker-20261115. No production website source changes.
- The owner enabled the Search Console API for the Google OAuth Desktop client project after the initial API HTTP 403. The local program repeated the legitimate read-only OAuth consent and verified sc-domain:jaytreebooks.com directly using Google's Search Console API. It stored a refresh token in current-Windows-user DPAPI vault; no token was printed, pushed to GitHub, moved to LAN or made available to any third-party ranking provider.
- Direct live GSC Search Analytics collection completed PASS on 2026-11-16, with 12 current and 12 previous period exact query/device combinations (six keywords, mobile + desktop). Current date window 2026-10-17 to 2026-11-13; prior 2026-09-19 to 2026-10-16. Data source explicitly gsc_api, not fixture_test.
- Real output paths under JayTree LAN GSC_FREE_20261115/runtime: snapshots/2026-11-16.json, history.csv, latest.md and dashboard.html. Files verified nonzero, report and static HTML offline content pass basic QC. Private exact query statistics and file hashes retained in private LAN stage log, not the public source repository.
- First live Google collection indicates very sparse impressions for target phrases. Do not infer page-one performance, no-impression rankings or Google deindexing from missing keyword rows.

## Final tests and security
- Complete Python suite 50/50 PASS and Node suite 56/56 PASS on JT-GE78 after local OAuth diagnostic hardening. New targeted test verifies permission errors reveal only a sanitized Google reason, never access tokens or user-specific API response bodies.
- Verified first actual Google OAuth property check PASS; actual collector exit code 0, output four files present and all 12 CSV rows tagged gsc_api.
- Secure OAuth certificate and Desktop client secrets were never added to Git. Local refresh token intentionally remains in per-user Windows DPAPI vault and can be revoked in Google Account settings.
- First actual Search Console data did not require OpenSEO, Windsor.ai, GSC Wizard, paid external rank tracker, or GitHub Actions.

## Open work
- WEEKLY AUTOMATION: NOT ACTIVE. Must integrate official API collector with an already authorized JayTree farm scheduler, avoiding new Windows Scheduled Tasks and GitHub Actions costs. Run in same Windows user profile on which OAuth vault is available, or provision a separately authorized runner. GE75 manager/SMB repair is a separate production workstream.
- Refresh tokens of Google External apps left in Testing may expire after seven days. Inspect the Google Auth Platform audience/publishing status before relying on unattended multi-week reporting.
- Google imposes ordinary free API quotas and low-volume query anonymization; these are not third-party subscription limits.
- Keep private GSC raw history and dashboard on JayTree LAN. Never publish detailed owner analytics on public website.

## Next three executable actions
1. Inspect existing approved Production Manager scheduling authority and decide one single safe Monday owner for this low-volume read-only collector; keep control on verified authorized machine/user.
2. Integrate and QC idempotent weekly job, no new Windows Task, no duplicate exporters; verify first scheduled execution.
3. After a second real weekly snapshot, compare momentum and improve relevant human-edited genre landing pages. Do not change the original two page-one SEO goals.

## Rollback
Remove or disable the isolated collector scheduler integration; preserve all original Google history, the new first real snapshot, encrypted vault and existing production website. Revoke Google consent if access is no longer desired. No live website files changed by this milestone.
## Preservation checkpoint and scheduler coordination
- Verified live source GitHub feature branch checkpoint: 15b07000c7a50a80b966189bcf64deb9a0893dc4. Its remote branch HEAD matched via git ls-remote.
- Verified SHA-256 copies of nine source/test/real-report/QC files in private LAN GSC_FREE_20261115/first_live_20261116. The private manifest hash is 099FE9D4226215E3E3B18FA2887198D01920B6C6A63582B02D1AB739EC993DE8. Do not upload this private manifest or report data to GitHub.
- Read-only Production Manager inspection found historical active lease-recovery work and GE75 holds. Do not modify or compete with that controller merely to schedule this small job. Weekly schedule remains PENDING; prefer a single authorized existing PM scheduler after fresh live manager health verification, with the same JT-GE78 Windows-user DPAPI context.
- Google API initial HTTP 403 was resolved after owner enabled API. A second Google consent, property check, and genuine data collection all passed. Private exact keyword ranks live only on LAN.