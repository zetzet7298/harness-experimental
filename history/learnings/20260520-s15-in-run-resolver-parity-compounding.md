# Learning — S15 In-Run Resolver Parity

**Date:** 2026-05-20  
**Feature:** full-equipment-system-port  
**Story:** S15 In-Run Resolver Parity

## What changed

S15 added an inspectable, non-user-facing `GameScene.getEquipmentVisualResolverStatus()` seam so browser smoke can prove which visual resolver path was selected in-run. The canonical 3-piece loadout now asserts exact equipped ids, exact run/idle basenames, exact layered part filenames, and no audit/hard fallback.

## Durable lesson

A 3-piece smoke loadout without a horse should not be forced to match a whole-loadout manifest that includes horse parts. For this loadout, the correct runtime path is `parts`, not `manifest`, as long as dynamic part coverage is complete and preview-backed. Future visual tests should assert the resolver path implied by the equipped item set instead of assuming every smoke loadout must use a precomposed whole-loadout sheet.

## Critical promotions

None. This is useful context for E4 visual work, but not yet a repeated P1 failure pattern.
