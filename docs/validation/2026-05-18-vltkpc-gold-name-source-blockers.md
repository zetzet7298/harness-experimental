# 2026-05-18 VLTKPC Gold Name Source Blockers

Resolved on 2026-05-18. The previous 9 ambiguous and 38 unmatched Hoàng Kim rows are now covered by source-backed row mappings.

- Verified row mappings: `171`
- Ambiguous rows: `0`
- Unmatched rows: `0`
- Catalog CJK display names: `0`

## Resolution Evidence

- Official VNG handbook rows remain preferred where a unique set+slot match exists: `113`.
- Official VNG/Zing supplemental/event rows cover An Bang, Định Quốc, Kim Quang, and Động Sát rows: `19`.
- Local Vietnamese `goldequip.txt` line evidence from `/var/www/vhst/item_port_all_in_one/item_data/settings/item/004/goldequip.txt` covers the remaining `39` rows via `game-source/data/vltk-normalized/localized-golditem-line-names.json`.
- `game-source/data/vltk-normalized/gold-name-row-map.audit.json` records `verifiedRowCount=171`, `ambiguousRowCount=0`, and `unmatchedRowCount=0`.
- `python3 scripts/vltk-audit-equipment-name-localization.py --require-complete` passes with `localizedNameCount=1231`, `localizedNameCountByQuality={gold:171, magic:500, normal:560}`, and `cjkCanonicalNameCount=0`.

## Source Policy

Do not translate or transliterate future names by guess. Add new names only through official VNG/Zing evidence, localized client/item-table rows, or an equivalent source artifact with exact row/slot/name provenance.
