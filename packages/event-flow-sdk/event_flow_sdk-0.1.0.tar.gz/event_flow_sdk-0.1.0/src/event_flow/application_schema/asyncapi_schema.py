from typing import Any, TypedDict

from .channel_schema import ChannelSchema
from .info_schema import InfoSchema
from .operation_schema import OperationSchema


class AsyncAPISchema(TypedDict, total=False):
    asyncapi: str
    info: InfoSchema
    channels: dict[str, ChannelSchema]
    operations: dict[str, OperationSchema]
    components: dict[str, Any]
