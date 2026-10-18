# Repository working agreements

## Source and external writes

- Read `README.md` and `DATABASES.md`; the selected `scripts/<database>/config.yaml` determines the target DB and fields. Do not transfer mappings between DBs.
- `scripts/fetch.py` writes fetched inputs under `data/`; `scripts/update.py` reads completed.md and writes back to Notion. Neither is a harmless syntax check. Do not fetch private records or update Notion merely to validate code.
- Preserve page IDs, existing values, config mappings and the distinction between raw.md and completed.md. Do not invent unavailable field values.
- Never read, print or commit `.env` values or tokens. Read private DB contents only within the user-authorized target and fields needed for the requested workflow; do not expose or commit those contents. Keep raw.md/completed.md ignored; inspect staged paths before commit.
- For an authorized update, inspect the exact target and intended fields; use `--dry-run --limit 5` first and report simulation and actual updates separately. Dry-run may still access the live service; it is not an offline test.
- Use a dedicated branch and PR against `master`. No offline automated test suite is established; validate Python syntax without importing network clients and use isolated mocked inputs for behavior changes.

## Review and local verification

- Meaning-preserving edits: final diff and relevant syntax/link/output checks. Behavior changes: one independent review. Auth/permissions/secrets/billing/migrations/production or broad impact: heightened review with specialist and rollback scrutiny.
- The agent chooses model/profile/effort and records review depth/reason in the PR. Failed invocations are not reviews and alone do not justify lowering depth; use an available method. Reassessed depth needs a reason. Re-review material changes, not typo/comment/evidence-only followups.
- Use affected repository checks; do not add dependencies or unrelated full suites just for verification. Failures, unresolved findings and missing required evidence block merge. Report untested coverage.
- Local validation is primary; optional Actions are skipped by default after checking enforced rules and repo exceptions. Existing automatic triggers remain: use [skip ci] only when permitted; do not dispatch/re-run by default. Record real run outcomes, using NOT_RUN only for no execution. Approval for merge, deletion, publication, deployment and paid operations remains required.
