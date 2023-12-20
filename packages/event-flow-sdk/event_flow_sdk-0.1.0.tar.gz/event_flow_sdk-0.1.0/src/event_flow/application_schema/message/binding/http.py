from typing import Any, TypedDict

from ..utils import export


@export
class HTTPMessageBinding(TypedDict):
    """
    This object contains information about the message representation in HTTP.

    Attributes:
        headers: A Schema object containing the definitions for HTTP-specific
        headers. This schema MUST be of type object and have a properties key.
        bindingVersion: The version of this binding. If omitted, "latest"
        MUST be assumed.

    Examples:
        {
            "headers": {
                "type": "object",
                "properties": {
                    "Content-Type": {
                        "type": "string",
                        "enum": [
                            "application/json"
                        ]
                    }
                }
            },
            "bindingVersion": "0.1.0"
        }
    """

    headers: dict[str, Any]
    bindingVersion: str
