#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime, timezone

base=Path(__file__).resolve().parent
out_json=base/'e2r-next-step.json'
out_md=base/'e2r-next-step.md'
preflight=base/'e2r-finalize-preflight.json'

def rj(p):
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding='utf-8'))

pf=rj(preflight)
cmd=''
label=''
if pf.get('option_a_canonical_ready'):
    label='canonical-close-now'
    cmd='python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-close-mig-ja5.py --confirm --reason "Canonical mapping completed" --append-verdict-note'
elif pf.get('option_b_ready_to_finalize'):
    label='provisional-close-now'
    cmd='python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-close-mig-ja5.py --confirm --reason "Provisional accepted by human" --append-verdict-note'
elif pf.get('option_b_ready_to_request_human'):
    label='await-human-approval-then-finalize-provisional'
    cmd='python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-finalize-provisional.py --human-approved --decided-by "<human>" --reason "Provisional accepted by human"'
else:
    label='continue-canonical-work'
    cmd='Hoàn tất canonical mapping rồi chạy: python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-run-option-a.py'

payload={
 'generated_at_utc':datetime.now(timezone.utc).isoformat(),
 'label':label,
 'command':cmd,
 'source_preflight':str(preflight),
 'facts':pf.get('facts',{})
}
out_json.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
out_md.write_text(
    '# E2R Next Step\n\n'
    f"Generated (UTC): `{payload['generated_at_utc']}`\n\n"
    f"- Label: **{label}**\n"
    f"- Command:\n\n```bash\n{cmd}\n```\n",encoding='utf-8')
print('wrote',out_json)
print('wrote',out_md)
print('next_label='+label)
print('next_cmd='+cmd)
