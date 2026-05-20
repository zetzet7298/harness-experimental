---
date: 2026-05-20
feature: full-equipment-system-port
categories: [pattern, decision, failure]
severity: standard
tags: [equipment, requirements, seed-coverage, audits, vhcnd]
---

# Learning: Requirement Parity Needs Catalog-Driven Coverage

**Category:** pattern  
**Severity:** standard  
**Tags:** [equipment, requirements, seed-coverage, audits, vhcnd]  
**Applicable-when:** Future stories add VHCND item/equipment rows, requirement keys, magic attributes, or generated runtime catalogs.

## What Happened

S7 validation found that the generated 9,552-item catalog already contained `magic_item_needreborn` and `magic_item_needtongban`, even though the old seed/label expectations only tracked the original eight requirement keys. `scripts/vltk-audit-equipment-label-coverage.py` failed on those two requirement labels, and the first requirement parity audit showed seed coverage did not count `inventory.bagItemIds`, so it underreported covered requirement keys.

## Root Cause / Key Insight

Static expected-key lists lag behind source-generated catalogs. For parity work, the generated runtime catalog is the concrete truth that must drive audits, labels, seed coverage, and fail-closed runtime handling; otherwise unsupported PC branches can become silently allowed or invisible in UI.

## Recommendation for Future Work

When a VHCND catalog/audit story introduces or regenerates source rows, first enumerate observed keys from `src/data/equipmentCatalog.json`, then update labels, runtime classification, and seed coverage from that observed set. Do not rely on old expected lists as proof that no new key is reachable.

---

# Learning: Fail-Closed Is Valid Only When Audited As Runtime Behavior

**Category:** decision  
**Severity:** standard  
**Tags:** [requirements, runtime, no-fabrication]  
**Applicable-when:** A VHCND source branch needs player state that the H5 runtime does not yet model.

## What Happened

VHCND `KItemList::EnoughAttrib` includes branches for skill, reborn, city/tong, and companion-slot gates. H5 currently lacks learned-skill, reborn-count, city/tong, and companion state, so S7 implemented explicit fail-closed runtime cases and Vietnamese labels instead of fabricating state or allowing the items.

## Root Cause / Key Insight

Exact parity does not mean inventing missing systems. Until the state model is ported, the safest source-compatible behavior is to deny requirements that cannot be evaluated and make that denial visible in popup/verdict text and audits.

## Recommendation for Future Work

When a source-backed requirement/effect depends on an unported H5 state system, add an explicit fail-closed runtime case, label it in Vietnamese, record the source branch in an audit, and defer full state-backed behavior to a dedicated story.

---

# Learning: Auto-Generated GitNexus AGENTS Blocks Can Clobber Workspace Routing

**Category:** failure  
**Severity:** standard  
**Tags:** [gitnexus, harness, workspace-routing]  
**Applicable-when:** GitNexus auto-analyze runs while editing harness docs or before commits.

## What Happened

During S7, GitNexus auto-analyze repeatedly rewrote the `<!-- gitnexus:start -->` block in `AGENTS.md` and created `CLAUDE.md`. That generated block removed the project-specific multi-repo routing instructions that distinguish harness, H5 game source, and VHCND source.

## Root Cause / Key Insight

Generic GitNexus onboarding text is not equivalent to this repo's specialized routing contract. The generated block is useful for simple repos, but here it can erase critical instructions that prevent agents from mixing `/var/www/vhcnd`, `/var/www/vltkunity`, harness, and game-source scopes.

## Recommendation for Future Work

Before any harness commit after GitNexus auto-analyze, inspect `git status` for `AGENTS.md` and `CLAUDE.md`. Revert generated routing changes unless the edit intentionally preserves the repo-specific VHCND/H5/harness routing block.
