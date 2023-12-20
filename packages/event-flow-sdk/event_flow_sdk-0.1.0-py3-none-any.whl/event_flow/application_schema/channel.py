from typing import Any, Callable

from ..utils import export
from .action_type import ActionType
from .channel_schema import ChannelSchema
from .components import Components
from .message import Event, Message
from .operation import Operation
from .reference import Reference

MessageId = str


@export
class Channel:
    """
    Describes a shared communication channel.

    Attributes:
        channel_id: An identifier for the described channel. The channelId
        value is case-sensitive.
        address: String representation of this channel's address. The address
        is typically the "topic name", "routing key", "event type", or "path".
        messages: A map of the messages that will be sent to this channel by
        any application at any time.
        title: A human-friendly title for the channel.
        summary: A short summary of the channel.
        description: An optional description of this channel. CommonMark
        syntax can be used for rich text representation.
    """

    def __init__(
        self,
        *,
        channel_id: str,
        address: str | None = None,
        title: str | None = None,
        summary: str | None = None,
        description: str | None = None,
    ) -> None:
        self.channel_id = channel_id
        self.address = address if address is not None else "unknown"
        self.messages: dict[MessageId, Reference] = {}
        self.title = title
        self.summary = summary
        self.description = description

        self.operations: list[Operation] = []
        self.components = Components()

    @property
    def reference(self) -> Reference:
        return Reference(f"#/channels/{self.channel_id}")

    def send(
        self,
        *,
        title: str | None = None,
        summary: str | None = None,
        description: str | None = None,
    ) -> Callable[[Event], Event]:
        def decorator(event: Event) -> Event:
            self.add_operation(
                action=ActionType.SEND,
                message=self.add_message(event=event),
                title=title,
                summary=summary,
                description=description,
            )

            return event

        return decorator

    def receive(
        self,
        *,
        title: str | None = None,
        summary: str | None = None,
        description: str | None = None,
    ) -> Callable[[Event], Event]:
        def decorator(event: Event) -> Event:
            self.add_operation(
                action=ActionType.RECEIVE,
                message=self.add_message(event=event),
                title=title,
                summary=summary,
                description=description,
            )

            return event

        return decorator

    def add_message(self, event: Event) -> Message:
        message = Message.from_event(event)
        self.messages[message.message_id] = message.reference()
        self.components.add_message(message.message_id, message.to_schema())
        return message

    def add_operation(
        self,
        action: ActionType,
        message: Message,
        title: str | None,
        summary: str | None,
        description: str | None,
    ) -> None:
        operation = Operation.with_message(
            action=action,
            channel=self.reference,
            message=message,
            title=title,
            summary=summary,
            description=description,
        )
        self.operations.append(operation)
        self.components.add_operation(operation.operation_id, operation.to_schema())

    def to_schema(self) -> dict[str, Any]:
        schema = ChannelSchema(
            address=self.address,
            messages=self.messages,
        )
        return schema
