#!/usr/bin/env python3
import csv, json
from pathlib import Path
from datetime import datetime, timezone

base = Path(__file__).resolve().parent
history_dir = base / 'e2r-golditem-progress-history'
history_dir.mkdir(parents=True, exist_ok=True)

template = base / 'e2r-golditem-manual-map-template.csv'
checklists = {
    'easy': base / 'e2r-golditem-review-checklist-easy.md',
    'medium': base / 'e2r-golditem-review-checklist-medium.md',
    'hard': base / 'e2r-golditem-review-checklist-hard.md',
}
out_json = base / 'e2r-golditem-progress-snapshot.json'
out_md = base / 'e2r-golditem-progress-snapshot.md'
out_diff_md = base / 'e2r-golditem-progress-diff-latest.md'
out_diff_json = base / 'e2r-golditem-progress-diff-latest.json'


def read_snapshot(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return None

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

now = datetime.now(timezone.utc)
ts = now.strftime('%Y%m%dT%H%M%SZ')

payload = {
    'generated_at_utc': now.isoformat(),
    'snapshot_id': ts,
    'template': {
        'path': str(template),
        'total_rows': total,
        'selected_rows': selected,
        'remaining_rows': remaining,
        'completion_pct': round((selected / total * 100.0), 2) if total else 0.0,
    },
    'checklists': check,
}

# determine previous history snapshot before writing new one
history_files = sorted(history_dir.glob('snapshot-*.json'))
prev_path = history_files[-1] if history_files else None
prev = read_snapshot(prev_path) if prev_path else None

# write current snapshot (rolling + dated)
out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
(history_dir / f'snapshot-{ts}.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# rolling markdown snapshot
lines = [
    '# E2R GoldItem Progress Snapshot',
    '',
    f"Generated (UTC): `{payload['generated_at_utc']}`",
    f"Snapshot ID: `{payload['snapshot_id']}`",
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
for tier in ('easy', 'medium', 'hard'):
    t = check[tier]
    lines.append(f"| {tier} | {t['done']} | {t['open']} | {t['total']} |")

lines += [
    '',
    '## Refresh command',
    '',
    '```bash',
    'cd /var/www/vltk-h5-survivors/harness-experimental',
    'python3 history/migrate-vhcnd-to-vhcnd/spike-scripts/e2r-golditem-progress-snapshot.py',
    '```',
]
out_md.write_text('\n'.join(lines) + '\n', encoding='utf-8')

# compute diff vs previous history snapshot
if prev is None:
    diff = {
        'generated_at_utc': now.isoformat(),
        'current_snapshot_id': ts,
        'previous_snapshot_id': None,
        'note': 'No previous snapshot in history yet.',
        'delta': None,
    }
    diff_md = [
        '# E2R GoldItem Progress Diff (Latest)',
        '',
        f"Current snapshot: `{ts}`",
        '',
        'Không có snapshot trước đó để so sánh.',
    ]
else:
    delta_selected = selected - int(prev['template']['selected_rows'])
    delta_remaining = remaining - int(prev['template']['remaining_rows'])
    delta_pct = round(payload['template']['completion_pct'] - float(prev['template']['completion_pct']), 2)
    checklist_delta = {}
    for tier in ('easy', 'medium', 'hard'):
        checklist_delta[tier] = {
            'done_delta': check[tier]['done'] - int(prev['checklists'][tier]['done']),
            'open_delta': check[tier]['open'] - int(prev['checklists'][tier]['open']),
        }
    diff = {
        'generated_at_utc': now.isoformat(),
        'current_snapshot_id': ts,
        'previous_snapshot_id': prev.get('snapshot_id'),
        'delta': {
            'selected_rows': delta_selected,
            'remaining_rows': delta_remaining,
            'completion_pct': delta_pct,
            'checklists': checklist_delta,
        },
    }
    diff_md = [
        '# E2R GoldItem Progress Diff (Latest)',
        '',
        f"Current snapshot: `{ts}`",
        f"Previous snapshot: `{prev.get('snapshot_id')}`",
        '',
        '## Template delta',
        '',
        f"- Δ selected rows: **{delta_selected:+d}**",
        f"- Δ remaining rows: **{delta_remaining:+d}**",
        f"- Δ completion: **{delta_pct:+.2f}%**",
        '',
        '## Checklist delta',
        '',
        '| Batch | Δ done | Δ open |',
        '|---|---:|---:|',
    ]
    for tier in ('easy', 'medium', 'hard'):
        d = checklist_delta[tier]
        diff_md.append(f"| {tier} | {d['done_delta']:+d} | {d['open_delta']:+d} |")

out_diff_json.write_text(json.dumps(diff, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
out_diff_md.write_text('\n'.join(diff_md) + '\n', encoding='utf-8')

print(f'wrote {out_json}')
print(f'wrote {out_md}')
print(f'wrote {out_diff_json}')
print(f'wrote {out_diff_md}')
print(f'history dir: {history_dir}')
