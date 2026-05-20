# 2026-05-18 VHCND Equipment Formula/Icon Parity

## Scope

This validation records the follow-up parity pass after user review found the prior equipment slice still too heuristic for damage/stat formulas and inventory icons.

## Source Evidence Applied

- `vhcnd` `KItemList::GetWeaponDamage` is mirrored in H5: weapon base min/max plus only `magic_weapondamagemin_v`, `magic_weapondamagemax_v`, and `magic_weapondamageenhance_p`; no-weapon damage remains `curStrength / 5 + 1`.
- `vhcnd` `KPlayer::SetNpcPhysicsDamage` is mirrored for lực tay: melee weapons add `curStrength / 5`, ranged weapons add `curDexterity / 5`.
- `vhcnd` `KNpcAttribModify::AddPhysicsDamageP` is no longer treated as a global physical-damage percent; it now feeds melee/ranged/hand enhance buckets by weapon target.
- `vhcnd` `KNpc::AppendSkillEffect` is reflected by `resolveSkillDamage`: skill `magic_physicsenhance_p` applies to NPC physics damage plus current additional physical damage, then applies weapon-type enhance and source-backed elemental skill damage from skill port packets.
- `vhcnd` `KItemList::EnoughAttrib` is reflected by `canEquipItem`: strength/dexterity/vitality/energy requirements now use current derived equipment stats, not only base profile stats.
- `vhcnd` `KPlayer::ChangeCurVitality` and `ChangeCurEngergy` are reflected with active `level_add.txt` values: vitality chains into HP/stamina by series and energy chains into mana by series.
- Equipment icons are source-backed from `/var/www/vhst/backend/app/admin/static/equipment-icons/index.json`, matched by `inventorySprite` first and Vietnamese name second; remaining icon gaps are resolved from `/var/www/vhcnd/item_spr_img` PNGs generated from source item SPRs.

## Changed Files

- `game-source/src/domain/equipment.ts` adds PC-like weapon damage, lực tay, current add-physics, weapon-bucket enhance, and skill damage resolution.
- `game-source/src/domain/types.ts` adds icon and formula trace fields used by runtime/audits.
- `game-source/src/systems/simulation.ts` uses `resolveSkillDamage` instead of fixed `skill.damage` for projectile damage.
- `game-source/src/data/skills.json` carries level-20 source-backed formula fields from `data/vltk-normalized/port-packets/skill-*.json`.
- `game-source/scripts/vltk-build-equipment-icon-manifest.py` copies icon PNGs into H5 runtime assets and annotates every catalog item with icon metadata.
- `game-source/scripts/vltk-audit-equipment-icon-coverage.py` requires every catalog item to have an existing runtime icon file.
- `game-source/scripts/vltk-audit-equipment-formula-parity.py` blocks the old simplified formula grouping, fixed `skill.damage` path, missing current-stat requirement checks, and missing `level_add.txt` vitality/energy chaining.

## Commands Run

```text
python3 scripts/vltk-build-equipment-icon-manifest.py
python3 scripts/vltk-audit-equipment-icon-coverage.py
python3 scripts/vltk-audit-equipment-formula-parity.py
python3 tests/test_vltk_porting_smoke.py
npm run typecheck
npm run build
google-chrome --headless=new --disable-gpu --no-sandbox --virtual-time-budget=10000 --window-size=390,844 --screenshot=artifacts/screenshots/2026-05-18-equipment-icons-sprpng-fixed-30s.png http://127.0.0.1:4173/
```

## Results

- Icon coverage: `total=1231`, `missing=0`, `missing_file=0`, `empty_image=0`, `bad_thumbnail=0`; thumbnails are regenerated as centered 64x64 PNGs from `inventorySprite` SPR PNG sources with alpha crop, padding, and aspect-ratio preservation.
- Formula audit: PC weapon/stat/skill/current-requirement/LevelAdd seams present; old simplified grouping and fixed projectile damage path absent.
- Stat coverage audit: passed with `--require-complete`.
- Label coverage audit: passed with `--require-complete`.
- Smoke tests: 52 passed.
- Typecheck: passed.
- Build: passed; existing Vite chunk-size warning remains.
- Browser screenshot smoke: `game-source/artifacts/screenshots/2026-05-18-equipment-icons-sprpng-fixed-30s.png` shows real item icons in the portrait equipment bag grid after switching catalog icons to inventorySprite SPR PNGs.

## Remaining Notes

- This pass removes known invented formula shortcuts from the H5 runtime. Future magic enums or skill formula branches must still be researched from `vhcnd` before claiming 100% parity for newly added content.
- Full arbitrary visual combinations continue to use the dynamic layered route; this pass is specifically for equipment formula parity and inventory icon correctness.
