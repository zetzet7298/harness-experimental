# E2R GoldItem Canonical Review Master Checklist

Mục tiêu: hoàn tất 100 dòng còn thiếu `selected_vhcnd_line` để chốt gate `mig-ja5`.

## Batch files

- Easy: `e2r-golditem-review-batch-easy.csv` (7 dòng)
- Medium: `e2r-golditem-review-batch-medium.csv` (30 dòng)
- Hard: `e2r-golditem-review-batch-hard.csv` (63 dòng)

## Checklist theo batch

- [ ] `e2r-golditem-review-checklist-easy.md`
- [ ] `e2r-golditem-review-checklist-medium.md`
- [ ] `e2r-golditem-review-checklist-hard.md`

## Canonical write target

- `e2r-golditem-manual-map-template.csv` (điền cột `selected_vhcnd_line`).

## Verify sau khi điền xong

```bash
cd /var/www/vltk-h5-survivors/game-source
python3 scripts/vltk-audit-equipment-stat-coverage.py \
  --catalog src/data/equipmentCatalog.json \
  --source src/domain/equipment.ts \
  --out /var/www/vltk-h5-survivors/harness-experimental/history/migrate-vltkpc-to-vhcnd/spike-scripts/outputs/e2r-equipment-stat-coverage.audit.json \
  --vltkpc-root /var/www/vhcnd/sources
```

Điều kiện pass chính: `noFabricationCheck.status = pass` và `sourceLinesValid = 1231`.

> Lưu ý: checklist/batch chỉ là trợ giúp review, không tự động sửa template canonical.
