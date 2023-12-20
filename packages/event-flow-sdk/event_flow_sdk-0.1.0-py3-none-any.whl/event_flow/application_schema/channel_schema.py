from typing import TypedDict


class ChannelSchema(TypedDict, total=False):
    address: str
    messages: list[dict[str, str]]
    title: str
    summary: str
    description: str
