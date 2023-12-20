from typing import TypedDict

from typing_extensions import NotRequired

from ..utils import export


@export
class Tag(TypedDict):
    """
    Allows adding meta data to a single tag.

    Attributes:
        name: The name of the tag.
        description: A short description for the tag. CommonMark syntax can
        be used for rich text representation.
    """

    name: str
    description: NotRequired[str]
