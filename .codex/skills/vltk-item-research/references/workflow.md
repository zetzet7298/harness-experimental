# VLTK Item Research Workflow

## 1. Identify The Data Source

Given an item name, first decide whether it is likely:

- Normal equipment: `helm.txt`, `armor.txt`, `meleeweapon.txt`, etc.
- Gold equipment: `GoldItem.txt`.
- Skill: `Skills.txt` plus `script/skill/*.lua`.
- Rank/title/effect: `RankSetting.txt`, `NpcRes`, UI ini files, or scripts.

Use `srcwalk files` for likely filenames and `srcwalk find` for exact strings when the encoding is already known. Also check `data/vltk-normalized/aliases.json` in the H5 repo for known Vietnamese/Chinese/mojibake aliases before declaring two names unrelated.

## 2. Extract Runtime PAK Tables

Run the extractor rather than manually rewriting PAK logic:

```bash
python3 .codex/skills/vltk-item-research/scripts/vltk_extract_tables.py \
  --client-dir /path/to/swrod3/bin/Client \
  --source-root /path/to/swrod3 \
  --out /tmp/vltk-decoded \
  --paths "\\settings\\item\\helm.txt" "\\settings\\item\\magicattrib.txt" \
  --all-matches \
  --query "Tu La phát kết"
```

Then inspect:

- `pak_utf8/*.txt` for decoded tables.
- `manifest.tsv` for package, method, size, and chosen encoding.
- `pak_raw/*.bin` if a conversion looks suspicious.

## 3. Validate Encoding Claims

When reporting a string, classify it:

- `decoded original`: present after PAK extraction and encoding conversion.
- `loose original`: present in loose file conversion.
- `manual translation`: translated by the agent from Chinese/effect code.
- `inference`: inferred from code or table relationship.

Never present a manually translated option name as existing Vietnamese text.

## 4. Parse Item Rows

For equipment rows, report:

- name, file, line
- item genre, detail type, particular type, level
- sprite path and object index
- description if original Vietnamese exists
- series, price
- base attributes and requirements by mapping ids through `KMagicDesc.cpp`

For generated options, query `magicattrib.txt` by the item detail type and requested magic level. Mention whether the option pool is all-series or series-specific.

## 5. Trace Generated Options

Use these code points to explain behavior:

- `KLibOfBPT::InitMAIT` classifies magic attributes by prefix/suffix, type, series, and level.
- `KItemGenerator::Gen_MagicAttrib` chooses up to six options from `nGeneratorLevel[6]`.
- Duplicate `nPropKind` is rejected.
- `KItem::SetAttrib_MA` stores the six generated options.

## 6. Answer Format

For Vietnamese users, answer in Vietnamese with concise concrete evidence:

```text
- Item: <name>
- Source: <path>:<line>
- Base stats: ...
- Requirements: ...
- Option pool: ...
- Gold variant / same sprite: ...
- Encoding note: ...
```

If a name is not found, list the closest hits and why they may or may not be the same item. If the answer will be used for porting, include a handoff note with canonical name, aliases, source row, and item fields, then switch to `vltk-spr-porting` for preview/compose work.
