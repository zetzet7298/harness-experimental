#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime, timezone

b=Path(__file__).resolve().parent
read=lambda n: json.loads((b/n).read_text(encoding='utf-8')) if (b/n).exists() else {}

# refresh dependencies if present
import subprocess
for script in ['e2r-control-dashboard.py','e2r-gate-readiness-check.py','e2r-golditem-manual-map-validate.py','e2r-ops-one-shot.py']:
    p=b/script
    if p.exists(): subprocess.run(['python3',str(p)],capture_output=True,text=True)

dashboard=read('e2r-control-dashboard.json')
gate=read('e2r-gate-readiness.json')
validate=read('e2r-golditem-manual-map-validate.json')
one=read('e2r-ops-one-shot-summary.json')
close_report=read('e2r-close-mig-ja5-report.json')

reqs=[]
reqs.append({'id':'R1','text':'Technical mapping validity ready','status':'proven' if (validate.get('status')=='pass' and int(validate.get('issue_count',999))==0) else 'missing','evidence':{'validate_status':validate.get('status'),'issue_count':validate.get('issue_count')}})
reqs.append({'id':'R2','text':'Gate readiness artifact exists','status':'proven' if gate.get('gate_status') else 'missing','evidence':{'gate_status':gate.get('gate_status')}})
reqs.append({'id':'R3','text':'Bead mig-ja5 closed with guard','status':'proven' if close_report.get('closed') else 'missing','evidence':{'close_report_closed':close_report.get('closed'),'close_gate_status':close_report.get('gate_status')}})
reqs.append({'id':'R4','text':'Human provisional decision explicit (or canonical ready path)','status':'proven' if ((gate.get('facts') or {}).get('accept_provisional_for_e_m3_to_e_m7') is True or gate.get('gate_status')=='ready-canonical') else 'missing','evidence':{'accept_provisional':(gate.get('facts') or {}).get('accept_provisional_for_e_m3_to_e_m7'),'gate_status':gate.get('gate_status')}})
reqs.append({'id':'R5','text':'Operator next-step command exists','status':'proven' if (b/'e2r-next-step.md').exists() else 'missing','evidence':{'next_step_exists':(b/'e2r-next-step.md').exists()}})

all_proven=all(r['status']=='proven' for r in reqs)
audit={
 'generated_at_utc':datetime.now(timezone.utc).isoformat(),
 'objective':'$khuym:swarming for E_M2R gate mig-ja5',
 'requirements':reqs,
 'overall_status':'complete' if all_proven else 'incomplete',
 'blocking_requirements':[r['id'] for r in reqs if r['status']!='proven'],
 'current_one_line':one.get('one_line'),
 'dashboard_next_action':dashboard.get('next_action')
}

(b/'e2r-swarming-completion-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# E2R Swarming Completion Audit','',f"Generated (UTC): `{audit['generated_at_utc']}`",'',f"Overall: **{audit['overall_status']}**",f"One-line: `{audit['current_one_line']}`",'', '| ID | Requirement | Status | Evidence |','|---|---|---|---|']
for r in reqs:
    ev=', '.join(f"{k}={v}" for k,v in r['evidence'].items())
    lines.append(f"| {r['id']} | {r['text']} | **{r['status']}** | {ev} |")
lines += ['', '## Blocking requirements','']
if audit['blocking_requirements']:
    lines += [f"- {x}" for x in audit['blocking_requirements']]
else:
    lines += ['- None']
lines += ['', '## Dashboard next action','', f"- {audit['dashboard_next_action']}"]
(b/'e2r-swarming-completion-audit.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('wrote completion audit; overall='+audit['overall_status'])
