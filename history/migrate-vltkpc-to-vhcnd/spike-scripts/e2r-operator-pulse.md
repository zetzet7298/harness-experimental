# E2R Operator Pulse

Generated (UTC): `2026-05-19T16:20:16.183670+00:00`

- Gate: **blocked**
- Bead mig-ja5: **in_progress**
- Map issues: **0**
- Remaining rows: **100**
- Accept provisional: **False**

## Preflight flags

- option_a_canonical_ready: `False`
- option_b_ready_to_finalize: `False`
- option_b_ready_to_request_human: `True`

## Next step

- label: **await-human-approval-then-finalize-provisional**
```bash
python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-finalize-provisional.py --human-approved --decided-by "<human>" --reason "Provisional accepted by human"
```

## Completion audit

- overall: **incomplete**
- blockers: `['R3', 'R4']`
