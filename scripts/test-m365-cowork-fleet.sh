#!/usr/bin/env bash
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
# Run every local-only Microsoft 365 Cowork migration gate.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

bash "$ROOT/scripts/test-m365-cowork-inventory.sh"
bash "$ROOT/scripts/test-m365-apache-notices.sh"
bash "$ROOT/scripts/test-m365-cowork-target.sh"
bash "$ROOT/scripts/test-sharepoint-state-contracts.sh"
bash "$ROOT/scripts/test-m365-connector-matrix.sh"
bash "$ROOT/scripts/test-power-platform-contracts.sh"
bash "$ROOT/scripts/test-m365-artifacts.sh"
bash "$ROOT/scripts/build-m365-cowork-packages.sh"

python3 -c "
import glob,json
[json.load(open(path, encoding='utf-8')) for path in glob.glob(
    '$ROOT/m365-cowork-ja/**/*.json',
    recursive=True,
)]
"

git -C "$ROOT" --no-pager diff --check
printf 'Microsoft 365 Cowork fleet validation: OK\n'
