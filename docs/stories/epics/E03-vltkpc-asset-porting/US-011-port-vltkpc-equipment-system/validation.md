# Validation

## Proof Strategy

Use source-backed smoke tests for catalog/slot/packet behavior, TypeScript checks for runtime integration, and Vite production build for bundle validity. Formula gaps remain explicit through `unsupportedAttributes` until PC parity evidence is added.

## Test Plan

| Layer | Cases |
| --- | --- |
| Unit | `tests/test_vltk_porting_smoke.py` verifies equipment catalog slot coverage, seed bag cell policy, source metadata, known gold item stats, source-backed blue/magic seed quality coverage, Vietnamese active-PAK equipment names, preview-gated current-loadout sheets, and manifest visual behavior. |
| Integration | `npm run typecheck` verifies generated JSON schema usage across domain, gateway, scenes, simulation, and HUD. |
| E2E | Browser smoke for equip/unequip/run handoff and current-loadout in-run visual sheet is recommended after visual runtime changes. |
| Platform | Portrait Phaser equipment scene and mobile one-cell bag policy are covered by implementation review and build. |
| Performance | `scripts/vltk-extract-required-sprs.py --workers auto` supports auto parallel copy work for long SPR extraction phases, and `scripts/vltk-run-equipment-visual-shard.py --workers auto` runs packet/extract/preview shard jobs and exposes compose commands only behind `--allow-compose` plus passed preview reports concurrently without composing or marking previews passed. |
| Logs/Audit | Not applicable; no backend persistence. |

## Fixtures

- `game-source/src/data/equipmentCatalog.json`
- `game-source/src/data/inventory.json`
- `game-source/src/data/profile.json`

## Commands

```text
python3 tests/test_vltk_porting_smoke.py
python3 -m py_compile scripts/vltk-extract-required-sprs.py scripts/vltk-normalize-equipment-index.py scripts/vltk-build-equipment-seed.py scripts/vltk-build-equipped-loadout-packet.py scripts/vltk-build-equipped-visual-loadout.py scripts/vltk-audit-equipment-visual-coverage.py scripts/vltk-audit-equipment-stat-coverage.py scripts/vltk-audit-equipment-quality-coverage.py scripts/vltk-fetch-vng-gold-name-sources.py scripts/vltk-audit-equipment-name-localization.py scripts/vltk-audit-equipment-label-coverage.py scripts/vltk-plan-equipment-visual-build.py scripts/vltk-build-equipment-visual-shard-jobs.py scripts/vltk-run-equipment-visual-shard.py scripts/vltk-plan-equipment-visual-parts.py scripts/vltk-build-equipment-visual-parts-packet.py scripts/vltk-export-equipment-visual-parts.py scripts/vltk-audit-equipment-visual-part-coverage.py scripts/port-vltkpc-equipped-character.py scripts/vltk-build-equipped-visual-manifest.py
python3 scripts/vltk-audit-equipment-stat-coverage.py --require-complete
python3 scripts/vltk-audit-equipment-quality-coverage.py --require-complete
python3 scripts/vltk-fetch-vng-gold-name-sources.py
python3 scripts/vltk-audit-equipment-name-localization.py --require-complete
python3 scripts/vltk-audit-equipment-label-coverage.py --require-complete
python3 scripts/vltk-build-equipment-icon-manifest.py
python3 scripts/vltk-audit-equipment-icon-coverage.py
python3 scripts/vltk-audit-equipment-formula-parity.py
python3 scripts/vltk-plan-equipment-visual-build.py --shards 32
python3 scripts/vltk-build-equipment-visual-shard-jobs.py --shard 0
python3 scripts/vltk-run-equipment-visual-shard.py --jobs data/vltk-normalized/equipment-visual-jobs/shard-000.json --start 2 --limit 2 --workers 2 --dry-run
python3 scripts/vltk-plan-equipment-visual-parts.py
python3 scripts/vltk-build-equipment-visual-parts-packet.py
python3 scripts/vltk-extract-required-sprs.py --packet data/vltk-normalized/port-packets/equipment-visual-parts-all.json --slug equipment-visual-parts-all --workers auto --extractor /var/www/vltk-h5-survivors/harness-experimental/.codex/skills/vltk-item-research/scripts/vltk_extract_tables.py
python3 scripts/vltk-export-equipment-visual-parts.py --workers auto
python3 scripts/vltk-audit-equipment-visual-part-coverage.py
npm run typecheck
npm run build
```

## Acceptance Evidence

- `python3 scripts/vltk-plan-equipment-visual-build.py --shards 32` passed on 2026-05-18 and produced `data/vltk-normalized/equipment-visual-build-plan.json` with 32 deterministic shards for `136,500` unique visual-signature combinations; `python3 scripts/vltk-build-equipment-visual-shard-jobs.py --shard 0` produced `data/vltk-normalized/equipment-visual-jobs/shard-000.json` with 4,266 preview-gated jobs with packet/extract/preview/compose commands, including the absolute local extractor path required for real SPR copy runs; `python3 scripts/vltk-run-equipment-visual-shard.py --jobs data/vltk-normalized/equipment-visual-jobs/shard-000.json --start 2 --limit 2 --workers 2 --dry-run` passed and proved the concurrent runner preserves the preview gate while reporting packet preview/runtime metadata updates.

- `python3 scripts/vltk-audit-equipment-visual-coverage.py --require-complete` intentionally exits non-zero on 2026-05-18 with combo gap `136,492`; brute-force combo precomposition is now documented as the fallback audit, not the intended completion path. `python3 scripts/vltk-plan-equipment-visual-parts.py` reports `273,000` brute-force run/idle combo sheets versus `278` unique dynamic part sheets (`~982x` reduction), and `python3 scripts/vltk-audit-equipment-visual-part-coverage.py` reports all dedicated part assets exported (`dedicatedPartAssetCountsByAction={run:139,idle:139}`, `remainingDedicatedPartAssetGap=0`) and `runtimeDynamicLayeringImplemented=true`, so the dynamic part-level visual path is complete.
- Real shard runs completed five packet/extract/preview pilots; the latest resumable command was `python3 scripts/vltk-run-equipment-visual-shard.py --jobs data/vltk-normalized/equipment-visual-jobs/shard-000.json --start 3 --limit 2 --workers 2 --keep-going` for pilots 000003-000004. Covered pilots: `equipment-visual-000000-chieu-da-ngoc-su-tu-ho-iep-song-ao-ao-khoac-cua-ao-si-bach-thuc-hoan`, `equipment-visual-000001-chieu-da-ngoc-su-tu-ho-iep-song-ao-ao-khoac-cua-ao-si-bat-quai-can`, `equipment-visual-000002-chieu-da-ngoc-su-tu-ho-iep-song-ao-ao-khoac-cua-ao-si-bo-can`, `equipment-visual-000003-chieu-da-ngoc-su-tu-ho-iep-song-ao-ao-khoac-cua-ao-si-huyen-sa-dien-trao`, and `equipment-visual-000004-chieu-da-ngoc-su-tu-ho-iep-song-ao-ao-khoac-cua-ao-si-khon-loc-mao`; run/idle previews were agent-reviewed to `passed`, matched 18/18 candidates, copied 9/9 SPRs with `missing=[]`, composed run/idle sheets, rebuilt the runtime manifest to 8 entries, and smoke-tested that the generated equipped item sprite sets match manifest entries used by `GameScene`.

- `python3 scripts/vltk-fetch-vng-gold-name-sources.py` captured 142 official VNG/Zing Hoàng Kim item-name evidence entries: 133 môn phái names from 10 school pages plus 9 supplemental An Bang/Định Quốc names into `data/vltk-normalized/vng-gold-equipment-name-sources.json`. `python3 scripts/vltk-build-gold-name-row-map.py` now verifies and applies all 171 GoldItem row mappings: 113 official VNG handbook rows, 13 official VNG/Zing supplemental rows, 6 official VNG CTC rows, and 39 local Vietnamese `goldequip.txt` row-evidence fallbacks in `data/vltk-normalized/localized-golditem-line-names.json`; `equipment-name-localization.audit.json` records `gold=171`, `cjkCanonicalNameCount=0`, `ambiguous=0`, `unmatched=0`, and `appliedToCatalog=true`.
- `python3 tests/test_vltk_porting_smoke.py` passed on 2026-05-18: 52 tests, including name-localization regression, Vietnamese attribute-label coverage/audit, equipment detail popup coverage, dynamic layered non-precomposed loadout coverage, and unique visual-signature gap coverage.
- `python3 scripts/vltk-build-equipment-icon-manifest.py` copied source-backed equipment icons and wrote `public/assets/equipment-icons/manifest.json`; `python3 scripts/vltk-audit-equipment-icon-coverage.py` passed with `total=1231`, `missing=0`, `missing_file=0`.
- `python3 scripts/vltk-audit-equipment-formula-parity.py` passed and confirms the H5 runtime no longer groups `magic_weapondamageenhance_p`, `magic_addphysicsdamage_p`, and `magic_physicsenhance_p` as one generic percent, no longer uses fixed `projectile.damage = skill.damage`, uses current derived stats for equipment requirements, and applies source `level_add.txt` vitality/energy HP/mana/stamina chaining.
- `npm run typecheck` passed on 2026-05-18.
- `npm run build` passed on 2026-05-18, with existing Vite chunk-size warning only.
- Headless Chrome screenshot `game-source/artifacts/screenshots/2026-05-18-equipment-icons-sprpng-fixed-30s.png` passed visual review for real equipment icons in the portrait bag grid after switching every item to `inventorySprite` SPR PNGs and direct `HTMLImageElement` texture registration.
