# Spike verdict — name/hash lookup and vhcnd audit dry-run

Date: 2026-05-19
Bead: `mig-rls`
Feature: `migrate-vhcnd-to-vhcnd`
Epic: `E_M1+E_M2`

## 1. Question

Can the migration proceed from E_M1/E_M2 into E_M3..E_M7 using the current vhcnd layout and current H5 US-011 audit/catalog metadata?

The spike had two gate questions:

1. Does the full named SPR set have enough evidence that the engine FNV-1a path hash can map named assets to the hashed pak extract store?
2. Can the first ordered US-011 audit dry-run be rerouted to `/var/www/vhcnd/sources` without mutating canonical `game-source` audit outputs?

## 2. Method

Inputs reviewed:

- `history/migrate-vhcnd-to-vhcnd/CONTEXT.md`
- `history/migrate-vhcnd-to-vhcnd/approach.md`
- `history/migrate-vhcnd-to-vhcnd/feasibility-matrix.md`
- `history/migrate-vhcnd-to-vhcnd/spike-scripts/fnv1a-probe-summary.json`
- `history/migrate-vhcnd-to-vhcnd/spike-scripts/fnv1a-probe-evidence.md`
- `history/migrate-vhcnd-to-vhcnd/spike-scripts/audit-dryrun-summary.json`
- `history/migrate-vhcnd-to-vhcnd/spike-scripts/audit-dryrun-evidence.md`
- `history/migrate-vhcnd-to-vhcnd/spike-scripts/e1-acceptance-evidence.md`

The spike used existing E_M1 acceptance evidence, the full-set FNV-1a probe summary, and the first ordered US-011 audit dry-run. No `game-source` or `vhcnd` files were mutated by this synthesis.

## 3. E_M1 isolation result

E_M1 isolation passed:

- Zero `/var/www/vhcnd` refs were returned under `/var/www/vhcnd` in the E_M1 acceptance check.
- The moved horse SPR `/var/www/vhcnd/item_spr/spr/item/equip/horse/horse003.spr` resolved successfully.
- `python3 /var/www/vhcnd/tools/scan_required_spr.py` completed with the same baseline counts as the pre-move scan:
  - `totalRequired=335`
  - `missingCount=10`
  - `okCount=325`

This means the vltkunity coupling break and SPR scan baseline are acceptable for E_M1, but it does not prove the US-011 equipment catalog source metadata is compatible with vhcnd.

## 4. Hash probe result

Source: `spike-scripts/fnv1a-probe-summary.json` and `spike-scripts/fnv1a-probe-evidence.md`.

Full-set probe numbers:

- `total_named`: `15184`
- `total_variants`: `371604`
- `hash_store_count`: `33646`
- `matched_variants`: `6`
- `matched_named_paths`: `1`
- `verdict`: `engine_hash_lookup=matched`

Sample match:

- named path: `spr/obj/corpse/enemy123_die_corpse/frame_007.png`
- variant: `spr/obj/corpse/enemy123_die_corpse/frame_007.png`
- hash: `216d3fe2`
- matched hashed store path: `/var/www/vhcnd/datasets/data_cdn/pak_extract/data_cdn_pak_extract/image2/216d3fe2.spr`

Interpretation: the full-set pass found a real FNV-1a-style match, but only for 1 named path and 6 case/path variants. This is useful evidence that the hash route is not completely impossible, but it is not sufficient as the primary gate for proceeding. Per the feasibility matrix, the spike decision should be based on audit coverage rather than hash lookup coverage.

## 5. Audit dry-run result

Source: `spike-scripts/audit-dryrun-summary.json` and `spike-scripts/audit-dryrun-evidence.md`.

First audit attempted:

- script: `vltk-audit-equipment-stat-coverage.py`
- cwd: `/var/www/vltk-h5-survivors/game-source`
- command:

```sh
python3 scripts/vltk-audit-equipment-stat-coverage.py \
  --catalog src/data/equipmentCatalog.json \
  --source src/domain/equipment.ts \
  --out /var/www/vltk-h5-survivors/harness-experimental/history/migrate-vhcnd-to-vhcnd/spike-scripts/outputs/equipment-stat-coverage.audit.json \
  --vhcnd-root /var/www/vhcnd/sources
```

Result:

- exit code: `1`
- top-level audit status: `fail`
- `itemsChecked`: `1231`
- `mismatchCount`: `1231`
- `sourceLinesValid`: `0`
- `noFabricationStatus`: `fail`
- source root tried: `/var/www/vhcnd/sources`

Exact gap recorded in the summary:

> Rerouting `--vhcnd-root` to `/var/www/vhcnd/sources` fails because catalog `source.path` values are `Client/Settings/item/*.txt`, but vhcnd does not expose those files under `/var/www/vhcnd/sources/Client/Settings/item/`. All 1,231 source line checks are `source-file-unreadable`.

First observed source gaps include `Client/Settings/item/GoldItem.txt` rows with `reason: source-file-unreadable` and `fileLineCount: null`.

The vhcnd input probe confirms the mismatch:

- expected by current catalog but missing:
  - `/var/www/vhcnd/sources/Client/Settings/item/GoldItem.txt`
  - `/var/www/vhcnd/sources/Client/Settings/item/armor.txt`
  - `/var/www/vhcnd/sources/Client/Settings/item/ring.txt`
- known existing but different vhcnd layout:
  - `/var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/item/004/GoldItem.txt`
  - `/var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/vn/GoldItem.txt`

The remaining eight ordered audits were intentionally not attempted after this stop condition, because the first audit proved the catalog source metadata points at an unavailable layout.

## 6. Gap summary

- E_M1 isolation is acceptable: vhcnd no longer depends on `/var/www/vhcnd`, and the required SPR scan baseline remains `335/10/325`.
- Hash probing is partially positive but weak as a migration gate: 1 named path matched out of 15,184 named paths after 371,604 variants.
- The audit dry-run is a hard blocker: current H5 equipment catalog source-line metadata still points to the old `Client/Settings/item/*.txt` layout.
- vhcnd provides item table inputs under `ServerNew/_bin_v2_/gs/Settings/item/004/` and related `ServerNew/_bin_v2_/gs/Settings/vn/` layout, not the old catalog-relative `Client/Settings/item/` paths.
- Because all `1231/1231` source-line checks became `source-file-unreadable`, downstream E_M3..E_M7 work would be based on an invalid source provenance layer if planning continues unchanged.

## 7. Verdict

`no-go (re-plan)`

Reason: the audit dry-run failed immediately and completely on source provenance. The pipeline cannot safely proceed to E_M3..E_M7 until planning accounts for vhcnd's actual `ServerNew/_bin_v2_/gs/Settings/...` source layout and rebuilds/translates the equipment catalog source metadata accordingly.

## 8. Smallest remediation plan

Before E_M3..E_M7, planning should add a pre-rebrand remediation bead that:

1. Maps current catalog `source.path` values from `Client/Settings/item/*.txt` to the vhcnd `ServerNew/_bin_v2_/gs/Settings/item/004/` and related `ServerNew/_bin_v2_/gs/Settings/vn/` table layout.
2. Rebuilds or translates `equipmentCatalog.json` source metadata so source files are readable under `/var/www/vhcnd/sources`.
3. Reruns the first audit (`vltk-audit-equipment-stat-coverage.py`) with redirected output under harness history until source-line checks are meaningful rather than `source-file-unreadable`.
4. Only after the first audit proves source metadata compatibility, reruns the remaining US-011 audits in the ordered list.

## 9. Next action

Present this `no-go (re-plan)` verdict to the user. The spike halts the migration pipeline until planning re-shapes the work pack around the vhcnd ServerNew item-table layout and the user re-approves the next gate.
