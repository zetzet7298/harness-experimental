---
date: 2026-05-20
feature: full-equipment-system-port
categories: [pattern, decision, failure]
severity: critical
tags: [equipment, visuals, catalog-identity, local-assets, browser-e2e]
---

# Learning: Visual Gates Must Repair Catalog Identity Before Copying SPRs

**Category:** pattern  
**Severity:** critical  
**Tags:** [equipment, visuals, catalog-identity, local-assets, browser-e2e]  
**Applicable-when:** Porting or validating equipped character visuals from VHCND catalog rows into H5 runtime assets.

## What Happened

S13 started with preview-passed smoke visual evidence, but the catalog gate still failed because its default ids were stale and the Vietnamese name `Địch Khái Lục Ngọc Trượng` resolved to a ring row instead of the user-intended staff/weapon row. The repair first mapped the three smoke examples to stable current catalog ids, documented row 97 as the ring, and only then copied the 12 HR01/RD01 SPRs into `game-source`. Validation combined catalog-gate dry-run/apply, dynamic part manifest regeneration, runtime-isolation checks, `$browser-navigation` on port 5173, and Playwright smoke.

## Root Cause / Key Insight

Equipment visual evidence is not enough when item identity is ambiguous. A passed SPR preview can still be wired to the wrong catalog row if name localization, gold-row mapping, or stale generated ids are not repaired first. The safe seam is: resolve catalog identity with source row/slot evidence → require passed preview evidence per basename → copy local sources into `game-source` → regenerate runtime manifests → run user-facing browser proof.

## Recommendation for Future Work

When porting VHCND equipment visuals, never use name search alone as the source of truth. Resolve item id, slot, `GoldItem`/table line, inventory sprite, and intended visual part before copying or wiring SPRs; if two rows share confusing names, document the non-target row explicitly so future gates cannot silently select it.
