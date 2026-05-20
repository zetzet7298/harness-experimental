# Item, Equipment, Option, and Quality Schema

## Core Code Pivots

Use `srcwalk` to open these exact files when verifying behavior:

- `KBasPropTbl.CPP` - reads item tables and `magicattrib.txt`.
- `KBasPropTbl.h` - table structs and classified magic-index tables.
- `KItemGenerator.CPP` - generates base equipment and magic options.
- `KItem.cpp` - applies base, requirement, and magic attributes.
- `KItem.h` - equipment detail enums and quality enum.
- `ScriptFuns.cpp` - `AddItem(...)` script API.
- `KMagicAttrib.h` + `KMagicDesc.cpp` - magic attrib ids and effect key names.

## Equipment Detail Enum

From `KItem.h`:

```text
equip_meleeweapon = 0
equip_rangeweapon = 1
equip_armor       = 2
equip_ring        = 3
equip_amulet      = 4
equip_boots       = 5
equip_belt        = 6
equip_helm        = 7
equip_cuff        = 8
equip_pendant     = 9
equip_horse       = 10
```

## Quality Enum

From `KItem.h`:

```text
equip_normal = 0  normal equipment, no generated magic option
equip_magic  = 1  magic equipment, roughly 1-2 prefix/suffix options
equip_rare   = 2  rare equipment, roughly 3-6 prefix/suffix options
equip_unique = 3  unique equipment
equip_set    = 4  set equipment
equip_gold   = 5  gold equipment from GoldItem.txt
```

The quality enum exists, but generated option count is controlled by the six `nGeneratorLevel` values passed into generation or stored on the item.

## Base Equipment Table Columns

`KBPT_Equipment::LoadRecord` maps normal equipment rows:

1. name
2. item genre
3. detail type
4. particular type
5. image/sprite path
6. object index
7. width
8. height
9. intro/description
10. series
11. price
12. item level
13. stack flag
14-34. seven base attributes: each `type, min, max`
35-46. six requirement attributes: each `type, value`

Common base/require magic ids from `KMagicDesc.cpp`:

```text
28 weapondamagemin_v
29 weapondamagemax_v
30 armordefense_v
31 durability_v
32 requirestr
33 requiredex
34 requirevit
35 requireeng
36 requirelevel
37 requireseries
38 requiresex
39 requiremenpai
```

For sex requirement, `0` is male and `1` is female in `KMagicDesc.cpp` display logic.

## GoldItem Table

`KBPT_Equipment_Gold::LoadRecord` uses the same common/base/require shape as normal equipment, plus fixed magic attribute indices and set id. Use `GoldItem.txt` when an item is hoàng kim or when a gold row shares the same sprite/detail as a normal item.

Important: Gold option indices usually refer to rows in `magicattrib.txt`; check whether the index is treated as table row number or zero-based code in the current code path before finalizing exact option labels.

## Magic Option Table

`magicattrib.txt` columns loaded by `KBPT_MagicAttrib_TF::LoadRecord`:

1. prefix/suffix name
2. pos: `1` prefix, `0` suffix
3. class/series requirement: `-1` or blank means all series; otherwise `0..4`
4. minimum magic level required
5. magic attrib id (`KMagicDesc.cpp` / `KMagicAttrib.h`)
6-11. three min/max value pairs
12. effect description
13-23. drop rates by equipment detail type (`0..10` from enum above)

Generation filters options by:

- prefix/suffix slot: `1 - (slot_index & 1)` in `KItemGenerator.CPP`.
- equipment detail type.
- item series.
- requested option level.
- drop-rate and luck.
- no duplicate `nPropKind` on the same generated item.

## AddItem Script API

`ScriptFuns.cpp` documents:

```text
AddItem(nItemClass, nDetailType, nParticualrType, nLevel, nSeries, nLuck, nItemLevel..6)
```

For equipment:

- `nItemClass=0` for `item_equip`.
- `nDetailType=7` for helm.
- `nParticularType` and `nLevel` locate row index as `particular * 10 + level - 1`.
- `nSeries` drives series-specific suffix options.
- `nLuck` improves the drop-rate threshold.
- `nItemLevel[0..5]` controls up to six generated magic options.
- If only one option level is passed, the code copies it to all six slots.

## Example: Tu La Phat Ket

After extracting and TCVN->UTF-8 conversion:

- Row file: `settings__item__helm.txt__update01.txt`
- Name: `Tu La phát kết`
- Detail: `equip_helm=7`
- Particular: `2`
- Level: `10`
- Sprite: `\spr\item\equip\cap\obj-ma-cap09-3.spr`
- Base: `armordefense_v=276`, `durability_v=30`
- Requirements: `requirelevel=60`, `requirestr=210`, `requiredex=110`, `requiresex=0`.

Generated helm options come from `magicattrib.txt` rows whose helm drop-rate column is non-zero, level requirement is less than or equal to the requested option level, and series matches the item series or all-series.
