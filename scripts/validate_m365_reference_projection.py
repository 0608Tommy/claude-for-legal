#!/usr/bin/env python3
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""Run the strict Microsoft 365 reference projection validator."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import TYPE_CHECKING, cast

from m365_reference_projection import (
    DEFAULT_CONTRACT_PATH,
    DEFAULT_PACKAGE_ROOT,
    load_contract,
    validate_projection,
)
from m365_reference_projection_types import ProjectionError

if TYPE_CHECKING:
    from collections.abc import Sequence


def _parse_arguments(argv: Sequence[str] | None) -> tuple[Path, Path]:
    """Parse the read-only check-mode CLI."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        required=True,
        help="validate without changing files",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_PACKAGE_ROOT,
        help="Cowork package root",
    )
    parser.add_argument(
        "--contract",
        type=Path,
        default=DEFAULT_CONTRACT_PATH,
        help="projection contract JSON",
    )
    arguments = parser.parse_args(argv)
    return cast("Path", arguments.root), cast("Path", arguments.contract)


def main(argv: Sequence[str] | None = None) -> int:
    """Run strict read-only projection validation."""
    package_root, contract_path = _parse_arguments(argv)
    try:
        contract = load_contract(contract_path)
        report = validate_projection(package_root, contract)
    except (OSError, ProjectionError) as validation_exception:
        sys.stderr.write(f"ERROR: {validation_exception}\n")
        return 1
    if report.errors:
        for reported_error in report.errors:
            sys.stderr.write(f"ERROR: {reported_error}\n")
        return 1
    totals = report.observed_totals
    sys.stdout.write(
        "Microsoft 365 reference projection: OK "
        f"({totals.package_count} packages, "
        f"{totals.registered_skill_count} skills, "
        f"{totals.projected_file_count} projected files)\n",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
