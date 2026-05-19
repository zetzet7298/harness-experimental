#!/usr/bin/env python3
import argparse, json, subprocess
from pathlib import Path
from datetime import datetime, timezone

base = Path(__file__).resolve().parent
decision_file = base / 'e2r-gate-decision.json'
report_file = base / 'e2r-finalize-provisional-report.json'

ap = argparse.ArgumentParser(description='Finalize provisional path with explicit human approval guards.')
ap.add_argument('--human-approved', action='store_true', help='Required explicit approval switch')
ap.add_argument('--decided-by', default='', help='Human approver identity')
ap.add_argument('--reason', default='Provisional accepted by human', help='Close reason')
args = ap.parse_args()

runs=[]

def run(cmd):
    p=subprocess.run(cmd,capture_output=True,text=True)
    runs.append({'cmd':cmd,'exit_code':p.returncode,'stdout_tail':p.stdout[-600:],'stderr_tail':p.stderr[-600:]})
    return p.returncode

status='blocked'
closed=False

if not args.human_approved or not args.decided_by.strip():
    status='blocked-missing-human-approval'
else:
    # set decision flag
    d=json.loads(decision_file.read_text(encoding='utf-8')) if decision_file.exists() else {}
    d['accept_provisional_for_e_m3_to_e_m7']=True
    d['decided_by']=args.decided_by.strip()
    d['decided_at']=datetime.now(timezone.utc).isoformat()
    d['decision_note']=d.get('decision_note') or 'Approved provisional path for E_M3..E_M7 progression.'
    decision_file.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    # execute option-b close chain
    run(['python3', str(base/'e2r-gate-readiness-check.py')])
    run(['python3', str(base/'e2r-ops-one-shot.py')])
    run(['python3', str(base/'e2r-close-mig-ja5.py'), '--confirm', '--reason', args.reason, '--append-verdict-note'])

    # inspect close report + gate
    gate=json.loads((base/'e2r-gate-readiness.json').read_text(encoding='utf-8')) if (base/'e2r-gate-readiness.json').exists() else {}
    close=json.loads((base/'e2r-close-mig-ja5-report.json').read_text(encoding='utf-8')) if (base/'e2r-close-mig-ja5-report.json').exists() else {}
    status=gate.get('gate_status','unknown')
    closed=bool(close.get('closed'))

payload={
 'generated_at_utc':datetime.now(timezone.utc).isoformat(),
 'human_approved_flag':bool(args.human_approved),
 'decided_by':args.decided_by,
 'result_status':status,
 'bead_closed':closed,
 'runs':runs
}
report_file.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f"finalize_status={status} bead_closed={closed}")
print(f"wrote {report_file}")
