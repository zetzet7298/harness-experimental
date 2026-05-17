# Product Docs

This directory is the living product contract for the brownfield H5 game source
at `/var/www/vltk-h5-survivors/game-source`.

Start with:

- `overview.md`: product goal, surfaces, non-goals, and source-of-truth routing.
- `current-state.md`: everything already built, currently active, and not done.
- `vltkpc-porting.md`: VLTKPC data/asset provenance, preview gates, and runtime
  asset rules.
- `roadmap.md`: near-term planned work and blocked/unknown items.

## Update Rule

When behavior changes:

1. Update the affected product doc.
2. Update or create the story packet.
3. Update `docs/TEST_MATRIX.md`.
4. Record a decision if the change affects architecture, scope, risk, or a
   previously settled product rule.
