# JayTree Books free Google Search Console collector -- 2026-11-15

## Owner-approved goal
Replace subscription-based OpenSEO routine checks with a free, first-party Google Search Console read-only weekly keyword history; preserve the two page-one SEO goals.

## Completed on JT-DESKTOP
- Inspected AGENTS.md, latest docs/CURRENT_HANDOFF.md, the existing 2026-09-24 Google Search Console baseline, LAN policies, branch status and GitHub main before coding.
- Created isolated Git worktree branch feat/free-gsc-weekly-tracker-20261115 from verified remote main; preserved active design/development worktrees.
- Added stdlib-only scripts/gsc_weekly_tracker.py: US exact-query/mobile-and-desktop, read-only Google API; 28-day vs previous-28-day comparison; 3-day Pacific date lag; no "rank >50" inference from absent impressions; atomic JSON/CSV/Markdown private LAN outputs and credential fail-closed.
- Added tests/test_gsc_weekly_tracker.py: 10/10 isolated unit tests PASS, covering filtering, exact goals, date math, missing data, direction, no secrets, unauthorized property, no fake snapshot, idempotency, separate fixture and baseline import.
- Imported historical 2026-09-24 Google evidence to runtime/legacy/2026-09-24.json; 16 clicks, 80 impressions, 5.475 overall average position. Not a current target keyword rank. Historical input remains unchanged.
- Tested no-auth runtime: PASS (BLOCKED, no fabricated live snapshot). --status reports oauth_present=false. No paid plugins or scheduled actions activated.
- Tested JT-GE75 via verified direct Local Control: host responded, but LAN path not readable in this worker's SMB session and python not on PATH. Do not assume GE75 is ready. No farm network/auth changes made to avoid concurrent production-manager repairs.
- Documented secure one-time Google read-only OAuth consent and approved future scheduler integration at docs/SEO_FREE_RANK_TRACKING.md.

## Verified vs pending
- PASS: Python source parse, ten focused tests, historical baseline archival, no-auth failure isolation, standalone CLI --status, LAN paths.
- PENDING: Actual Google OAuth user consent and secret delivery, first live API pull/Google index and search-position verification, authenticated worker, weekly trigger and two successive real weekly history receipts.
- NOT DONE: A live free weekly run or any claim that site ranks in Google top 50.
- No public website changes, content changes, Payhip changes, SEO target changes, GitHub Actions minute usage, Windows Scheduled Tasks, or subscription payments.

## Exact next three actions
1. Have owner authorize the official Search Console API once, using Google Cloud OAuth and webmasters.readonly, without sharing secrets in chat. Securely provision the approved runner.
2. On an authorized host with Python and LAN access, run one live read-only collection for sc-domain:jaytreebooks.com; validate actual output/query positions and secrets isolation.
3. After first valid receipt, integrate weekly Monday collection into the existing authorized Production Manager scheduler and verify a second real checkpoint. Restore GE75 path/Python first if GE75 chosen; otherwise use Desktop standby under explicit authority.

## Rollback
Remove this isolated runner and unconfigured integration while retaining private LAN historical audit files. Site files and previous production deploy are untouched. Do not delete original data/seo-search-baseline.json or rewrite concurrent branches.

## Storage / source
Worktree: F:\JayTreeFarmStorageV2\Projects\JayTreeBooksWebsiteRedesign_20261114\GSC_FREE_20261115\source
Private LAN runtime: F:\JayTreeFarmStorageV2\Projects\JayTreeBooksWebsiteRedesign_20261114\GSC_FREE_20261115\runtime
Git branch: feat/free-gsc-weekly-tracker-20261115
Git full SHA: see independently verified remote SHA in LAN milestone log and final handoff after commit/push. Not yet production deployed.
## Final offline QA receipt before GitHub source checkpoint
- Complete repository Python unit suite 35/35 PASS on JT-DESKTOP; raw logs archived under GSC_FREE_20261115/qc.
- Complete repository Node test suite 56/56 PASS; raw logs archived in the same LAN QC folder.
- Source targeted unit suite 10/10 PASS, legacy archive migration PASS, real Google OAuth absent -> BLOCKED (expected), git diff --check PASS.
- Live Search Console auth and scheduled weekly collection remain BLOCKED, not silently marked complete.