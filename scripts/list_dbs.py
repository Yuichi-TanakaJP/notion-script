"""
インテグレーションがアクセスできる Notion DB の一覧を表示する

使い方:
  python scripts/list_dbs.py
"""
import sys
import os

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.notion_helper import notion


def get_plain_title(title_list: list) -> str:
    return "".join(t.get("plain_text", "") for t in title_list) or "(無題)"


def main():
    results = []
    cursor = None

    while True:
        kwargs = {"filter": {"property": "object", "value": "database"}, "page_size": 100}
        if cursor:
            kwargs["start_cursor"] = cursor
        res = notion.search(**kwargs)
        results.extend(res["results"])
        if not res.get("has_more"):
            break
        cursor = res["next_cursor"]

    if not results:
        print("アクセス可能なDBが見つかりません。")
        print("Notion のインテグレーション設定でDBを共有してください。")
        return

    print(f"アクセス可能な DB: {len(results)} 件\n")
    for db in results:
        name = get_plain_title(db.get("title", []))
        db_id = db["id"]
        url = db.get("url", "")
        print(f"  {name}")
        print(f"    db_id: {db_id}")
        print(f"    url  : {url}")
        print()


if __name__ == "__main__":
    main()
