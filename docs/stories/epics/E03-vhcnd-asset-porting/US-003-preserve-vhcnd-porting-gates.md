# US-003 Preserve VHCND Porting Gates

## Status

implemented

## Lane

high-risk

## Product Contract

VHCND data and SPR assets must preserve provenance, pass preview review before
runtime wiring, and never be loaded from `/var/www/vhcnd` at H5 runtime.

## Relevant Product Docs

- `docs/product/vhcnd-porting.md`
- `docs/product/current-state.md`

## Acceptance Criteria

- Porting scripts document packet, preview, source-copy, and compose workflow.
- Known loadout packet keeps Phiên Vũ horse and Địch Khái Trúc Trượng weapon SPRs.
- Alias lookup prefers corrected known-good packet data over broader candidates.
- Runtime source SPRs are copied into `game-source/public/assets/character/vhcnd/source/`.
- Smoke tests cover the known packet/alias contract.

## Design Notes

- Resolve item identity with item-research evidence before visual work.
- Use `vhcnd-spr-porting` workflow for extraction, preview, copy, and composition.
- Keep preview/report files under `data/vltk-normalized/previews/`.

## Validation

| Layer | Expected proof |
| --- | --- |
| Unit | `python3 tests/test_vltk_porting_smoke.py` passed in game-source on 2026-05-17. |
| Integration | Porting scripts operate on packet/index artifacts. |
| E2E | Browser visual smoke planned separately. |
| Platform | Not applicable. |
| Release | Not defined. |

## Harness Delta

- Added `docs/product/vhcnd-porting.md` and test matrix row for porting gates.

## Evidence

- `game-source/scripts/README.md` documents the one-command loadout gate.
- `game-source/docs/VHCND_SPR_PORTING_PLAYBOOK.md` documents preview/copy/compose
  requirements.
- `game-source/tests/test_vltk_porting_smoke.py` covers known packet and alias
  behavior.
- `python3 tests/test_vltk_porting_smoke.py` ran 4 tests and passed on
  2026-05-17.
