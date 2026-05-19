#!/usr/bin/env python3
import csv, json, re
from pathlib import Path
from datetime import datetime, timezone

base = Path(__file__).resolve().parent
canonical = base / 'e2r-golditem-manual-map-template.csv'
proposals = base / 'e2r-golditem-selected-repair-proposals.csv'
preview = base / 'e2r-golditem-manual-map-template.preview.csv'
out_json = base / 'e2r-preview-repair-impact.json'
out_md = base / 'e2r-preview-repair-impact.md'

gold_file = Path('/var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/item/004/GoldItem.txt')
line_count = max(0, sum(1 for _ in gold_file.open('r', encoding='cp1258', errors='replace')) - 1) if gold_file.exists() else 0

rows = list(csv.DictReader(canonical.open(newline='', encoding='utf-8')))
fields = list(rows[0].keys())
props = {r['H5_ID']: r for r in csv.DictReader(proposals.open(newline='', encoding='utf-8'))}

applied = 0
for r in rows:
    p = props.get(r['H5_ID'])
    if not p:
        continue
    newv = (p.get('proposed_selected') or '').strip()
    if not newv:
        continue
    oldv = (r.get('selected_vhcnd_line') or '').strip()
    if oldv != newv:
        r['selected_vhcnd_line'] = newv
        applied += 1
        note = (r.get('reviewer_note') or '').strip()
        mark = f"PREVIEW-REPAIR:{oldv}->{newv}"
        r['reviewer_note'] = (note + ' | ' + mark).strip(' |') if note else mark

with preview.open('w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader(); w.writerows(rows)

# validate both canonical and preview

def validate(rows_):
    issues=[]
    selected=0
    for r in rows_:
        sid=(r.get('selected_vhcnd_line') or '').strip()
        if not sid:
            continue
        selected += 1
        if not sid.isdigit():
            issues.append('non-numeric'); continue
        n=int(sid)
        if n<1 or n>line_count:
            issues.append('out-of-range'); continue
        cand=(r.get('candidate_vhcnd_lines') or '').strip()
        if cand:
            cset={int(m.group(1)) for m in re.finditer(r'(\d+)\(', cand)}
            if cset and n not in cset:
                issues.append('not-in-candidate-list')
    return {'selected':selected,'issue_count':len(issues)}

canon_rows = list(csv.DictReader(canonical.open(newline='', encoding='utf-8')))
prev_rows = list(csv.DictReader(preview.open(newline='', encoding='utf-8')))
canon = validate(canon_rows)
prev = validate(prev_rows)

payload={
  'generated_at_utc': datetime.now(timezone.utc).isoformat(),
  'canonical_template': str(canonical),
  'preview_template': str(preview),
  'applied_changes_in_preview': applied,
  'canonical': canon,
  'preview': prev,
  'delta': {
      'issue_count': prev['issue_count']-canon['issue_count'],
      'selected': prev['selected']-canon['selected']
  }
}
out_json.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

md=[
'# E2R Preview Repair Impact',
'',
f"Generated (UTC): `{payload['generated_at_utc']}`",
'',
f"- Applied changes in preview: **{applied}**",
f"- Canonical issues: **{canon['issue_count']}**",
f"- Preview issues: **{prev['issue_count']}**",
f"- Delta issues: **{payload['delta']['issue_count']}**",
'',
'Preview only; canonical template was not modified.'
]
out_md.write_text('\n'.join(md)+'\n',encoding='utf-8')
print(json.dumps(payload,ensure_ascii=False))
