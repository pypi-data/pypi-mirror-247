from typing import TypedDict

from typing_extensions import NotRequired

from ..tag import Tag
from ..utils import export
from .binding import MessageBinding, ProtocolName
from .example import MessageExample
from .trait import MessageTrait


@export
class MessageMeta(TypedDict):
    correlationId: NotRequired[str]
    contentType: NotRequired[str]
    name: NotRequired[str]
    title: NotRequired[str]
    summary: NotRequired[str]
    description: NotRequired[str]
    tags: NotRequired[list[Tag]]
    bindings: NotRequired[dict[ProtocolName, MessageBinding]]
    examples: NotRequired[list[MessageExample]]
    traits: NotRequired[list[MessageTrait]]
