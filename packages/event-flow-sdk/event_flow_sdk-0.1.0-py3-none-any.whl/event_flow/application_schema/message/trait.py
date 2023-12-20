from typing import TypedDict

from typing_extensions import NotRequired

from ..tag import Tag
from ..utils import export
from .binding import MessageBinding, ProtocolName
from .example import MessageExample
from .header import Header


@export
class MessageTrait(TypedDict):
    """
    Describes a message received on a given channel and operation.

    Attributes:
        messageId: Unique string used to identify the message. The id MUST be
        unique among all messages described in the API. The messageId value is
        case-sensitive.
        headers: Schema definition of the application headers.
        correlationId: Definition of the correlation ID used for message
        tracing or matching.
        contentType: The content type to use when encoding/decoding a
        message's payload.
        name: A machine-friendly name for the message.
        title: A human-friendly title for the message.
        summary: A short summary of what the message is about.
        description: A verbose explanation of the message.
        tags: A list of tags for logical grouping and categorization of
        messages.
        bindings: A map where the keys describe the name of the protocol and
        the values describe protocol-specific definitions for the message.
        examples: List of examples.
    """

    messageId: NotRequired[str]
    headers: NotRequired[list[Header]]
    correlationId: NotRequired[str]
    contentType: NotRequired[str]
    name: NotRequired[str]
    title: NotRequired[str]
    summary: NotRequired[str]
    description: NotRequired[str]
    tags: NotRequired[list[Tag]]
    bindings: NotRequired[dict[ProtocolName, MessageBinding]]
    examples: NotRequired[list[MessageExample]]
