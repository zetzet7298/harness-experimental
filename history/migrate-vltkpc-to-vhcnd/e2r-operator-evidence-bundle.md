# E2R Operator Evidence Bundle

Generated (UTC): `2026-05-19T16:17:31.581160+00:00`

## Current status
- Gate: **blocked**
- Bead `mig-ja5`: **in_progress**
- Map issues: **0**
- Remaining rows: **100**
- Accept provisional: **False**
- Completion audit: **incomplete** (blockers: `['R3', 'R4']`)

## Recommended next command
```bash
python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-finalize-provisional.py --human-approved --decided-by "<human>" --reason "Provisional accepted by human"
```

## Evidence artifacts index
- Dashboard: `history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-control-dashboard.md`
- Pulse: `history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-operator-pulse.md`
- Preflight: `history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-finalize-preflight.md`
- Next step: `history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-next-step.md`
- Completion audit: `history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-swarming-completion-audit.md`
- Decision packet: `history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-gate-decision-packet.md`
- Decision simulation: `history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-decision-simulation.md`
- Human decision receipt: `history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-human-decision-receipt.md`
- Finalize handoff: `history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-ready-for-human-approval.md`

## Finalize command set (quick copy)
### Provisional
```bash
python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-approve-and-finalize.py   --decided-by "<human>"   --mode accept-provisional   --note "Provisional accepted by human"   --apply
```

### Canonical
```bash
python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-approve-and-finalize.py   --decided-by "<human>"   --mode canonical-first   --note "Canonical completion required"   --apply
```
