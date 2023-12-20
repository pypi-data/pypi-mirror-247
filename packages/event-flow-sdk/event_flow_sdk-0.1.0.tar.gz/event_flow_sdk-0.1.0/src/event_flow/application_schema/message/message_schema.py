from typing import Any, TypedDict


class MessageSchema(TypedDict, total=False):
    messageId: str
    name: str
    title: str
    summary: str
    description: str
    headers: dict[str, Any]
    payload: dict[str, Any]
