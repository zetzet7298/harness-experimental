# Epic Map — migrate-vltkpc-to-vhcnd

> Mode: `high_risk_feature`. Shape: epic map (capability/risk areas), not phases.
> Read `CONTEXT.md` and `approach.md` first. Each epic is gated by validating.
> E_M1 and E_M2 have executed. E_M2 returned `no-go (re-plan)`, so E_M2R now gates the original E_M3..E_M7 rebrand sweep.

## Legend

- `entry` — what must already be true before the epic starts
- `exit` — concrete proof that lets the next epic start
- `risk` — the dominant risk class this epic absorbs
- `gating` — which validating gate this epic answers (Gate 3 unless noted)

---

## E_M1 — Disk migration: vltkunity → vhcnd

- **Capability:** make `/var/www/vhcnd/` the only canonical source-of-truth root by absorbing the four paths vhcnd currently borrows from vltkunity.
- **Entry:** D5/D6 locked; pre-migration snapshot is on `main`; filesystem identity confirmed (VQ-2).
- **Work:**
  - Move `/var/www/vltkunity/item_spr/` → `/var/www/vhcnd/item_spr/`.
  - Move `/var/www/vltkunity/item_spr_img/` → `/var/www/vhcnd/item_spr_img/`.
  - Move `/var/www/vltkunity/other-game/item_spr_like_img/` → `/var/www/vhcnd/other-game/item_spr_like_img/`.
  - Move (or recreate, since it is metadata-only) `/var/www/vltkunity/other-game/download-source/data_cdn_spr_img/` → `/var/www/vhcnd/other-game/download-source/data_cdn_spr_img/`.
  - Update `web/manifest.json`, `web/manifest_required_config_missing_only.{json,csv}`, `web/manifest_data_cdn_lite.json`, `web/manifest_downloads_like.json` so every `root` and `sprRoot` field starts with `/var/www/vhcnd/...`.
  - Update `tools/scan_required_spr.py` default `--spr-root` and `--config-dir` to point at vhcnd.
- **Exit:**
  - `rg /var/www/vltkunity /var/www/vhcnd` returns zero.
  - The four manifest `root`/`sprRoot` fields point at existing directories.
  - `python3 tools/scan_required_spr.py` runs and emits a fresh `manifest_required_config_scan.json` whose `missingCount` is recorded as the new baseline.
- **Risk absorbed:** R6 partial; surfaces R1 if missing count regresses.
- **Gating:** Gate 3.

---

## E_M2 — Feasibility spike: name↔hash and vhcnd asset coverage

- **Capability:** prove (or disprove) that vhcnd, post-move, has enough named assets and tables to run the existing US-011 audits without leaving any audit script unable to find inputs. Resolves CONTEXT.md OQ-1.
- **Entry:** E_M1 exit met.
- **Work:**
  - Compute engine FNV-1a (KStrBase.cpp:881-887, init=0, multiply-then-XOR) for every named SPR/PNG path under `vhcnd/item_spr/` and `vhcnd/item_spr_img/`. Record matches against on-disk hash files in `vhcnd/datasets/data_cdn/pak_extract/...`. Try `spr/...`, `Spr/...`, `\spr\...`, `Spr\...`, with and without leading slash, upper and lower case. Fail closed: if zero matches across all variants, the engine is reading data through a different mechanism (e.g., `KPakList::pFindElemFileA` may consume the full original filename via a different hash domain).
  - Run every existing US-011 audit (`scripts/vltk-audit-equipment-{stat,quality,series,visual,visual-part,formula-parity,label,name-localization,icon}-coverage.py`) with input roots rerouted to vhcnd. Capture each audit's exit code, missing counters, and output JSON. The point is to know the gap, not to fix it yet.
  - Identify any missing inputs the H5 pipeline cannot rebuild from vhcnd alone (e.g., decoded VNG gold-name evidence under `data/vltk-normalized/vng-gold-equipment-name-sources.json`, screen capture baselines, etc.).
- **Exit:**
  - Spike report at `history/migrate-vltkpc-to-vhcnd/spike-name-hash.md` with: hash mapping verdict, audit gap summary, go/no-go for E_M3..E_M7, and (if no-go) the smallest remediation plan.
  - User approval on the spike result before authorising E_M3.
- **Risk absorbed:** R1 (the dominant risk).
- **Gating:** spike result halts the pipeline if it fails; user re-approves before continuing.

---


## E_M2R — Source provenance remediation: vhcnd ServerNew layout

- **Capability:** make `src/data/equipmentCatalog.json` and the US-011 audit scripts use readable, non-`vltkpc`, non-`vltkunity` source provenance under `/var/www/vhcnd/sources` before any broad rebrand sweep.
- **Entry:** E_M1 accepted; E_M2 spike report says `no-go (re-plan)` specifically because all 1,231 catalog source-line checks are `source-file-unreadable` when `--vltkpc-root` is redirected to `/var/www/vhcnd/sources`.
- **Work:**
  - Map the 12 current catalog source files from `Client/Settings/item/*.txt` to vhcnd's real `ServerNew/_bin_v2_/gs/Settings/item/004/*.txt` and related `ServerNew/_bin_v2_/gs/Settings/vn/*.txt` layout.
  - Patch the no-fabrication audit path policy so vhcnd `ServerNew/...` source paths are accepted and old `Client/Settings/...` is no longer required for this migration path.
  - Translate or rebuild catalog `source.path` metadata so source files are readable under `/var/www/vhcnd/sources`; preserve `localizedSource` until a dedicated localization pass can safely map it.
  - Add row-identity evidence for a sample from every source file; do not rely only on line-count checks because GoldItem row layout differs between the old PC file and vhcnd `004/GoldItem.txt`.
  - Rerun the first stat audit and then the remaining ordered US-011 audits with output redirected under `history/migrate-vltkpc-to-vhcnd/spike-scripts/outputs/`.
- **Exit:**
  - First audit is no longer blocked by `source-file-unreadable`; `sourceLinesValid` is meaningful and the report records vhcnd source roots.
  - Remaining US-011 audits have been attempted in order, with pass/fail/gap details captured in a new E_M2R evidence report.
  - No runtime code reads from `/var/www/vltkpc` or `/var/www/vltkunity`; any source files needed for H5 provenance are copied/translated into game-source artifacts or read from `/var/www/vhcnd` only during tooling.
- **Risk absorbed:** source provenance correctness; prevents a cosmetic rebrand from hiding invalid audit evidence.
- **Gating:** Gate 3. If row-identity evidence cannot be established, return to planning before E_M3.

---

## E_M3 — Harness rebrand

- **Capability:** make the agent harness say `vhcnd` everywhere it now says `vltkpc`, including epic folder structure, AGENTS.md routing, decision records, and skill SKILL.md files.
- **Entry:** E_M2R exit accepted.
- **Work:**
  - Rewrite the 38 harness files from the scout (AGENTS.md, README.md, docs/HARNESS.md, docs/product/*, docs/decisions/0004, docs/stories/backlog.md, docs/stories/epics/E03-vltkpc-asset-porting/*, docs/validation/*.md, docs/TEST_MATRIX.md).
  - Rename `docs/stories/epics/E03-vltkpc-asset-porting/` to `docs/stories/epics/E03-vhcnd-asset-porting/` and rewrite epic README.
  - Decide US-IDs for existing implemented stories under E03: keep IDs (US-003, US-006..US-011) and just rename the epic, since renumbering would break TEST_MATRIX evidence rows.
  - Rebrand the four `.codex/skills/vltk-{item-research, skill-porting, map-porting, spr-porting}/` references to vhcnd. Decide skill rename or keep as `vltk-*` since they cover VLTK family generally; default = keep skill names, change inner references only.
  - Add a new ADR `docs/decisions/0005-vhcnd-canonical-source.md` recording D3..D6.
  - Add a new story packet under the renamed epic for this migration (story slug `migrate-vltkpc-to-vhcnd`) once beads are scheduled.
  - Update `docs/HARNESS_BACKLOG.md` if any harness improvements surface.
- **Exit:** `git ls-files | xargs grep -l vltkpc` in harness-experimental returns zero (excluding history snapshots that intentionally retain old names).
- **Risk absorbed:** none new; mechanical.
- **Gating:** Gate 3.

---

## E_M4 — Game-source rebrand: out-of-scope paths

- **Capability:** make every game-source script and config that previously read `/var/www/vltkpc/...` read from the corresponding vhcnd location.
- **Entry:** E_M2 go and E_M3 in flight or done.
- **Work:**
  - Centralise vhcnd paths in one Python module (e.g., `scripts/_vhcnd_paths.py`) keyed by intent: `ITEM_TABLES_ROOT`, `GOLDITEM_TABLE`, `LEVEL_ADD_TABLE`, `ENGINE_SOURCE_ROOT`, `NAMED_SPR_ROOT`, `NAMED_PNG_ROOT`, `HASH_SPR_ROOT`. This protects R3 (split table layout).
  - Rewrite each script that hardcodes `/var/www/vltkpc/...` to import the new module.
  - Rename and update `scripts/check-no-runtime-vltkpc.sh` → `scripts/check-no-runtime-vhcnd.sh`. Update its needle, its message, and every doc/CI/validation file that references the old name.
- **Exit:** `rg /var/www/vltkpc /var/www/vltk-h5-survivors/game-source` returns zero; `python3 -m py_compile scripts/*.py` passes.
- **Risk absorbed:** R3, R5.
- **Gating:** Gate 3.

---

## E_M5 — Game-source rebrand: internal identifiers and runtime

- **Capability:** rename internal paths, asset keys, animation prefixes, and the localStorage key so the runtime no longer says `vltkpc` anywhere.
- **Entry:** E_M4 done.
- **Work:**
  - Rename directories: `public/assets/character/vltkpc/` → `vhcnd/`, `public/assets/skills/vltkpc/` → `vhcnd/`, `public/assets/maps/vltkpc/` → `vhcnd/`. Update every `fetch('/assets/...')` call in `src/game/scenes/*.ts` and every script that writes there.
  - Rename animation prefix templates `player-run-mounted-vltkpc-h{H}-a{A}` → `player-run-mounted-vhcnd-h{H}-a{A}`. Update the prefix-generating code in `GameScene.ts` and any animation registry.
  - Migrate localStorage key `vltkpc-wardrobe-selection-v1` → `vhcnd-wardrobe-selection-v1`. Implement a one-shot shim that reads the old key on boot, writes the new one, and deletes the old. Default = include the shim. (R4.)
  - Rename asset keys (`vltkpc-equipped-tu-la-...`), file slug fields in port packets and audits where `vltkpc` appears in slug strings, and update generators so freshly produced packets use the new slug.
  - Update `playerSheet` constant in `src/game/constants.ts`.
- **Exit:** `rg vltkpc /var/www/vltk-h5-survivors/game-source` returns zero; `npm run typecheck` and `npm run build` pass.
- **Risk absorbed:** R4.
- **Gating:** Gate 3.

---

## E_M6 — Validation regen and TEST_MATRIX sync

- **Capability:** prove the rebrand did not break any previously-passing US-011 evidence. Restore green status row by row.
- **Entry:** E_M5 done.
- **Work:**
  - Rebuild manifests against the renamed asset roots: `equipped-visual-manifest.json`, `equipment-visual-parts-manifest.json`, `equipment-icons/manifest.json`.
  - Re-run the Python smoke test, every audit script, and the byte-identical catalog rebuild assertion.
  - Re-run `npm run typecheck`, `npm run build`, `npm run test:pbt`.
  - Regenerate the Playwright baseline with `npm run test:smoke -- --update-snapshots`. Surface the new PNG to the user for visual review (R2 — anti-pattern: silent regen).
  - Update `docs/TEST_MATRIX.md` evidence column on every row whose paths or commands changed.
  - Write a new validation report at `docs/validation/2026-MM-DD-vhcnd-rebrand.md` with all command outputs and pass/fail counts.
- **Exit:** every previously `implemented` row in TEST_MATRIX is still `implemented`, with vhcnd-rooted evidence; the new validation report is committed.
- **Risk absorbed:** R2.
- **Gating:** Gate 3 plus user visual review of the regenerated baseline.

---

## E_M7 — GitNexus, group alias, and isolation proof

- **Capability:** make tooling discovery match the new naming and prove `/var/www/vltkunity/` is no longer required by anything in the migrated surfaces.
- **Entry:** E_M6 done.
- **Work:**
  - Re-register or rename the gitnexus repo: per D3 default, `vltkpc` → `vhcnd`. Game-source repo decision deferred pending OQ-3 (rename `vltk-h5-survivors` to `vhcnd-h5-survivors` is implied but not yet locked; planning records this as an open question).
  - Refresh `gitnexus analyze /var/www/vhcnd --name vhcnd --force --no-stats`.
  - Refresh group `gitnexus group sync ...` after deciding `@vltk-porting` → `@vhcnd-porting` rename or split.
  - Final isolation probe: `rg /var/www/vltkunity` and `rg /var/www/vltkpc` across `/var/www/vhcnd`, `/var/www/vltk-h5-survivors/harness-experimental`, `/var/www/vltk-h5-survivors/game-source`. Both must return zero. Record the proof in the validation report.
  - Update AGENTS.md routing in harness to reflect the final repo names.
- **Exit:** isolation probe is zero; `gitnexus_query` returns results from the renamed repo.
- **Risk absorbed:** finality (no orphan refs).
- **Gating:** Gate 3.

---

## Open questions still to lock with the user

- **OQ-3 (now needs lock):** Should the gitnexus repo for game-source also rename from `vltk-h5-survivors` to `vhcnd-h5-survivors`? D3 says rebrand triệt để, but the underlying GitHub repo is `zetzet7298/vltk-h5-survivors` which is a separate rename concern.
- **OQ-4:** Is the existing US-004 ("Import Real VLTK Tables") subsumed by this migration, or does it remain a separate story?
- **OQ-5:** Should `.codex/skills/vltk-*` skills be renamed to `.codex/skills/vhcnd-*`, or stay as the VLTK-family generic name and only change inner references?

These do not block planning approval; they will be locked before the affected
epic begins.

## Bead policy

No beads are created during planning. Beads are created after E_M2 (the spike)
returns go and validating accepts feasibility for E_M1+E_M3..E_M7. E_M1 may be
authorised first as its own bead set since it is a prerequisite for the spike.

## Approval requested

Approve this epic map. After approval, planning will produce only the current
work pack for E_M1 and E_M2 (the prerequisite move plus the gating spike),
without writing any beads for E_M3..E_M7 until the spike returns go.
