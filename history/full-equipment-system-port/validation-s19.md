# Validation — S19 Full Validation Chain

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Story:** `current-story-pack-s19.md`
**Result:** PASS

## Commands Run

From `/var/www/vltk-h5-survivors/game-source`:

```bash
npm run typecheck
npm run test:pbt
npm run check:no-runtime-vhcnd
npm run build
```

GitNexus:

```text
detect_changes(repo="vltk-h5-survivors", scope="all")
```

Browser smoke via `agent-browser` on `http://127.0.0.1:5173` with viewport `390x844`.

## Results

| Gate | Result | Evidence |
| --- | --- | --- |
| TypeScript | PASS | `tsc --noEmit` completed before property tests. |
| Property tests | PASS | `17 passed (17)` files, `239 passed (239)` tests. |
| Runtime isolation | PASS | `OK: runtime isolation clean (no /var/www/vhcnd literals and no symlinks under src/ or public/)`. |
| Production build | PASS | Vite build completed: `✓ built in 6.79s`. |
| GitNexus changed-scope | PASS | `changed_count: 0`, `affected_count: 0`, `risk_level: none`. |
| Browser smoke | PASS | `window.__vltkPrototype.game` exists; active scene list reports `EquipmentScene` active; screenshot saved `/tmp/s19-smoke-equipment.png`; page errors empty. |

## Non-Blocking Warnings

- Vite reported `dist/assets/index-*.js` is larger than 500 kB after minification (`17,035.42 kB`, gzip `931.24 kB`) and suggested code splitting / chunk warning tuning. This is not a functional blocker for S19, but it is relevant for future performance/release work.

## Decision

S19 validation chain passes. Continue to S20 handoff/review pack.
