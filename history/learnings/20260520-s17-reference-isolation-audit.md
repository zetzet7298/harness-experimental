---
date: 2026-05-20
feature: full-equipment-system-port
categories: [pattern]
severity: standard
tags: [runtime-isolation, docs, skills, audit]
---

# Learning: Separate active routing references from archival migration evidence

**Category:** pattern
**Severity:** standard
**Tags:** [runtime-isolation, docs, skills, audit]
**Applicable-when:** Future agents scan for stale source roots or forbidden paths across both active instructions and historical Khuym artifacts.

## What Happened

S17 scanned active harness instructions/docs/`.codex` skills, active game-source docs/scripts, and runtime `src/` / `public/` folders for old PC source names, `/var/www/vltkunity`, runtime `/var/www/vhcnd` references, and symlinks. The active scope was clean, while archival files under `history/migrate-vhcnd-to-vhcnd/` still mention old roots as migration evidence.

## Root Cause / Key Insight

A repo-wide text search can mix active operational instructions with immutable historical evidence. Treating both categories the same would either create false-positive cleanup work or erase useful audit history.

## Recommendation for Future Work

When auditing stale source references, define the active scope first (`AGENTS.md`, `docs/`, repo-local `.codex/`, active `scripts/`, runtime `src/` and `public/`). Report archival `history/` hits separately and only rewrite them if a documented policy explicitly requires anonymizing historical evidence.
