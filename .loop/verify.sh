#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

errors=0

if [ "$(cat ignition/impl-1/probe.txt)" != "ignition ok" ]; then
  echo "FAIL: probe.txt content mismatch"
  errors=$((errors + 1))
fi

if ! grep -q '=== loopd status ===' ignition/impl-1/status.txt; then
  echo "FAIL: status.txt missing loopd status header"
  errors=$((errors + 1))
fi

if grep -q 'UNKNOWN_INTENT' ignition/impl-1/tail.txt; then
  echo "FAIL: tail.txt contains UNKNOWN_INTENT"
  errors=$((errors + 1))
fi

if [ "$errors" -ne 0 ]; then
  echo "verify failed with $errors error(s)"
  exit 1
fi

echo "verify passed"
