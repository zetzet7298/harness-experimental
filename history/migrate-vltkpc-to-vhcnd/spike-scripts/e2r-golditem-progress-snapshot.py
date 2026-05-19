#!/usr/bin/env python3
import csv, json
from pathlib import Path
from datetime import datetime, timezone

base = Path(__file__).resolve().parent
template = base / 'e2r-golditem-manual-map-template.csv'
checklists = {
    'easy': base / 'e2r-golditem-review-checklist-easy.md',
    'medium': base / 'e2r-golditem-review-checklist-medium.md',
    'hard': base / 'e2r-golditem-review-checklist-hard.md',
}
out_json = base / 'e2r-golditem-progress-snapshot.json'
out_md = base / 'e2r-golditem-progress-snapshot.md'

rows = list(csv.DictReader(template.open(newline='', encoding='utf-8')))
total = len(rows)
selected = sum(1 for r in rows if (r.get('selected_vhcnd_line') or '').strip())
remaining = total - selected

check = {}
for tier, p in checklists.items():
    txt = p.read_text(encoding='utf-8') if p.exists() else ''
    done = txt.count('| [x] |') + txt.count('| [X] |')
    open_ = txt.count('| [ ] |')
    check[tier] = {'done': done, 'open': open_, 'total': done + open_}

payload = {
    'generated_at_utc': datetime.now(timezone.utc).isoformat(),
    'template': {
        'path': str(template),
        'total_rows': total,
        'selected_rows': selected,
        'remaining_rows': remaining,
        'completion_pct': round((selected / total * 100.0), 2) if total else 0.0,
    },
    'checklists': check,
}
out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

lines = [
    '# E2R GoldItem Progress Snapshot',
    '',
    f"Generated (UTC): `{payload['generated_at_utc']}`",
    '',
    '## Canonical template progress',
    '',
    f"- Total rows: **{total}**",
    f"- Selected rows: **{selected}**",
    f"- Remaining rows: **{remaining}**",
    f"- Completion: **{payload['template']['completion_pct']}%**",
    '',
    '## Checklist progress',
    '',
    '| Batch | Done | Open | Total |',
    '|---|---:|---:|---:|',
]
for tier in ('easy','medium','hard'):
    t = check[tier]
    lines.append(f"| {tier} | {t['done']} | {t['open']} | {t['total']} |")

lines += [
    '',
    '## Refresh command',
    '',
    '```bash',
    'cd /var/www/vltk-h5-survivors/harness-experimental',
    'python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-golditem-progress-snapshot.py',
    '```',
]
out_md.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(f'wrote {out_json}')
print(f'wrote {out_md}')
