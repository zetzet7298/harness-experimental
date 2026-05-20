# Brownfield Docs Validation Report

Date: 2026-05-17

## Scope

Populate Harness docs for the brownfield H5 game-source state: what has been
done, what is active, what is planned, and which validation gates apply.

## Commands Run

```text
srcwalk guide
srcwalk map --scope /var/www/vltk-h5-survivors/harness-experimental
srcwalk map --scope /var/www/vltk-h5-survivors/game-source
srcwalk files 'docs/**/*.md' --scope /var/www/vltk-h5-survivors/harness-experimental
srcwalk files 'src/**/*' --scope /var/www/vltk-h5-survivors/game-source
srcwalk files 'scripts/**/*' --scope /var/www/vltk-h5-survivors/game-source
srcwalk files 'tests/**/*' --scope /var/www/vltk-h5-survivors/game-source
npm run typecheck
npm run build
python3 -m unittest tests/test_vltk_porting_smoke.py
python3 tests/test_vltk_porting_smoke.py
```

## Results

| Check | Result | Notes |
| --- | --- | --- |
| Harness source inspection | passed | Existing README, intake, architecture, test matrix, stories, decisions, and templates inspected. |
| Game-source inspection | passed | Package scripts, Phaser scenes, simulation, gateway, scripts, docs, data, assets, and smoke test paths inspected. |
| Product docs populated | passed | Brownfield overview, current state, VHCND porting, and roadmap added. |
| Story packets populated | passed | Done/active/planned work mapped to US-001 through US-005. |
| Typecheck | passed | `npm run typecheck` passed in game-source. |
| Build | passed | `npm run build` passed in game-source; Vite reported the existing large chunk warning. |
| Python smoke command discovery | failed as expected | `python3 -m unittest tests/test_vltk_porting_smoke.py` failed because `tests` is not a Python package. Use the file path command instead. |
| Python smoke | passed | `python3 tests/test_vltk_porting_smoke.py` ran 4 tests successfully. |
| Browser smoke | pending | US-005 tracks this gap. |

## Evidence

- `docs/product/overview.md`
- `docs/product/current-state.md`
- `docs/product/vhcnd-porting.md`
- `docs/product/roadmap.md`
- `docs/stories/backlog.md`
- `docs/TEST_MATRIX.md`
- `docs/decisions/0004-brownfield-h5-source-routing.md`

## Gaps

- Browser smoke/playtest evidence remains planned.
