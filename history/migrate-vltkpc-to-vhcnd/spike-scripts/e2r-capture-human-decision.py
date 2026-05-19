#!/usr/bin/env python3
import argparse, json
from pathlib import Path
from datetime import datetime, timezone

base = Path(__file__).resolve().parent
decision_file = base / 'e2r-gate-decision.json'
receipt_md = base / 'e2r-human-decision-receipt.md'
receipt_json = base / 'e2r-human-decision-receipt.json'

ap = argparse.ArgumentParser(description='Capture explicit human decision for E2R gate.')
ap.add_argument('--decided-by', required=True, help='Human approver identity')
ap.add_argument('--mode', choices=['accept-provisional','canonical-first'], required=True)
ap.add_argument('--note', default='', help='Optional note')
ap.add_argument('--apply', action='store_true', help='Write decision into e2r-gate-decision.json (default: preview only)')
args = ap.parse_args()

accept = args.mode == 'accept-provisional'
now = datetime.now(timezone.utc).isoformat()

payload = {
    'generated_at_utc': now,
    'decided_by': args.decided_by,
    'mode': args.mode,
    'accept_provisional_for_e_m3_to_e_m7': accept,
    'note': args.note,
    'applied': bool(args.apply),
}

if args.apply:
    d = json.loads(decision_file.read_text(encoding='utf-8')) if decision_file.exists() else {}
    d['accept_provisional_for_e_m3_to_e_m7'] = accept
    d['decided_by'] = args.decided_by
    d['decided_at'] = now
    d['decision_note'] = args.note or d.get('decision_note') or ('Approved provisional path for E_M3..E_M7 progression.' if accept else 'Require canonical completion before E_M3..E_M7.')
    decision_file.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

receipt_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
receipt_md.write_text(
    '# E2R Human Decision Receipt\n\n'
    f"- Generated (UTC): `{now}`\n"
    f"- Decided by: **{args.decided_by}**\n"
    f"- Mode: **{args.mode}**\n"
    f"- accept_provisional_for_e_m3_to_e_m7: **{accept}**\n"
    f"- Applied to decision file: **{bool(args.apply)}**\n"
    f"- Note: {args.note or '-'}\n",
    encoding='utf-8'
)

print(f"decision_mode={args.mode} accept={accept} applied={bool(args.apply)}")
print(f"wrote {receipt_json}")
print(f"wrote {receipt_md}")
