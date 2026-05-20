# Learning — S5 Formula Ledger Compounding

**Date:** 2026-05-20  
**Feature:** full-equipment-system-port  
**Story:** S5 formula ledger  
**Evidence:** `history/full-equipment-system-port/review-report-s5.md`

## What Happened

S5 found that the old formula audit was too weak: it passed because it searched for `PC_MAX_RESIST = 95` as a marker, even though active local VHCND source has `MAX_RESIST = 150` in `sources/Client/Classes/gamecore/GameDataDef.h:134`. The story replaced loose marker checking with a ledger-backed audit and reconciled H5 tests/code to the active VHCND value.

## Durable Pattern

Formula parity gates must validate source-backed ledger entries, not only search for a marker in H5 code. A stale marker can make a wrong constant look intentionally verified.

## Future Rule

For S6/S7/S8, every newly ported option, requirement, or stat vector must add a ledger/audit entry that verifies both sides:

1. VHCND source/table path + line or row marker.
2. H5 implementation marker or fixture expectation.
3. Explicit status (`matched`, `unsupported`, or blocked), with downstream stories failing on accidental omissions.

## Watchout

Changing source-backed constants can invalidate older invariants. S5 updated resist tests to preserve the raw PC attenuation formula rather than forcing a non-negative clamp that was not proven by source evidence.
