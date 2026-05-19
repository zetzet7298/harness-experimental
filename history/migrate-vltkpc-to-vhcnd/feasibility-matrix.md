# Feasibility Matrix — E_M1 + E_M2

> Built from concrete evidence during validating, not plausibility language.
> Each assumption is tied to a verifiable check, a verify-time result, and
> the action triggered by that result.

## Assumptions

| ID | Assumption | Verification | Result | Action |
| --- | --- | --- | --- | --- |
| A1 | vltkunity and vhcnd are on the same filesystem so `mv` is an atomic rename. | `stat -c '%m' /var/www/vhcnd /var/www/vltkunity` | Both report `/`. | Pass. Move is rename. |
| A2 | vhcnd has 5 and only 5 callers of vltkunity paths. | `rg -l '/var/www/vltkunity' /var/www/vhcnd` | Returns exactly the 5 known: `web/manifest.json`, `web/manifest_data_cdn_lite.json`, `web/manifest_downloads_like.json`, `web/manifest_required_config_missing_only.{json,csv}`. | Pass. No hidden callers. |
| A3 | vltkunity does not consume vhcnd. | `rg -l '/var/www/vhcnd' /var/www/vltkunity` (excluding datasets/archives) | Zero matches. | Pass. Direction is one-way. |
| A4 | `tools/scan_required_spr.py` runs end-to-end and emits a JSON report. | `python3 tools/scan_required_spr.py --config-dir <vhcnd-real> --spr-root /var/www/vltkunity/item_spr` | Runs to completion. `total=335, missing=10, ok=325`. | Pass. Pre-move baseline = 10 missing. |
| A5 | The audit script's argparse defaults are correct against vhcnd. | Read defaults; `--config-dir` default points at `sources/servernew_up/...` which does not exist. | Fail. The default has a stale prefix. | E_M1 must drop `servernew_up/` from the default. Already noted in `current-work.md`. |
| A6 | Engine FNV-1a (`KStrBase.cpp:881-887`) is the hash that produced the on-disk hash filenames. | Compute hash for 20 named SPR variants; cross-check against 33,646 on-disk hash files. | Zero matches. | Disprove. The hash decoder route is dead-end. |
| A7 | Post-move audit coverage is `>=` pre-move. | E_M1 acceptance check 4. | Cannot run until move executes. | Open — verifies during execution. |
| A8 | US-011 audit scripts can run with explicit `--config-dir`/`--root` flags pointing at vhcnd. | Read each audit script for argparse plumbing; exists per `execplan.md`. | Read-only check; not yet attempted live. | Open — runs in E_M2. |

## Implication for E_M2 spike scope

A6 is now disproved at verify time. The spike no longer needs to attempt full
FNV-1a hash matching at scale; the probe is conclusive on a representative
sample (0/20 across 4 path variants × 33,646 hash candidates). The spike
shrinks to:

1. Run the same probe on the full named SPR set (one final pass to rule out a
   surprise from a long-tail filename), and record the verdict.
2. Run the audit dry-run against vhcnd-rooted inputs.
3. Decide go/go-with-remediation/no-go based on audit coverage, not on the
   hash probe.

This is a small reduction, not a structural change. The spike still gates
E_M3..E_M7. The exit criterion remains `spike-name-hash.md` written and user-approved.

## Risks revisited

- **R1 (was high) → high but bounded.** Pre-move audit shows 325/335 named
  SPRs already cover the required item-table references. The 10 missing are
  the actual gap; the spike characterises them.
- **R2..R6** unchanged.
- **New finding** — `tools/scan_required_spr.py` default `--config-dir`
  contains a non-existent `servernew_up/` prefix. E_M1 work covers this.

## Integration readiness

- No git uncommitted state in harness or game-source (post-D1 snapshot).
- No active beads, no active workers, no reservations. Clean execution surface.
- `.khuym/state.json` reflects planning-complete with epic_id `E_M1+E_M2`.
- `critical-patterns.md` exists (placeholder); no prior pattern blocks.
- The four documents (CONTEXT, discovery, approach, epic-map, current-work)
  are all present and consistent.

## Mode-required current-work artifacts

| Mode | Required | Present |
| --- | --- | --- |
| `high_risk_feature` | epic map, current work pack with feasibility evidence and spike question | All present. |

## Bead readiness

Beads are NOT created and SHOULD NOT be created until E_M2 returns go.
Current work is non-bead spike + manual move. The validating skill accepts
this and explicitly does not require beads at this gate.

## Outcome

READY for execution of E_M1 + E_M2 only. No code change is yet authorised
beyond:

1. The E_M1 disk move and the 5 manifest/tool field edits inside vhcnd.
2. The E_M2 spike: probe script under `history/migrate-vltkpc-to-vhcnd/spike-scripts/`, audit dry-run output under the same folder, spike report at `history/migrate-vltkpc-to-vhcnd/spike-name-hash.md`.

After spike returns go, planning re-shapes the work pack for E_M3..E_M7 and
validating runs again.

---

## Post-E_M2R planning update

E_M2 has now executed. The integration readiness section above is historical for E_M1+E_M2 and is superseded for the next gate by E_M2R.

| ID | Assumption | Verification | Current evidence | Action |
| --- | --- | --- | --- | --- |
| E2R-A1 | The 12 catalog source filenames exist under vhcnd `Settings/item/004/`. | Existence + line count against catalog max source line. | Planning probe found all 12 files under `/var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/item/004/`, each with line count >= current catalog max line for that file. | Validating should rerun and record the table. |
| E2R-A2 | The first audit blocker is path policy, not missing data. | Rerun stat audit after source path translation/policy patch. | E_M2 dry-run showed 1231/1231 `source-file-unreadable`, because the audit looked for `/var/www/vhcnd/sources/Client/Settings/item/*.txt`. | E_M2R implementation must make these paths readable under vhcnd. |
| E2R-A3 | Line preservation may be unsafe for GoldItem. | Compare sample old PC rows, vhcnd `item/004/GoldItem.txt`, and catalog item ids/names/sprites. | Planning sample shows old `GoldItem.txt:2` and vhcnd `004/GoldItem.txt:2/3` are not a trivial one-line match. | Validation must require row-identity evidence or a deterministic remap. |

## Updated outcome

READY for validation of E_M2R only. Execution beads should remain uncreated until validating accepts the current story pack in `current-work.md`.

---

## E_M2R validation result

Validation decision: `READY WITH CONSTRAINTS`.

Reality gate:

- Mode fit: PASS (`high_risk_feature` remains appropriate; provenance touches all 1,231 catalog items and gates broad rebrand).
- Repo fit: PASS (target game-source scripts/catalog exist; vhcnd `ServerNew/_bin_v2_/gs/Settings/item/004` and `Settings/vn` roots exist).
- Assumptions: PASS WITH CONSTRAINTS (all 12 source files exist; non-GoldItem remap is deterministic by numeric/sprite key; GoldItem remains the first execution bead's gating probe).
- Smaller path: PASS (only E_M2R beads were created; E_M3..E_M7 remain gated).
- Proof surface: PASS (`history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-validation-evidence.md` and `e2r-validation-summary.json`).

Created current-work beads:

1. `mig-e2r-probe-njc` — E_M2R probe: vhcnd source row remap evidence.
2. `mig-e2r-implementation-651` — E_M2R implementation: translate catalog provenance and audit policy. Depends on probe.
3. `mig-e2r-audit-rerun-d4u` — E_M2R audit rerun: US-011 ordered audits on vhcnd provenance. Depends on implementation.
4. `mig-e2r-synthesis-30w` — E_M2R synthesis: go/no-go for resuming E_M3. Depends on audit rerun.

Bead review:

- `bv --robot-triage --graph-root mig-e2r-probe-njc` reports 4 open beads, 1 actionable, 3 blocked, no cycles.
- `mig-e2r-probe-njc` is the only actionable start bead and explicitly blocks implementation unless GoldItem remap is solved or reported as `[BLOCKED]`.
- `bv --robot-suggest`, `bv --robot-insights`, and `bv --robot-priority` were run. Suggestions were label/priority heuristics only; no critical bead-structure issue was found.

Approval status: execution is **not** auto-approved. Human approval is required before invoking `khuym:swarming`.
