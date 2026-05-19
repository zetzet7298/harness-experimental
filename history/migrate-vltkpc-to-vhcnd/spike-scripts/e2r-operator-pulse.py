#!/usr/bin/env python3
import json, subprocess
from pathlib import Path
from datetime import datetime, timezone

base = Path(__file__).resolve().parent
out_json = base / 'e2r-operator-pulse.json'
out_md = base / 'e2r-operator-pulse.md'

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

# Refresh core artifacts
for cmd in [
    ['python3', str(base/'e2r-control-dashboard.py')],
    ['python3', str(base/'e2r-finalize-preflight.py')],
    ['python3', str(base/'e2r-generate-next-step.py')],
]:
    run(cmd)

read = lambda p: json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
dash = read(base/'e2r-control-dashboard.json')
pf = read(base/'e2r-finalize-preflight.json')
nexts = read(base/'e2r-next-step.json')
audit = read(base/'e2r-swarming-completion-audit.json')

pulse = {
    'generated_at_utc': datetime.now(timezone.utc).isoformat(),
    'gate_status': dash.get('gate_status'),
    'bead_status': (dash.get('bead') or {}).get('status'),
    'map_issue_count': dash.get('map_issue_count'),
    'remaining_rows': dash.get('map_remaining_rows'),
    'accept_provisional': dash.get('accept_provisional'),
    'preflight': {
        'option_a_canonical_ready': pf.get('option_a_canonical_ready'),
        'option_b_ready_to_finalize': pf.get('option_b_ready_to_finalize'),
        'option_b_ready_to_request_human': pf.get('option_b_ready_to_request_human'),
    },
    'next_step_label': nexts.get('label'),
    'next_step_command': nexts.get('command'),
    'completion_audit_overall': audit.get('overall_status'),
    'completion_audit_blockers': audit.get('blocking_requirements'),
}
out_json.write_text(json.dumps(pulse, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

md = [
'# E2R Operator Pulse',
'',
f"Generated (UTC): `{pulse['generated_at_utc']}`",
'',
f"- Gate: **{pulse['gate_status']}**",
f"- Bead mig-ja5: **{pulse['bead_status']}**",
f"- Map issues: **{pulse['map_issue_count']}**",
f"- Remaining rows: **{pulse['remaining_rows']}**",
f"- Accept provisional: **{pulse['accept_provisional']}**",
'',
'## Preflight flags',
'',
f"- option_a_canonical_ready: `{pulse['preflight']['option_a_canonical_ready']}`",
f"- option_b_ready_to_finalize: `{pulse['preflight']['option_b_ready_to_finalize']}`",
f"- option_b_ready_to_request_human: `{pulse['preflight']['option_b_ready_to_request_human']}`",
'',
'## Next step',
'',
f"- label: **{pulse['next_step_label']}**",
'```bash', pulse['next_step_command'] or '', '```',
'',
'## Completion audit',
'',
f"- overall: **{pulse['completion_audit_overall']}**",
f"- blockers: `{pulse['completion_audit_blockers']}`",
]
out_md.write_text('\n'.join(md)+'\n', encoding='utf-8')
print('wrote', out_json)
print('wrote', out_md)
print('pulse_next='+str(pulse['next_step_label']))
