#!/usr/bin/env bash
# .loop/verify.sh — product-x 验证脚本
# 退出码：0 = PASS, 1 = FAIL
# FAIL 时 stderr 输出失败断言（供 verify AI 抓证据）
set -euo pipefail

PASS=0
FAIL=0

assert_pass() { PASS=$((PASS+1)); }
assert_fail() { FAIL=$((FAIL+1)); echo "FAIL: $1" >&2; }

# --- Assertion 1: AGENTS.md exists and is non-empty ---
if [ -s "AGENTS.md" ]; then
  assert_pass
else
  assert_fail "AGENTS.md missing or empty"
fi

# --- Assertion 2: No Python syntax errors in any .py file ---
PY_ERRORS=""
while IFS= read -r -d '' f; do
  if ! python3 -c "compile(open('$f').read(), '$f', 'exec')" 2>/dev/null; then
    PY_ERRORS="$PY_ERRORS $f"
  fi
done < <(find . -name "*.py" -not -path "./.git/*" -print0 2>/dev/null)

if [ -z "$PY_ERRORS" ]; then
  assert_pass
else
  assert_fail "Python syntax errors in:$PY_ERRORS"
fi

# --- Assertion 3: contracts/ directory exists and has at least one .md file ---
CONTRACT_COUNT=$(find contracts/ -name "*.md" 2>/dev/null | wc -l)
if [ "$CONTRACT_COUNT" -ge 1 ]; then
  assert_pass
else
  assert_fail "contracts/ missing or has no .md files (found $CONTRACT_COUNT)"
fi

# --- Summary ---
echo "verify.sh: $PASS passed, $FAIL failed"

if [ "$FAIL" -gt 0 ]; then
  exit 1
fi
exit 0
