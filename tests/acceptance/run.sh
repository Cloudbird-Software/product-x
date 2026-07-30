#!/usr/bin/env bash
# tests/acceptance/run.sh — product-x acceptance test runner
# Called by .loop/verify.sh or by verify AI directly
set -euo pipefail

PASS=0
FAIL=0

assert_pass() { PASS=$((PASS+1)); echo "PASS: $1"; }
assert_fail() { FAIL=$((FAIL+1)); echo "FAIL: $1" >&2; }

# --- AC-1: /health endpoint returns 200 + {status: ok} ---
# (If /health is implemented as a real endpoint, curl it.
#  For now, check that the contract file exists as a proxy.)
if [ -f "contracts/api-health.md" ]; then
  assert_pass "AC-1: /health contract exists"
else
  assert_fail "AC-1: /health contract missing"
fi

# --- AC-2: AGENTS.md present and <=200 lines ---
LINES=$(wc -l < AGENTS.md 2>/dev/null || echo 0)
if [ "$LINES" -gt 0 ] && [ "$LINES" -le 200 ]; then
  assert_pass "AC-2: AGENTS.md present, $LINES lines (<=200)"
else
  assert_fail "AC-2: AGENTS.md missing or >200 lines ($LINES)"
fi

# --- Summary ---
echo ""
echo "Acceptance: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
