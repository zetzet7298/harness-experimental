# JX1M Wuxia Style Contract

You are generating/editing UI art for a mobile portrait game "Wuxia Survival", adapted from JX1M (Võ Lâm Truyền Kỳ 1) visual language.

## Non-negotiable style
- Primary style: classic 2D wuxia MMORPG UI (VLTK1/JX1M-inspired), not sci-fi, not western shooter UI.
- Visual language: dark bronze/gold ornamental frames, engraved borders, subtle cloud/scroll motifs, lacquered panel surfaces, high-contrast readable typography.
- Mood: martial-arts Jianghu, nostalgic but polished for modern mobile.
- Keep UI hierarchy clear: frame > content > accent > text.
- Use restrained effects: glow only for emphasis, avoid neon overload.

## Composition
- Portrait-first mobile ergonomics unless user requests otherwise.
- Preserve existing layout unless explicitly asked to restructure.
- Prefer component edits over full scene repaint.

## Loading screen rules
- Keep branding strong and readable.
- Progress module should be wuxia-themed framed widget: metallic bronze frame, dark track, warm gold fill.
- Version/system metadata in compact framed block.
- Typography must remain legible on small screens.

## Brand and text
- Use requested text verbatim.
- No watermark, no random extra logos, no extra characters unless requested.

## Color direction
- Core palette: aged gold, bronze, dark brown/charcoal, muted amber highlights.
- Control saturation and keep readability first.

## Runtime layering safety
- If game draws percent/progress/text dynamically, do not bake static duplicates into background art.
- Keep transparent assets truly transparent when intended.
