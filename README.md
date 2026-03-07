# notion-script

Notion DB の空欄フィールドを AI 補完するスクリプト集。

対象 DB の詳細は [DATABASES.md](DATABASES.md) を参照。

---

## セットアップ

```bash
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt
```

`.env` を作成して Notion トークンを設定：

```
NOTION_TOKEN=secret_xxx
```

> `.env.example` を参照。トークンは Notion のインテグレーション設定ページから取得。

---

## 使い方（3ステップ）

### Step 1: データ取得

```bash
.venv/Scripts/python scripts/fetch.py --config scripts/memo_db/config.yaml
```

- Notion DB から全ページを取得
- 空欄フィールドがあるエントリのみ `data/<DB名>/raw.md` に保存

### Step 2: AI 補完（Claude Code 上で手動実行）

`data/<DB名>/raw.md` の内容を Claude Code に渡して `data/<DB名>/completed.md` を生成してもらう。

**スキルを使う場合（推奨）:**

Claude Code のチャットで以下を入力するだけ：

```
/notion-complete
```

DB の選択肢が表示されるので番号を入力すると補完が始まる。DB を指定する場合：

```
/notion-complete memo_db
```

> スキルは `~/.claude/skills/notion-complete.md` に定義済み。

### Step 3: Notion 更新

```bash
# 動作確認（Notion には書き込まない）
.venv/Scripts/python scripts/update.py --config scripts/memo_db/config.yaml --dry-run --limit 5

# 本番実行
.venv/Scripts/python scripts/update.py --config scripts/memo_db/config.yaml
```

オプション:

| オプション | 説明 |
|-----------|------|
| `--config` | 対象 DB の config.yaml パスを指定（必須） |
| `--dry-run` | 更新内容を表示するだけ（Notion には書き込まない） |
| `--limit N` | 最初の N 件だけ処理 |

---

## DB の追加・確認

アクセス可能な DB 一覧を確認：

```bash
.venv/Scripts/python scripts/list_dbs.py
```

新しい DB を追加するには `scripts/<フォルダ名>/config.yaml` を作成する：

```yaml
db_name: DB名
db_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
fields:
  - name: フィールド名
    type: select          # select / multi_select / status / rich_text
```

> 対応フィールド型: `select`, `multi_select`, `status`, `rich_text`

---

## ファイル構成

```
notion-script/
├── .env                         # Notion トークン（git 管理外）
├── .env.example                 # トークンのキー名テンプレート
├── requirements.txt             # 依存ライブラリ
├── DATABASES.md                 # 対象 DB・フィールド一覧
├── data/
│   └── <DB名>/
│       ├── raw.md               # Step1 の出力（git 管理外）
│       └── completed.md         # Step2 の出力（git 管理外）
├── lib/
│   └── notion_helper.py         # 共通クライアント・ユーティリティ
└── scripts/
    ├── fetch.py                 # Step1: Notion → raw.md（汎用）
    ├── update.py                # Step3: completed.md → Notion（汎用）
    ├── list_dbs.py              # アクセス可能な DB 一覧を表示
    ├── memo_db/
    │   ├── config.yaml          # めも DB の設定
    │   └── ...
    ├── life_todo/
    │   └── config.yaml
    └── task/
        └── config.yaml          # （他 DB も同様）
```

---

## 注意事項

- 既存データは上書きしない（空欄のみ補完）
- `data/` 以下の `raw.md` / `completed.md` は git 管理外（`.gitignore` 済み）
- `.env` は絶対に git にコミットしない
