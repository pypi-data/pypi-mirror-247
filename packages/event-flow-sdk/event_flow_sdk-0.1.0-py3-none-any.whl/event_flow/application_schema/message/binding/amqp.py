from typing import TypedDict

from ..utils import export


@export
class AMQPMessageBinding(TypedDict):
    """
    This object contains information about the message representation in AMQP.

    Attributes:
        contentEncoding: A MIME encoding for the message content.
        messageType: Application-specific message type.
        bindingVersion: The version of this binding. If omitted, "latest" MUST be assumed.

    Examples:
        {
            "contentEncoding": "gzip",
            "messageType": "user.signup",
            "bindingVersion": "0.2.0"
        }
    """

    contentEncoding: str
    messageType: str
    bindingVersion: str
