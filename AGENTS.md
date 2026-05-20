# thay vì dùng bash, grep, glob, native read file tool -> use srcwalk skill instead
# Khi giao tiếp với human. bắt buộc dùng tiếng việt
# Agent Operating Guide

This repository is in Harness v0. There is no product implementation yet.

The current job of agents is to preserve and grow the collaboration harness
before writing application code. Do not scaffold application source folders,
platform shells, package scripts, CI, or tests unless a later story explicitly
moves the project into implementation.


## Workspace Routing

This repository is now the Codex CLI harness/control workspace. The game implementation lives outside this Git root at `/var/www/vltk-h5-survivors/game-source`, and the legacy PC source mirror lives at `/var/www/vhcnd`.

- Do harness/process/skill edits in `/var/www/vltk-h5-survivors/harness-experimental`.
- Do H5 game code, runtime assets, packets, and Vite/Phaser validation in `/var/www/vltk-h5-survivors/game-source`.
- Do not query this harness repo as the H5 source. For H5 code use GitNexus `repo: "vltk-h5-survivors"`, which is registered to `/var/www/vltk-h5-survivors/game-source`.
- For legacy PC source/tables use GitNexus `repo: "vhcnd"`, registered to `/var/www/vhcnd`.
- For combined search use GitNexus `repo: "@vltk-porting"`; inspect each result's `_repo` field (`h5` or `pc`) before acting.

## Source Of Truth

Read in this order:

1. `README.md` for project status.
2. `docs/HARNESS.md` for the human-agent operating model.
3. `docs/FEATURE_INTAKE.md` before turning any prompt into work.
4. The user-provided spec or prompt, when one exists.
5. `docs/product/` for current product contracts.
6. `docs/ARCHITECTURE.md` before proposing implementation shape.
7. `docs/stories/` for story packets and backlog.
8. `docs/TEST_MATRIX.md` for proof status.
9. `docs/decisions/` for why important choices were made.

This harness does not ship with a project-specific `SPEC.md`. When the human
provides a spec for a new project, treat that spec as input material for the
first buildout. Derive product docs, story packets, architecture decisions, and
validation expectations from it. Product docs, stories, tests, and decisions
then become the living contract that agents should update as the system evolves.

## Task Loop

For every task:

1. Classify the request with `docs/FEATURE_INTAKE.md`.
2. Identify whether the input is a new spec, spec slice, change request, new
   initiative, maintenance request, or harness improvement.
3. Locate the affected product docs and story files.
4. Check `docs/TEST_MATRIX.md` for existing proof and gaps.
5. Work only inside the selected lane: tiny, normal, or high-risk.
6. Before finishing, ask:
   - Did product truth change?
   - Did validation expectations change?
   - Did architecture rules change?
   - Did we discover a repeated failure pattern?
   - Did the next agent need a clearer instruction?
7. Update routine harness files directly, or add a proposal to
   `docs/HARNESS_BACKLOG.md` when the change is structural.

## Harness Change Policy

Agents may update directly:

- Story status and evidence.
- `docs/TEST_MATRIX.md` rows.
- Links from story packets to product docs.
- Validation notes and reports.
- Small clarifications tied to the current task.

Agents should ask for human confirmation before:

- Changing architecture direction.
- Removing validation requirements.
- Changing the source-of-truth hierarchy.
- Changing risk classification rules.
- Replacing the feature workflow.


## Skill Usage Matrix

Use the smallest skill set that covers the task. If a task needs both data identity and visuals, resolve data first, then port assets.

| Task | Use skill | When to use / rule |
| --- | --- | --- |
| Navigate or inspect repo code/docs | `srcwalk` | Use before raw bash/grep/glob/read; read paths only after `srcwalk` identifies them. |
| Look up VLTK item stats, requirements, options, GoldItem rows, skills, table evidence, encoding, or PAK source rows | `vhcnd-item-research` | Research only; return concrete source paths/lines, decoded names, provenance, and uncertainty notes. |
| Port/extract/preview/compose/wire VHCND `.spr`, character equipment animation, NpcRes parts, horse/weapon/body visuals, or H5 spritesheets | `vhcnd-spr-porting` | Use index/packet workflow in `/var/www/vltk-h5-survivors/game-source`, require visual preview gate, copy source SPRs into game-source before runtime use. |
| Port/fix VHCND maps, minimaps, Region_C/Region_S, Ground.dat, BuildinObj.Dat, map enemies, map aspect/zoom/object alignment | `vhcnd-map-porting` | Use before map runtime or asset changes; preserve PC render coordinates (`y/2`, no vertical stretch), copy assets into game-source, and validate map packet/runtime tests. |
| Resolve an equipped character or item visual from names | `vhcnd-item-research` then `vhcnd-spr-porting` | Identify item/row/mapping first; only port after engine mapping and preview evidence. |
| Build or adjust Phaser/Vite gameplay code | `game-studio:phaser-2d-game` | Use in `/var/www/vltk-h5-survivors/game-source` for scenes, simulation/render split, input, cameras, sprites, HUD integration, and Phaser patterns. |
| Browser smoke test or screenshot game behavior | `game-studio:game-playtest` | Use for localhost playtest, HUD/debug checks, screenshots, console/runtime issue capture. |
| Write or update ADRs, playbooks, product docs, or technical runbooks | `document-writer` | Keep docs concise, structured, linked to source-of-truth files, and scoped to the current change. |
| Create or upgrade a Codex skill | `skill-creator` | Use before editing `.codex/skills/*/SKILL.md`; validate the skill after changes. |
| Inspect impact, graph context, or changed scope | `gitnexus-*` tools/skills | Use before editing symbols and before commit; report high/critical risk instead of proceeding silently. |


## GitNexus Multi-Repo Porting

For VHCND-to-H5 porting, use the GitNexus group `vltk-porting`:

- H5 member: `h5 -> vltk-h5-survivors -> /var/www/vltk-h5-survivors/game-source`.
- PC member: `pc -> vhcnd -> /var/www/vhcnd`.
- Harness repo: `/var/www/vltk-h5-survivors/harness-experimental`; do not use it for H5 source queries.
- Query H5 only with `repo: "vltk-h5-survivors"`.
- Query PC source/tables only with `repo: "vhcnd"`.
- Query both repos with `repo: "@vltk-porting"`; results include `_repo` so agents can see whether evidence came from `h5` or `pc`.
- For PC engine evidence, prefer GitNexus queries/context for symbols such as `KItemChangeRes`, `GetHorseRes`, `GetWeaponRes`, `KItem`, and `KItemGenerator`; use `vhcnd-item-research` scripts for decoded PAK/table rows.
- Refresh H5 index with `gitnexus analyze /var/www/vltk-h5-survivors/game-source --name vltk-h5-survivors --force --no-stats --skip-agents-md`.
- Refresh PC index with `GITNEXUS_NO_GITIGNORE=1 gitnexus analyze /var/www/vhcnd --name vhcnd --force --no-stats`.
- After either refresh, run `gitnexus group sync vltk-porting --skip-embeddings`.

## Asset Porting Rule

Do not make the H5 app read assets directly from `/var/www/vhcnd` at runtime. Do not use symlink/symbolic-link from runtime asset folders to `/var/www/vhcnd` or any out-of-scope root. When searching or porting VHCND sprites, equipment, assets, or PAK-derived files, work in `/var/www/vltk-h5-survivors/game-source` and read `scripts/README.md` plus `docs/VHCND_SPR_PORTING_PLAYBOOK.md` there first. Use the normalized index/packet -> preview gate -> move required source SPR/assets into game-source -> compose runtime asset flow; never wire candidate SPRs before visual preview.

## Done Definition

A task is done only when:

- The requested change is completed or the blocker is documented.
- Relevant docs, stories, and test matrix entries remain current.
- Validation commands were run when they exist.
- Missing harness capabilities were added to `docs/HARNESS_BACKLOG.md`.
- The final response says what changed and what was not attempted.

<!-- gitnexus:start -->
# GitNexus — Workspace Routing

This harness repository is not the H5 game source index. Use explicit repo parameters:

| Target | GitNexus repo | Path |
| --- | --- | --- |
| H5 game source | `vltk-h5-survivors` | `/var/www/vltk-h5-survivors/game-source` |
| VHCND legacy source | `vhcnd` | `/var/www/vhcnd` |
| Cross-repo group | `@vltk-porting` | `h5` + `pc` members |

When calling MCP tools from this harness, always pass `repo`. Do not omit `repo`, because multiple repos are indexed.

<!-- gitnexus:end -->

<!-- KHUYM:START -->
# Khuym Workflow

Use `khuym:using-khuym` first in this repo unless you are resuming an already approved Khuym handoff.

## Startup

1. Read this file at session start and again after any context compaction.
2. If `.khuym/onboarding.json` is missing or outdated, stop and run `khuym:using-khuym` before continuing.
3. If `.codex/khuym_status.mjs` exists, run `node .codex/khuym_status.mjs --json` as the first quick scout step.
4. If `.khuym/HANDOFF.json` exists, do not auto-resume. Surface the saved state and wait for user confirmation.
5. If `history/learnings/critical-patterns.md` exists, read it before planning or execution work.

## Chain

```
khuym:using-khuym
  → khuym:exploring
  → khuym:planning
  → khuym:validating
  → khuym:swarming
  → khuym:executing
  → khuym:reviewing
  → khuym:compounding
```

## Critical Rules

1. Never execute without validating.
2. `CONTEXT.md` is the source of truth for locked decisions.
3. If context usage passes roughly 65%, write `.khuym/HANDOFF.json` and pause cleanly.
4. Treat `.khuym/state.json` as the single runtime state file for routing, current focus, and operator notes.
5. After compaction, re-read `AGENTS.md`, run `node .codex/khuym_status.mjs --json` if present, then re-open `.khuym/HANDOFF.json`, `.khuym/state.json`, and the active feature context before more work.
6. P1 review findings block merge.

## Working Files

```
.khuym/
  onboarding.json     ← onboarding state for the Khuym plugin
  state.json          ← single runtime state file for agents, tools, and humans
  HANDOFF.json        ← pause/resume artifact
  reservations.json   ← local file reservations for same-session Codex swarms

history/<feature>/
  CONTEXT.md          ← locked decisions
  discovery.md        ← research findings
  approach.md         ← approach + risk map

history/learnings/
  critical-patterns.md

.beads/               ← bead/task files when beads are in use
.spikes/              ← spike outputs when validation requires them
```

.codex/
  khuym_status.mjs    ← read-only scout command for onboarding, state, and handoff
  khuym_state.mjs     ← shared state helpers used by the scout command
  khuym_reservations.mjs ← local reservation helper used by swarming, executing, and hooks

## Codex Guardrails

- Repo-local `.codex/` files installed by Khuym are workflow guardrails, not optional decoration.
- Use `node .codex/khuym_status.mjs --json` as the preferred quick scout step when it is available.
- Treat `compact_prompt` recovery instructions as mandatory.
- Use `bv` only with `--robot-*` flags. Bare `bv` launches the TUI and should be avoided in agent sessions.
- If the repo is only partially onboarded, stay in bootstrap/planning mode and surface what is missing before implementation.

## Session Finish

Before ending a substantial Khuym work chunk:

1. Update or close the active bead/task if one exists.
2. Leave `.khuym/state.json` and `.khuym/HANDOFF.json` consistent with the current pause/resume state.
3. Mention any remaining blockers, open questions, or next actions in the final response.
<!-- KHUYM:END -->

<!-- bv-agent-instructions-v2 -->

---

## Beads Workflow Integration

This project uses [beads_rust](https://github.com/Dicklesworthstone/beads_rust) (`br`) for issue tracking and [beads_viewer](https://github.com/Dicklesworthstone/beads_viewer) (`bv`) for graph-aware triage. Issues are stored in `.beads/` and tracked in git.

### Using bv as an AI sidecar

bv is a graph-aware triage engine for Beads projects (.beads/beads.jsonl). Instead of parsing JSONL or hallucinating graph traversal, use robot flags for deterministic, dependency-aware outputs with precomputed metrics (PageRank, betweenness, critical path, cycles, HITS, eigenvector, k-core).

**Scope boundary:** bv handles *what to work on* (triage, priority, planning). `br` handles creating, modifying, and closing beads.

**CRITICAL: Use ONLY --robot-* flags. Bare bv launches an interactive TUI that blocks your session.**

#### The Workflow: Start With Triage

**`bv --robot-triage` is your single entry point.** It returns everything you need in one call:
- `quick_ref`: at-a-glance counts + top 3 picks
- `recommendations`: ranked actionable items with scores, reasons, unblock info
- `quick_wins`: low-effort high-impact items
- `blockers_to_clear`: items that unblock the most downstream work
- `project_health`: status/type/priority distributions, graph metrics
- `commands`: copy-paste shell commands for next steps

```bash
bv --robot-triage        # THE MEGA-COMMAND: start here
bv --robot-next          # Minimal: just the single top pick + claim command

# Token-optimized output (TOON) for lower LLM context usage:
bv --robot-triage --format toon
```

#### Other bv Commands

| Command | Returns |
|---------|---------|
| `--robot-plan` | Parallel execution tracks with unblocks lists |
| `--robot-priority` | Priority misalignment detection with confidence |
| `--robot-insights` | Full metrics: PageRank, betweenness, HITS, eigenvector, critical path, cycles, k-core |
| `--robot-alerts` | Stale issues, blocking cascades, priority mismatches |
| `--robot-suggest` | Hygiene: duplicates, missing deps, label suggestions, cycle breaks |
| `--robot-diff --diff-since <ref>` | Changes since ref: new/closed/modified issues |
| `--robot-graph [--graph-format=json\|dot\|mermaid]` | Dependency graph export |

#### Scoping & Filtering

```bash
bv --robot-plan --label backend              # Scope to label's subgraph
bv --robot-insights --as-of HEAD~30          # Historical point-in-time
bv --recipe actionable --robot-plan          # Pre-filter: ready to work (no blockers)
bv --recipe high-impact --robot-triage       # Pre-filter: top PageRank scores
```

### br Commands for Issue Management

```bash
br ready              # Show issues ready to work (no blockers)
br list --status=open # All open issues
br show <id>          # Full issue details with dependencies
br create --title="..." --type=task --priority=2
br update <id> --status=in_progress
br close <id> --reason="Completed"
br close <id1> <id2>  # Close multiple issues at once
br sync --flush-only  # Export DB to JSONL
```

### Workflow Pattern

1. **Triage**: Run `bv --robot-triage` to find the highest-impact actionable work
2. **Claim**: Use `br update <id> --status=in_progress`
3. **Work**: Implement the task
4. **Complete**: Use `br close <id>`
5. **Sync**: Always run `br sync --flush-only` at session end

### Key Concepts

- **Dependencies**: Issues can block other issues. `br ready` shows only unblocked work.
- **Priority**: P0=critical, P1=high, P2=medium, P3=low, P4=backlog (use numbers 0-4, not words)
- **Types**: task, bug, feature, epic, chore, docs, question
- **Blocking**: `br dep add <issue> <depends-on>` to add dependencies

### Session Protocol

```bash
git status              # Check what changed
git add <files>         # Stage code changes
br sync --flush-only    # Export beads changes to JSONL
git commit -m "..."     # Commit everything
git push                # Push to remote
```

<!-- end-bv-agent-instructions -->
