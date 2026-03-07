"""
汎用 Notion DB フェッチスクリプト
config.yaml で対象 DB・フィールドを指定して使用する

使い方:
  python scripts/fetch.py --config scripts/memo_db/config.yaml

出力先: data/<config のフォルダ名>/raw.md
"""
import sys
import os
import yaml
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from lib.notion_helper import (
    notion,
    get_select_name,
    get_multi_select_names,
    get_status_name,
    get_plain_text,
)


def get_title(props: dict) -> str:
    for val in props.values():
        if val.get("type") == "title":
            texts = val.get("title", [])
            return texts[0]["plain_text"] if texts else "(無題)"
    return "(無題)"


def fetch_all_pages(db_id: str) -> list:
    pages = []
    cursor = None
    while True:
        kwargs = {"database_id": db_id, "page_size": 100}
        if cursor:
            kwargs["start_cursor"] = cursor
        res = notion.databases.query(**kwargs)
        pages.extend(res["results"])
        if not res.get("has_more"):
            break
        cursor = res["next_cursor"]
    return pages


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


def fmt(val) -> str:
    if val is None or val == [] or val == "":
        return "[空欄]"
    if isinstance(val, list):
        return ", ".join(val) if val else "[空欄]"
    return str(val)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="config.yaml のパス")
    args = parser.parse_args()

    with open(args.config, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    db_name = config["db_name"]
    db_id = config["db_id"]
    fields = config["fields"]  # [{"name": "...", "type": "..."}]

    # 出力先: data/<configのフォルダ名>/raw.md
    config_dir_name = os.path.basename(os.path.dirname(os.path.abspath(args.config)))
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(root, "data", config_dir_name, "raw.md")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print(f"{db_name} からデータを取得中...")
    pages = fetch_all_pages(db_id)
    print(f"{len(pages)} 件取得")

    blank_pages = []
    for page in pages:
        props = page["properties"]
        page_id = page["id"]
        title = get_title(props)

        values = {
            f["name"]: get_field_value(props.get(f["name"], {}), f["type"])
            for f in fields
        }

        if any(v is None or v == [] or v == "" for v in values.values()):
            blank_pages.append((page_id, title, values))

    lines = [
        f"# {db_name} - 空欄補完対象データ",
        f"取得日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"総件数: {len(pages)} 件中 {len(blank_pages)} 件が補完対象",
        "",
    ]

    for page_id, title, values in blank_pages:
        lines += ["---", "", f"## {title}", f"- page_id: {page_id}"]
        for fname, val in values.items():
            lines.append(f"- {fname}: {fmt(val)}")
        lines.append("")

    lines += ["---", "", f"取得完了: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"保存完了: {output_path} ({len(blank_pages)} 件)")


if __name__ == "__main__":
    main()
