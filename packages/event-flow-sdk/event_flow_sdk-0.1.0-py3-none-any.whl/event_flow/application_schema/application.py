from typing import Any

from ..utils import export
from .asyncapi_schema import AsyncAPISchema
from .channel import Channel
from .components import Components
from .info_schema import InfoSchema


@export
class EventFlow:
    def __init__(
        self,
        *,
        channels: list[Channel] | None = None,
        title: str = "EventFlow",
        version: str = "0.1.0",
        description: str = "",
    ) -> None:
        self.asyncapi_version = "3.0.0"
        self.title = title
        self.version = version
        self.description = description

        self.channels = channels if channels else []
        self.components = Components()

    def add_channel(self, channel: Channel) -> None:
        self.channels.append(channel)
        self.components.add_channel(channel_id=channel.channel_id, channel=channel.to_schema())
        self.components.merge(channel.components)

    def asyncapi(self) -> dict[str, Any]:
        return AsyncAPISchema(
            asyncapi=self.asyncapi_version,
            info=InfoSchema(
                title=self.title,
                version=self.version,
                description=self.description,
            ),
            channels={channel.channel_id: channel.reference() for channel in self.channels},
            operations={
                operation.operation_id: operation.reference()
                for channel in self.channels
                for operation in channel.operations
            },
            components=self.components.to_schema(),
        )
