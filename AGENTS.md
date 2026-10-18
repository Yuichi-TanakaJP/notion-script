# Repository working agreements

## Source and external writes

- Read `README.md` and `DATABASES.md`; the selected `scripts/<database>/config.yaml` determines the target DB and fields. Do not transfer mappings between DBs.
- `scripts/fetch.py` writes fetched inputs under `data/`; `scripts/update.py` reads completed.md and writes back to Notion. Neither is a harmless syntax check. Do not fetch private records or update Notion merely to validate code.
- Preserve page IDs, existing values, config mappings and the distinction between raw.md and completed.md. Do not invent unavailable field values.
- Never read, print or commit `.env` values or tokens. Read private DB contents only within the user-authorized target and fields needed for the requested workflow; do not expose or commit those contents. Keep raw.md/completed.md ignored; inspect staged paths before commit.
- For an authorized update, inspect the exact target and intended fields; use `--dry-run --limit 5` first and report simulation and actual updates separately. Dry-run may still access the live service; it is not an offline test.
- Use a dedicated branch and PR against `master`. No offline automated test suite is established; validate Python syntax without importing network clients and use isolated mocked inputs for behavior changes.

## Review and local verification

- Known, isolated low-risk edits with reversible effects (not just Git-revertible): affected checks and final diff; independent review/UAT docs optional. Size/extension alone is not low risk; high-risk gates and stricter domain rules override this exemption.
- Other behavior changes: affected tests, changed-path check and one independent review. Build/integration/UAT only where affected. Record results in PR or existing UAT; update changed acceptance contracts.
- Auth/permissions/secrets/billing/migrations, external send/publish controls, live-data/processed-state writes, scheduler execution controls (including retry/exit gating), production or broad high impact: independent specialist/domain and rollback scrutiny, related full suite/build and relevant UAT. Investigate unknown impact before granting a low-risk exemption.
- Choose model/effort for risk; briefly report scope/results/untested coverage. Failed reviews do not count or waive required scope. Re-review material changes only. Required-check failures and correctness/safety/requirement findings block; optional polish does not.
- Local checks first; optional Actions default off subject to enforced rules/domain exceptions. Preserve triggers; [skip ci] only when allowed, no default dispatch/reruns. No execution = NOT_RUN, never PASS. Existing merge/deletion/deploy/publication/paid-operation approvals remain.
