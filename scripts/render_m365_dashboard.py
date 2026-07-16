#!/usr/bin/env python3
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""Render safe HTML, Markdown, and CSV legal dashboards."""

from __future__ import annotations

import csv
import html
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Final, NamedTuple, cast
from urllib.parse import urlparse

ALLOWED_SCHEMES: Final = frozenset({"http", "https", "mailto"})
FORMULA_PREFIXES: Final = ("=", "+", "-", "@")
SEVERITY_ORDER: Final = ("Blocking", "High", "Medium", "Low")
ITEM_COLUMN_INDEX: Final = 2
EXPECTED_ARGUMENT_COUNT: Final = 3


class Finding(NamedTuple):
    """One normalized dashboard row."""

    severity: str
    category: str
    item: str
    owner: str
    status: str
    date: str
    details: str
    url: str | None


class Dashboard(NamedTuple):
    """Normalized dashboard input."""

    title: str
    generated_at: str
    scope: str
    reviewer_note: str
    rows: tuple[Finding, ...]


def _require_object(value: object, context: str) -> dict[str, object]:
    """Require a JSON object.

    Parameters
    ----------
    value:
        Candidate JSON value.
    context:
        Human-readable location.

    Returns
    -------
    dict[str, object]
        Validated object.

    Raises
    ------
    TypeError
        If the value is not an object.

    """
    if not isinstance(value, dict):
        message = f"{context} must be an object"
        raise TypeError(message)
    return cast("dict[str, object]", value)


def _require_string(value: object, context: str) -> str:
    """Require a JSON string.

    Parameters
    ----------
    value:
        Candidate JSON value.
    context:
        Human-readable location.

    Returns
    -------
    str
        Validated string.

    Raises
    ------
    TypeError
        If the value is not a string.

    """
    if not isinstance(value, str):
        message = f"{context} must be a string"
        raise TypeError(message)
    return value


def _optional_string(value: object, context: str) -> str | None:
    """Require an optional JSON string.

    Parameters
    ----------
    value:
        Candidate JSON value.
    context:
        Human-readable location.

    Returns
    -------
    str | None
        Validated string or ``None``.

    Raises
    ------
    TypeError
        If the value is neither a string nor ``None``.

    """
    if value is None:
        return None
    return _require_string(value, context)


def _finding(value: object, index: int) -> Finding:
    """Normalize one finding row.

    Parameters
    ----------
    value:
        Candidate row.
    index:
        Row index for errors.

    Returns
    -------
    Finding
        Normalized finding.

    """
    row = _require_object(value, f"rows[{index}]")
    severity = _require_string(row.get("severity"), "severity")
    if severity not in SEVERITY_ORDER:
        message = f"rows[{index}].severity is invalid"
        raise ValueError(message)
    return Finding(
        severity=severity,
        category=_require_string(row.get("category"), "category"),
        item=_require_string(row.get("item"), "item"),
        owner=_require_string(row.get("owner"), "owner"),
        status=_require_string(row.get("status"), "status"),
        date=_require_string(row.get("date"), "date"),
        details=_require_string(row.get("details"), "details"),
        url=_optional_string(row.get("url"), "url"),
    )


def load_dashboard(path: Path) -> Dashboard:
    """Load and validate a dashboard input.

    Parameters
    ----------
    path:
        JSON input path.

    Returns
    -------
    Dashboard
        Normalized dashboard.

    Raises
    ------
    TypeError
        If rows are not an array.

    """
    raw: object = json.loads(path.read_text(encoding="utf-8"))
    document = _require_object(raw, "dashboard")
    raw_rows = document.get("rows")
    if not isinstance(raw_rows, list):
        message = "rows must be an array"
        raise TypeError(message)
    rows = tuple(_finding(row, index) for index, row in enumerate(raw_rows))
    return Dashboard(
        title=_require_string(document.get("title"), "title"),
        generated_at=_require_string(
            document.get("generatedAt"),
            "generatedAt",
        ),
        scope=_require_string(document.get("scope"), "scope"),
        reviewer_note=_require_string(
            document.get("reviewerNote"),
            "reviewerNote",
        ),
        rows=rows,
    )


def _safe_url(value: str | None) -> str | None:
    """Return a URL only when its scheme is allowed.

    Parameters
    ----------
    value:
        Candidate URL.

    Returns
    -------
    str | None
        Allowed URL or ``None``.

    """
    if value is None:
        return None
    parsed = urlparse(value)
    return value if parsed.scheme in ALLOWED_SCHEMES else None


def _csv_cell(value: str) -> str:
    """Neutralize spreadsheet formula prefixes.

    Parameters
    ----------
    value:
        Candidate cell text.

    Returns
    -------
    str
        Safe cell text.

    """
    return f"'{value}" if value.startswith(FORMULA_PREFIXES) else value


def _summary(dashboard: Dashboard) -> str:
    """Build the summary statistics line.

    Parameters
    ----------
    dashboard:
        Normalized dashboard.

    Returns
    -------
    str
        Summary line.

    """
    counts = Counter(row.severity for row in dashboard.rows)
    labels = {
        "Blocking": "🔴",
        "High": "🟠",
        "Medium": "🟡",
        "Low": "🟢",
    }
    parts = [
        f"{labels[severity]} {counts[severity]} {severity}"
        for severity in SEVERITY_ORDER
    ]
    return f"{len(dashboard.rows)}件: " + " · ".join(parts)


def _html_row(row: Finding) -> str:
    """Render one escaped HTML table row.

    Parameters
    ----------
    row:
        Finding to render.

    Returns
    -------
    str
        HTML row.

    """
    safe_url = _safe_url(row.url)
    item = html.escape(row.item, quote=True)
    if safe_url is not None:
        safe_href = html.escape(safe_url, quote=True)
        item = f'<a href="{safe_href}">{item}</a>'
    values = (
        row.severity,
        row.category,
        item,
        row.owner,
        row.status,
        row.date,
        row.details,
    )
    cells = []
    for index, value in enumerate(values):
        rendered = (
            value
            if index == ITEM_COLUMN_INDEX
            else html.escape(value, quote=True)
        )
        cells.append(f"<td>{rendered}</td>")
    return "<tr>" + "".join(cells) + "</tr>"


def render_html(dashboard: Dashboard) -> str:
    """Render a standalone HTML dashboard.

    Parameters
    ----------
    dashboard:
        Normalized dashboard.

    Returns
    -------
    str
        Complete HTML document.

    """
    rows = "\n".join(_html_row(row) for row in dashboard.rows)
    title = html.escape(dashboard.title, quote=True)
    metadata = html.escape(
        f"{dashboard.generated_at} · {dashboard.scope}",
        quote=True,
    )
    summary = html.escape(_summary(dashboard), quote=True)
    note = html.escape(dashboard.reviewer_note, quote=True)
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
body{{font-family:system-ui,sans-serif;margin:2rem;color:#1f2933}}
table{{border-collapse:collapse;width:100%}}
th,td{{border:1px solid #cbd5e1;padding:.5rem;text-align:left}}
th{{background:#e2e8f0;cursor:pointer}}
.summary{{font-weight:700;margin:1rem 0}}
.note{{background:#f8fafc;border-left:4px solid #2563eb;padding:1rem}}
</style>
</head>
<body>
<h1>{title}</h1>
<p>{metadata}</p>
<p class="summary">{summary}</p>
<div class="note"><strong>レビュー担当者向け注記:</strong> {note}</div>
<table id="findings">
<thead><tr>
<th>Severity</th><th>Category</th><th>Item</th><th>Owner</th>
<th>Status</th><th>Date</th><th>Details</th>
</tr></thead>
<tbody>
{rows}
</tbody>
</table>
<script>
document.querySelectorAll("th").forEach((header,index)=>{{
  header.addEventListener("click",()=>{{
    const body=document.querySelector("#findings tbody");
    const rows=Array.from(body.querySelectorAll("tr"));
    rows.sort((left,right)=>left.children[index].textContent.localeCompare(
      right.children[index].textContent,"ja"));
    rows.forEach(row=>body.appendChild(row));
  }});
}});
</script>
</body>
</html>
"""


def render_markdown(dashboard: Dashboard) -> str:
    """Render a Markdown dashboard.

    Parameters
    ----------
    dashboard:
        Normalized dashboard.

    Returns
    -------
    str
        Markdown text.

    """
    lines = [
        f"# {dashboard.title}",
        "",
        f"{dashboard.generated_at} · {dashboard.scope}",
        "",
        f"**{_summary(dashboard)}**",
        "",
        f"> **レビュー担当者向け注記:** {dashboard.reviewer_note}",
        "",
        "| Severity | Category | Item | Owner | Status | Date | Details |",
        "|---|---|---|---|---|---|---|",
    ]
    lines.extend(
        "| "
        + " | ".join(
            value.replace("|", "\\|").replace("\n", " ")
            for value in (
                row.severity,
                row.category,
                row.item,
                row.owner,
                row.status,
                row.date,
                row.details,
            )
        )
        + " |"
        for row in dashboard.rows
    )
    return "\n".join(lines) + "\n"


def write_csv(dashboard: Dashboard, path: Path) -> None:
    """Write an Excel-compatible safe CSV file.

    Parameters
    ----------
    dashboard:
        Normalized dashboard.
    path:
        Output path.

    """
    with path.open("w", encoding="utf-8-sig", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(
            (
                "Severity",
                "Category",
                "Item",
                "Owner",
                "Status",
                "Date",
                "Details",
                "URL",
            ),
        )
        for row in dashboard.rows:
            writer.writerow(
                tuple(
                    _csv_cell(value)
                    for value in (
                        row.severity,
                        row.category,
                        row.item,
                        row.owner,
                        row.status,
                        row.date,
                        row.details,
                        _safe_url(row.url) or "",
                    )
                ),
            )


def render_files(input_path: Path, output_directory: Path) -> None:
    """Render all implemented dashboard formats.

    Parameters
    ----------
    input_path:
        JSON input path.
    output_directory:
        Output directory.

    """
    dashboard = load_dashboard(input_path)
    output_directory.mkdir(parents=True, exist_ok=True)
    (output_directory / "dashboard.html").write_text(
        render_html(dashboard),
        encoding="utf-8",
    )
    (output_directory / "dashboard.md").write_text(
        render_markdown(dashboard),
        encoding="utf-8",
    )
    write_csv(dashboard, output_directory / "dashboard.csv")


def main() -> int:
    """Render files from command-line paths.

    Returns
    -------
    int
        Zero on success, two for invalid usage.

    """
    if len(sys.argv) != EXPECTED_ARGUMENT_COUNT:
        sys.stderr.write(
            "usage: render_m365_dashboard.py INPUT.json OUTPUT_DIRECTORY\n",
        )
        return 2
    render_files(Path(sys.argv[1]), Path(sys.argv[2]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
