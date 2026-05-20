# H5 SPR Porting Tools

Run from `/var/www/vltk-h5-survivors/game-source`.

## Normalize All Equipment

```bash
python3 scripts/vltk-normalize-equipment-index.py
```

Optional profiles:

```bash
python3 scripts/vltk-normalize-equipment-index.py --sex female --unmounted --out /tmp/female.json --summary-out /tmp/female.summary.json
```

## One-command Loadout Gate

Use this first for H5 loadouts. It resolves aliases, writes a packet, updates the PAK SPR manifest cache, copies source SPRs into the repo, and writes a preview report. It stops at `pending` by default.

```bash
python3 scripts/vltk-port-loadout.py "Phiên Vũ" "Địch Khái" --slug equipped-phien-vu-dich-khai-loadout
```

After human review passes the PNG, compose with the report gate:

```bash
python3 scripts/vltk-port-loadout.py "Phiên Vũ" "Địch Khái" \
  --slug equipped-phien-vu-dich-khai-loadout \
  --preview-status passed \
  --reviewer-note "Preview checked." \
  --compose
```

## Preview Candidates

```bash
python3 scripts/vltk-preview-candidates.py 'Phiên Vũ' --input data/vltk-normalized/port-packets/equipped-phien-vu-dich-khai.json
python3 scripts/vltk-preview-candidates.py '敌忾竹杖' --kind gold
python3 scripts/vltk-preview-candidates.py --input data/vltk-normalized/port-packets/<packet>.json --report-out data/vltk-normalized/previews/<slug>.report.json
```

## Extract Required SPRs

```bash
python3 scripts/vltk-extract-required-sprs.py --dry-run
python3 scripts/vltk-extract-required-sprs.py
```

For index-selected items:

```bash
python3 scripts/vltk-extract-required-sprs.py --equipment-index data/vltk-normalized/equipment-index.json --item '敌忾竹杖'
```

## Compose Character Sheet

```bash
python3 scripts/port-vhcnd-equipped-character.py \
  --packet data/vltk-normalized/port-packets/equipped-phien-vu-dich-khai.json \
  --preview-report data/vltk-normalized/previews/equipped-phien-vu-dich-khai-loadout.report.json
```

Default legacy compose should still produce Phiên Vũ white horse and `MA_RW_026_HR01.spr` staff, but new work should prefer `vltk-port-loadout.py` and the preview report gate.
