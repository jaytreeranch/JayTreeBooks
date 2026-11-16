# JayTree Books - Free Google Search Console Ranking History

Status (2026-11-15): offline collector built; live OAuth authorization and weekly trigger PENDING. No paid OpenSEO service or rank tracker is required.

## Goals and methodology
The unmodified page-one goals are **psychological mystery books** and **new mystery book**. Secondary diagnostics are psychological thriller books, mystery books, jaytree books, and the hollow bell.

The script scripts/gsc_weekly_tracker.py calls Google's official read-only Search Console API. It extracts US Google Web search impressions, clicks, CTR and average position separately for mobile and desktop, per exact query, over two complete 28-day periods. End dates lag three days in Pacific time. There are no third-party API credits or Python dependencies. Search Console API usage quotas apply.

Blank position means NO REPORTABLE SEARCH CONSOLE IMPRESSIONS, not position 51 or an indexing failure. Some low-volume queries are anonymized. A smaller average position is better; 25 to 18 is positive movement.

## Verified on November 15
- The previous first-party baseline data/seo-search-baseline.json was imported to private LAN runtime/legacy/2026-09-24.json. It records site-wide 16 clicks, 80 impressions and average position 5.475 during August 25 to September 21, 2026. Those are NOT the target-query positions.
- On JT-DESKTOP: Python 3.14 available; offline unit tests 10/10 PASS; the script can read and archive the legacy baseline; and live mode correctly returns BLOCKED when OAuth is absent without writing fake rank snapshots.
- On JT-GE75: connected via verified Local Control hostname, but tested worker cannot read this LAN worktree through SMB and has no python executable on PATH. This must be fixed before GE75 can own the collector.
- Google read-only OAuth not currently authorized in this runtime. No first-party current Google ranking result exists yet.
- No automated weekly schedule, paid plug-in or Windows Scheduled Task has been enabled.

## Google one-time consent prerequisite
1. Verify the owner's existing Search Console domain property at https://search.google.com/search-console for sc-domain:jaytreebooks.com.
2. Register or reuse an authorized Google Cloud OAuth client at https://console.cloud.google.com/ and enable the Search Console API.
3. Approve OAuth consent for read-only scope https://www.googleapis.com/auth/webmasters.readonly.
4. Keep client ID, client secret and refresh token in private authorized host/LAN secret storage. Never post those values in chat, GitHub, the public website or a log.
5. Securely inject environment variables JT_GSC_OAUTH_CLIENT_ID, JT_GSC_OAUTH_CLIENT_SECRET and JT_GSC_OAUTH_REFRESH_TOKEN into the job runner. Alternatively supply a short-lived JT_GSC_ACCESS_TOKEN for one test. The collector never writes tokens to disk.
6. Verify first live Search Console receipt and owner/property permission through authorized Local Control; ONLY THEN integrate a weekly Monday trigger with existing JayTree Production Manager scheduling facilities, once secure host access is healthy. Do not use Windows Scheduled Tasks or unapproved GitHub Actions minutes.

Google authorization documentation: https://developers.google.com/webmaster-tools/v1/how-tos/authorizing
Search Analytics API documentation: https://developers.google.com/webmaster-tools/v1/searchanalytics/query

## CLI and outputs
Source: scripts/gsc_weekly_tracker.py (Python stdlib only).
- Run with --status for the readiness report without connecting to Google.
- Run with --out PATH to collect authoritative live GSC data after secure consent.
- Option --as-of YYYY-MM-DD pins the snapshot date (default is Pacific calendar day).
- Option --import-legacy PATH archives the historical first-party snapshot, without confusing it with current reports.
- Option --fixture PATH is for TESTS ONLY. It writes isolated fixture files.

LAN storage: \\JT-DESKTOP\JayTreeFarm\Projects\JayTreeBooksWebsiteRedesign_20261114\GSC_FREE_20261115\runtime
- snapshots/YYYY-MM-DD.json : dated GSC evidence (idempotent on same day)
- history.csv : cumulative exact-keyword and device observations
- latest.md : current and previous 28-day comparison
- legacy/ : separately labeled older first-party baseline
- fixture_snapshots/ and fixture-history.csv : NEVER presented as real Google analytics

No public site files, Payhip links, page metadata, or existing baseline were changed. Script failure exits with code 2 before writing an authoritative history snapshot. Rollback is removal of the new runner/integration, preserving the source baseline and private historical data.

## QA
Run python -m unittest discover -s tests -p test_gsc_weekly_tracker.py -v. Ten target tests verify fixed keywords, windows, filtering, null rank semantics, position movement, idempotency, fixture isolation, permission checking, safe OAuth failure and historic baseline import.

## Nov 16: fully self-hosted secure Google sign-in and offline dashboard
The following first-party components are now developed and QC-tested:
- scripts/gsc_local_auth.py: on Windows uses the official Google Desktop OAuth2 browser consent flow with PKCE (state checked, callback listener bound exclusively to 127.0.0.1); only webmasters.readonly permission is requested. Verifies access to sc-domain:jaytreebooks.com before saving authorization. Uses current-Windows-user DPAPI to encrypt refresh token, OAuth client ID and client secret in %LOCALAPPDATA%\JayTree\GSC\oauth-v1.dpapi. No browser cookies or third-party plugin tokens are extracted.
- scripts/gsc_weekly_tracker.py: now automatically uses that encrypted, local OAuth vault to refresh a temporary access token. Legacy env-based explicit authorization remains supported, but is not required once Google consent is completed.
- scripts/gsc_local_dashboard.py: after a genuine Search Console collection, produces a static, offline LAN dashboard.html with keyword, device, impressions, clicks, average ranking position, previous 28-day average, movement, and local SVG position history. It has NO external scripts, CDNs, tracking pixels or subscriptions. Test-only fixtures produce fixture-dashboard.html and never overwrite genuine reports.
- All 49 Python regression tests and 56 Node tests pass on JT-GE78. No Google permission has yet been granted; therefore there are still no genuine November keyword positions and no weekly job is active.

### One-time owner-controlled consent, without paid software
Official Google documentation: https://developers.google.com/identity/protocols/oauth2/native-app and https://developers.google.com/webmaster-tools/v1/how-tos/authorizing

1. In the owner's existing Google account, open Google Cloud Console: https://console.cloud.google.com/. Create or select a Google Cloud project and enable the **Google Search Console API**. This API is free.
2. Under Google Auth Platform, configure app branding/audience, and create an **OAuth client of type Desktop app**. Only request **https://www.googleapis.com/auth/webmasters.readonly**. Choose the appropriate Google publishing/audience setting; an External app left in Testing may have a refresh token that expires after seven days.
3. Download the OAuth Desktop client JSON **privately to the Windows Downloads directory of the computer that will run the collector**, or keep it in a private approved local path. Do not paste or upload its contents to chat or GitHub.
4. Once that file is available, the JayTree Local Control tunnel can launch:
   python scripts/gsc_local_auth.py --status
   python scripts/gsc_local_auth.py --authorize
   The local program opens Google's official consent screen in that computer's browser. The account owner approves Google read-only permission; the temporary loopback callback stores an encrypted token on the SAME Windows user profile.
5. Then the JayTree Local Control operator validates:
   python scripts/gsc_local_auth.py --check
   python scripts/gsc_weekly_tracker.py --out <JayTree private LAN runtime>
   Only after a genuine Google receipt succeeds should the existing authorized farm manager schedule Monday collection. No Windows Scheduled Task, externally hosted app, or GitHub Actions schedule is authorized here.

A browser login on a different computer does not automatically authorize this runner, and Google consent cannot be bypassed safely. The per-user Windows DPAPI vault is intentionally not portable between GE78 and GE75.

### Availability and cost facts
Google explicitly states **all Search Console API use is free** at https://developers.google.com/webmaster-tools/pricing. Its public usage quotas at https://developers.google.com/webmaster-tools/limits still apply; no system can promise unlimited Google private data extraction. This tracker needs approximately 24 Search Analytics calls for six keywords times two devices times two windows per weekly report, which is very small relative to published quotas. We avoid arbitrary third-party plan quotas, account caps, credit purchases and subscription fees.

### Unattended-run status and recovery
- Current authorized developer host JT-GE78: source and Python functional. The new CLI was status-checked, but shows private_consent_exists=false and no Desktop OAuth client JSON detected in the standard Downloads path.
- JT-DESKTOP tunnel previously failed its MCP probe HTTP 429 (connection/session issue, not proof the PC is offline). GE75 worker access still needs its own SMB/Python correction.
- Google consent and first real read: BLOCKED pending legitimate owner action. Until that consent is granted, this code MUST NOT claim a live report or activate recurring schedules.
- Revoking consent in Google Account security ends future access. Removing the private encrypted vault disables this worker. Reauthorization is required if consent expires, is revoked or changes Windows user.
- Rollback: remove the standalone local auth and dashboard runner source changes and retain all private historical snapshots; public website and Payhip code are unaffected.