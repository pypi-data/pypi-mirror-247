from typing import Literal

from .amqp import *
from .http import *
from .kafka import *

__all__ = amqp.__all__ + http.__all__ + kafka.__all__

ProtocolName = Literal["http", "amqp", "kafka"]
MessageBinding = AMQPMessageBinding | HTTPMessageBinding | KafkaMessageBinding
