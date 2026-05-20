# 0004 Brownfield H5 Source Routing

Date: 2026-05-17

## Status

Accepted

## Context

The harness repository is now separate from the H5 implementation. The active
game code, runtime assets, packet artifacts, and Vite/Phaser validation live in
`/var/www/vltk-h5-survivors/game-source`, while this repo remains the agent
control workspace.

Legacy VHCND source and tables also live outside this repo at `/var/www/vhcnd`.
Agents need durable routing rules so docs work does not accidentally query or
edit the wrong repository.

## Decision

Keep the harness and game implementation as separate working roots:

- Harness/process/product docs: `/var/www/vltk-h5-survivors/harness-experimental`.
- H5 implementation/runtime assets: `/var/www/vltk-h5-survivors/game-source`.
- Legacy PC source/tables/assets: `/var/www/vhcnd`.

Product truth for the H5 brownfield state lives in this harness under
`docs/product/`, `docs/stories/`, `docs/TEST_MATRIX.md`, and `docs/decisions/`.
Implementation evidence remains in game-source.

## Alternatives Considered

1. Move harness docs back into game-source. Rejected because the current workspace
   intentionally separates control/process from implementation.
2. Treat game-source docs as the only truth. Rejected because agents need harness
   story packets, validation matrix, and decisions for ongoing collaboration.

## Consequences

Positive:

- Agents have explicit routing before editing docs, game code, or legacy assets.
- Brownfield state can be documented without moving implementation files.
- GitNexus repo parameters remain unambiguous for H5, PC, and cross-repo work.

Tradeoffs:

- Documentation updates must reference files outside the harness Git root.
- Completion audits must inspect both harness docs and game-source evidence.

## Follow-Up

- Keep `docs/product/current-state.md` current after major game-source changes.
- Add browser smoke evidence for the current prototype.

