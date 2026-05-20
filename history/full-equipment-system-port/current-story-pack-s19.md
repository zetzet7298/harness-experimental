# Current Story Pack — S19 Full Validation Chain

**Feature:** full-equipment-system-port
**Epic:** E5 Isolation, validation, and release hygiene
**Mode:** `high_risk_feature`
**Prepared after:** S18 heavy artifact / gitignore policy passed and pushed.

## Story Outcome

Run the full current validation chain for the equipment-port state after S16-S18: TypeScript typecheck, property tests, runtime isolation, production build, GitNexus changed-scope check, and browser smoke on port `5173`.

## Acceptance Criteria

1. `npm run typecheck` passes.
2. `npm run test:pbt` passes.
3. `npm run check:no-runtime-vhcnd` passes.
4. `npm run build` passes.
5. GitNexus `detect_changes` reports no unexpected uncommitted code changes.
6. Browser smoke on `http://127.0.0.1:5173` confirms Phaser game boot and active `EquipmentScene` without page errors.
7. Validation artifact records warnings separately from blockers.

## Non-Goals

- Do not change gameplay, data, formulas, visuals, or gitignore policy in S19.
- Do not treat non-failing bundler size warnings as blockers unless they break runtime behavior.

## Expected Files / Impact Surface

- `history/full-equipment-system-port/validation-s19.md`
- `history/full-equipment-system-port/review-report-s19.md`

## Planning Handoff

S19 is a validation-only slice. If all gates pass, proceed to S20 handoff/review pack.
