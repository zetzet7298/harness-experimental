#!/usr/bin/env python3
import argparse, subprocess, json
from pathlib import Path
from datetime import datetime, timezone

base = Path(__file__).resolve().parent
out = base / 'e2r-run-option-b-report.json'
decision_file = base / 'e2r-gate-decision.json'

ap = argparse.ArgumentParser(description='Execute Option B runbook (provisional accept path).')
ap.add_argument('--accept-provisional', action='store_true', help='Explicitly set accept_provisional_for_e_m3_to_e_m7=true')
ap.add_argument('--decided-by', default='', help='Human approver name/id (required with --accept-provisional)')
args=ap.parse_args()

runs=[]

# apply repair + verify chain
cmd_apply=['python3', str(base / 'e2r-golditem-apply-repair-proposals.py'), '--apply', '--verify']
p=subprocess.run(cmd_apply,capture_output=True,text=True)
runs.append({'cmd':cmd_apply,'exit_code':p.returncode,'stdout_tail':p.stdout[-500:],'stderr_tail':p.stderr[-500:]})

if args.accept_provisional:
    if not args.decided_by.strip():
        raise SystemExit('--decided-by là bắt buộc khi dùng --accept-provisional')
    d=json.loads(decision_file.read_text(encoding='utf-8')) if decision_file.exists() else {}
    d['accept_provisional_for_e_m3_to_e_m7']=True
    d['decided_by']=args.decided_by.strip()
    d['decided_at']=datetime.now(timezone.utc).isoformat()
    d['decision_note']=d.get('decision_note') or 'Approved provisional path for E_M3..E_M7 progression.'
    decision_file.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

for cmd in ([['python3', str(base / 'e2r-gate-readiness-check.py')], ['python3', str(base / 'e2r-ops-one-shot.py')]]):
    p=subprocess.run(cmd,capture_output=True,text=True)
    runs.append({'cmd':cmd,'exit_code':p.returncode,'stdout_tail':p.stdout[-500:],'stderr_tail':p.stderr[-500:]})

ready=None
gate_json=base/'e2r-gate-readiness.json'
if gate_json.exists():
    g=json.loads(gate_json.read_text(encoding='utf-8'))
    ready=g.get('gate_status')

payload={
 'generated_at_utc':datetime.now(timezone.utc).isoformat(),
 'option':'B_provisional_accept',
 'accept_provisional_flag_set':bool(args.accept_provisional),
 'decided_by':args.decided_by,
 'runs':runs,
 'gate_status_after_runs':ready,
 'is_ready_provisional_approved': ready=='ready-provisional-approved'
}
out.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f"OPTION_B gate_status={ready} ready_provisional={payload['is_ready_provisional_approved']}")
print(f"wrote {out}")
