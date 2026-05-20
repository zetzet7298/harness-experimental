#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path
from datetime import datetime, timezone

base = Path(__file__).resolve().parent
snapshot_script = base / 'e2r-golditem-progress-snapshot.py'
gate_script = base / 'e2r-gate-readiness-check.py'

snapshot_json = base / 'e2r-golditem-progress-snapshot.json'
diff_json = base / 'e2r-golditem-progress-diff-latest.json'
gate_json = base / 'e2r-gate-readiness.json'

out_json = base / 'e2r-ops-one-shot-summary.json'
out_md = base / 'e2r-ops-one-shot-summary.md'


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    return {
        'cmd': cmd,
        'exit_code': p.returncode,
        'stdout_tail': p.stdout[-500:],
        'stderr_tail': p.stderr[-500:],
    }

r1 = run(['python3', str(snapshot_script)])
r2 = run(['python3', str(gate_script)])

snapshot = json.loads(snapshot_json.read_text(encoding='utf-8')) if snapshot_json.exists() else {}
diff = json.loads(diff_json.read_text(encoding='utf-8')) if diff_json.exists() else {}
gate = json.loads(gate_json.read_text(encoding='utf-8')) if gate_json.exists() else {}

gate_status = gate.get('gate_status', 'unknown')
selected = ((snapshot.get('template') or {}).get('selected_rows'))
total = ((snapshot.get('template') or {}).get('total_rows'))
remaining = ((snapshot.get('template') or {}).get('remaining_rows'))
completion = ((snapshot.get('template') or {}).get('completion_pct'))

delta_sel = (((diff.get('delta') or {}).get('selected_rows')) if isinstance(diff.get('delta'), dict) else None)
delta_rem = (((diff.get('delta') or {}).get('remaining_rows')) if isinstance(diff.get('delta'), dict) else None)

one_line = f"E2R_GATE status={gate_status} selected={selected}/{total} remaining={remaining} completion={completion}% delta_selected={delta_sel if delta_sel is not None else 'n/a'} delta_remaining={delta_rem if delta_rem is not None else 'n/a'}"

payload = {
    'generated_at_utc': datetime.now(timezone.utc).isoformat(),
    'one_line': one_line,
    'gate_status': gate_status,
    'snapshot': snapshot,
    'diff': diff,
    'runs': {'snapshot': r1, 'gate': r2},
}
out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

md = [
    '# E2R Ops One-shot Summary',
    '',
    f"Generated (UTC): `{payload['generated_at_utc']}`",
    '',
    '## One-line status',
    '',
    f"`{one_line}`",
    '',
    '## Command exits',
    '',
    f"- snapshot script exit: **{r1['exit_code']}**",
    f"- gate script exit: **{r2['exit_code']}**",
    '',
    '## Artifacts',
    '',
    '- `e2r-golditem-progress-snapshot.json`',
    '- `e2r-golditem-progress-diff-latest.json`',
    '- `e2r-gate-readiness.json`',
]
out_md.write_text('\n'.join(md) + '\n', encoding='utf-8')

print(one_line)
print(f'wrote {out_json}')
print(f'wrote {out_md}')
