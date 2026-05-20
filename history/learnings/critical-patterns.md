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

