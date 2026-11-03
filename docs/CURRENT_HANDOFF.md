# CURRENT HANDOFF — November 3, 2026: Hollow Bell V6 PRIVATE GitHub Release staging

**Current status:** The original 30-second Hollow Bell Beneath the Ice V6 MP4 and approved portrait JPG are stored on JayTree LAN AND uploaded with matching server SHA-256 to an existing **GitHub Release PRIVATE DRAFT** in this repository: tag hollow-bell-beneath-the-ice-v6-20261101, release ID 433067322. Authenticated server reports two matching assets. Unauthenticated GitHub release tag lookup HTTP 404, thus it is NOT PUBLIC. Never claim it is a published video.

**Root cause of old MP4 site 404:** _config.yml intentionally excludes media/social/video from GitHub Pages. Existing public official-trailer GitHub Release delivery returned HTTP 206. Do not use broken JayTreeBooks.com media/video URLs as source for Social Poster uploads.

**Exact approved hashes:** MP4 SHA256 211b150ccb1e7487faa9e1dd9fdd4c31bafb61f6a6341bc23c27f531e9219897, 20,768,108 bytes; portrait JPG SHA256 7b959cb19ccaf2fb232ab082d9d7e95d11ae8ede0bf73503c36cdf808c6b3c1e, 638,324 bytes. Independent authenticated stage receipt on LAN SHA 31d6410de79685f101722ee5fe52669e4bfdcefdea282f38f078b191ab32d622.

**Continue at:** docs/handoffs/2026-11-03-hollow-bell-v6-private-release-staging.md and Social Poster feature/hollow-bell-v6-release-admission-20261102 docs/CURRENT_HANDOFF.md. V6 delivery candidate remains disabled, gated by independent rights/signed release, exact account OAuth/remote duplicate check, and subsequent public release URL verification. No social upload. **DO NOT START OTHER BOOK VIDEOS.**

**Scope:** Feature-branch documentation only; JayTreeBooks main/deployed site and media archive unchanged. Private draft is separate from Git history. Rollback: preserve draft private until owner authorizes deletion; revert feature docs if necessary.

---

# JayTreeBooks — CURRENT HANDOFF

**Status at 2026-10-31: DOCUMENTATION BOOTSTRAP ONLY — PROJECT STATE NOT AUDITED.**

## Where to resume
- Repository: `jaytreeranch/JayTreeBooks`
- Default branch at bootstrap: `main`
- Instructions: `AGENTS.md`
- Standing policy: [JayTree Development Continuity](https://github.com/jaytreeranch/JayTreeLLC/blob/main/docs/JAYTREE_DEVELOPMENT_CONTINUITY_POLICY.md); the authenticated private operational policy is in `jaytreeranch/JayTree-Video-Studio/docs/JAYTREE_DEVELOPMENT_CONTINUITY_POLICY.md`.
- Last verified implementation branch/remote SHA: **NOT YET RECONCILED**
- Live app/deployment/queue: **NOT INSPECTED**
- Tests/QA: **NOT RUN as part of this documentation bootstrap**
- Production/publishing: **NOT MODIFIED by bootstrap**
- Parallel work/owner approvals: **CHECK BEFORE WORK**
- Backup/rollback: **CHECK EXISTING REPO AND LIVE HOST BEFORE CHANGING**

## Next exact actions
1. Read `AGENTS.md`, repository README and existing project-specific status documents. Discover recent commits/PRs and active development branches. Check live project through the existing authorized connection.
2. Record the actual stage, branch, verified remote SHA, source location, tests, deployment, blockers, rollback, next task in this file, then commit/push and verify again.
3. Append every coherent stage under `docs/handoffs/`. Never present the bootstrap as verified app status.

## Mandatory per-stage handoff fields
UTC timestamp; task/stage; affected source/tests/docs; verified remote commit SHA and branch; actual tests PASS/FAIL/BLOCKED; artifact hashes and safe storage; deployment/prod state; pending decisions; security gates; rollback; exact next action. Update this file and push it with every stage.
