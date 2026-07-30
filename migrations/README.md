# Migration Dual-Script Spec (R3)

## Convention

Every database migration lives in its own numbered directory under `migrations/`:

```
migrations/
  001_forward_compatible/
    up.sh        # forward migration (apply)
    down.sh      # rollback migration (undo)
  002_non_rollbackable/
    up.sh        # forward migration
    down.sh      # MUST exit 1 (intentionally non-rollbackable)
    NON_ROLLBACKABLE   # marker file
```

## Rules

1. **Every migration must have both `up.sh` and `down.sh`.**
2. `up.sh` must be **forward-compatible**: it must work on a production snapshot
   without requiring downtime.
3. `down.sh` must **roll back** the changes made by `up.sh`.
4. If a migration is intentionally non-rollbackable (e.g. destructive schema change
   that cannot be undone), `down.sh` must `exit 1` and the directory must contain
   a `NON_ROLLBACKABLE` marker file.
5. **Non-rollbackable migrations cause CI to go red.** This is by design — it
   forces human review before merging.
6. Scripts receive `MIGRATION_SNAPSHOT_DIR` env var pointing to the production
   snapshot directory.

## CI Verification

The `migration-test.yml` workflow:
1. Triggers on PRs that modify `migrations/**`.
2. Creates a mock production snapshot.
3. Runs all `up.sh` scripts in order.
4. Runs all `down.sh` scripts in reverse order.
5. Any `down.sh` that exits non-zero → CI red.

## Adding a New Migration

```bash
mkdir migrations/NNN_description
# Write up.sh (forward-compatible, idempotent)
# Write down.sh (rollback, or exit 1 if non-rollbackable + touch NON_ROLLBACKABLE)
```
