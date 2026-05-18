# Porting Playbook

## 1. Resolve Active Data

1. Read `bin/Client/package.ini`.
2. Extract `\settings\Skills.txt`, `\settings\Missles.txt`, and the referenced `\script\skill\*.lua` with `--all-matches`.
3. Choose the first matching extracted file according to package order.
4. Record all duplicate skill names and explain which active row is used.

## 2. Build Evidence Map

Start by writing a one-skill profile for the exact target. Do not use a previous skill as the behavior template. A known-good port can guide process, but it cannot supply form/count/scale/assets unless the active PC rows prove reuse.

Create a table with source path, line, field, value, and H5 destination for:

- skill row identity and base fields
- missile row movement/asset fields
- missile status-to-AnimFile mapping from engine draw/load code
- source SPR dimensions, frame count, direction count, interval, and frame-compression method
- level script formulas at requested level
- engine enum/cast/movement formulas
- H5 runtime texture key, animation prefix, scale, and spawn/reference-point adapter notes
- explicit comparison against any similar existing H5 skill, with copied values marked forbidden unless source rows match

Do not edit H5 until this map is complete.

## 3. Patch Order

1. Update `skills.json` values and `sourcePath/sourceRow` to active evidence.
2. Update `types.ts` only for fields backed by evidence.
3. Update `simulation.ts` using exact engine formulas.
4. Extract/copy SPR/WAV into repo-local assets.
5. Compose runtime sprite metadata.
6. Generate all-directions/all-frames contact sheet before preview passes.
7. Update browser/runtime wiring with skill-specific texture key/prefix/scale.
8. Re-check spawn origin/reference point in H5 auto-target mode.

## 4. Validation

Run:

```bash
npm run typecheck
python3 tests/test_vltk_porting_smoke.py
npm run build
```

Add browser screenshot/video proof when projectile count, direction, animation, or SFX changes.

Visual proof must include:

- source SPR all-directions/all-frames contact sheet
- packet note proving which `AnimFile*` is flight vs impact/precast/end
- runtime screenshot after wiring, with enough scale to recognize the PC silhouette
- explicit note when H5 auto-targeting changes spawn/reference point compared with PC click targeting
