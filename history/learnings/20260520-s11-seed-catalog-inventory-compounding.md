---
date: 2026-05-20
feature: full-equipment-system-port
categories: [pattern, decision]
severity: standard
tags: [equipment, inventory, qa-catalog, browser-e2e, runtime-isolation]
---

# Learning: Keep QA Catalog Browsing Separate From Normal Seed Inventory

**Category:** pattern
**Severity:** standard
**Tags:** [equipment, inventory, qa-catalog, browser-e2e, runtime-isolation]
**Applicable-when:** Future equipment/UI slices need QA access to many generated VHCND rows without making the normal mobile bag huge or changing equip/stat semantics.

## What Happened

S11 added a mode toggle in `game-source/src/game/scenes/EquipmentScene.ts`: `Kho: Seed` keeps the bounded seed inventory, while `Kho: Catalog` sources the full generated catalog for the selected slot. Tests in `game-source/tests/properties/equipmentScene.unit.test.ts` mirror the private pagination/filter contracts so seed mode remains capped but catalog mode can page beyond five pages. Browser E2E on `http://127.0.0.1:5173` verified the user-facing canvas states: seed `1/1`, catalog `1/26`, next page `2/26`, and popup opening from a catalog item.

## Root Cause / Key Insight

The normal inventory and the QA catalog have conflicting UX requirements. Normal play needs a small phone-friendly seed bag, but port validation needs reachability for every generated item in a selected slot. Splitting the source mode solved the reachability problem without bloating `inventory.json`, changing item occupancy, or touching equip/stat formulas.

## Recommendation for Future Work

When a future slice needs broad QA reachability, add an explicit test/debug mode with visible labels and mode-specific tests instead of changing the normal gameplay data path. Always validate canvas-only UI changes with `$browser-navigation` screenshots on port `5173`, because source-level tests can prove contracts but not whether the Phaser canvas is actually user-facing and readable.
