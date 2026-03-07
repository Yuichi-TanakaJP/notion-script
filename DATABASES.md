# Notion DB 一覧

インテグレーションがアクセスできる DB と補完対象フィールドの一覧。
最終更新: 2026-03-07

---

## Animal

| 項目 | 値 |
|------|-----|
| フォルダ | `scripts/animal/` |
| DB ID | `220cae2d-86b8-80bb-b653-c296839567b1` |
| URL | https://www.notion.so/220cae2d86b880bbb653c296839567b1 |

### 補完対象フィールド

| フィールド名 | 型 |
|------------|-----|
| 種類 | `select` |

```bash
python scripts/fetch.py --config scripts/animal/config.yaml
python scripts/update.py --config scripts/animal/config.yaml --dry-run
```

---

## Life Todo

| 項目 | 値 |
|------|-----|
| フォルダ | `scripts/life_todo/` |
| DB ID | `226cae2d-86b8-80a4-a94d-c7f2071bf5a9` |
| URL | https://www.notion.so/226cae2d86b880a4a94dc7f2071bf5a9 |

### 補完対象フィールド

| フィールド名 | 型 |
|------------|-----|
| 重要度 | `select` |
| タグ | `multi_select` |
| 進捗めも | `rich_text` |
| カテゴリー | `select` |
| ステータス | `select` |

```bash
python scripts/fetch.py --config scripts/life_todo/config.yaml
python scripts/update.py --config scripts/life_todo/config.yaml --dry-run
```

---

## めも

| 項目 | 値 |
|------|-----|
| フォルダ | `scripts/memo_db/` |
| DB ID | `226cae2d-86b8-80f8-801c-f207af0c7387` |
| URL | https://www.notion.so/226cae2d86b880f8801cf207af0c7387 |

### 補完対象フィールド

| フィールド名 | 型 |
|------------|-----|
| ステータス | `select` |
| カテゴリー | `select` |
| タグ | `multi_select` |
| 重要度 | `select` |
| メモ | `rich_text` |

```bash
python scripts/fetch.py --config scripts/memo_db/config.yaml
python scripts/update.py --config scripts/memo_db/config.yaml --dry-run
```

---

## Source LOG

| 項目 | 値 |
|------|-----|
| フォルダ | `scripts/source_log/` |
| DB ID | `220cae2d-86b8-8028-aee2-d3f8fb3fadb5` |
| URL | https://www.notion.so/220cae2d86b88028aee2d3f8fb3fadb5 |

### 補完対象フィールド

| フィールド名 | 型 |
|------------|-----|
| 1行要約 | `rich_text` |

```bash
python scripts/fetch.py --config scripts/source_log/config.yaml
python scripts/update.py --config scripts/source_log/config.yaml --dry-run
```

---

## Task

| 項目 | 値 |
|------|-----|
| フォルダ | `scripts/task/` |
| DB ID | `21acae2d-86b8-81a6-9afb-cb0b42098991` |
| URL | https://www.notion.so/21acae2d86b881a69afbcb0b42098991 |

### 補完対象フィールド

| フィールド名 | 型 |
|------------|-----|
| タグ | `multi_select` |
| 重要度 | `select` |
| カテゴリー | `select` |
| ステータス | `select` |
| 進捗めも | `rich_text` |

```bash
python scripts/fetch.py --config scripts/task/config.yaml
python scripts/update.py --config scripts/task/config.yaml --dry-run
```

---

## タスクリスト

| 項目 | 値 |
|------|-----|
| フォルダ | `scripts/task_list/` |
| DB ID | `221cae2d-86b8-808c-bf67-fb78a361463a` |
| URL | https://www.notion.so/221cae2d86b8808cbf67fb78a361463a |

### 補完対象フィールド

| フィールド名 | 型 |
|------------|-----|
| 選択 | `select` |

```bash
python scripts/fetch.py --config scripts/task_list/config.yaml
python scripts/update.py --config scripts/task_list/config.yaml --dry-run
```

---
