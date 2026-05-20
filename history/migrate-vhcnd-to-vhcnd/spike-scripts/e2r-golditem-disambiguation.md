# GoldItem Deterministic Disambiguation Strategy

## 1. Problem Statement
The VHCND GoldItem.txt source contains 5,945 rows, a significant expansion over the legacy source. Many items share identical identification keys:
- `(ItemGenre, DetailType, ParticularType, SpritePath)`
- Example: `An Bang Băng Tinh Thạch Hạng Liên` has 50+ matches in VHCND.

## 2. Methodology: Evidence-Backed Mapping
We performed a multi-pass algorithmic matching process between the 171 H5 Gold items and the VHCND source.

### Scoring Heuristics
1. **Identity (100 pts):** Matches `Genre`, `Detail`, `Particular`, and `SpritePath`.
2. **Sprite Substitution (80 pts):** Matches `Genre/Detail/Particular` but `SpritePath` differs slightly (e.g., `obj-ma-cap03-2.spr` vs `obj-ma-cap03-3.spr`).
3. **Series Match (30 pts):** Matches `nSeries`.
4. **Requirement Match (20 pts):** Proportional match of all `RequireType/Data` pairs.
5. **Magic Attribute Match (40 pts):** Proportional match of all `MagicType/Min/Max` triples.
6. **Provenance Boost (50 pts):** Match of `DefMagic1` (VHCND) against `SourceLine` (Legacy) when suspected as a legacy line index.

## 3. Findings & Decision

### Stats
- **Total H5 Gold Items:** 171
- **Algorithmic Confidence:**
  - **High:** 0 items (Due to exhaustive naming variations and sprite path versioning)
  - **Medium:** 22 items
  - **Unresolved:** 149 items (Score ties across multiple "Timed" vs "Permanent" vs "Enhanced" versions)

### Blocker Analysis
The `GoldItem.txt` in VHCND is not a simple expansion; it is a reorganized catalog.
- Many items have shifted Sprite versions (e.g., `-2.spr` -> `-3.spr`).
- Magic attributes in H5 are often resolved from `magicattrib.txt`, while VHCND GoldItem rows have hardcoded attribute indices that don't always align with the legacy H5 mapping.
- **Critical Ambiguity:** Even with magic stat matching, "Timed" vs "Permanent" items (identical stats, different name prefixes) create unsafe ties.

## 4. Required Action: Manual Mapping Artifact
Because algorithmic resolution yields **149/171 unresolved items** with safety ties, we must transition to a **Manual Mapping Artifact** provided by the developer or derived from a Vietnamese "Source Line" index.

**Blockers for [DONE]:**
- Algorithmic matching confidence is < 15%.
- Zero-tie requirement is not met.

## 5. Recommendation
**[BLOCKED]** - Do not proceed with automatic rebrand for Gold items. The E_M2R implementation must be paused until an explicit `line-to-line` map is provided for the 171 items.

Next step: Developer to provide a JSON mapping of `H5_ID -> VHCND_Line`.

---
*Created by Worker-E2R-GoldRescue*
