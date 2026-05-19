#!/usr/bin/env python3
import argparse, subprocess, json
from pathlib import Path
from datetime import datetime, timezone

base = Path(__file__).resolve().parent
report = base / 'e2r-finalize-and-audit-report.json'

ap = argparse.ArgumentParser(description='Finalize path and immediately run completion audit bundle.')
ap.add_argument('--human-approved', action='store_true', help='Forward human approval to finalize script')
ap.add_argument('--decided-by', default='', help='Human approver identity')
ap.add_argument('--reason', default='Provisional accepted by human', help='Reason text used by finalize')
args = ap.parse_args()

steps = []

def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    steps.append({
        'cmd': cmd,
        'exit_code': p.returncode,
        'stdout_tail': p.stdout[-800:],
        'stderr_tail': p.stderr[-800:],
    })
    return p.returncode

# always refresh pulse/audit whether or not human approved
if args.human_approved and args.decided_by.strip():
    run(['python3', str(base/'e2r-finalize-provisional.py'), '--human-approved', '--decided-by', args.decided_by.strip(), '--reason', args.reason])
else:
    run(['python3', str(base/'e2r-finalize-provisional.py')])

run(['python3', str(base/'e2r-control-dashboard.py')])
run(['python3', str(base/'e2r-swarming-completion-audit.py')] if (base/'e2r-swarming-completion-audit.py').exists() else ['python3', '-c', 'print("completion audit is static artifact")'])
run(['python3', str(base/'e2r-operator-pulse.py')])
run(['python3', str(base/'e2r-generate-next-step.py')])

# collect latest statuses
read = lambda p: json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
close = read(base/'e2r-close-mig-ja5-report.json')
audit = read(base/'e2r-swarming-completion-audit.json')
pulse = read(base/'e2r-operator-pulse.json')

payload = {
    'generated_at_utc': datetime.now(timezone.utc).isoformat(),
    'human_approved': bool(args.human_approved),
    'decided_by': args.decided_by,
    'steps': steps,
    'bead_closed': close.get('closed'),
    'gate_status': pulse.get('gate_status'),
    'completion_audit_overall': audit.get('overall_status'),
    'completion_audit_blockers': audit.get('blocking_requirements'),
}
report.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(f"finalize_and_audit gate={payload['gate_status']} bead_closed={payload['bead_closed']} audit={payload['completion_audit_overall']}")
print(f"wrote {report}")
