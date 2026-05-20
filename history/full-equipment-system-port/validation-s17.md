# Validation — S17 Reference / Runtime Isolation Audit

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Story:** `current-story-pack-s17.md`
**Result:** PASS — no active remediation required.

## Commands Run

From `/var/www/vltk-h5-survivors`:

```bash
rg -n --hidden -i 'vltkpc|vltk-pc|/var/www/vltkpc|/var/www/vltk-pc' \
  harness-experimental/{AGENTS.md,docs,.codex} \
  game-source/{docs,scripts,.codex,AGENTS.md,README.md,package.json}

rg -n --hidden -i 'vltkunity|/var/www/vltkunity' \
  harness-experimental/{AGENTS.md,docs,.codex} \
  game-source/{docs,scripts,.codex,AGENTS.md,README.md,package.json}

rg -n --hidden -i 'vltkpc|vltk-pc|/var/www/vltkpc|/var/www/vltk-pc|vltkunity|/var/www/vltkunity|/var/www/vhcnd' \
  game-source/src game-source/public

find game-source/src game-source/public -type l -print
```

From `/var/www/vltk-h5-survivors/game-source`:

```bash
npm run check:no-runtime-vhcnd
```

## Evidence

- Active docs/skills/scripts scan for old source names returned no matches.
- Active docs/skills/scripts scan for `/var/www/vltkunity` returned no matches.
- Runtime `src/` + `public/` forbidden-root scan returned no matches.
- Runtime `src/` + `public/` symlink scan returned no entries.
- `npm run check:no-runtime-vhcnd` passed with: `OK: runtime isolation clean (no /var/www/vhcnd literals and no symlinks under src/ or public/)`.

## Cần xử lý tiếp

None for active docs, repo-local `.codex` skills, active scripts, or runtime folders.

Archival files under `history/migrate-vhcnd-to-vhcnd/` still mention old roots as historical migration evidence. They are not active instructions and should not be rewritten unless a future documentation policy explicitly says archival evidence must be anonymized.

## Decision

S17 passes as an audit-only slice. No remediation bead is needed.
