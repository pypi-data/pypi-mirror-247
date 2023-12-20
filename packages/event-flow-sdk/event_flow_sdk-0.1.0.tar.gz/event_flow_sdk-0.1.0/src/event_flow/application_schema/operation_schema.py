from typing import TypedDict


class OperationSchema(TypedDict, total=False):
    action: str
    channel: dict[str, str]
    title: str
    summary: str
    description: str
    messages: list[dict[str, str]]
