# US-001 Document Brownfield State

## Status

implemented

## Lane

normal

## Product Contract

The harness must describe what has been built, what is active, what is next, and
where proof lives for the brownfield H5 game source.

## Relevant Product Docs

- `docs/product/overview.md`
- `docs/product/current-state.md`
- `docs/product/roadmap.md`

## Acceptance Criteria

- Current H5 runtime state is documented from inspected game-source files.
- Existing VLTKPC porting assets/scripts/tests are referenced without claiming
  broader coverage than exists.
- Future work is captured as roadmap/story backlog items instead of unresolved
  chat context.

## Design Notes

- Harness repo remains separate from game-source.
- Product docs are the living state summary; game-source files remain the
  implementation evidence.

## Validation

| Layer | Expected proof |
| --- | --- |
| Unit | Not applicable; documentation-only story. |
| Integration | `srcwalk` inspection of harness and game-source docs/source. |
| E2E | Not applicable. |
| Platform | Not applicable. |
| Release | Completion audit in final response. |

## Harness Delta

- Populated brownfield product docs and updated docs index files.
- Added test matrix rows for current prototype and porting workflows.

## Evidence

- Inspected `game-source/package.json`, `src/game/`, `src/systems/`, `src/gateway/`,
  `scripts/README.md`, `docs/VLTKPC_SPR_PORTING_PLAYBOOK.md`, and
  `tests/test_vltk_porting_smoke.py` with `srcwalk`.

