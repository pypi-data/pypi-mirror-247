from ..utils import export


@export
class Reference:
    """
    A simple object to allow referencing other components in the app,
    internally and externally.
    """

    def __init__(self, reference: str) -> None:
        self._reference = reference

    def __call__(self) -> dict[str, str]:
        return {"$ref": self._reference}
