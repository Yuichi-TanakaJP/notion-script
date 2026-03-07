# notion-script

Notion DB の空欄フィールドを AI 補完するスクリプト集。

---

## 対象 DB

| DB名 | DB ID | URL |
|------|-------|-----|
| めも | `226cae2d-86b8-80f8-801c-f207af0c7387` | https://www.notion.so/226cae2d86b880f8801cf207af0c7387 |

補完対象フィールド: `カテゴリー`（select）、`タグ`（multi_select）、`ステータス`（select）、`メモ`（rich_text）

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
.venv/Scripts/python scripts/01_fetch.py
```

- Notion DB から全ページを取得
- 空欄フィールドがあるエントリのみ `data/raw.md` に保存

### Step 2: AI 補完（Claude Code 上で手動実行）

`data/raw.md` の内容を Claude Code に渡して `data/completed.md` を生成してもらう。

プロンプト例：
```
raw.md を読んで、空欄フィールドを補完した completed.md を生成してください。
```

### Step 3: Notion 更新

```bash
# 動作確認（Notion には書き込まない）
.venv/Scripts/python scripts/03_update.py --dry-run --limit 5

# 本番実行
.venv/Scripts/python scripts/03_update.py
```

オプション:

| オプション | 説明 |
|-----------|------|
| `--dry-run` | 更新内容を表示するだけ（Notion には書き込まない） |
| `--limit N` | 最初の N 件だけ処理 |

---

## ファイル構成

```
notion-script/
├── .env                    # Notion トークン（git 管理外）
├── .env.example            # トークンのキー名テンプレート
├── requirements.txt        # 依存ライブラリ
├── data/
│   ├── raw.md             # Step1 の出力（git 管理外）
│   └── completed.md       # Step2 の出力（git 管理外）
├── lib/
│   └── notion_helper.py   # 共通クライアント・ユーティリティ
└── scripts/
    ├── 01_fetch.py        # Step1: Notion → raw.md
    └── 03_update.py       # Step3: completed.md → Notion
```

---

## 注意事項

- 既存データは上書きしない（空欄のみ補完）
- `data/raw.md` と `data/completed.md` は git 管理外（`.gitignore` 済み）
- `.env` は絶対に git にコミットしない
