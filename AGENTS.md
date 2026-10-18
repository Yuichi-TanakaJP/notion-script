# Repository working agreements

## Source and external writes

- Read `README.md` and `DATABASES.md`; the selected `scripts/<database>/config.yaml` determines the target DB and fields. Do not transfer mappings between DBs.
- `scripts/fetch.py` writes fetched inputs under `data/`; `scripts/update.py` reads completed.md and writes back to Notion. Neither is a harmless syntax check. Do not fetch private records or update Notion merely to validate code.
- Preserve page IDs, existing values, config mappings and the distinction between raw.md and completed.md. Do not invent unavailable field values.
- Never read, print or commit `.env` values, tokens or private DB contents. Keep raw.md/completed.md ignored; inspect staged paths before commit.
- For an authorized update, inspect the exact target and intended fields; use `--dry-run --limit` first and report simulation and actual updates separately. Dry-run may still access the live service; it is not an offline test.
- Use a dedicated branch and PR against `master`. No offline automated test suite is established; validate Python syntax without importing network clients and use isolated mocked inputs for behavior changes.

## Review and verification defaults

- **省略可**: 意味・動作・運用判断・契約・実行手順を変えないdocs/comment等。最終diffと関連syntax/link/outputを確認する。
- **通常**: 動作を変えるcode/UI/API/config/schedule/external I/O。独立レビューを1回行う。
- **重点**: auth/permission/secrets/billing/DB migration/production operation/広い影響。独立レビューに専門・security・rollback観点を含める。
- model/profile/reasoning effortはagentがリスクと不確実性から選ぶ。レビューの起動失敗・quota・認証・model利用不能は完了ではなく、その失敗だけを理由にdepthを下げない。利用可能な別手段で必要な結果を満たす。変更内容の再評価でdepthを変える場合は理由を記録する。
- 意味のあるレビュー後修正だけ再レビューする。typo/comment/evidenceだけなら最終diff確認とする。PRにdepthと理由・実施結果を記録する。
- ローカルのリスク相応の検証を主とし、Actionsは任意・既定スキップ。未実行やbilling停止はNOT_RUNでありPASSではない。それだけでmergeを止めないが、ローカル失敗・未解決指摘・必須証拠不足はHOLD。実際の強制branch ruleと明示のrepo例外を確認し、無断でbypassしない。
- この方針は削除・本番deploy・公開・課金・mergeの承認を代替しない。既存の固有安全・データ・UAT条件は保持する。
