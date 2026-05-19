#!/usr/bin/env python3
import argparse, csv, json
from pathlib import Path
from datetime import datetime, timezone

base = Path(__file__).resolve().parent
template = base / 'e2r-golditem-manual-map-template.csv'
proposals = base / 'e2r-golditem-selected-repair-proposals.csv'
out_report = base / 'e2r-golditem-apply-repair-report.json'

parser = argparse.ArgumentParser(description='Apply selected-line repair proposals into manual map template.')
parser.add_argument('--apply', action='store_true', help='Actually write changes to template (default: dry-run).')
args = parser.parse_args()

rows = list(csv.DictReader(template.open(newline='', encoding='utf-8')))
fields = list(rows[0].keys()) if rows else ['H5_ID','candidate_vhcnd_lines','selected_vhcnd_line','reviewer_note']
prop_rows = list(csv.DictReader(proposals.open(newline='', encoding='utf-8')))
prop = {r['H5_ID']: r for r in prop_rows}

changes = []
for r in rows:
    hid = r.get('H5_ID','')
    p = prop.get(hid)
    if not p:
        continue
    newv = (p.get('proposed_selected') or '').strip()
    if not newv:
        continue
    oldv = (r.get('selected_vhcnd_line') or '').strip()
    if oldv == newv:
        continue
    note_old = (r.get('reviewer_note') or '').strip()
    mark = f"AUTO-REPAIR:{oldv}->{newv} ({p.get('reason','')})"
    note_new = (note_old + ' | ' + mark).strip(' |') if note_old else mark
    changes.append({'H5_ID': hid, 'from': oldv, 'to': newv})
    if args.apply:
        r['selected_vhcnd_line'] = newv
        r['reviewer_note'] = note_new

if args.apply:
    with template.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)

report = {
    'generated_at_utc': datetime.now(timezone.utc).isoformat(),
    'mode': 'apply' if args.apply else 'dry-run',
    'template': str(template),
    'proposals': str(proposals),
    'change_count': len(changes),
    'changes_preview': changes[:100]
}
out_report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f"mode={report['mode']} change_count={len(changes)}")
print(f"wrote {out_report}")
