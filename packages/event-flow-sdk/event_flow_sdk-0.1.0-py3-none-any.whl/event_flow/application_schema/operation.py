from typing import Any

from ..utils import export
from .action_type import ActionType
from .message import Message
from .operation_schema import OperationSchema
from .reference import Reference


@export
class Operation:
    """
    Describes a specific operation.

    Attributes:
        operation_id: The operation this application MUST implement.
        action: Use send when it's expected that the application will send a
        message to the given channel, and receive when the application should
        expect receiving messages from the given channel.
        channel: A pointer to the definition of the channel in which this
        operation is performed.
        title: A human-friendly title for the operation.
        summary: A short summary of what the operation is about.
        description: A verbose explanation of the operation. CommonMark syntax
        can be used for rich text representation.
        messages: A list of pointers pointing to the supported Message that
        can be processed by this operation.
    """

    def __init__(
        self,
        *,
        operation_id: str,
        action: ActionType,
        channel: Reference,
        title: str | None,
        summary: str | None,
        description: str | None,
    ) -> None:
        self.operation_id = operation_id
        self.action = action
        self.channel = channel
        self.title = title
        self.summary = summary
        self.description = description

        self.messages: list[Reference] = []

    @property
    def reference(self) -> Reference:
        return Reference(f"#/components/operations/{self.operation_id}")

    def __str__(self) -> str:
        return f"'<Operation> operation_id: {self.operation_id}'"

    def __repr__(self) -> str:
        return f"'<Operation> operation_id: {self.operation_id}'"

    @classmethod
    def with_message(
        cls,
        *,
        action: ActionType,
        channel: Reference,
        message: Message,
        title: str | None,
        summary: str | None,
        description: str | None,
    ) -> "Operation":
        operation = cls(
            operation_id=f"on{message.message_id}",
            action=action,
            channel=channel,
            title=title,
            summary=summary,
            description=description,
        )
        operation.add_message(message)
        return operation

    def add_message(self, message: Message) -> None:
        self.messages.append(message.reference)

    def to_schema(self) -> dict[str, Any]:
        schema = OperationSchema(
            action=self.action.value,
            channel=self.channel(),
            messages=[message() for message in self.messages],
        )
        return schema
