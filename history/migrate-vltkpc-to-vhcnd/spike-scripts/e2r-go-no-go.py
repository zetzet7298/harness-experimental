#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime, timezone

base=Path(__file__).resolve().parent
out_json=base/'e2r-go-no-go.json'
out_md=base/'e2r-go-no-go.md'

def rj(name):
    p=base/name
    if not p.exists(): return {}
    return json.loads(p.read_text(encoding='utf-8'))

integrity=rj('e2r-artifact-integrity-check.json')
pre=rj('e2r-finalize-preflight.json')
audit=rj('e2r-swarming-completion-audit.json')
pulse=rj('e2r-operator-pulse.json')

integrity_ok=(integrity.get('status')=='pass')
audit_complete=(audit.get('overall_status')=='complete')
ready_now = bool(pre.get('option_a_canonical_ready') or pre.get('option_b_ready_to_finalize'))
needs_human = bool(pre.get('option_b_ready_to_request_human'))

if audit_complete:
    verdict='GO'
elif integrity_ok and needs_human:
    verdict='GO-WAITING-HUMAN-APPROVAL'
else:
    verdict='NO-GO'

blockers=[]
if not integrity_ok:
    blockers.append('artifact-integrity-fail')
for b in (audit.get('blocking_requirements') or []):
    blockers.append(str(b))
if needs_human:
    blockers.append('human-approval-required')

payload={
 'generated_at_utc':datetime.now(timezone.utc).isoformat(),
 'verdict':verdict,
 'integrity_ok':integrity_ok,
 'preflight':{
   'option_a_canonical_ready':pre.get('option_a_canonical_ready'),
   'option_b_ready_to_finalize':pre.get('option_b_ready_to_finalize'),
   'option_b_ready_to_request_human':pre.get('option_b_ready_to_request_human'),
 },
 'audit_overall':audit.get('overall_status'),
 'gate_status':pulse.get('gate_status'),
 'next_step_label':pulse.get('next_step_label'),
 'next_step_command':pulse.get('next_step_command'),
 'blockers':sorted(set(blockers))
}
out_json.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

lines=['# E2R Go/No-Go Verdict','',f"Generated (UTC): `{payload['generated_at_utc']}`",'',f"## Verdict: **{verdict}**",'',f"- Integrity OK: **{integrity_ok}**",f"- Audit overall: **{payload['audit_overall']}**",f"- Gate status: **{payload['gate_status']}**",'', '## Preflight', '', f"- option_a_canonical_ready: `{payload['preflight']['option_a_canonical_ready']}`", f"- option_b_ready_to_finalize: `{payload['preflight']['option_b_ready_to_finalize']}`", f"- option_b_ready_to_request_human: `{payload['preflight']['option_b_ready_to_request_human']}`", '', '## Blockers', '']
if payload['blockers']:
    lines += [f"- {b}" for b in payload['blockers']]
else:
    lines += ['- None']
lines += ['', '## Next Step', '', '```bash', payload['next_step_command'] or '', '```']
out_md.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('verdict='+verdict)
print('wrote',out_json)
print('wrote',out_md)
