from collections.abc import Iterable

from .exceptions import ValidationError

class FormatChecker: ...

class Draft202012Validator:
    def __init__(
        self,
        schema: object,
        *,
        format_checker: FormatChecker | None = ...,
    ) -> None: ...

    @classmethod
    def check_schema(cls, schema: object) -> None: ...

    def iter_errors(self, instance: object) -> Iterable[ValidationError]: ...
