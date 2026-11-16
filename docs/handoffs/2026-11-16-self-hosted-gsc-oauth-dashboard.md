# 2026-11-16 -- JayTree Free Self-Hosted Google Ranking System

## Objective
Eliminate reliance on paid OpenSEO/Windsor/GSC Wizard for routine rankings. Use only official FREE Google Search Console API and locally controlled JayTree code. Keep original Page 1 targets "psychological mystery books" and "new mystery book".

## Verified work
Host: JT-GE78, authenticated native JayTree Local Control tunnel (hostname_test confirmed). Desktop tunnel currently returns HTTP 429, yet LAN share is available from GE78; do not call Desktop offline.
Repository: jaytreeranch/JayTreeBooks, isolated feature branch feat/free-gsc-weekly-tracker-20261115. No public website release or merge.
Source additions: scripts/gsc_local_auth.py, scripts/gsc_local_dashboard.py, tests/test_gsc_local_auth.py. Modified scripts/gsc_weekly_tracker.py to support secure local vault and offline historical HTML report.
Windows per-user DPAPI test: encrypted refresh token fixture is not plaintext and decrypts only inside current user context. OAuth flow requests webmasters.readonly, PKCE, random anti-CSRF state, loopback 127.0.0.1; no access token is stored on disk. Does not copy tokens from connected third-party apps.
Static dashboard: generated from actual GSC history only, plus separately labeled fixture test reports. No network dependencies or tracking pixels.
QC 2026-11-16: 24/24 targeted GSC unit tests PASS; full Python 49/49 PASS; full Node 56/56 PASS. Logs at D:\Projects\JayTreeGSCFree_20261116_QC. Py_compile and CLI --status PASS.
Baseline (historic only): September 2026 first-party 16 clicks/80 impressions, 5.475 overall average position; not a ranking for goal phrases.

## Limitations and not-yet-done
Google OAuth client JSON is not present in inspected Downloads or GSC local authorization. Google requires the account owner to authorize read-only permission. Do NOT bypass Google consent, scrape browser cookies, print credentials, or confuse first-party account state with OAuth authorization.
Live Google API pull: NOT RUN, no real new ranking report.
Recurring automated Monday collection: NOT ACTIVE; no Windows Scheduled Task, paid vendor, or new Actions schedule.
Google Search Console API is free with Google-imposed usage quotas; "no limits" is not literally possible for someone else's search data. Weekly 24 reads expected, well inside published request limits.
On GE78, credentials are intentionally bound to Windows user via DPAPI. GE75 cannot reuse encrypted vault without separate legitimate authorization or approved secure key migration.

## Next three actions
1. Owner creates/reuses free Google Cloud project and Google Desktop OAuth client, enables Search Console API, authorizes official read-only scope. Download client JSON privately to the target host. Watch External Testing 7-day refresh-token expiration.
2. Use the verified GE78 tunnel to launch local OAuth browser authorization (requires owner consent), validate exact domain property and run first genuine 28-day comparison; verify private LAN history.csv and dashboard.html.
3. Only after first live PASS: integrate the existing JayTree Production Manager scheduler for weekly Monday read-only collection, verify subsequent snapshots, and fix GE75 worker access before considering that host as publisher.

## Rollback and continuity
Rollback changes only on this feature branch, no public website, Payhip, game, or video code touched. Preserve LAN history and original 2026-09-24 baseline. No secrets committed to GitHub. Commit/push remote SHA in stage log; do not claim live deployment.