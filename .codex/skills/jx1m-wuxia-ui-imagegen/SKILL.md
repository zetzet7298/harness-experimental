---
name: jx1m-wuxia-ui-imagegen
description: Generate, edit, and replace game UI raster assets for this project in JX1M (Võ Lâm Truyền Kỳ 1) wuxia style. Use when creating or revising loading screen, HUD, menu panels, progress bars, logo treatment, then applying those assets into survivors paths.
---

# JX1M Wuxia UI ImageGen

Apply a strict style contract for UI images and complete the integration into `survivors` assets.

## Workflow
1. Identify target UI from project docs first, especially `/var/www/vhst/docs/ui/*.csv` and related notes.
2. Determine task mode:
- `generate`: create new UI asset.
- `edit`: modify existing UI asset.
- `replace`: apply approved output to survivors asset paths.
3. Use built-in `image_gen` by default.
4. Apply the style contract in `references/style-contract.md` as the base prompt layer.
5. Add task constraints: exact text, orientation, dimensions, no-overlap layering.

## Replace Operation (required when user asks apply/replace)
1. Locate target asset path in `survivors` (for loading: `Assets/UI/Splash/`).
2. Backup current files first (`.bak`, `.bak2`...).
3. Resize/crop generated output to exact destination dimensions.
4. Write to destination files.
5. Ensure runtime layering safety:
- Background should not contain static progress/text if runtime draws them.
- Logo files should keep intended alpha behavior (no accidental opaque checker/white backdrop).
6. Verify using Unity Play Mode capture via `ScreenCapture.CaptureScreenshot()` through `execute_code`.

## Prompt Rules
- Enforce exact user text verbatim.
- Keep wuxia aesthetics: bronze/gold ornamental framing, engraved details, restrained glow.
- Avoid generic modern flat UI and neon sci-fi look.
- Prioritize readability on mobile portrait screens.

## References
- Style contract: `references/style-contract.md`
- Local UI mapping: `/var/www/vhst/docs/ui/jx1m-ui-game-matrix.csv`
- Priority migration list: `/var/www/vhst/docs/ui/jx1m-ui-priority-copy-replace.csv`
