#!/usr/bin/env bash
set -euo pipefail
# Rollback: remove the column added by up.sh
echo "[migration 001] down: removing column 'created_at'"
echo "[migration 001] down: done"
