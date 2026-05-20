---
date: 2026-05-20
feature: full-equipment-system-port
categories: [pattern, decision]
severity: standard
tags: [equipment-ui, tooltip, formatter-reuse, no-fabrication]
---

# Learning: Tooltip UI Should Reuse Source-Backed Formatters

**Category:** pattern  
**Severity:** standard  
**Tags:** [equipment-ui, tooltip, formatter-reuse, no-fabrication]  
**Applicable-when:** Future equipment UI work needs richer item text, popup hierarchy, or VLTK-style display formatting.

## What Happened

S10 improved the equipment popup by restructuring the body into VLTK-style grouped lines while preserving the existing equip/close flow. The implementation reused `SERIES_LABELS`, `formatEquipmentRequirement`, and `formatEquipmentAttributes` instead of adding new ad-hoc translation or option formatting in the scene. Static scene tests were updated to anchor both the visible hierarchy and the formatter calls.

## Root Cause / Key Insight

Equipment UI can easily drift into fabricated or inconsistent text if scene code formats each option manually. The domain label/formatter layer is the safer seam because it is already audited for observed catalog keys and can pair special cases such as weapon min/max ranges.

## Recommendation for Future Work

When improving equipment UI text, keep display hierarchy in the scene but keep option/requirement semantics in `equipmentLabels.ts`. Tests should assert both user-facing section labels and formatter reuse so future UI changes do not bypass source-backed formatting.
