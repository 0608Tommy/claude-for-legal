"""Run and expose package-local regulatory fixture validators."""

from __future__ import annotations

import sys
from pathlib import Path

from .fixture_audits import (
    validate_authority,
    validate_public_comment_audit,
)
from .fixture_classification import validate_source
from .fixture_evidence import coverage_complete
from .fixture_operations import (
    cursor_should_advance,
    validate_scope,
    validate_setup_session,
)
from .fixture_records import validate_comment, validate_gap
from .fixture_runner import run_fixture_suite
from .fixture_types import load_json_object

__all__ = (
    "coverage_complete",
    "cursor_should_advance",
    "validate_authority",
    "validate_comment",
    "validate_gap",
    "validate_public_comment_audit",
    "validate_scope",
    "validate_setup_session",
    "validate_source",
)


def main() -> int:
    """Run every fixture and write deterministic named outcomes.

    Returns
    -------
    int
        Zero after every fixture produces its expected result.

    """
    fixture_path = Path(__file__).with_name(
        "regulatory-contract-fixtures.json",
    )
    result = run_fixture_suite(load_json_object(fixture_path))
    lines = [
        *(
            f"direct mutation: {item.name} -> {item.result}"
            for item in result.direct_outcomes
        ),
        f"regulatory contract fixtures: OK ({result.case_count} cases)",
    ]
    sys.stdout.write("\n".join(lines))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
