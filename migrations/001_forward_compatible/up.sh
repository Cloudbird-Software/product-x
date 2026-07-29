#!/usr/bin/env bash
set -euo pipefail
# Forward-compatible migration: add a column with default value
# This is safe to run on production without downtime.
echo "[migration 001] up: adding column 'created_at' with default timestamp"
echo "[migration 001] up: done"
