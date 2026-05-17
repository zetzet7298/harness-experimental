# Agent Operating Guide

This repository is in Harness v0. There is no product implementation yet.

The current job of agents is to preserve and grow the collaboration harness
before writing application code. Do not scaffold application source folders,
platform shells, package scripts, CI, or tests unless a later story explicitly
moves the project into implementation.


## Workspace Routing

This repository is now the Codex CLI harness/control workspace. The game implementation lives outside this Git root at `/var/www/vltk-h5-survivors/game-source`, and the legacy PC source mirror lives at `/var/www/vltkpc`.

- Do harness/process/skill edits in `/var/www/vltk-h5-survivors/harness-experimental`.
- Do H5 game code, runtime assets, packets, and Vite/Phaser validation in `/var/www/vltk-h5-survivors/game-source`.
- Do not query this harness repo as the H5 source. For H5 code use GitNexus `repo: "vltk-h5-survivors"`, which is registered to `/var/www/vltk-h5-survivors/game-source`.
- For legacy PC source/tables use GitNexus `repo: "vltkpc"`, registered to `/var/www/vltkpc`.
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
| Look up VLTK item stats, requirements, options, GoldItem rows, skills, table evidence, encoding, or PAK source rows | `vltk-item-research` | Research only; return concrete source paths/lines, decoded names, provenance, and uncertainty notes. |
| Port/extract/preview/compose/wire VLTKPC `.spr`, character equipment animation, NpcRes parts, horse/weapon/body visuals, or H5 spritesheets | `vltk-spr-porting` | Use index/packet workflow in `/var/www/vltk-h5-survivors/game-source`, require visual preview gate, copy source SPRs into game-source before runtime use. |
| Resolve an equipped character or item visual from names | `vltk-item-research` then `vltk-spr-porting` | Identify item/row/mapping first; only port after engine mapping and preview evidence. |
| Build or adjust Phaser/Vite gameplay code | `game-studio:phaser-2d-game` | Use in `/var/www/vltk-h5-survivors/game-source` for scenes, simulation/render split, input, cameras, sprites, HUD integration, and Phaser patterns. |
| Browser smoke test or screenshot game behavior | `game-studio:game-playtest` | Use for localhost playtest, HUD/debug checks, screenshots, console/runtime issue capture. |
| Write or update ADRs, playbooks, product docs, or technical runbooks | `document-writer` | Keep docs concise, structured, linked to source-of-truth files, and scoped to the current change. |
| Create or upgrade a Codex skill | `skill-creator` | Use before editing `.codex/skills/*/SKILL.md`; validate the skill after changes. |
| Inspect impact, graph context, or changed scope | `gitnexus-*` tools/skills | Use before editing symbols and before commit; report high/critical risk instead of proceeding silently. |


## GitNexus Multi-Repo Porting

For VLTKPC-to-H5 porting, use the GitNexus group `vltk-porting`:

- H5 member: `h5 -> vltk-h5-survivors -> /var/www/vltk-h5-survivors/game-source`.
- PC member: `pc -> vltkpc -> /var/www/vltkpc`.
- Harness repo: `/var/www/vltk-h5-survivors/harness-experimental`; do not use it for H5 source queries.
- Query H5 only with `repo: "vltk-h5-survivors"`.
- Query PC source/tables only with `repo: "vltkpc"`.
- Query both repos with `repo: "@vltk-porting"`; results include `_repo` so agents can see whether evidence came from `h5` or `pc`.
- For PC engine evidence, prefer GitNexus queries/context for symbols such as `KItemChangeRes`, `GetHorseRes`, `GetWeaponRes`, `KItem`, and `KItemGenerator`; use `vltk-item-research` scripts for decoded PAK/table rows.
- Refresh H5 index with `gitnexus analyze /var/www/vltk-h5-survivors/game-source --name vltk-h5-survivors --force --no-stats --skip-agents-md`.
- Refresh PC index with `GITNEXUS_NO_GITIGNORE=1 gitnexus analyze /var/www/vltkpc --name vltkpc --force --no-stats`.
- After either refresh, run `gitnexus group sync vltk-porting --skip-embeddings`.

## Asset Porting Rule

Do not make the H5 app read assets directly from `/var/www/vltkpc` at runtime. When searching or porting VLTKPC sprites, equipment, assets, or PAK-derived files, work in `/var/www/vltk-h5-survivors/game-source` and read `scripts/README.md` plus `docs/VLTKPC_SPR_PORTING_PLAYBOOK.md` there first. Use the normalized index/packet -> preview gate -> copy source SPR into game-source -> compose runtime asset flow; never wire candidate SPRs before visual preview.

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
| VLTKPC legacy source | `vltkpc` | `/var/www/vltkpc` |
| Cross-repo group | `@vltk-porting` | `h5` + `pc` members |

When calling MCP tools from this harness, always pass `repo`. Do not omit `repo`, because multiple repos are indexed.

<!-- gitnexus:end -->
