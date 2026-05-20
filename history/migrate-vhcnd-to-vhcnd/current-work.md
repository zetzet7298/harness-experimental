# Current Story Pack — E_M2R source provenance remediation

Epic: `E_M2R — Source provenance remediation: vhcnd ServerNew layout`
Mode: `high_risk_feature`

> This supersedes the previous E_M1+E_M2 current work pack. E_M1 and E_M2 are complete; E_M2 returned `no-go (re-plan)`. The next validation target is this remediation story only. Do not start E_M3..E_M7 until E_M2R passes and the user re-approves.

## Entry state

- `/var/www/vhcnd` is isolated from `/var/www/vhcnd` for the moved asset roots; E_M1 accepted.
- E_M2 spike report exists at `history/migrate-vhcnd-to-vhcnd/spike-name-hash.md` with verdict `no-go (re-plan)`.
- First US-011 dry-run attempted `vltk-audit-equipment-stat-coverage.py` with `--vhcnd-root /var/www/vhcnd/sources` and failed because catalog `source.path` values still point at `Client/Settings/item/*.txt`.
- Current catalog facts:
  - `src/data/equipmentCatalog.json` has `1231` items.
  - It uses 12 distinct `source.path` values: `GoldItem.txt`, `armor.txt`, `helm.txt`, `meleeweapon.txt`, `boot.txt`, `horse.txt`, `rangeweapon.txt`, `amulet.txt`, `belt.txt`, `cuff.txt`, `pendant.txt`, `ring.txt` under `Client/Settings/item/`.
  - vhcnd has corresponding files under `/var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/item/004/` and name/localization-side files under `/var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/vn/`.
- Existing stat audit hard-codes `SOURCE_PATH_PREFIX = 'Client/Settings/'`; that policy is incompatible with vhcnd provenance and must be changed or parameterized.

## Exit state

E_M2R is done only when all of the following are proven:

1. Catalog source metadata is readable through `/var/www/vhcnd/sources` without referring to `/var/www/vhcnd` or `/var/www/vhcnd`.
2. The stat audit's no-fabrication check accepts the vhcnd `ServerNew/_bin_v2_/gs/Settings/...` provenance policy and reports that policy in its JSON output.
3. The first audit no longer fails with `source-file-unreadable` for all items. If it still fails for row mismatches or true source gaps, those must be recorded as real gaps, not path-layout blockers.
4. At least one sampled item from each of the 12 source files has row-identity evidence (source file exists; line exists; row fields plausibly correspond to the catalog item). GoldItem requires special care because the vhcnd row layout differs around the first rows.
5. The remaining ordered US-011 audits are attempted after the first audit reaches meaningful source-line checks, with all outputs redirected under this feature's history folder.
6. E_M3..E_M7 remain unstarted; this story only clears the provenance blocker.

## Likely files touched during execution

Game source (`/var/www/vltk-h5-survivors/game-source`):

- `scripts/vltk-audit-equipment-stat-coverage.py`
- `scripts/vltk-normalize-equipment-index.py` or a small companion migration script if translating the existing catalog is safer than rebuilding it immediately
- `src/data/equipmentCatalog.json`
- Possibly `data/vltk-normalized/equipment-index.json` and `data/vltk-normalized/equipment-index.summary.json` if the catalog is rebuilt rather than patched

Harness evidence (`/var/www/vltk-h5-survivors/harness-experimental`):

- `history/migrate-vhcnd-to-vhcnd/spike-scripts/e2r-source-metadata-evidence.md`
- `history/migrate-vhcnd-to-vhcnd/spike-scripts/e2r-audit-summary.json`
- `history/migrate-vhcnd-to-vhcnd/spike-scripts/outputs/*.audit.json`
- `.beads/issues.jsonl` only after validating accepts execution beads

## Feasibility assumptions and validation questions

| ID | Assumption / question | Risk | Proof validating must require |
| --- | --- | --- | --- |
| E2R-A1 | Every current catalog source file has a vhcnd counterpart under `Settings/item/004/`. | LOW | Existence + line-count table for the 12 filenames. |
| E2R-A2 | Preserving old source line numbers is sufficient for non-GoldItem rows. | MEDIUM | Sample row identity from each non-GoldItem file: name/object sprite/detail fields where applicable. |
| E2R-A3 | GoldItem requires row remapping or explicit evidence; old line numbers are not blindly valid. | HIGH | Probe old-vs-vhcnd GoldItem rows and choose either a deterministic remap or record a blocking gap. |
| E2R-A4 | The stat audit can be safely parameterized away from `Client/Settings/` without weakening Req 14.5. | MEDIUM | Audit JSON includes accepted source path policy and rejects missing/empty/non-vhcnd paths. |
| E2R-A5 | Remaining US-011 audits can run once stat provenance is fixed. | MEDIUM | Ordered audit dry-run summary after the stat audit clears the path-layout blocker. |

## Verification commands/checks for validation/execution

Run from `/var/www/vltk-h5-survivors/game-source` unless noted.

```bash
python3 -m py_compile scripts/vltk-audit-equipment-stat-coverage.py scripts/vltk-normalize-equipment-index.py

python3 scripts/vltk-audit-equipment-stat-coverage.py   --catalog src/data/equipmentCatalog.json   --source src/domain/equipment.ts   --out /var/www/vltk-h5-survivors/harness-experimental/history/migrate-vhcnd-to-vhcnd/spike-scripts/outputs/e2r-equipment-stat-coverage.audit.json   --vhcnd-root /var/www/vhcnd/sources
```

Additional validation-only probes:

- Verify `src/data/equipmentCatalog.json` contains no `Client/Settings/item/` source paths after the remediation if the selected path is translation.
- Verify every catalog `source.path` resolves below `/var/www/vhcnd/sources` and no catalog source path starts with `/var/www/vhcnd` or `/var/www/vhcnd`.
- Run a row-identity probe for the 12 source files and write the findings to `e2r-source-metadata-evidence.md`.
- Attempt remaining ordered US-011 audits from the existing US-011 `execplan.md`, redirecting all `--out` paths to `history/migrate-vhcnd-to-vhcnd/spike-scripts/outputs/`.

## Out of scope

- No harness-wide `vhcnd` → `vhcnd` textual sweep yet.
- No `.codex/skills/` rename yet.
- No GitNexus repo/group rename yet.
- No Playwright snapshot regeneration yet.
- No broad asset folder rename under `public/assets/*/vhcnd` yet.

## Planned bead mapping after validating accepts

Do **not** create beads until `khuym:validating` accepts this current story. If validation accepts, create only these current-work beads:

1. `E_M2R probe`: inventory the 12 source files, line counts, and row-identity samples; write `e2r-source-metadata-evidence.md`.
2. `E_M2R implementation`: patch/translate catalog provenance and audit path policy; compile scripts.
3. `E_M2R audit rerun`: rerun stat audit and remaining ordered US-011 audits to harness outputs; write `e2r-audit-summary.json`.
4. `E_M2R synthesis`: update `spike-name-hash.md` or a new `e2r-verdict.md` with go/no-go for resuming E_M3.

## Handoff

Planning has reshaped the work around the E_M2 no-go result. Invoke `khuym:validating` to verify this E_M2R current story and either approve bead creation for E_M2R or send it back to planning with concrete blockers.
