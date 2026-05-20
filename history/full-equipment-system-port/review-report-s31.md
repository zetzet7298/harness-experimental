# Review Report — S31 Missing Source Affected-Row Handling

**Date:** 2026-05-20
**Reviewer:** Codex local review
**Scope:** Affected catalog rows for 38 absent source SPRs, runtime unresolved handling, tests, and validation evidence.

## Verdict

PASS for this bounded fallback/unresolved handling slice. No P1/P2 blocker found.

## Checks

- No asset fabrication: affected rows keep original candidate/provenance and gain `missingSourceSprites`; no substitute SPRs were created.
- Runtime safety: both out-of-run preview and in-run resolver skip `missing-local-source-spr` rows, so absent part sheets are not requested.
- Evidence continuity: `equipment-visual-missing-impact.audit.json` ties 38 absent basenames to 182 affected catalog rows.
- Visual-status audit now separates `missing-local-source-spr` from ordinary candidates, preventing false progress claims.
- Validation covers runtime isolation, tests, build, browser smoke, and GitNexus changed-scope review.

## Remaining Work

Continue with the next Khuym story to reduce the remaining source-backed gaps: ordinary visual candidates still need preview/local-copy advancement, and `missing-npcres-mapping` / `missing-resource-resolution` rows still need table/resource investigation.
