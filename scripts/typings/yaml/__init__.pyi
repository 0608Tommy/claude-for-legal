# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0

import re
from collections.abc import Callable

class YAMLError(Exception):
    ...


class MappingNode:
    value: list[tuple[object, object]]


class BaseLoader:
    def __init__(self, stream: str) -> None: ...

    def construct_object(
        self,
        node: object,
        deep: bool = False,
    ) -> object: ...

    def construct_mapping(
        self,
        node: MappingNode,
        deep: bool = False,
    ) -> dict[object, object]: ...

    def get_single_data(self) -> object: ...

    def dispose(self) -> None: ...

    @classmethod
    def add_constructor(
        cls,
        tag: str,
        constructor: Callable[[BaseLoader, MappingNode], object],
    ) -> None: ...


class SafeLoader(BaseLoader):
    yaml_implicit_resolvers: dict[
        str | None,
        list[tuple[str, re.Pattern[str]]],
    ]

    @classmethod
    def add_implicit_resolver(
        cls,
        tag: str,
        regexp: re.Pattern[str],
        first: list[str] | None,
    ) -> None: ...


class TagToken:
    ...


def scan(stream: str, Loader: type[BaseLoader]) -> list[object]: ...
