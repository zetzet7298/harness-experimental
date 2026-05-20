# Current Story Pack — S13 Smoke Loadout Visual Gate

**Feature:** full-equipment-system-port  
**Epic:** E4 Equipped visual parity pipeline  
**Mode:** `high_risk_feature`  
**Prepared after:** S12 review/compounding passed and pushed.

## Story Outcome

Make the user-specified smoke loadout visual gate source-backed and repeatable for: `Tu La phát kết` (head), `Giáng Sa bào` (body), and the Địch Khái staff/weapon item the user describes as `Địch Khái Lục Ngọc Trượng`. The gate must prove preview-passed visual SPR basenames, local copied source SPRs under `game-source`, no symlink/runtime VHCND dependency, and a clear blocker if current catalog identity/localization is wrong.

## Entry State

- Existing runtime visual assets and manifest include `equipped-current-catalog-mounted` with `passed-generated` status and local runtime PNG/JSON outputs.
- Existing `data/vltk-normalized/equipment-port-loadout.audit.json` records six copied smoke-set SPR basenames under `public/assets/character/vhcnd/source/smoke-3piece-tu-la-giang-sa-dich-khai/`.
- Current `src/data/equipmentCatalog.json` rows for `Tu La phát kết`, `Giáng Sa bào`, and the Địch Khái weapon have `visual.resolvedSprites: []` and `candidateStatus: missing-resource-resolution` / `missing-npcres-mapping`.
- `scripts/vltk-port-loadout.py --mode catalog-gate` default item ids are stale (`vhcnd-*-helm/armor/gold-*` ids no longer exist in the 9552-row generated catalog).
- Name-based selection of `Địch Khái Lục Ngọc Trượng` currently resolves a ring (`GoldItem.txt:97`) while the smoke weapon visual evidence and user intent point to the staff/weapon row (`GoldItem.txt:98`, inventory sprite `obj-staff13.spr`).

## Source / Local Evidence

- `public/assets/character/vhcnd/equipped-visual-manifest.json` — contains `passed-generated` entries including `equipped-current-catalog-mounted`.
- `data/vltk-normalized/equipment-port-loadout.audit.json` — existing local-copy audit for the smoke source folder.
- `src/data/equipmentCatalog.json` — current catalog item ids and visual fields.
- `scripts/vltk-port-loadout.py:31-36` — stale default catalog-gate ids.
- `scripts/README.md` and `docs/VHCND_SPR_PORTING_PLAYBOOK.md` — preview-gated local-copy rule; no runtime `/var/www/vhcnd`, no symlink.

## Acceptance Criteria

1. Smoke identity is corrected and documented: Tu La head row, Giáng Sa body row, and the correct Địch Khái staff/weapon row are selected by stable current catalog ids or source-backed aliases.
2. Catalog-gate mode no longer fails on stale default ids and no longer returns `required=0` for the smoke loadout.
3. Every copied source SPR needed by the smoke loadout exists under `public/assets/character/vhcnd/source/smoke-3piece-tu-la-giang-sa-dich-khai/` and is not a symlink.
4. Preview evidence for every copied basename is `passed` / `passed-generated`; unreviewed SPRs remain blocked.
5. The validation report names any remaining identity/localization ambiguity instead of silently treating a ring as the staff weapon.
6. Validation passes: catalog gate dry-run/apply, visual coverage audit for this loadout, symlink scan, runtime isolation, typecheck/build as needed, and browser screenshot if runtime visual wiring changes.

## Non-Goals

- Do not batch-port all equipment visuals in S13; S14/S16 own broad coverage.
- Do not wire unreviewed candidate SPRs.
- Do not use symlink or make runtime read `/var/www/vhcnd`.
- Do not fix unrelated gold-name localization rows unless they block the smoke identity.
