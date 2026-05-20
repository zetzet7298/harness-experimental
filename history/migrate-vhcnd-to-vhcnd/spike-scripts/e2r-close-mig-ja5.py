#!/usr/bin/env python3
import argparse, json, subprocess
from pathlib import Path
from datetime import datetime, timezone

base = Path(__file__).resolve().parent
report = base / 'e2r-close-mig-ja5-report.json'
gate_json = base / 'e2r-gate-readiness.json'
verdict_md = base.parent / 'e2r-verdict.md'

ap = argparse.ArgumentParser(description='Safely close bead mig-ja5 only when gate is ready.')
ap.add_argument('--confirm', action='store_true', help='Required to perform close action')
ap.add_argument('--reason', default='Gate ready and decision packet executed', help='Close reason text')
ap.add_argument('--append-verdict-note', action='store_true', help='Append timestamped addendum into e2r-verdict.md')
args = ap.parse_args()

# refresh gate state first
subprocess.run(['python3', str(base / 'e2r-gate-readiness-check.py')], check=False, capture_output=True, text=True)

if not gate_json.exists():
    raise SystemExit('Missing e2r-gate-readiness.json')

gate = json.loads(gate_json.read_text(encoding='utf-8'))
status = gate.get('gate_status')
ready = status in ('ready-canonical', 'ready-provisional-approved')

payload = {
    'generated_at_utc': datetime.now(timezone.utc).isoformat(),
    'gate_status': status,
    'ready_to_close': ready,
    'confirm_flag': bool(args.confirm),
    'closed': False,
    'close_output': None,
}

if ready and args.confirm:
    cmd = ['bash', '-lc', f'cd /var/www/vltk-h5-survivors/harness-experimental && CI=1 br close mig-ja5 --reason "{args.reason}" --json']
    p = subprocess.run(cmd, capture_output=True, text=True)
    payload['closed'] = (p.returncode == 0)
    payload['close_output'] = {'exit_code': p.returncode, 'stdout': p.stdout[-1200:], 'stderr': p.stderr[-1200:]}

    if payload['closed'] and args.append_verdict_note:
        note = (
            f"\n\n## Gate close addendum ({datetime.now(timezone.utc).isoformat()})\n"
            f"- mig-ja5 closed\n- gate_status: `{status}`\n- close reason: {args.reason}\n"
        )
        verdict_md.write_text(verdict_md.read_text(encoding='utf-8') + note, encoding='utf-8')
else:
    payload['close_output'] = {
        'exit_code': None,
        'stdout': '',
        'stderr': 'Skipped close: gate not ready or --confirm not provided.'
    }

report.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f"gate_status={status} ready={ready} confirm={args.confirm} closed={payload['closed']}")
print(f"wrote {report}")
