#!/usr/bin/env python3
import json, subprocess
from pathlib import Path
from datetime import datetime, timezone

base = Path(__file__).resolve().parent
out_md = base / 'e2r-control-dashboard.md'
out_json = base / 'e2r-control-dashboard.json'

# Refresh key artifacts
subprocess.run(['python3', str(base / 'e2r-ops-one-shot.py')], check=False, capture_output=True, text=True)
subprocess.run(['python3', str(base / 'e2r-gate-readiness-check.py')], check=False, capture_output=True, text=True)
subprocess.run(['python3', str(base / 'e2r-golditem-manual-map-validate.py')], check=False, capture_output=True, text=True)

# Read states
read = lambda p: json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
one = read(base / 'e2r-ops-one-shot-summary.json')
gate = read(base / 'e2r-gate-readiness.json')
val = read(base / 'e2r-golditem-manual-map-validate.json')
dec = read(base / 'e2r-gate-decision.json')

# Bead status
br = subprocess.run(['bash','-lc','cd /var/www/vltk-h5-survivors/harness-experimental && CI=1 br show mig-ja5 --json'],capture_output=True,text=True)
bead = None
if br.returncode == 0:
    try:
        arr = json.loads(br.stdout)
        bead = arr[0] if arr else None
    except Exception:
        bead = None

remaining = int(val.get('missing_selected_rows') or 0)
issues = int(val.get('issue_count') or 0)
gate_status = gate.get('gate_status','unknown')
accept = bool(dec.get('accept_provisional_for_e_m3_to_e_m7'))

if gate_status in ('ready-canonical','ready-provisional-approved'):
    next_action = 'Run safe close: python3 .../e2r-close-mig-ja5.py --confirm --reason "..." --append-verdict-note'
elif issues > 0:
    next_action = 'Resolve mapping issues first (apply repair proposals or manual fix), then rerun one-shot.'
elif remaining > 0 and not accept:
    next_action = 'Human decision required: set accept_provisional=true OR continue canonical completion.'
else:
    next_action = 'Rerun one-shot and verify gate state manually.'

payload = {
    'generated_at_utc': datetime.now(timezone.utc).isoformat(),
    'bead': {'id':'mig-ja5','status': (bead or {}).get('status')},
    'gate_status': gate_status,
    'one_line': one.get('one_line'),
    'map_selected_rows': val.get('selected_rows'),
    'map_total_rows': val.get('total_rows'),
    'map_remaining_rows': remaining,
    'map_issue_count': issues,
    'accept_provisional': accept,
    'decided_by': dec.get('decided_by',''),
    'next_action': next_action,
}
out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

md = [
    '# E2R Control Dashboard',
    '',
    f"Generated (UTC): `{payload['generated_at_utc']}`",
    '',
    f"- Bead `mig-ja5`: **{payload['bead']['status']}**",
    f"- Gate status: **{gate_status}**",
    f"- One-line: `{payload['one_line']}`",
    f"- Map selected: **{payload['map_selected_rows']}/{payload['map_total_rows']}** (remaining **{remaining}**)",
    f"- Map issues: **{issues}**",
    f"- Accept provisional: **{accept}**",
    f"- Decided by: **{payload['decided_by'] or '-'}**",
    '',
    '## Next action',
    '',
    f"- {next_action}",
]
out_md.write_text('\n'.join(md) + '\n', encoding='utf-8')
print(f"dashboard gate={gate_status} remaining={remaining} issues={issues} accept={accept}")
print(f"wrote {out_md}")
print(f"wrote {out_json}")
