#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

python3 scripts/validate_site.py --local

if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  python3 scripts/validate_site.py --gh
else
  echo "Skipping --gh checks: gh is not installed or not authenticated."
fi

python3 scripts/validate_site.py --live
