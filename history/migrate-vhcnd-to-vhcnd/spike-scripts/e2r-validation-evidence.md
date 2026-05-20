# E_M2R Validation Evidence
## Reality gate
- Mode: `high_risk_feature` — PASS, because source provenance affects all 1,231 catalog items and gates broad rebrand.
- Current work: remediate vhcnd ServerNew source metadata before E_M3..E_M7.
- Repo fit: PASS. Target scripts and catalog exist in game-source; vhcnd source roots exist.
- Smaller path: PASS. The smallest safe path is a current-work chain starting with row-remap probe; broad rebrand remains gated.
- Proof surface: PASS. Evidence is command output and file probes captured in `e2r-validation-summary.json`.

## E2R-A1 source file inventory

| File | Items | 004 exists | 004 lines | Catalog max line | Covers | vn exists |
| --- | ---: | --- | ---: | ---: | --- | --- |
| `GoldItem.txt` | 171 | True | 6332 | 172 | True | True |
| `amulet.txt` | 40 | True | 22 | 21 | True | True |
| `armor.txt` | 280 | True | 292 | 141 | True | True |
| `belt.txt` | 40 | True | 22 | 21 | True | True |
| `boot.txt` | 80 | True | 42 | 41 | True | True |
| `cuff.txt` | 40 | True | 22 | 21 | True | True |
| `helm.txt` | 280 | True | 143 | 141 | True | True |
| `horse.txt` | 60 | True | 333 | 61 | True | True |
| `meleeweapon.txt` | 120 | True | 72 | 61 | True | True |
| `pendant.txt` | 40 | True | 22 | 21 | True | True |
| `rangeweapon.txt` | 60 | True | 32 | 31 | True | True |
| `ring.txt` | 20 | True | 12 | 11 | True | True |

Result: PASS for existence and line-count coverage across all 12 files.

## E2R-A2/E2R-A3 row identity/remap probe

| File | Items | Unique key matches | Ambiguous | No match |
| --- | ---: | ---: | ---: | ---: |
| `GoldItem.txt` | 171 | 12 | 146 | 13 |
| `amulet.txt` | 40 | 40 | 0 | 0 |
| `armor.txt` | 280 | 280 | 0 | 0 |
| `belt.txt` | 40 | 40 | 0 | 0 |
| `boot.txt` | 80 | 80 | 0 | 0 |
| `cuff.txt` | 40 | 40 | 0 | 0 |
| `helm.txt` | 280 | 280 | 0 | 0 |
| `horse.txt` | 60 | 60 | 0 | 0 |
| `meleeweapon.txt` | 120 | 120 | 0 | 0 |
| `pendant.txt` | 40 | 40 | 0 | 0 |
| `rangeweapon.txt` | 60 | 60 | 0 | 0 |
| `ring.txt` | 20 | 20 | 0 | 0 |

Interpretation:
- Non-GoldItem rows are feasible but must be remapped by row identity/key, not by preserving old line numbers.
- GoldItem remains the gating constraint: numeric/sprite key alone is insufficient (`12` unique, `146` ambiguous, `13` no-match). The first E_M2R bead must solve or block on GoldItem remapping before implementation beads run.

## E2R-A4 current stat audit blocker confirmation

- Command exit code: `1`
- noFabricationStatus: `fail`
- itemsChecked: `1231`
- sourceLinesValid: `0`
- mismatchCount: `1231`
- first mismatch reasons: `[('source-file-unreadable', 1231)]`

Result: PASS as a validating proof of the blocker. The failure is reproducible and specifically path-policy/source-path related before E_M2R implementation.

## Decision

`READY WITH CONSTRAINTS` for E_M2R execution beads. Constraints:

- Non-GoldItem rows are remappable by numeric/sprite key (1060/1060 unique across 11 files), but same-line preservation is not valid because vhcnd files include different/header rows.
- GoldItem cannot use numeric/sprite key alone: 12 unique, 146 ambiguous, 13 no-match among 171 items. First execution bead must produce deterministic GoldItem remap or stop before implementation.
- Current stat audit still fails as expected before E_M2R implementation: source-file-unreadable via Client/Settings/item/*.txt under /var/www/vhcnd/sources.

Only E_M2R beads may be created. E_M3..E_M7 remain gated.
