#!/usr/bin/env bash
set -euo pipefail
# This migration is intentionally non-rollbackable.
# Data lost during up.sh cannot be restored.
# down.sh MUST exit 1 to signal CI that rollback is impossible.
echo "[migration 002] down: ERROR — this migration is non-rollbackable" >&2
echo "[migration 002] down: Data destroyed by up.sh cannot be recovered." >&2
exit 1
