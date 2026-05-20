# Critical Patterns

This file is mandatory context before planning or executing per the Khuym
priority rules. Capture only patterns that, when forgotten, repeatedly cause
P1 review findings, broken validation, or skipped human gates.

## Patterns

> Seeded by E_M2R compounding. Keep this section high-signal.

## [20260519] Refresh full gate-artifact chain before go/no-go
**Category:** pattern
**Feature:** migrate-vhcnd-to-vhcnd (E_M2R)
**Tags:** [khuym, swarming, reviewing, gate-artifacts]

E_M2R đã đạt `ready-canonical` và bead đã đóng, nhưng `go-no-go` từng còn `NO-GO` do artifact downstream chưa refresh đủ chuỗi. Nguyên nhân là các file verdict phụ thuộc nhau theo pipeline, không tự đồng bộ khi chỉ cập nhật mapping/template. Quy tắc vận hành: mỗi lần gate state đổi, bắt buộc chạy lại chuỗi `completion-audit -> integrity-check -> operator-pulse -> go-no-go` trước khi kết luận hoặc handoff.

**Full entry:** history/learnings/20260519-e2r-canonical-gate-review-compounding.md

## [20260520] Catalog-driven audits before parity claims
**Category:** pattern
**Feature:** full-equipment-system-port
**Tags:** [equipment, generated-catalogs, audits, no-fabrication]

S7 found generated catalog requirement keys (`magic_item_needreborn`, `magic_item_needtongban`) that old expected lists did not cover. Root cause: static expectations lag behind source-generated data, letting reachable PC branches avoid labels, seed coverage, or runtime classification. Future rule: before closing any VHCND catalog/parity slice, enumerate observed keys from the generated runtime catalog and drive labels, seed coverage, and runtime/audit classification from that observed set.

**Full entry:** history/learnings/20260520-s7-requirement-parity-compounding.md

## [20260520] Resolve equipment visual identity before copying SPRs
**Category:** pattern
**Feature:** full-equipment-system-port
**Tags:** [equipment, visuals, catalog-identity, local-assets]

S13 showed that preview-passed SPRs can still be unsafe when generated catalog ids are stale or localized names point at the wrong row: `Địch Khái Lục Ngọc Trượng` initially selected a ring while the user intended the staff/weapon row. Future rule: before copying or wiring any equipment visual, prove item id + slot + source row + inventory sprite identity first, document confusing non-target rows, then run the preview/local-copy/runtime-isolation/browser chain.

**Full entry:** history/learnings/20260520-s13-smoke-visual-identity-compounding.md
