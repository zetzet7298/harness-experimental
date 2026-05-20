# Learning — S6 Magic Attribute Parity Compounding

**Date:** 2026-05-20  
**Feature:** full-equipment-system-port  
**Story:** S6 magic attribute parity

## What Happened

The generated catalog had many `magic_unknown_*` keys because the seed builder carried a partial hard-coded `MAGIC_NAMES` map. Those unknowns made stat coverage look safer than it was: an unknown key could be exempted before anyone knew whether it was a real VHCND option.

S6 changed the source of key names to the active VHCND `KMagicAttrib.h` enum and added a dedicated audit that classifies every catalog attribute key as implemented, unsupported/deferred, unknown, or uncategorized.

## Durable Pattern

Do not let generated `unknown_*` names become acceptance placeholders. First map ids to the authoritative source enum/table; only then decide whether the runtime effect is implemented or explicitly blocked.

## Future Rule

Before S8 stat-vector parity can pass, every S6 `unsupported` key that affects player combat stats must either gain runtime semantics with source evidence or remain a documented blocker in the review report.
