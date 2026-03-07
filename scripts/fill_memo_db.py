import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lib.notion_helper import notion, get_select_name, get_multi_select_names, get_status_name, get_plain_text

# 補完データ
# 各エントリに含まれるキーのみ補完対象。既存値がある場合はスキップ。
ENTRIES = [
    {
        "page_id": "21bcae2d-86b8-8085-abf0-d6241afe7fca",
        "name": "メンバーシップ型雇用",
        "カテゴリー": "ビジネス",
        "タグ": ["ビジネス"],
        "ステータス": "理解済み",
        "メモ": "業務内容を限定せず人に仕事を合わせる日本型雇用システム",
    },
    {
        "page_id": "21bcae2d-86b8-8017-a2da-c53cc3364dc6",
        "name": "ジョブ型雇用",
        "カテゴリー": "ビジネス",
        "タグ": ["ビジネス"],
        "ステータス": "理解済み",
        "メモ": "業務内容・勤務地・労働時間を明確に定めた契約型雇用システム",
    },
    {
        "page_id": "21bcae2d-86b8-8019-9fac-caf03c8cba7c",
        "name": "成長マインドセット",
        "カテゴリー": "思考",
        "タグ": ["思考法"],
        "ステータス": "理解済み",
        "メモ": "能力は努力と学習で成長できるという信念",
    },
    {
        "page_id": "21bcae2d-86b8-80a0-add5-e2b0a399b4bf",
        "name": "硬直マインドセット",
        "カテゴリー": "思考",
        "タグ": ["思考法"],
        "ステータス": "理解済み",
        "メモ": "能力は固定されているという信念。成長マインドセットの対概念",
    },
    {
        "page_id": "21bcae2d-86b8-8022-81d6-c864dec566d8",
        "name": "ゼロベース思考",
        "カテゴリー": "思考",
        "タグ": ["思考法"],
        "ステータス": "理解済み",
        "メモ": "過去の前提を捨てゼロから最適解を考えるアプローチ",
    },
    {
        "page_id": "21bcae2d-86b8-8039-aac7-c7e20b1d9ab3",
        "name": "仮説思考",
        "カテゴリー": "思考",
        "タグ": ["思考法"],
        "ステータス": "理解済み",
        "メモ": "制約を超えて理想状態を想定しアクションプランを立てる思考法",
    },
    {
        "page_id": "21bcae2d-86b8-80fd-8c3c-d424b3ccd5b8",
        "name": "システマティック処理",
        "カテゴリー": "思考",
        "タグ": ["思考法"],
        "ステータス": "理解済み",
        "メモ": "計画的・体系的に情報を収集・整理・分析するアプローチ",
    },
    {
        "page_id": "21bcae2d-86b8-8009-b675-ed7969bb47ee",
        "name": "インベスタシンキング",
        "カテゴリー": "思考",
        "タグ": ["投資判断"],
        "ステータス": "理解済み",
        "メモ": "投資家視点で企業価値・リスクを見極める思考プロセス",
    },
    # タグ・ステータスのみ補完（メモあり）
    {
        "page_id": "21bcae2d-86b8-80f2-a556-ecc41d7c20b9",
        "name": "マインドマップ",
        "タグ": ["思考法"],
        "ステータス": "理解済み",
    },
    {
        "page_id": "21bcae2d-86b8-80c6-80f9-e8937b2ffb95",
        "name": "新しいことに挑戦するマインドのポイント",
        "タグ": ["思考法"],
        "ステータス": "理解済み",
    },
    {
        "page_id": "21bcae2d-86b8-8058-bb6d-e75d56337f1a",
        "name": "アナロジー思考",
        "タグ": ["思考法"],
        "ステータス": "理解済み",
    },
    {
        "page_id": "21bcae2d-86b8-80c0-99c8-e06aa070af79",
        "name": "デザイン思考",
        "タグ": ["思考法"],
        "ステータス": "理解済み",
    },
    {
        "page_id": "21bcae2d-86b8-8030-af36-e8a7038d3bfd",
        "name": "ゼロ秒思考",
        "タグ": ["思考法"],
        "ステータス": "理解済み",
    },
    # カテゴリー・タグ・ステータスのみ補完（メモあり）
    {
        "page_id": "21bcae2d-86b8-80b5-8d73-fb1f4c407a9f",
        "name": "人は聞き方が9割",
        "カテゴリー": "思考",
        "タグ": ["思考法"],
        "ステータス": "理解済み",
    },
    {
        "page_id": "21bcae2d-86b8-801d-a77a-fbe8c54dd614",
        "name": "アンカリング効果",
        "カテゴリー": "思考",
        "タグ": ["思考法"],
        "ステータス": "理解済み",
    },
    {
        "page_id": "229cae2d-86b8-8080-a1a0-f8e0c57c0281",
        "name": "先物受渡適格最割安",
        "カテゴリー": "投資・金融",
        "タグ": ["株式取引"],
        "ステータス": "理解済み",
    },
    {
        "page_id": "220cae2d-86b8-809a-89e7-ca9bf670a99f",
        "name": "AIがやるべき仕事",
        "カテゴリー": "技術・IT",
        "タグ": ["技術動向"],
        "ステータス": "理解済み",
    },
    {
        "page_id": "229cae2d-86b8-80f2-9478-fb9d7661b4e4",
        "name": "財政政策",
        "カテゴリー": "経済理論",
        "タグ": ["政策"],
        "ステータス": "理解済み",
    },
    {
        "page_id": "229cae2d-86b8-8042-a02a-e271e44ed548",
        "name": "アメリカの祝日",
        "カテゴリー": "個人タスク",
        "タグ": ["国際投資"],
        "ステータス": "理解済み",
        "メモ": "米国株式市場の休場日確認用",
    },
    {
        "page_id": "229cae2d-86b8-8042-a5ea-ef4707d53011",
        "name": "中国の祝日",
        "カテゴリー": "個人タスク",
        "タグ": ["国際投資"],
        "ステータス": "理解済み",
        "メモ": "中国株式市場の休場日確認用",
    },
    {
        "page_id": "21ccae2d-86b8-8036-ae87-e54a9882e43d",
        "name": "AWS",
        "カテゴリー": "技術・IT",
        "タグ": ["技術"],
        "ステータス": "要調査",
        "メモ": "Amazonのクラウドサービス。内容未記入のため要調査",
    },
]


def get_existing_props(page_id: str) -> dict:
    page = notion.pages.retrieve(page_id=page_id)
    props = page["properties"]

    cat_prop = props.get("カテゴリー", {})
    tag_prop = props.get("タグ", {})
    status_prop = props.get("ステータス", {})
    memo_prop = props.get("メモ", {})

    return {
        "カテゴリー": get_select_name(cat_prop),
        "タグ": get_multi_select_names(tag_prop),
        "ステータス": get_status_name(status_prop),
        "メモ": get_plain_text(memo_prop.get("rich_text", [])),
    }


def build_update_payload(entry: dict, existing: dict) -> dict:
    props = {}

    if "カテゴリー" in entry and not existing["カテゴリー"]:
        props["カテゴリー"] = {"select": {"name": entry["カテゴリー"]}}

    if "タグ" in entry and not existing["タグ"]:
        props["タグ"] = {"multi_select": [{"name": t} for t in entry["タグ"]]}

    if "ステータス" in entry and not existing["ステータス"]:
        props["ステータス"] = {"status": {"name": entry["ステータス"]}}

    if "メモ" in entry and not existing["メモ"]:
        props["メモ"] = {
            "rich_text": [{"type": "text", "text": {"content": entry["メモ"]}}]
        }

    return props


def main():
    print(f"処理対象: {len(ENTRIES)} 件\n")

    success = 0
    skipped = 0
    failed = 0

    for entry in ENTRIES:
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
