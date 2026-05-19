# Approach — migrate-vltkpc-to-vhcnd

> Read `CONTEXT.md` first. CONTEXT.md is source of truth.

## Repo reality (mapped during planning)

| Concern | vltkpc (current refs) | vhcnd (target) |
| --- | --- | --- |
| Item tables for tooling | `/var/www/vltkpc/extracted_build_jxwin_soucgoc_hoiquanvolam/source_from_vmdk/SourceNew/swrod3/bin/Client/Settings/item/*.txt` (42 flat files) | `/var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/item/*.txt` (49) and `004/*.txt` (67 files, GoldItem under `004/`). Layout is split across two directories, not a flat replacement. |
| Engine source for parity reads | `bin/Client/Classes/...` under vltkpc | `/var/www/vhcnd/sources/Client/Classes/...` |
| Named SPRs/PNGs | inside vltkpc Client tree | none on disk inside vhcnd; named SPRs live in vltkunity (`item_spr/`, `item_spr_img/`) and must be moved per D5/D6 |
| Hash SPRs (raw extracts) | n/a | 34,419 hash files under `/var/www/vhcnd/datasets/data_cdn/pak_extract/.../*.spr` |
| Engine name→hash | not used | engine FNV-1a custom (KStrBase.cpp:881-887, init=0, multiply-then-XOR-toupper); test of `horse003.spr` did not match any hash on disk under tested path variants |

The path map is not a string replace; tooling needs explicit path constants
keyed by intent (item tables, GoldItem table, engine source root, level_add).

## Path

The work splits into seven capability/risk areas. The order matters because
some areas invalidate evidence produced by earlier ones. The plan handles the
biggest unknown (asset coverage after vltkunity move) inside a feasibility
spike before authorising the rebrand sweep.

1. **E_M1 — Disk migration (vltkunity → vhcnd).** Move the four paths in D6
   from vltkunity into vhcnd at matching relative names, then update the four
   vhcnd `web/manifest*.json` `root`/`sprRoot` fields and the
   `tools/scan_required_spr.py` default `--spr-root`. Verify `tools/scan_required_spr.py`
   completes against the new root. Acceptance: zero vhcnd file references
   `/var/www/vltkunity/`; the four manifests resolve to existing files; the
   audit script reports the same or fewer missing SPRs as it did against
   vltkunity.

2. **E_M2 — Feasibility spike (OQ-1).** Decide whether the rebranded H5
   tooling can rely on the named SPRs in `vhcnd/item_spr` (post-move) and on
   the named tables in `vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/item/`,
   or whether a name→hash decoder is required. The spike (a) recomputes the
   engine FNV-1a hash for every named path under `vhcnd/item_spr` and looks
   for matches in `vhcnd/datasets/.../*.spr`, (b) re-runs the existing US-011
   audits against vhcnd-rooted inputs to measure the coverage gap, and
   (c) records the answer plus a go/no-go for E_M4. Spike failure halts the
   pipeline and returns to planning per khuym priority rule 5.

3. **E_M3 — Harness rebrand.** Rewrite `AGENTS.md`, `README.md`, `docs/HARNESS.md`,
   `docs/product/*.md`, `docs/decisions/0004-brownfield-h5-source-routing.md`,
   `docs/stories/backlog.md`, `docs/stories/epics/E03-vltkpc-asset-porting/*`,
   `docs/validation/*.md`, `docs/TEST_MATRIX.md` so that every textual occurrence
   of `vltkpc` becomes `vhcnd` (paths, repo names, group alias, story IDs only
   when an explicit decision authorises). Rename the epic folder
   `docs/stories/epics/E03-vltkpc-asset-porting/` to
   `docs/stories/epics/E03-vhcnd-asset-porting/`. Rebrand `.codex/skills/`
   subskills `vltk-item-research`, `vltk-skill-porting`, `vltk-map-porting`,
   `vltk-spr-porting`. Acceptance: harness-experimental contains zero
   `vltkpc` matches under `git ls-files`.

4. **E_M4 — Game-source rebrand: out-of-scope paths.** Replace every hardcoded
   `/var/www/vltkpc/...` constant in `scripts/*.py` and `scripts/*.sh` with a
   vhcnd path (using the path map above; not a flat string replace). Update
   `scripts/check-no-runtime-vltkpc.sh` needle and rename to
   `scripts/check-no-runtime-vhcnd.sh`. Update all `python3 -m py_compile`
   targets in story `execplan.md` accordingly. Acceptance: every script
   compiles, the smoke test still produces the same row counts in the
   normalized index, and `rg "/var/www/vltkpc"` returns zero.

5. **E_M5 — Game-source rebrand: internal identifiers.** Rename
   `public/assets/character/vltkpc/` → `public/assets/character/vhcnd/`,
   `public/assets/skills/vltkpc/` → `public/assets/skills/vhcnd/`,
   `public/assets/maps/vltkpc/` → `public/assets/maps/vhcnd/`. Update animation
   prefix templates `player-run-mounted-vltkpc-h{H}-a{A}` →
   `player-run-mounted-vhcnd-h{H}-a{A}`. Migrate localStorage key
   `vltkpc-wardrobe-selection-v1` → `vhcnd-wardrobe-selection-v1` with a
   one-shot read-from-old, write-to-new shim or a documented breaking change.
   Update asset key strings (`vltkpc-equipped-tu-la-...`), file slug fields in
   port packets/audits/manifests (`equipment-port-loadout.audit.json`, etc.),
   and the runtime guard `WARDROBE_PREF_KEY`. Acceptance: `rg vltkpc` in
   game-source returns zero matches; typecheck and build still pass.

6. **E_M6 — Validation regen.** Rebuild `equipped-visual-manifest.json` and
   `equipment-visual-parts-manifest.json` against the renamed asset folders,
   re-run `python3 scripts/vltk-build-equipment-icon-manifest.py` against the
   moved icon source, regenerate Playwright snapshot
   `tests/smoke/equipment-loadout.spec.ts-snapshots/equipment-loadout-3piece-chromium-linux.png`
   with `npm run test:smoke -- --update-snapshots`, re-run
   `python3 tests/test_vltk_porting_smoke.py`, `npm run typecheck`,
   `npm run build`, `npm run test:pbt`, and `npm run test:smoke`. Update
   `docs/TEST_MATRIX.md` evidence rows whose paths or commands changed.
   Acceptance: every previously-implemented row still says `implemented` with
   its evidence pointing at the new vhcnd-rooted artifacts.

7. **E_M7 — GitNexus, group, and final isolation proof.** Re-register the
   game source as gitnexus repo `vhcnd-h5-survivors` (subject to D3 — see
   open question), keep or rename `@vltk-porting` → `@vhcnd-porting`, refresh
   group sync, and prove `/var/www/vltkunity/` is no longer required by
   running `rg /var/www/vltkunity` across vhcnd, harness, and game-source.
   Acceptance: `rg vltkunity` returns zero across the three roots; gitnexus
   group answers a probe query for both members.

## Risks

- **R1 (high) — name→hash mapping unsolved.** OQ-1 says no path variant of
  `horse003.spr` matches an on-disk hash. If post-move named SPRs do not
  cover what runtime tooling needs, E_M4 cannot succeed. E_M2 spike must
  resolve this before E_M3..E_M7 are scheduled.
- **R2 (high) — Playwright baseline regen.** Renaming asset folders and
  animation prefixes invalidates the locked screenshot in
  `tests/smoke/.../equipment-loadout-3piece-chromium-linux.png`. The new
  baseline must be human-reviewed before marking US-011 evidence implemented
  again. Anti-patterns include silently regenerating without preview gate.
- **R3 (medium) — split table layout.** vhcnd splits item tables across the
  root `Settings/item/` and `004/` subdirectory, not a flat replacement. A
  bulk find-replace will silently miss `004/GoldItem.txt`. Path constants
  must be intent-keyed.
- **R4 (medium) — localStorage migration.** Existing local saves use the
  `vltkpc-wardrobe-selection-v1` key. Without a shim, players lose state
  on first launch after migration. Decide between a one-shot shim or an
  explicit breaking change record in `docs/decisions/`.
- **R5 (medium) — out-of-scope guard rename.** `scripts/check-no-runtime-vltkpc.sh`
  is referenced from CI hooks and validation reports. Renaming requires
  updating every reference, not just the file.
- **R6 (low) — encoding mismatch.** Sample reads of vhcnd item tables show
  CP-1258/Vietnamese-Windows encoding; existing tooling targeted GBK and
  CP-1258 mixed. Decoders may need a small fix when re-rooted, but this is
  bounded.

## Proof needs

- E_M1 acceptance — `tools/scan_required_spr.py --spr-root /var/www/vhcnd/item_spr` runs, missing-count delta vs vltkunity is recorded.
- E_M2 acceptance — written spike report at `history/migrate-vltkpc-to-vhcnd/spike-name-hash.md` with go/no-go and evidence.
- E_M3 acceptance — `rg vltkpc /var/www/vltk-h5-survivors/harness-experimental` returns zero.
- E_M4 acceptance — `rg /var/www/vltkpc /var/www/vltk-h5-survivors/game-source` returns zero, `python3 -m py_compile scripts/*.py` passes.
- E_M5 acceptance — `rg vltkpc /var/www/vltk-h5-survivors/game-source` returns zero, `npm run typecheck` and `npm run build` pass.
- E_M6 acceptance — every previously passing validation command from US-011 `execplan.md` passes against the new paths; Playwright baseline regenerated and recorded.
- E_M7 acceptance — `rg /var/www/vltkunity /var/www/vhcnd /var/www/vltk-h5-survivors` returns zero outside this CONTEXT.md and the migration story packet.

## Affected files (initial slice; refined per epic)

- harness-experimental: 38 files (scout count); plus the epic folder rename and the new story packet under `docs/stories/epics/E03-vhcnd-asset-porting/migrate-vltkpc-to-vhcnd/`.
- game-source: 430 files (scout count); plus directory renames under `public/assets/character/`, `public/assets/skills/`, `public/assets/maps/` and the snapshot regenerate.
- vhcnd: 5 manifest files in `web/`, 1 default in `tools/scan_required_spr.py`, optional AGENTS.md adjustment if it falsely claims `item_spr/` lives at vhcnd root.
- /var/www/vltkunity/: source filesystem; only the four moved paths are touched; the rest is untouched (out of scope for now).

## Validating questions for the validating skill

- VQ-1: Does the E_M2 spike resolve OQ-1 without requiring a name→hash decoder? If yes, beads for E_M3..E_M7 are authorised. If no, planning re-shapes E_M4 to plumb a decoder first.
- VQ-2: Has the disk-space headroom been measured? Free space on `/var/www` is 37 GB. The four paths move (rename, not copy) on the same filesystem, so the move is an inode rename and consumes no extra space. Validating must confirm the filesystem identity before executing the move.
- VQ-3: Are vhcnd manifest roots and the audit script the only consumers of vltkunity, or did the scout miss callers? Re-run `rg /var/www/vltkunity` across vhcnd, harness, and game-source as a final check before E_M1.
- VQ-4: Is there any branch protection, deploy hook, or external CI that would break when `/assets/character/vltkpc/` is renamed mid-flight? If yes, schedule E_M5 last.

---
Updated scope: added item_data/, downloads_spr_img_struct/, item_spr_like/ to E_M1.

---

## Post-E_M2 re-plan addendum — source provenance remediation

E_M2 has executed and returned `no-go (re-plan)`. The original E_M3..E_M7 order is therefore **paused** until a new remediation epic proves that H5 catalog provenance can be expressed against vhcnd's real `ServerNew/_bin_v2_/gs/Settings/...` layout.

### New inserted work: E_M2R — vhcnd source metadata remediation

This work sits between E_M2 and E_M3. It is not a broad rebrand sweep; it is a narrow provenance fix so the existing US-011 audit chain can read source files under `/var/www/vhcnd/sources` and produce meaningful source-line results.

Known evidence:

- Current catalog items: `1231`.
- Current catalog source paths: 12 distinct files under `Client/Settings/item/*.txt` (`GoldItem`, `armor`, `helm`, `meleeweapon`, `boot`, `horse`, `rangeweapon`, `amulet`, `belt`, `cuff`, `pendant`, `ring`).
- First E_M2 dry-run failed with `sourceLinesValid=0`, `mismatchCount=1231`, all due to `source-file-unreadable` under `/var/www/vhcnd/sources/Client/Settings/item/...`.
- vhcnd has candidate item tables under `ServerNew/_bin_v2_/gs/Settings/item/004/` and localization/name tables under `ServerNew/_bin_v2_/gs/Settings/vn/`.
- Simple line preservation is **not automatically safe**: for example, old `Client/Settings/item/GoldItem.txt:2` points at `梦龙法冠`, while vhcnd `item/004/GoldItem.txt` contains a different row layout around lines 2–3. The remediation must include a row-identity probe instead of only checking that line numbers are in range.

Recommended path:

1. Add a small source-path resolver/mapping in game-source tooling that can translate catalog provenance from old `Client/Settings/item/<file>.txt` to vhcnd-relative paths under `ServerNew/_bin_v2_/gs/Settings/item/004/<file>.txt` and, when needed for localized names, `ServerNew/_bin_v2_/gs/Settings/vn/<file>.txt`.
2. Patch `vltk-audit-equipment-stat-coverage.py` so the no-fabrication gate is not hard-coded to `SOURCE_PATH_PREFIX = 'Client/Settings/'`. It should accept vhcnd `ServerNew/_bin_v2_/gs/Settings/...` source paths and report the accepted prefix/path policy in the audit JSON.
3. Rebuild or translate `src/data/equipmentCatalog.json` source metadata so each item's `source.path` is readable beneath `/var/www/vhcnd/sources`; update stable ids/slugs only in a later rebrand epic unless validation proves ids must change here.
4. Add a verification probe that samples at least one item from every distinct source file and confirms the target row exists and is plausibly the same row (name/object sprite/detail fields where available). Line-count-only success is not enough for the planning gate.
5. Rerun the first US-011 stat audit redirected to harness outputs. Only if it no longer fails with `source-file-unreadable`, continue to the remaining ordered audits.

Rejected alternatives:

- **Proceed directly to E_M3:** rejected because the audit provenance layer is currently invalid for all 1,231 catalog items.
- **Flat string replace `Client/Settings/item` → `ServerNew/.../item/004`:** rejected because GoldItem evidence shows row layout/line semantics may differ.
- **Keep catalog provenance pointing at `/var/www/vltkpc`:** rejected by the user's isolation requirement and the final no-`vltkpc` invariant.

### Updated order

`E_M1` ✅ → `E_M2` ✅ no-go → **`E_M2R` validating/execution next** → `E_M3` harness rebrand → `E_M4` game-source hardcoded path rebrand → `E_M5` internal identifier rebrand → `E_M6` validation regen → `E_M7` GitNexus/isolation proof.
