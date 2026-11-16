# 2026-11-16 -- Free first-party Google Search Console OAuth and dashboard QC passed; live Google consent and scheduler PENDING.
See docs/handoffs/2026-11-16-self-hosted-gsc-oauth-dashboard.md and docs/SEO_FREE_RANK_TRACKING.md.

# JayTree Books - Current source handoff index (2026-11-15)

Live published website status is documented in docs/CURRENT_HANDOFF.md. Do not confuse this development branch with a new live website release.

Free Search Console keyword tracking: STAGED/OFFLINE TESTED, not yet live. Source scripts/gsc_weekly_tracker.py and dedicated historical import are validated; private LAN archive exists. Google OAuth permission and authenticated weekly trigger are missing. GE75 authenticated SMB access and Python are not verified; Desktop tunnel and Python are working. OpenSEO routine checks are discontinued. Two fixed page-one SEO goals retained.

See docs/SEO_FREE_RANK_TRACKING.md for exact setup and docs/handoffs/2026-11-15-free-google-search-console-ranking-collector.md for receipt, blockers, rollback and next actions.
Full offline regression: 35 Python and 56 Node tests PASS. Live OAuth and weekly execution still pending.
