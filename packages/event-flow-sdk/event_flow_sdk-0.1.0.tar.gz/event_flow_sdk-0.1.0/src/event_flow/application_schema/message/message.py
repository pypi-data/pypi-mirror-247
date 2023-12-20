from typing import Any

from pydantic import BaseModel

from ..components import Components
from ..reference import Reference
from ..tag import Tag
from ..utils import export
from .event import Event
from .example import MessageExample
from .message_schema import MessageSchema


@export
class Message:
    """
    Describes a message received on a given channel and operation.

    Attributes:
        messageId: Unique string used to identify the message. The id MUST be
        unique among all messages described in the API. The messageId value is
        case-sensitive.
        headers: Schema definition of the application headers.
        payload: Definition of the message payload.
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
        traits: A list of traits to apply to the message object.
    """

    def __init__(
        self,
        message_id: str,
        headers: BaseModel,
        payload: BaseModel,
        content_type: str | None,
        name: str | None,
        title: str | None,
        summary: str | None,
        description: str | None,
        tags: list[Tag] | None,
        examples: list[MessageExample] | None,
    ) -> None:
        self.message_id = message_id
        self.headers = headers
        self.payload = payload
        self.content_type = content_type
        self.name = name
        self.title = title
        self.summary = summary
        self.description = description
        self.tags = tags
        self.examples = examples

        self.components = Components()

    @property
    def reference(self) -> Reference:
        return Reference(f"#/components/messages/{self.message_id}")

    def __str__(self) -> str:
        return f"'<Message> message_id: {self.message_id}'"

    def __repr__(self) -> str:
        return f"'<Message> message_id: {self.message_id}'"

    @classmethod
    def from_event(cls, event: Event) -> "Message":
        message_meta: dict[str, str] = event.message_meta
        return cls(
            message_id=event.name(),
            headers=event.headers(),
            payload=event.payload(),
            content_type=message_meta.get("contentType"),
            name=message_meta.get("name"),
            title=message_meta.get("title"),
            summary=message_meta.get("summary"),
            description=message_meta.get("description"),
            tags=message_meta.get("tags"),
            examples=message_meta.get("examples"),
        )

    def to_schema(self) -> dict[str, Any]:
        headers_schema = self.headers.model_json_schema(ref_template="#/components/schemas/{model}")
        payload_schema = self.payload.model_json_schema(ref_template="#/components/schemas/{model}")
        if "$defs" in headers_schema:
            self.components.add_schemas(headers_schema.pop("$defs"))

        if "$defs" in payload_schema:
            self.components.add_schemas(payload_schema.pop("$defs"))

        schema = MessageSchema(
            messageId=self.message_id,
            headers=headers_schema,
            payload=payload_schema,
        )

        if self.content_type:
            schema["contentType"] = self.content_type
        if self.name:
            schema["name"] = self.name
        if self.title:
            schema["title"] = self.title
        if self.summary:
            schema["summary"] = self.summary
        if self.description:
            schema["description"] = self.description
        if self.tags:
            schema["tags"] = self.tags
        if self.examples:
            schema["examples"] = self.examples
        return schema
