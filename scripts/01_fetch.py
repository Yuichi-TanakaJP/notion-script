"""
Step 1: Notion DB から全データを取得して data/raw.md に保存する
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import datetime
from lib.notion_helper import (
    notion,
    get_select_name,
    get_multi_select_names,
    get_status_name,
    get_plain_text,
)

DB_ID = "226cae2d-86b8-80f8-801c-f207af0c7387"
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "raw.md")


def get_title(props: dict) -> str:
    for val in props.values():
        if val.get("type") == "title":
            texts = val.get("title", [])
            return texts[0]["plain_text"] if texts else "(無題)"
    return "(無題)"


def fetch_all_pages() -> list:
    pages = []
    cursor = None
    while True:
        kwargs = {"database_id": DB_ID, "page_size": 100}
        if cursor:
            kwargs["start_cursor"] = cursor
        res = notion.databases.query(**kwargs)
        pages.extend(res["results"])
        if not res.get("has_more"):
            break
        cursor = res["next_cursor"]
    return pages


def fmt(val) -> str:
    if val is None or val == [] or val == "":
        return "[空欄]"
    if isinstance(val, list):
        return ", ".join(val) if val else "[空欄]"
    return str(val)


def main():
    print("Notionからデータを取得中...")
    pages = fetch_all_pages()
    print(f"{len(pages)} 件取得")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    blank_pages = []
    for page in pages:
        props = page["properties"]
        page_id = page["id"]
        title = get_title(props)

        cat = get_select_name(props.get("カテゴリー", {}))
        tags = get_multi_select_names(props.get("タグ", {}))

        status_prop = props.get("ステータス", {})
        if status_prop.get("type") == "status":
            status = get_status_name(status_prop)
        else:
            status = get_select_name(status_prop)

        memo = get_plain_text(props.get("メモ", {}).get("rich_text", []))

        # 空欄フィールドが1つ以上ある場合のみ対象
        has_blank = any(v is None or v == [] or v == "" for v in [cat, tags, status, memo])
        if has_blank:
            blank_pages.append((page_id, title, cat, tags, status, memo))

    lines = [
        "# めも DB - 空欄補完対象データ",
        f"取得日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"総件数: {len(pages)} 件中 {len(blank_pages)} 件が補完対象",
        "",
    ]

    for page_id, title, cat, tags, status, memo in blank_pages:
        lines += [
            "---",
            "",
            f"## {title}",
            f"- page_id: {page_id}",
            f"- カテゴリー: {fmt(cat)}",
            f"- タグ: {fmt(tags)}",
            f"- ステータス: {fmt(status)}",
            f"- メモ: {fmt(memo)}",
            "",
        ]

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"保存完了: {OUTPUT_PATH} ({len(blank_pages)} 件)")


if __name__ == "__main__":
    main()
