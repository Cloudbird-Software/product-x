#!/usr/bin/env bash
set -euo pipefail
# Non-rollbackable migration: destructive schema change (e.g. drop column)
echo "[migration 002] up: dropping column 'legacy_field' (destructive, non-rollbackable)"
echo "[migration 002] up: done"
