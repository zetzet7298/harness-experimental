---
date: 2026-05-20
feature: full-equipment-system-port
categories: [pattern, decision]
severity: standard
tags: [equipment-ui, mobile-scroll, validation, browser-proof]
---

# Learning: Lock UI interaction changes with source contracts plus browser debug evidence

**Category:** pattern
**Severity:** standard
**Tags:** [equipment-ui, mobile-scroll, validation, browser-proof]
**Applicable-when:** Future equipment UI slices replace an existing interaction model, especially when canvas UI is hard to inspect through normal DOM assertions.

## What Happened

S16 replaced page-by-page equipment bag navigation in `src/game/scenes/EquipmentScene.ts` with hold/drag vertical scrolling and moved the item popup to viewport-center math. Property tests in `tests/properties/equipmentScene.unit.test.ts` were rewritten to reject the old pagination API (`bagPageCount`, `PAGE_SIZE`, `MAX_BAG_PAGES`, `pageIndicator`) and require scroll handlers, tap-vs-drag threshold, and centered-popup math. Browser proof on port `5173` used the scene debug getter to verify `bagOffset` changed from `0` to `10` after drag and `popupCentered: true` after tapping an item.

## Root Cause / Key Insight

Phaser/canvas UI changes are not reliably proven by DOM text snapshots alone. The robust proof combined source-contract tests for the static interaction invariants with a non-user-facing scene debug getter for runtime UAT, avoiding OCR or fragile canvas pixel assertions.

## Recommendation for Future Work

When changing canvas-only equipment UI behavior, pair source-contract property tests with a small non-user-facing debug getter that exposes the exact runtime invariant under test. Keep the debug getter limited to state already visible to the scene, and validate with `agent-browser` on port `5173` before claiming player-facing behavior is fixed.
