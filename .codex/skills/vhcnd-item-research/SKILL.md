---
name: vhcnd-item-research
description: Research local VLTK/JX/SwordOnline item and equipment data, including PAK extraction, legacy Vietnamese/Chinese encodings, item rows, magic options, quality tiers, GoldItem rows, AddItem parameters, and code paths such as KBasPropTbl, KItemGenerator, KItem, Skills.txt, magicattrib.txt, helm/armor/weapon/horse tables. Use when the user asks to find, decode, understand, compare, or export VLTK items, trang bị, thuộc tính, phẩm chất, option, skill, or source/data table evidence. For SPR asset porting or runtime spritesheet work, use the separate vhcnd-spr-porting skill.
---

# VHCND Item Research

## Quick Workflow

1. Start with the exact item or skill name the user gave; do not begin with a broad repo tour.
2. Use `srcwalk` first for repo navigation and code/table evidence.
3. If raw search fails, assume legacy encoding or PAK compression before concluding the item is absent.
4. Decode runtime PAK tables with `scripts/vltk_extract_tables.py`, then search the UTF-8 outputs.
5. Check `data/vltk-normalized/aliases.json` when a Vietnamese, Chinese, or mojibake name may refer to the same equipment.
6. Answer in Vietnamese with concrete rows, file paths, ids, requirements, stats, option sources, and uncertainty notes.

## Main Script

Use the extractor for repeatable decoding:

```bash
python3 .codex/skills/vhcnd-item-research/scripts/vltk_extract_tables.py \
  --client-dir /path/to/swrod3/bin/Client \
  --source-root /path/to/swrod3 \
  --out /tmp/vltk-decoded \
  --query "Tu La phát kết" \
  --include-loose
```

Useful flags:
- `--paths`: specific virtual PAK paths, e.g. `\\settings\\item\\helm.txt`.
- `--all-matches`: extract every package containing a virtual path, not only the first package-order hit.
- `--query`: search decoded UTF-8 outputs and print matching lines.
- `--include-loose`: convert loose `Client/Settings`, `Client/Ui`, and `Client/script` text files.

## Porting Handoff

If research will feed SPR/H5 work, stop at identity and evidence: canonical name, aliases, source row, item fields, resource table inputs, and uncertainty. Do not choose or wire runtime animation SPRs here; hand off to `vhcnd-spr-porting`, which owns preview gates, moving/copying SPR source into game-source, PAK manifest cache, and composer/wire decisions.

When handing off, always include:
- Active package-order evidence (`package.ini` + extracted `update*.pak` row).
- Duplicated-name rows (same Vietnamese name, different `particular/level`) and which row is currently active.
- Exact `tableValue`, computed engine index (`tableValue - 2` when code path confirms), and unresolved ambiguity notes.

## References

Read only what is needed:
- `references/workflow.md`: exact lookup flow, package order, encoding rules, and evidence discipline.
- `references/item-schema.md`: item table columns, equipment enums, quality tiers, and option generation.
- `references/known-layout.md`: common paths in the extracted JXWin source tree.

## Rules Of Thumb

- Runtime data may come from PAK before loose tables; check `Client/package.ini` order.
- Loose tables can be stale or Chinese GBK while PAK overrides contain Vietnamese TCVN3.
- Item display names may be Vietnamese, while `magicattrib.txt` option names can remain Chinese.
- Do not translate silently. Say whether a term is original text, decoded text, or inferred translation.
- For equipment options, distinguish base attributes, requirements, generated magic attributes, and GoldItem fixed options.
- If the task moves from lookup into character SPR porting, switch to `vhcnd-spr-porting`.
- When a corrected alias is discovered, update `data/vltk-normalized/aliases.json` instead of relying on memory.
- Treat inventory sprites such as `obj-*.spr` and `horse*.spr` as item evidence only, not character animation proof.
- If the user reports “đúng item name nhưng sai visual”, do not re-argue item mapping in this skill; hand off immediately with row evidence to `vhcnd-spr-porting` for layer/direction/runtime diagnosis.
