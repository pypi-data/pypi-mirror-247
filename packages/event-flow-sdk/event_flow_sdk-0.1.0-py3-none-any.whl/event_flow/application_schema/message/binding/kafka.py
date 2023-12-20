from typing import Any, Literal, TypedDict

from ..utils import export


@export
class KafkaMessageBinding(TypedDict):
    """
    This object contains information about the message representation in Kafka.

    Attributes:
        key: The message key.
        schema_id_location: If a Schema Registry is used when performing this operation, tells where the id of schema
        is stored (e.g. header or payload).
        schema_id_payload_encoding: Number of bytes or vendor specific values when schema id is encoded in payload
        (e.g confluent/ apicurio-legacy / apicurio-new).
        schema_lookup_strategy: Freeform string for any naming strategy class to use. Clients should default to the
        vendor default if not supplied.
        binding_version: The version of this binding. If omitted, "latest" MUST be assumed.

    Examples:
        {
            "key": {
                "type": "string",
                "enum": [
                    "myKey"
                ]
            },
            "schemaIdLocation": "payload",
            "schemaIdPayloadEncoding": "apicurio-new",
            "schemaLookupStrategy": "TopicIdStrategy",
            "bindingVersion": "0.3.0"
        },
        {
            "key": {
                "$ref": "path/to/user-create.avsc#/UserCreate"
            },
            "schemaIdLocation": "payload",
            "schemaIdPayloadEncoding": "4",
            "bindingVersion": "0.3.0"
        }
    """

    key: dict[str, Any]
    schemaIdLocation: Literal["header", "payload"]
    schemaIdPayloadEncoding: Literal["confluent", "apicurio-legacy", "apicurio-new"]
    schemaLookupStrategy: str
    bindingVersion: str
