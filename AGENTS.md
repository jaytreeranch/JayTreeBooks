# JayTree development continuity — mandatory agent instructions

Applies to all ChatGPT, Work, Codex, AI-agent and developer work in this JayTree repository. Read at the START of every coding session; obey throughout the work.

1. Start by inspecting this repository's latest branch/commit, README, existing status and handoff docs, and actual machine/runtime state. Honor existing project-specific instructions and concurrent work. Never rebuild from scratch solely because this is a new chat.
2. **After every coherent development milestone and before the end of every session:** commit and PUSH all non-sensitive changed source, tests, schemas, configuration templates and documentation to the correct GitHub repository. Use a feature branch or draft PR when work is not production-certified. Do not force-push, rewrite others' work, or require a merge to preserve progress.
3. Update `docs/CURRENT_HANDOFF.md` (or the repository's existing authoritative `docs/CURRENT_STATUS.md`) alongside the code. When needed, add timestamped records under `docs/handoffs/`. Include: actual completed changes, files, tests/receipts with PASS/FAIL/PENDING, live runtime, blockers, owner approvals, next precise executable action, rollback, media locations/checksums, branch, and **verified remote commit SHA**.
4. The checkpoint is **not complete** until GitHub remote presence and SHA have been verified. If verification or push fails, record `NOT_PUSHED` / `NOT_VERIFIED`, preserve local work and explicitly tell the owner. Never imply success merely from creating local files or commits.
5. Keep production media, AI models, private databases, personal files, keys, tokens, credentials and large artifacts on authorized JayTree LAN storage; put only safe code/docs and sanitized small assets in Git. No default GitHub Actions spending for backups.
6. Do not publish media, deploy production, alter protected services, or merge release branches on the strength of a code checkpoint alone. Separate development from verified production authorization.
7. At the next chat start, re-read this file and the latest handoff, compare GitHub/working tree/live runtime, verify authorized JayTree MCP hostname before host commands, then continue the stated next step.

Canonical owner policy (private): `jaytreeranch/JayTree-Video-Studio/docs/JAYTREE_DEVELOPMENT_CONTINUITY_POLICY.md`.
For projects with existing stricter production/security policies, follow those too. Repository files are discovery aids; a new ordinary ChatGPT chat must still be given project access and/or the account-wide continuity instruction.
