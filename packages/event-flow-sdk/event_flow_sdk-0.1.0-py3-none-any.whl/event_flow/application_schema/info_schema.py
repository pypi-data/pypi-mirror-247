from typing import TypedDict

from ..utils import export


@export
class InfoSchema(TypedDict, total=False):
    title: str
    version: str
    description: str
