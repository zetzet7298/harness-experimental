#!/usr/bin/env python3
import csv, json, re
from pathlib import Path
from datetime import datetime, timezone

base = Path(__file__).resolve().parent
template = base / 'e2r-golditem-manual-map-template.csv'
gold_file = Path('/var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/item/004/GoldItem.txt')
out_json = base / 'e2r-golditem-manual-map-validate.json'
out_md = base / 'e2r-golditem-manual-map-validate.md'

rows = list(csv.DictReader(template.open(newline='', encoding='utf-8')))
line_count = max(0, sum(1 for _ in gold_file.open('r', encoding='cp1258', errors='replace')) - 1) if gold_file.exists() else 0

issues = []
selected_count = 0
for r in rows:
    sid = (r.get('selected_vhcnd_line') or '').strip()
    if not sid:
        continue
    selected_count += 1
    if not sid.isdigit():
        issues.append({'H5_ID': r['H5_ID'], 'selected_vhcnd_line': sid, 'issue': 'non-numeric'})
        continue
    n = int(sid)
    if n < 1 or n > line_count:
        issues.append({'H5_ID': r['H5_ID'], 'selected_vhcnd_line': sid, 'issue': f'out-of-range-1..{line_count}'})

    cand = (r.get('candidate_vhcnd_lines') or '').strip()
    if cand:
        cand_lines = {int(m.group(1)) for m in re.finditer(r'(\d+)\(', cand)}
        if cand_lines and n not in cand_lines:
            issues.append({'H5_ID': r['H5_ID'], 'selected_vhcnd_line': sid, 'issue': 'not-in-candidate-list'})

payload = {
    'generated_at_utc': datetime.now(timezone.utc).isoformat(),
    'template_path': str(template),
    'golditem_path': str(gold_file),
    'golditem_data_line_count': line_count,
    'total_rows': len(rows),
    'selected_rows': selected_count,
    'missing_selected_rows': len(rows) - selected_count,
    'issue_count': len(issues),
    'issues': issues,
    'status': 'pass' if len(issues) == 0 else 'fail'
}
out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

md = [
    '# E2R GoldItem Manual Map Validation',
    '',
    f"Generated (UTC): `{payload['generated_at_utc']}`",
    '',
    f"- GoldItem data lines: **{line_count}**",
    f"- Selected rows: **{selected_count}/{len(rows)}**",
    f"- Missing selected: **{len(rows)-selected_count}**",
    f"- Issue count: **{len(issues)}**",
    f"- Status: **{payload['status']}**",
]
if issues:
    md += ['', '## Issues (first 50)', '', '| H5_ID | selected_vhcnd_line | issue |', '|---|---:|---|']
    for it in issues[:50]:
        md.append(f"| `{it['H5_ID']}` | {it['selected_vhcnd_line']} | {it['issue']} |")
else:
    md += ['', 'Không phát hiện lỗi định dạng/range/candidate trên các dòng đã chọn.']

out_md.write_text('\n'.join(md) + '\n', encoding='utf-8')
print(f"status={payload['status']} selected={selected_count}/{len(rows)} issues={len(issues)}")
print(f"wrote {out_json}")
print(f"wrote {out_md}")
