---
date: 2026-05-20
feature: full-equipment-system-port
categories: [pattern, failure]
severity: standard
tags: [equipment, visual-audit, tests, generated-catalog]
---

# Learning: Visual Coverage Needs Both Status Counts and Unsafe-Wiring Gates

**Category:** pattern  
**Severity:** standard  
**Tags:** [equipment, visual-audit, tests, generated-catalog]  
**Applicable-when:** Updating generated equipment catalog visuals or validating preview-gated runtime asset safety.

## What Happened

S14 found that existing visual tests still asserted stale 1231-row/136500-combination assumptions while the current generated catalog has 9552 rows and only three preview-passed resolved visual rows. The fix added `vltk-audit-equipment-visual-status.py`, which reports the full status distribution and fails only if a row is actually wired/resolved without passed preview evidence and local copied source SPRs. Python smoke tests were changed from stale fixed constants to current catalog-driven invariants.

## Root Cause / Key Insight

Coverage gaps and unsafe wiring are different states. Missing NpcRes/resource rows should stay visible in counts for future porting, but they should not fail a slice unless the runtime treats them as ready. Conversely, any `candidateSprite`/`resolvedSprites` row must be stricter than a count: every basename needs passed preview evidence and repo-local non-symlink source files.

## Recommendation for Future Work

When expanding visual coverage, separate "how much is missing" from "what is unsafe to run". Add a status-count audit for backlog planning and a fail-fast unsafe-wiring gate for runtime eligibility; keep tests derived from current generated catalog summaries instead of hardcoding old catalog sizes.
