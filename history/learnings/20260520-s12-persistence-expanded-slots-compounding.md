---
date: 2026-05-20
feature: full-equipment-system-port
categories: [pattern, decision]
severity: standard
tags: [equipment, persistence, expanded-slots, tests]
---

# Learning: Expanded Slot Persistence Can Stay Version-Compatible When Slot Order Drives Shape

**Category:** decision
**Severity:** standard
**Tags:** [equipment, persistence, expanded-slots, tests]
**Applicable-when:** Future equipment slot/schema slices need to support older sparse saved loadouts while adding new optional slots.

## What Happened

S12 proved that the current `EQUIPMENT_STATE_VERSION = 1` shape can load sparse legacy payloads into the expanded 15-slot loadout without a version bump. The persistence code already iterates `EQUIPMENT_SLOT_ORDER` for empty loadout construction, sanitization, and saving; tests now cover legacy original-slot payloads, valid extended-slot ids, extended slot/item mismatch rejection, and extended-slot save JSON. Runtime logic did not need to change; the slice was a test/comment hardening pass with validation through typecheck, property tests, runtime isolation, build, GitNexus detect_changes, and browser smoke.

## Root Cause / Key Insight

The persisted schema is sparse (`Partial<Record<EquipmentSlot, string>>`) while the in-memory loadout is full (`Record<EquipmentSlot, string | null>`). That separation lets missing new slots naturally become `null`, so a migration framework or version bump would add risk without improving compatibility. The real failure mode was stale proof wording ("eleven slots") and missing extended-slot examples, not runtime behavior.

## Recommendation for Future Work

When adding optional equipment slots, first check whether the in-memory full-shape builder is driven by the canonical slot order. If it is, prefer compatibility tests for sparse old payloads and explicit new-slot round trips before changing persistence versions or adding migration code.
