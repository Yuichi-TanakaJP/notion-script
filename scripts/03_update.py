"""
Step 3: data/completed.md を読み込んで Notion DB を更新する
空欄フィールドのみ更新（既存データは上書きしない）
"""
import sys
import os
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lib.notion_helper import (
    notion,
    get_select_name,
    get_multi_select_names,
    get_status_name,
    get_plain_text,
)

INPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "completed.md")


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
    if status_prop.get("type") == "status":
        status = get_status_name(status_prop)
    else:
        status = get_select_name(status_prop)

    return {
        "カテゴリー": get_select_name(props.get("カテゴリー", {})),
        "タグ": get_multi_select_names(props.get("タグ", {})),
        "ステータス": status,
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
        props["ステータス"] = {"status": {"name": entry["ステータス"]}}

    if "メモ" in entry and not existing["メモ"]:
        props["メモ"] = {
            "rich_text": [{"type": "text", "text": {"content": entry["メモ"]}}]
        }

    return props


def main():
    if not os.path.exists(INPUT_PATH):
        print(f"エラー: {INPUT_PATH} が見つかりません。先に02_analyze（AI補完）を実施してください。")
        return

    entries = parse_completed_md(INPUT_PATH)
    print(f"処理対象: {len(entries)} 件\n")

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
                print(f"[SKIP]    {name} — 全フィールド補完済み")
                skipped += 1
                continue

            notion.pages.update(page_id=page_id, properties=payload)
            updated_keys = ", ".join(payload.keys())
            print(f"[OK]      {name} — 更新: {updated_keys}")
            success += 1

        except Exception as e:
            print(f"[ERROR]   {name} ({page_id}) — {e}")
            failed += 1

    print(f"\n完了: 成功={success}, スキップ={skipped}, 失敗={failed}")


if __name__ == "__main__":
    main()
