#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   E2R_DECIDED_BY="<human>" E2R_MODE="accept-provisional|canonical-first" \
#   E2R_NOTE="..." bash history/migrate-vhcnd-to-vhcnd/spike-scripts/e2r-run-on-approval.sh

MODE="${E2R_MODE:-}"
DECIDED_BY="${E2R_DECIDED_BY:-}"
NOTE="${E2R_NOTE:-Approved by human}"
CONFIRM="${E2R_CONFIRM:-}"

if [[ -z "$MODE" || -z "$DECIDED_BY" ]]; then
  echo "[E2R] Missing required env vars."
  echo "Set E2R_MODE and E2R_DECIDED_BY."
  exit 2
fi

if [[ "$MODE" != "accept-provisional" && "$MODE" != "canonical-first" ]]; then
  echo "[E2R] Invalid E2R_MODE: $MODE"
  exit 2
fi

if [[ "$CONFIRM" != "YES" ]]; then
  echo "[E2R] Safety stop: set E2R_CONFIRM=YES to execute apply flow."
  echo "Example: E2R_CONFIRM=YES E2R_DECIDED_BY=... E2R_MODE=... bash .../e2r-run-on-approval.sh"
  exit 2
fi

cd /var/www/vltk-h5-survivors/harness-experimental

echo "[E2R] Running preflight..."
python3 history/migrate-vhcnd-to-vhcnd/spike-scripts/e2r-finalize-preflight.py

echo "[E2R] Running approve-and-finalize..."
python3 history/migrate-vhcnd-to-vhcnd/spike-scripts/e2r-approve-and-finalize.py \
  --decided-by "$DECIDED_BY" \
  --mode "$MODE" \
  --note "$NOTE" \
  --apply

echo "[E2R] Refreshing go/no-go + pulse..."
python3 history/migrate-vhcnd-to-vhcnd/spike-scripts/e2r-go-no-go.py
python3 history/migrate-vhcnd-to-vhcnd/spike-scripts/e2r-operator-pulse.py

echo "[E2R] Done. Check artifacts:"
echo "  - history/migrate-vhcnd-to-vhcnd/spike-scripts/e2r-approve-and-finalize-report.json"
echo "  - history/migrate-vhcnd-to-vhcnd/spike-scripts/e2r-go-no-go.json"
echo "  - history/migrate-vhcnd-to-vhcnd/spike-scripts/e2r-operator-pulse.json"
