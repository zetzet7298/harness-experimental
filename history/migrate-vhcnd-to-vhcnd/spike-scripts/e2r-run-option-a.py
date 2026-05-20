#!/usr/bin/env python3
import subprocess, json
from pathlib import Path
from datetime import datetime, timezone

base = Path(__file__).resolve().parent
out = base / 'e2r-run-option-a-report.json'
cmds = [
    ['python3', str(base / 'e2r-golditem-manual-map-validate.py')],
    ['python3', str(base / 'e2r-ops-one-shot.py')],
    ['python3', str(base / 'e2r-gate-readiness-check.py')],
]

runs=[]
for cmd in cmds:
    p=subprocess.run(cmd,capture_output=True,text=True)
    runs.append({'cmd':cmd,'exit_code':p.returncode,'stdout_tail':p.stdout[-500:],'stderr_tail':p.stderr[-500:]})

ready = None
gate_json = base / 'e2r-gate-readiness.json'
if gate_json.exists():
    g=json.loads(gate_json.read_text(encoding='utf-8'))
    ready=g.get('gate_status')

payload={
 'generated_at_utc':datetime.now(timezone.utc).isoformat(),
 'option':'A_canonical_first',
 'runs':runs,
 'gate_status_after_runs':ready,
 'is_ready_canonical': ready=='ready-canonical'
}
out.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f"OPTION_A gate_status={ready} ready_canonical={payload['is_ready_canonical']}")
print(f"wrote {out}")
