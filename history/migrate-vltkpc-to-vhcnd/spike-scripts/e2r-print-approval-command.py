#!/usr/bin/env python3
import argparse

ap = argparse.ArgumentParser(description='Print a safe, copy-paste approval command for e2r-run-on-approval.sh')
ap.add_argument('--decided-by', required=True)
ap.add_argument('--mode', choices=['accept-provisional','canonical-first'], required=True)
ap.add_argument('--note', default='Approved by human')
args = ap.parse_args()

cmd = (
    f'E2R_CONFIRM="YES" \\\nE2R_DECIDED_BY="{args.decided_by}" \\\nE2R_MODE="{args.mode}" \\\nE2R_NOTE="{args.note}" \\\n'
    'bash history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-run-on-approval.sh'
)
print(cmd)
