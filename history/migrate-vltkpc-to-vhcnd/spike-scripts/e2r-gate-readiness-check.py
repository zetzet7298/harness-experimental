#!/usr/bin/env python3
import csv, json
from pathlib import Path
from datetime import datetime, timezone

base = Path(__file__).resolve().parent
out_json = base / 'e2r-gate-readiness.json'
out_md = base / 'e2r-gate-readiness.md'

# Inputs
manual_template = base / 'e2r-golditem-manual-map-template.csv'
stat_audit = base / 'outputs/e2r-equipment-stat-coverage.audit.json'
verdict_md = base.parent / 'e2r-verdict.md'
decision_file = base / 'e2r-gate-decision.json'

# default decision contract for human
if not decision_file.exists():
    decision_file.write_text(json.dumps({
        'accept_provisional_for_e_m3_to_e_m7': False,
        'decision_note': 'Set true only when human explicitly accepts provisional Gold mapping.',
        'decided_by': '',
        'decided_at': ''
    }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# Collect facts
rows = list(csv.DictReader(manual_template.open(newline='', encoding='utf-8')))
total = len(rows)
selected = sum(1 for r in rows if (r.get('selected_vhcnd_line') or '').strip())
remaining = total - selected

stat = json.loads(stat_audit.read_text(encoding='utf-8')) if stat_audit.exists() else {}
no_fab = ((stat.get('noFabricationCheck') or {}).get('status') == 'pass')
stat_top_pass = (stat.get('status') == 'pass')

decision = json.loads(decision_file.read_text(encoding='utf-8'))
accept_provisional = bool(decision.get('accept_provisional_for_e_m3_to_e_m7'))

canonical_ready = (remaining == 0 and stat_top_pass and no_fab)
provisional_ready = (remaining > 0 and stat_top_pass and no_fab and accept_provisional)

if canonical_ready:
    gate_status = 'ready-canonical'
elif provisional_ready:
    gate_status = 'ready-provisional-approved'
else:
    gate_status = 'blocked'

payload = {
    'generated_at_utc': datetime.now(timezone.utc).isoformat(),
    'gate_status': gate_status,
    'facts': {
        'selected_rows': selected,
        'total_rows': total,
        'remaining_rows': remaining,
        'stat_audit_status': stat.get('status'),
        'no_fabrication_status': (stat.get('noFabricationCheck') or {}).get('status'),
        'accept_provisional_for_e_m3_to_e_m7': accept_provisional,
    },
    'required_to_close_mig_ja5': {
        'path_a_canonical': [
            'remaining_rows == 0',
            'stat_audit_status == pass',
            'no_fabrication_status == pass'
        ],
        'path_b_provisional_acceptance': [
            'remaining_rows > 0',
            'stat_audit_status == pass',
            'no_fabrication_status == pass',
            'accept_provisional_for_e_m3_to_e_m7 == true (human decision)'
        ]
    }
}
out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

md = [
    '# E2R Gate Readiness Check',
    '',
    f"Generated (UTC): `{payload['generated_at_utc']}`",
    '',
    f"**Gate status:** `{gate_status}`",
    '',
    '## Facts',
    '',
    f"- Gold mapping selected: **{selected}/{total}** (remaining **{remaining}**)",
    f"- Stat audit status: **{payload['facts']['stat_audit_status']}**",
    f"- No-fabrication status: **{payload['facts']['no_fabrication_status']}**",
    f"- Human accepts provisional: **{accept_provisional}**",
    '',
    '## Close mig-ja5 when',
    '',
    '- Path A (canonical): remaining = 0 and audits pass.',
    '- Path B (provisional accepted): remaining > 0, audits pass, and human sets decision file to true.',
    '',
    '## Decision file',
    '',
    f'- `{decision_file}`',
]
out_md.write_text('\n'.join(md) + '\n', encoding='utf-8')

print(f'wrote {out_json}')
print(f'wrote {out_md}')
print(f'gate_status={gate_status}')
