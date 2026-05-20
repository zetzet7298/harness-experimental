# Current Story Pack — S10 VLTK-Style Equipment Tooltip

**Feature:** full-equipment-system-port  
**Epic:** E3 Portrait equipment UI + inventory/seed workflow  
**Mode:** `high_risk_feature`  
**Prepared after:** S8 review/compounding passed and pushed.

## Story Outcome

Upgrade the outside-run equipment detail popup so it reads like a compact VLTK equipment tooltip on a portrait/mobile screen: quality-colored title, level/series/durability/source metadata, explicit equip verdict, grouped requirements, grouped base attributes, grouped magic attributes, and visual candidate status. The popup must preserve the existing equip/close flow and must not calculate stats locally or fabricate unsupported option text.

## Entry State

- `EquipmentScene.showItemPopup` already opens a bottom sheet, shows icon/title/source/requirements/verdict/base/magic/visual fields, and wires `Mặc` / `Đóng` actions.
- Current popup is a plain text block and does not strongly mimic VLTK hierarchy: no Ngũ hành line, no durability line, no grouped section labels per attribute list, and it uses `formatEquipmentAttribute` one-by-one instead of `formatEquipmentAttributes`, so weapon min/max pairing can be less readable.
- `equipmentLabels.ts` already provides quality/series labels and attribute/requirement formatters; S10 should reuse those instead of adding new formula/translation logic.

## Source / Local Evidence

- `/var/www/vltk-h5-survivors/game-source/src/game/scenes/EquipmentScene.ts:433-477` — current popup implementation and action wiring.
- `/var/www/vltk-h5-survivors/game-source/src/domain/equipmentLabels.ts:343-393` — source-backed attribute formatting helpers, including weapon min/max range pairing.
- `/var/www/vltk-h5-survivors/game-source/tests/properties/equipmentScene.unit.test.ts:312-361` — current popup contract tests.
- GitNexus impact for `showItemPopup` reported LOW risk: direct caller `createBagGrid`, affected processes `create` and `createBagGrid` only.

## Acceptance Criteria

1. Popup title and border remain quality-colored and identify the quality tier (`Trắng`, `Xanh`, `Hoàng Kim`, etc.).
2. Popup body includes VLTK-style grouped sections:
   - `Môn phái/Vị trí` or slot metadata.
   - `Ngũ hành` using `SERIES_LABELS` when item series is known.
   - `Độ bền` from source item fields.
   - `Yêu cầu` formatted with `formatEquipmentRequirement`.
   - `Trạng thái mặc` with `Đủ điều kiện` or Vietnamese refusal reasons.
   - `Thuộc tính cơ bản` using `formatEquipmentAttributes`.
   - `Thuộc tính thêm` using `formatEquipmentAttributes`.
   - `Hiển thị` / visual candidate status.
3. Existing `Mặc` and `Đóng` buttons still call `equipSelected()` and `closeItemPopup()`.
4. Tests anchor the popup hierarchy and formatter usage so future regressions cannot flatten the popup back into an unstructured blob.
5. Validation passes: `npm run typecheck`, targeted equipment-scene unit tests, and `npm run check:no-runtime-vhcnd`.

## Non-Goals

- No new item formulas or attribute semantics.
- No browser screenshot requirement in this slice unless implementation changes runtime rendering beyond text/layout constants.
- No direct `/var/www/vhcnd` runtime reads and no symlinks.
