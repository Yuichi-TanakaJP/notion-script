import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

notion = Client(auth=os.environ["NOTION_TOKEN"])


def get_plain_text(rich_text_list: list) -> str | None:
    if not rich_text_list:
        return None
    return rich_text_list[0].get("plain_text") or None


def get_select_name(prop: dict) -> str | None:
    val = prop.get("select")
    return val["name"] if val else None


def get_multi_select_names(prop: dict) -> list[str]:
    return [item["name"] for item in prop.get("multi_select", [])]


def get_status_name(prop: dict) -> str | None:
    val = prop.get("status")
    return val["name"] if val else None
