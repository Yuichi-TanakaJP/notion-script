"""
汎用 Notion DB 更新スクリプト
config.yaml で対象 DB・フィールドを指定して使用する

使い方:
  python scripts/update.py --config scripts/memo_db/config.yaml
  python scripts/update.py --config scripts/memo_db/config.yaml --dry-run
  python scripts/update.py --config scripts/memo_db/config.yaml --dry-run --limit 5

入力元: data/<config のフォルダ名>/completed.md
"""
import sys
import os
import re
import yaml
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.notion_helper import (
    notion,
    get_select_name,
    get_multi_select_names,
    get_status_name,
    get_plain_text,
)


def parse_completed_md(path: str, fields: list) -> list:
    with open(path, encoding="utf-8") as f:
        content = f.read()

    field_names = [f["name"] for f in fields]
    entries = []

    for block in content.split("---"):
        title_m = re.search(r"^## (.+)$", block, re.MULTILINE)
        page_id_m = re.search(r"- page_id: (.+)$", block, re.MULTILINE)
        if not title_m or not page_id_m:
            continue

        entry = {
            "name": title_m.group(1).strip(),
            "page_id": page_id_m.group(1).strip(),
        }

        for fname in field_names:
            m = re.search(rf"- {re.escape(fname)}: (.+)$", block, re.MULTILINE)
            if m:
                val = m.group(1).strip()
                if val and val != "[空欄]":
                    entry[fname] = val

        entries.append(entry)

    return entries


def get_field_value(prop: dict, field_type: str):
    if field_type == "select":
        return get_select_name(prop)
    elif field_type == "multi_select":
        return get_multi_select_names(prop)
    elif field_type == "status":
        return get_status_name(prop)
    elif field_type == "rich_text":
        return get_plain_text(prop.get("rich_text", []))
    return None


def get_existing_props(page_id: str, fields: list) -> dict:
    page = notion.pages.retrieve(page_id=page_id)
    props = page["properties"]
    return {
        f["name"]: get_field_value(props.get(f["name"], {}), f["type"])
        for f in fields
    }


def build_update_payload(entry: dict, existing: dict, fields: list) -> dict:
    props = {}
    for field in fields:
        fname = field["name"]
        ftype = field["type"]
        if fname not in entry or existing.get(fname):
            continue
        val = entry[fname]
        if ftype == "select":
            props[fname] = {"select": {"name": val}}
        elif ftype == "multi_select":
            tags = [t.strip() for t in val.split(",")]
            props[fname] = {"multi_select": [{"name": t} for t in tags]}
        elif ftype == "status":
            props[fname] = {"status": {"name": val}}
        elif ftype == "rich_text":
            props[fname] = {"rich_text": [{"type": "text", "text": {"content": val}}]}
    return props


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="config.yaml のパス")
    parser.add_argument("--dry-run", action="store_true", help="Notionに書き込まず確認のみ")
    parser.add_argument("--limit", type=int, default=None, help="処理件数の上限")
    args = parser.parse_args()

    with open(args.config, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    fields = config["fields"]

    config_dir_name = os.path.basename(os.path.dirname(os.path.abspath(args.config)))
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(root, "data", config_dir_name, "completed.md")

    if not os.path.exists(input_path):
        print(f"エラー: {input_path} が見つかりません。先にAI補完を実施してください。")
        return

    entries = parse_completed_md(input_path, fields)
    if args.limit:
        entries = entries[: args.limit]

    mode = "[DRY-RUN] " if args.dry_run else ""
    print(f"{mode}処理対象: {len(entries)} 件\n")

    success = 0
    skipped = 0
    failed = 0

    for entry in entries:
        page_id = entry["page_id"]
        name = entry["name"]
        try:
            existing = get_existing_props(page_id, fields)
            payload = build_update_payload(entry, existing, fields)

            if not payload:
                print(f"[SKIP]    {name} -全フィールド補完済み")
                skipped += 1
                continue

            updated_keys = ", ".join(payload.keys())
            if args.dry_run:
                print(f"[DRY-RUN] {name} -更新予定: {updated_keys}")
            else:
                notion.pages.update(page_id=page_id, properties=payload)
                print(f"[OK]      {name} -更新: {updated_keys}")
            success += 1

        except Exception as e:
            print(f"[ERROR]   {name} ({page_id}) -{e}")
            failed += 1

    label = "ドライラン" if args.dry_run else "完了"
    print(f"\n{label}: 対象={success}, スキップ={skipped}, 失敗={failed}")

    if not args.dry_run and os.path.exists(input_path):
        from datetime import datetime
        footer = (
            f"\n---\n"
            f"\nNotion更新日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            f"\n結果: 成功={success}, スキップ={skipped}, 失敗={failed}"
        )
        with open(input_path, "a", encoding="utf-8") as f:
            f.write(footer)


if __name__ == "__main__":
    main()
