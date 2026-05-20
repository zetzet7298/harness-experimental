#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime, timezone

base=Path(__file__).resolve().parent
out_json=base/'e2r-gate-forecast.json'
out_md=base/'e2r-gate-forecast.md'

read=lambda p: json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}

gate=read(base/'e2r-gate-readiness.json')
validate=read(base/'e2r-golditem-manual-map-validate.json')
preview=read(base/'e2r-preview-repair-impact.json')
decision=read(base/'e2r-gate-decision.json')

selected=int((validate.get('selected_rows') or 0))
total=int((validate.get('total_rows') or 0))
remaining=int((validate.get('missing_selected_rows') or max(total-selected,0)))
stat_pass=((gate.get('facts') or {}).get('stat_audit_status')=='pass')
no_fab=((gate.get('facts') or {}).get('no_fabrication_status')=='pass')
accept=bool(decision.get('accept_provisional_for_e_m3_to_e_m7'))

canon_issues=int(validate.get('issue_count') or 0)
preview_issues=int(((preview.get('preview') or {}).get('issue_count')) if preview else canon_issues)

scenarios=[]

def status(rem, issues, accept_flag):
    canonical_ready=(rem==0 and issues==0 and stat_pass and no_fab)
    provisional_ready=(rem>0 and issues==0 and stat_pass and no_fab and accept_flag)
    if canonical_ready: return 'ready-canonical'
    if provisional_ready: return 'ready-provisional-approved'
    return 'blocked'

scenarios.append({
 'name':'current-state',
 'remaining_rows':remaining,
 'map_issue_count':canon_issues,
 'accept_provisional':accept,
 'forecast_gate_status':status(remaining,canon_issues,accept),
})
scenarios.append({
 'name':'after-apply-proposals-without-provisional-accept',
 'remaining_rows':remaining,
 'map_issue_count':preview_issues,
 'accept_provisional':False,
 'forecast_gate_status':status(remaining,preview_issues,False),
})
scenarios.append({
 'name':'after-apply-proposals-with-provisional-accept',
 'remaining_rows':remaining,
 'map_issue_count':preview_issues,
 'accept_provisional':True,
 'forecast_gate_status':status(remaining,preview_issues,True),
})

payload={
 'generated_at_utc':datetime.now(timezone.utc).isoformat(),
 'inputs':{
   'selected_rows':selected,'total_rows':total,'remaining_rows':remaining,
   'stat_pass':stat_pass,'no_fabrication_pass':no_fab,
   'current_map_issue_count':canon_issues,'preview_map_issue_count':preview_issues,
   'current_accept_provisional':accept,
 },
 'scenarios':scenarios
}
out_json.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

lines=['# E2R Gate Forecast','',f"Generated (UTC): `{payload['generated_at_utc']}`",'',
'| Scenario | Remaining | Map issues | Accept provisional | Forecast |','|---|---:|---:|:---:|---|']
for s in scenarios:
 lines.append(f"| {s['name']} | {s['remaining_rows']} | {s['map_issue_count']} | {str(s['accept_provisional'])} | **{s['forecast_gate_status']}** |")
lines += ['', 'Interpretation nhanh:', '- Nếu apply proposals và human bật accept provisional => có thể chuyển sang `ready-provisional-approved`.', '- Nếu không accept provisional thì vẫn blocked do còn 100 dòng chưa canonical.']
out_md.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('wrote',out_json)
print('wrote',out_md)
