# Current Story Pack — S17 Reference / Runtime Isolation Audit

**Feature:** full-equipment-system-port
**Epic:** E5 Isolation, validation, and release hygiene
**Mode:** `high_risk_feature`
**Prepared after:** S16 review/compounding passed and pushed.

## Story Outcome

Re-scan active project instructions, repo-local `.codex` skills, H5 docs/scripts, and runtime folders to prove the current equipment-port workflow no longer depends on the old PC source name, `/var/www/vltkunity`, direct runtime reads from `/var/www/vhcnd`, or symlinked runtime assets. Produce an explicit "cần xử lý tiếp" list if any active reference remains.

## Entry State

- `CONTEXT.md` D1 requires VHCND as the canonical PC source and disallows new references to the old source name.
- `CONTEXT.md` D2 requires runtime assets/data to live in `game-source`, with no direct `/var/www/vhcnd` runtime reads and no symlinks to out-of-scope roots.
- Earlier migration history may contain archival references to old roots as evidence, but active docs/skills/scripts must not instruct new agents to use them.
- `game-source` already has `npm run check:no-runtime-vhcnd` for runtime `src/` and `public/` isolation.

## Acceptance Criteria

1. Active harness instructions/docs/`.codex` skills and active game-source docs/scripts do not contain `vltkpc`, `vltk-pc`, `/var/www/vltkpc`, or `/var/www/vltk-pc`.
2. Active harness instructions/docs/`.codex` skills and active game-source docs/scripts do not instruct using `/var/www/vltkunity`.
3. `game-source/src` and `game-source/public` contain no `/var/www/vhcnd`, old source root, or `/var/www/vltkunity` literals.
4. `game-source/src` and `game-source/public` contain no symlinks.
5. `npm run check:no-runtime-vhcnd` passes.
6. Validation artifact includes a concrete "cần xử lý tiếp" list.

## Non-Goals

- Do not rewrite archival migration history merely because it mentions old roots as historical evidence.
- Do not remove build-time audit scripts that intentionally read `/var/www/vhcnd` as source evidence; only runtime wiring is forbidden.
- Do not change catalog/formula/visual behavior in S17.

## Expected Files / Impact Surface

- `history/full-equipment-system-port/validation-s17.md`
- optional documentation clarifications only if active forbidden references are found.

## Planning Handoff

S17 is a direct audit slice. If validation finds no active forbidden references, no execution bead is required. If validation finds active forbidden references, create a focused remediation bead before closing S17.
