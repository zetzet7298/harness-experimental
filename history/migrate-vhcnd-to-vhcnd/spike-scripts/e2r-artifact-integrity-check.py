#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime, timezone

base = Path(__file__).resolve().parent
out_json = base / 'e2r-artifact-integrity-check.json'
out_md = base / 'e2r-artifact-integrity-check.md'

required = [
    'e2r-control-dashboard.md',
    'e2r-control-dashboard.json',
    'e2r-finalize-preflight.md',
    'e2r-finalize-preflight.json',
    'e2r-next-step.md',
    'e2r-next-step.json',
    'e2r-swarming-completion-audit.md',
    'e2r-swarming-completion-audit.json',
    'e2r-gate-decision-packet.md',
    'e2r-decision-simulation.md',
    'e2r-ready-for-human-approval.md',
    'e2r-operator-pulse.md',
    'e2r-operator-pulse.json',
    'e2r-approve-and-finalize.py',
    'e2r-finalize-and-audit.py',
    'e2r-close-mig-ja5.py',
]

checks=[]
missing=[]
for name in required:
    p=base/name
    ok=p.exists()
    checks.append({'artifact':name,'exists':ok})
    if not ok:
        missing.append(name)

root_bundle = Path('history/migrate-vhcnd-to-vhcnd/e2r-operator-evidence-bundle.md')
bundle_exists = root_bundle.exists()
if not bundle_exists:
    missing.append(str(root_bundle))

status='pass' if not missing else 'fail'
payload={
    'generated_at_utc': datetime.now(timezone.utc).isoformat(),
    'status': status,
    'required_count': len(required)+1,
    'missing_count': len(missing),
    'missing': missing,
    'checks': checks,
    'bundle_exists': bundle_exists
}
out_json.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

lines=[
    '# E2R Artifact Integrity Check','',
    f"Generated (UTC): `{payload['generated_at_utc']}`",'',
    f"- Status: **{status}**",
    f"- Missing count: **{len(missing)}**",'',
    '| Artifact | Exists |','|---|:---:|'
]
for c in checks:
    lines.append(f"| `{c['artifact']}` | {'✅' if c['exists'] else '❌'} |")
lines.append(f"| `history/migrate-vhcnd-to-vhcnd/e2r-operator-evidence-bundle.md` | {'✅' if bundle_exists else '❌'} |")
if missing:
    lines += ['', '## Missing', ''] + [f"- `{m}`" for m in missing]
out_md.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(f"integrity_status={status} missing={len(missing)}")
print(f"wrote {out_json}")
print(f"wrote {out_md}")
