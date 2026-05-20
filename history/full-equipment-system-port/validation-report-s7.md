# Validation Report — S7 Equip Condition Parity

**Feature:** full-equipment-system-port  
**Mode:** `high_risk_feature`  
**Date:** 2026-05-20  
**Decision:** `READY WITH CONSTRAINTS — CREATE CURRENT-STORY BEADS`

## Reality Gate

S7 is valid and necessary. The current catalog now has 9,552 equipment items and contains VHCND requirement keys that H5 does not fully label or classify:

| Requirement key | Requirement rows | Items | Example source |
| --- | ---: | ---: | --- |
| `magic_item_needreborn` | 44 | 44 | `ServerNew/_bin_v2_/gs/Settings/item/004/GoldItem.txt:436` |
| `magic_item_needtongban` | 500 | 500 | `ServerNew/_bin_v2_/gs/Settings/item/004/ShiPin.txt:12` |
| `magic_requiredex` | 847 | 847 | `GoldItem.txt:23` |
| `magic_requirelevel` | 7613 | 7613 | `GoldItem.txt:2` |
| `magic_requiremenpai` | 4898 | 4898 | `GoldItem.txt:2` |
| `magic_requireseries` | 100 | 100 | `armor.txt:12` |
| `magic_requiresex` | 1036 | 1036 | `GoldItem.txt:188` |
| `magic_requirestr` | 1515 | 1515 | `GoldItem.txt:2` |

Validation contradicts any assumption that S7 can ignore unsupported PC requirement branches: `magic_item_needreborn` and `magic_item_needtongban` are present in runtime catalog data.

## Feasibility Matrix

| Assumption | Evidence | Result |
| --- | --- | --- |
| Catalog requirement keys can be enumerated deterministically. | Python probe over `src/data/equipmentCatalog.json` counted all requirement keys and examples. | PASS |
| Existing seed workflow still runs after S6/S7 entry. | `python3 scripts/vltk-build-equipment-seed.py` wrote 9,552 catalog items and 15 equipped slots. | PASS |
| Existing seed coverage can identify reachable requirement keys. | `python3 scripts/vltk-audit-equipment-seed-coverage.py` passed; it covers current expected keys but does not yet expect `magic_item_needreborn` / `magic_item_needtongban`. | PASS WITH GAP |
| Label coverage proves unsupported requirement keys are visible. | `python3 scripts/vltk-audit-equipment-label-coverage.py` failed with `requirementLabelMissing: ['magic_item_needreborn', 'magic_item_needtongban']`. | FAIL — must be fixed in S7 |
| Runtime condition parity can be bounded. | H5 `PlayerProfile` lacks reborn/companion state; VHCND `EnoughAttrib` has explicit branches. These can be fail-closed with source-backed audit first, then optionally state-backed later. | PASS WITH CONSTRAINT |

## Blocking Findings For Execution

1. `magic_item_needreborn` appears in the catalog and has no H5 requirement label/runtime parity audit classification.
2. `magic_item_needtongban` appears in the catalog and has no H5 requirement label/runtime parity audit classification.
3. Seed coverage currently reports only the original eight expected requirement keys, so S7 needs to update coverage/audit expectations without fabricating rows for absent keys.
4. The existing validation chain stopped at label coverage failure; PBT/typecheck/runtime isolation/build still need to be run after S7 fixes.

## Required Current-Story Beads

Validation accepts S7 feasibility if execution is split into current-story beads only:

1. **S7A requirement parity audit** — add deterministic source-backed audit for every catalog requirement key and classify implemented, fail-closed unsupported, missing label, missing seed coverage, and source enum id/name.
2. **S7B runtime/label fail-closed parity** — update `canEquipItem` / label formatting so observed unsupported VHCND requirement keys do not silently pass and show Vietnamese reasons.
3. **S7C validation and seed coverage** — update seed/label coverage expectations, regenerate audit artifacts/data if needed, and run the full command chain.

## Validation Commands Already Run

From `/var/www/vltk-h5-survivors/game-source`:

```bash
python3 scripts/vltk-build-equipment-seed.py
python3 scripts/vltk-audit-equipment-seed-coverage.py
python3 scripts/vltk-audit-equipment-label-coverage.py  # expected fail before S7 fixes
```

The label command failed exactly on the two S7 requirement gaps. That is an actionable validation result, not a tool failure.

## Execution Approval Scope

The validated work is S7 only: requirement parity audit, fail-closed requirement handling/labels, seed coverage updates, and validation artifacts. S7 must not implement portrait redesign, visual SPR porting, or full skill/reborn/companion systems beyond explicit fail-closed requirement semantics unless a source-backed catalog row forces a narrower state addition and tests prove it.
