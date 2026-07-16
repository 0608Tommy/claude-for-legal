#!/usr/bin/env bash
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUTPUT="$ROOT/m365-cowork-ja/.cache/artifact-test"
FIXTURE="$ROOT/m365-cowork-ja/artifacts/fixtures/sample-findings.json"

rm -rf "$OUTPUT"
python3 "$ROOT/scripts/render_m365_dashboard.py" "$FIXTURE" "$OUTPUT"

grep -Fq '&lt;script&gt;alert' "$OUTPUT/dashboard.html"
if grep -Fq "<script>alert('unsafe')</script>" "$OUTPUT/dashboard.html"; then
  echo "raw untrusted HTML was emitted" >&2
  exit 1
fi
if grep -Fq 'javascript:alert' "$OUTPUT/dashboard.html"; then
  echo "unsafe URL scheme was emitted" >&2
  exit 1
fi
grep -Fq "'=HYPERLINK" "$OUTPUT/dashboard.csv"
grep -Fq "'@external-value" "$OUTPUT/dashboard.csv"
grep -Fq 'https://example.invalid/review' "$OUTPUT/dashboard.html"
grep -Fq 'mailto:legal@example.invalid' "$OUTPUT/dashboard.html"

printf 'M365 artifact renderers: OK\n'
