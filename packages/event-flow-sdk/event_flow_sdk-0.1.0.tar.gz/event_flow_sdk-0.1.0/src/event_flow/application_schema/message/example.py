from typing import Any, TypedDict

from ..utils import export


@export
class MessageExample(TypedDict):
    """
    Message Example Object represents an example of a Message and MUST
    contain either headers and/or payload fields.

    Attributes:
        headers: The value of this field MUST validate against the Message's headers field.
        payload: The value of this field MUST validate against the Message's payload field.
        name: A machine-friendly name.
        summary: A short summary of what the example is about.
    """

    headers: dict[str, Any]
    payload: dict[str, Any]
    name: str
    summary: str
