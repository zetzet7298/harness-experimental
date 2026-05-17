# Roadmap

## Now

- Keep harness docs synchronized with the brownfield game-source state.
- Preserve the playable offline Phaser prototype and VLTKPC porting gates.
- Validate the current state with `npm run build`, `npm run typecheck`, and the
  Python VLTK porting smoke test when docs or source contracts change.

## Next

- Capture a browser smoke/playtest report for the H5 prototype, including HUD,
  stress controls, and console health.
- Add a story for real VLTK table import replacing or expanding
  `src/data/vltk-samples.json`.
- Generalize equipped character composition beyond the current known loadout.
- Add an explicit validation report whenever preview status is changed from
  pending to passed.

## Later

- Define progression, skill, enemy, map, and loot contracts from verified VLTKPC
  data.
- Decide whether backend persistence is needed and record a decision before
  introducing server/API infrastructure.
- Add CI only after the validation commands stabilize locally.

