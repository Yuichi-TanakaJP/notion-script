"""
Step 3: data/completed.md を読み込んで Notion DB を更新する
空欄フィールドのみ更新（既存データは上書きしない）

使い方:
  python scripts/03_update.py               # 全件更新
  python scripts/03_update.py --dry-run     # 更新内容を確認するだけ（Notionには書き込まない）
  python scripts/03_update.py --limit 3     # 最初の3件だけ更新
  python scripts/03_update.py --dry-run --limit 3  # 最初の3件をドライラン
"""
import sys
import os
import re
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from lib.notion_helper import (
    notion,
    get_select_name,
    get_multi_select_names,
    get_status_name,
    get_plain_text,
)

INPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "completed.md")


def parse_completed_md(path: str) -> list:
    with open(path, encoding="utf-8") as f:
        content = f.read()

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

        for field in ["カテゴリー", "タグ", "ステータス", "メモ"]:
            m = re.search(rf"- {field}: (.+)$", block, re.MULTILINE)
            if m:
                val = m.group(1).strip()
                if val and val != "[空欄]":
                    entry[field] = val

        entries.append(entry)

    return entries


def get_existing_props(page_id: str) -> dict:
    page = notion.pages.retrieve(page_id=page_id)
    props = page["properties"]

    status_prop = props.get("ステータス", {})
    status_type = status_prop.get("type", "select")  # 実際のフィールド型を記録
    if status_type == "status":
        status = get_status_name(status_prop)
    else:
        status = get_select_name(status_prop)

    return {
        "カテゴリー": get_select_name(props.get("カテゴリー", {})),
        "タグ": get_multi_select_names(props.get("タグ", {})),
        "ステータス": status,
        "ステータス型": status_type,  # build_update_payload で使う
        "メモ": get_plain_text(props.get("メモ", {}).get("rich_text", [])),
    }


def build_update_payload(entry: dict, existing: dict) -> dict:
    props = {}

    if "カテゴリー" in entry and not existing["カテゴリー"]:
        props["カテゴリー"] = {"select": {"name": entry["カテゴリー"]}}

    if "タグ" in entry and not existing["タグ"]:
        tags = [t.strip() for t in entry["タグ"].split(",")]
        props["タグ"] = {"multi_select": [{"name": t} for t in tags]}

    if "ステータス" in entry and not existing["ステータス"]:
        status_type = existing.get("ステータス型", "select")
        props["ステータス"] = {status_type: {"name": entry["ステータス"]}}

    if "メモ" in entry and not existing["メモ"]:
        props["メモ"] = {
            "rich_text": [{"type": "text", "text": {"content": entry["メモ"]}}]
        }

    return props


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Notionに書き込まず確認のみ")
    parser.add_argument("--limit", type=int, default=None, help="処理件数の上限")
    args = parser.parse_args()

    if not os.path.exists(INPUT_PATH):
        print(f"エラー: {INPUT_PATH} が見つかりません。先にAI補完を実施してください。")
        return

    entries = parse_completed_md(INPUT_PATH)
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
            existing = get_existing_props(page_id)
            payload = build_update_payload(entry, existing)

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

    if not args.dry_run and os.path.exists(INPUT_PATH):
        from datetime import datetime
        footer = (
            f"\n---\n"
            f"\nNotion更新日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            f"\n結果: 成功={success}, スキップ={skipped}, 失敗={failed}"
        )
        with open(INPUT_PATH, "a", encoding="utf-8") as f:
            f.write(footer)


if __name__ == "__main__":
    main()
