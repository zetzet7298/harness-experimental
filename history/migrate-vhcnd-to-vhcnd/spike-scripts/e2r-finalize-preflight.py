#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime, timezone

base = Path(__file__).resolve().parent
out_json = base / 'e2r-finalize-preflight.json'
out_md = base / 'e2r-finalize-preflight.md'

def read_json(p):
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding='utf-8'))
    except Exception:
        return {}

val = read_json(base / 'e2r-golditem-manual-map-validate.json')
gate = read_json(base / 'e2r-gate-readiness.json')
dec = read_json(base / 'e2r-gate-decision.json')

remaining = int(val.get('missing_selected_rows') or 0)
issues = int(val.get('issue_count') or 0)
stat_pass = (gate.get('facts') or {}).get('stat_audit_status') == 'pass'
no_fab = (gate.get('facts') or {}).get('no_fabrication_status') == 'pass'
accept = bool((gate.get('facts') or {}).get('accept_provisional_for_e_m3_to_e_m7')) or bool(dec.get('accept_provisional_for_e_m3_to_e_m7'))

option_a_ready = (remaining == 0 and issues == 0 and stat_pass and no_fab)
option_b_ready_to_finalize = (remaining > 0 and issues == 0 and stat_pass and no_fab and accept)
option_b_ready_to_request_human = (remaining > 0 and issues == 0 and stat_pass and no_fab and not accept)

payload = {
  'generated_at_utc': datetime.now(timezone.utc).isoformat(),
  'facts': {
    'remaining_rows': remaining,
    'issue_count': issues,
    'stat_pass': stat_pass,
    'no_fabrication_pass': no_fab,
    'accept_provisional': accept,
    'gate_status': gate.get('gate_status')
  },
  'option_a_canonical_ready': option_a_ready,
  'option_b_ready_to_finalize': option_b_ready_to_finalize,
  'option_b_ready_to_request_human': option_b_ready_to_request_human,
  'recommended_next_command': (
    'python3 history/migrate-vhcnd-to-vhcnd/spike-scripts/e2r-finalize-provisional.py --human-approved --decided-by "<human>" --reason "Provisional accepted by human"'
    if option_b_ready_to_request_human else
    'python3 history/migrate-vhcnd-to-vhcnd/spike-scripts/e2r-close-mig-ja5.py --confirm --reason "Canonical mapping completed" --append-verdict-note'
    if option_a_ready else
    'Continue canonical mapping or fix blockers before finalize'
  )
}
out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

lines = [
  '# E2R Finalize Preflight',
  '',
  f"Generated (UTC): `{payload['generated_at_utc']}`",
  '',
  f"- remaining_rows: **{remaining}**",
  f"- issue_count: **{issues}**",
  f"- stat_pass: **{stat_pass}**",
  f"- no_fabrication_pass: **{no_fab}**",
  f"- accept_provisional: **{accept}**",
  f"- gate_status: **{payload['facts']['gate_status']}**",
  '',
  f"- Option A canonical ready: **{option_a_ready}**",
  f"- Option B ready to finalize now: **{option_b_ready_to_finalize}**",
  f"- Option B ready to request human approval: **{option_b_ready_to_request_human}**",
  '',
  '## Recommended next command',
  '',
  f"`{payload['recommended_next_command']}`"
]
out_md.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('wrote', out_json)
print('wrote', out_md)
