#!/usr/bin/env python3
import argparse, subprocess, json
from pathlib import Path
from datetime import datetime, timezone

base = Path(__file__).resolve().parent
report = base / 'e2r-approve-and-finalize-report.json'

ap = argparse.ArgumentParser(description='Orchestrate human decision capture and finalize+audit flow.')
ap.add_argument('--decided-by', required=True, help='Human approver identity')
ap.add_argument('--mode', choices=['accept-provisional','canonical-first'], required=True)
ap.add_argument('--note', default='', help='Decision note')
ap.add_argument('--apply', action='store_true', help='Apply decision + run finalize-and-audit')
args = ap.parse_args()

steps=[]

def run(cmd):
    p=subprocess.run(cmd,capture_output=True,text=True)
    steps.append({'cmd':cmd,'exit_code':p.returncode,'stdout_tail':p.stdout[-800:],'stderr_tail':p.stderr[-800:]})
    return p.returncode

# always capture receipt first (preview or apply)
cmd=['python3', str(base/'e2r-capture-human-decision.py'), '--decided-by', args.decided_by, '--mode', args.mode]
if args.note:
    cmd += ['--note', args.note]
if args.apply:
    cmd += ['--apply']
run(cmd)

if args.apply:
    if args.mode == 'accept-provisional':
        run(['python3', str(base/'e2r-finalize-and-audit.py'), '--human-approved', '--decided-by', args.decided_by, '--reason', args.note or 'Provisional accepted by human'])
    else:
        run(['python3', str(base/'e2r-run-option-a.py')])
        run(['python3', str(base/'e2r-close-mig-ja5.py'), '--confirm', '--reason', args.note or 'Canonical mapping completed', '--append-verdict-note'])
        run(['python3', str(base/'e2r-control-dashboard.py')])
        run(['python3', str(base/'e2r-swarming-completion-audit.py')])
        run(['python3', str(base/'e2r-operator-pulse.py')])

# summarize
read=lambda p: json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
close=read(base/'e2r-close-mig-ja5-report.json')
audit=read(base/'e2r-swarming-completion-audit.json')
pulse=read(base/'e2r-operator-pulse.json')

payload={
    'generated_at_utc': datetime.now(timezone.utc).isoformat(),
    'decided_by': args.decided_by,
    'mode': args.mode,
    'apply': bool(args.apply),
    'steps': steps,
    'gate_status': pulse.get('gate_status'),
    'bead_closed': close.get('closed'),
    'completion_audit_overall': audit.get('overall_status'),
    'completion_audit_blockers': audit.get('blocking_requirements')
}
report.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f"approve_finalize mode={args.mode} apply={args.apply} gate={payload['gate_status']} bead_closed={payload['bead_closed']} audit={payload['completion_audit_overall']}")
print(f"wrote {report}")
