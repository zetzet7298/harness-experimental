# Current Story Pack — S21 Equipment Visual Batch Preflight Repair

**Feature:** full-equipment-system-port
**Epic:** E4 Equipped visual parity pipeline
**Mode:** `high_risk_feature`
**Prepared after:** S20 handoff identified visual batch preview expansion as the next incomplete `CONTEXT.md` task.

## Story Outcome

Repair the current visual batch preflight tooling so it can safely generate shard jobs even when a visual slot has zero representatives in a freshly generated plan, and repair stale Python smoke expectations from S16 centered-popup work. This keeps the preview-gated batch path usable without bypassing item identity, preview, local-copy, or runtime-isolation rules.

## Entry State

- Existing tracked visual build plan can generate shard jobs and dry-run the preview runner.
- A freshly generated plan from current runtime catalog can have `horse: 0`, because only three preview-backed catalog rows are currently resolved.
- `scripts/vltk-build-equipment-visual-shard-jobs.py` crashed with `IndexError` when a slot representative list was empty.
- `tests/test_vltk_porting_smoke.py` still expected the pre-S16 lower anchored popup (`panelY = 342`).

## Acceptance Criteria

1. Empty visual slots in a plan no longer crash shard-job generation.
2. Shard jobs explicitly clear empty slots instead of accidentally inheriting seed inventory equipment.
3. `scripts/vltk-build-equipped-loadout-packet.py` supports `--clear-slot <slot>` for deterministic packet generation.
4. Python smoke tests cover the centered popup contract and empty-slot shard behavior.
5. Validation covers fresh-plan dry-run, existing-plan dry-run, Python smoke, typecheck, property tests, runtime isolation, build, and GitNexus changed-scope review.

## Non-Goals

- Do not mark new preview reports as passed automatically.
- Do not compose or wire new runtime sheets in S21.
- Do not claim full visual coverage; S21 only repairs the safe batch preflight path.

## Expected Files / Impact Surface

- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-build-equipped-loadout-packet.py`
- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-build-equipment-visual-shard-jobs.py`
- `/var/www/vltk-h5-survivors/game-source/tests/test_vltk_porting_smoke.py`
- `history/full-equipment-system-port/validation-s21.md`
- `history/full-equipment-system-port/review-report-s21.md`

## Planning Handoff

S21 is a bounded tooling repair. It unblocks future visual batch preview work but does not itself expand the preview-passed catalog coverage.
