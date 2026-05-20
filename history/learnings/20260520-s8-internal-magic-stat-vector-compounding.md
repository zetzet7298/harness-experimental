---
date: 2026-05-20
feature: full-equipment-system-port
categories: [pattern, decision, failure]
severity: standard
tags: [equipment, character-stats, audits, pbt, no-fabrication]
---

# Learning: CharacterStats Vector Changes Need Atomic Runtime, Fixture, and Audit Updates

**Category:** pattern  
**Severity:** standard  
**Tags:** [equipment, character-stats, audits, pbt, no-fabrication]  
**Applicable-when:** Future VHCND equipment stat stories add fields to `CharacterStats`, implement new `magic_*` runtime cases, or move unsupported keys to implemented.

## What Happened

S8 moved six internal magic damage keys from unsupported audit status into runtime support. The safe path required touching `src/domain/types.ts`, `emptyStats` defaults in `src/domain/equipment.ts`, `applyAttribute` runtime cases, generated magic/stat audit artifacts, source-backed unit fixtures, and PBT additive projections together. Validation had to include seed rebuild, magic/stat/requirement/label audits, typecheck, PBT, runtime isolation, and build because `CharacterStats` feeds equip snapshots and run-start flows.

## Root Cause / Key Insight

`CharacterStats` is a wide integration type, not a local implementation detail. Adding a field without updating defaults, test stubs, property projections, and generated parity audits can either break typecheck or create weaker evidence where a new stat exists but is not proven in the out-of-run/in-run aggregation path.

## Recommendation for Future Work

When adding any VHCND equipment stat vector field, update the full chain atomically: interface field, `emptyStats` default, `applyAttribute` mapping, source-backed fixture from real catalog rows, PBT/arbitrary coverage where the stat is additive, generated parity audits, and runtime isolation/build gates. Treat a green narrow unit test as insufficient unless the catalog-driven audit also moves the relevant observed key from unsupported to implemented.
