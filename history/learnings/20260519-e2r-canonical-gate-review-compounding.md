---
date: 2026-05-19
feature: migrate-vhcnd-to-vhcnd (E_M2R gate)
categories: [pattern, decision, failure]
severity: standard
tags: [khuym, reviewing, swarming, gate-artifacts, canonical-path]
---

# Learning: E_M2R canonical gate closure cần chuỗi artifact refresh đồng bộ

**Category:** pattern
**Severity:** critical
**Tags:** [khuym, gate, artifact-consistency, e2r]
**Applicable-when:** Khi verdict GO/NO-GO phụ thuộc nhiều file trung gian (preflight, pulse, completion audit, integrity, dashboard).

## What Happened

Trong E_M2R, sau khi chuyển từ provisional sang canonical 149/149, `gate-readiness` đã `ready-canonical` và bead `mig-ja5` đã đóng. Tuy nhiên một số artifact điều hướng vẫn còn trạng thái cũ (`NO-GO`, `await-human-approval`) do chưa refresh đủ chuỗi script phụ thuộc. Sau khi chạy lại `e2r-artifact-integrity-check.py` + `e2r-operator-pulse.py` + `e2r-go-no-go.py`, verdict đã đồng bộ về `GO`.

## Root Cause / Key Insight

Các artifact được tính theo dependency chain; cập nhật một mắt xích (ví dụ map template) không tự kéo theo refresh toàn bộ verdict downstream. Nếu không chạy lại chain theo đúng thứ tự, dashboard/go-no-go có thể mâu thuẫn với trạng thái thực.

## Recommendation for Future Work

Khi gate đổi trạng thái (đặc biệt blocked -> ready), luôn chạy full refresh chain theo thứ tự: `validate -> gate-readiness -> completion-audit -> integrity-check -> operator-pulse -> go-no-go`, rồi mới kết luận và handoff.

---

# Learning: Canonical path là cách hợp lệ để bỏ yêu cầu human approval provisional

**Category:** decision
**Severity:** standard
**Tags:** [decision, canonical, provisional, gate-policy]
**Applicable-when:** Khi đang có 2 đường chốt gate: provisional cần human approval hoặc canonical full completion.

## What Happened

Ban đầu flow dừng ở `GO-WAITING-HUMAN-APPROVAL` vì còn 100 dòng chưa map. Khi hoàn tất canonical map 149/149 với `issue_count=0`, gate chuyển `ready-canonical` và cho phép đóng bead bằng guarded close script mà không cần bật `accept_provisional`.

## Root Cause / Key Insight

Thiết kế gate đã cho phép 2 con đường độc lập: Path A (canonical) và Path B (provisional). Khi Path A đạt điều kiện, blocker human của Path B không còn áp dụng.

## Recommendation for Future Work

Nếu chi phí canonical còn khả thi, ưu tiên hoàn tất Path A để giảm rủi ro quyết định người dùng và tránh merge trong trạng thái ràng buộc tạm thời.

---

# Learning: Reviewing cần ghi rõ P2/P3 để tránh hiểu nhầm "đã done sạch"

**Category:** failure
**Severity:** standard
**Tags:** [reviewing, p2, handoff-quality]
**Applicable-when:** Khi review pass nhưng vẫn còn chỉ dẫn next-step lỗi thời.

## What Happened

Review pass không có P1, nhưng `e2r-control-dashboard`/`e2r-operator-pulse` vẫn gợi ý `canonical-close-now` dù bead đã `closed`. Điều này không sai logic gate nhưng có thể gây thao tác dư.

## Root Cause / Key Insight

Thông điệp hướng dẫn chưa tách nhánh `already-closed`; vì vậy sau khi đóng bead thành công, output vẫn dùng template cũ.

## Recommendation for Future Work

Trong reviewing report, luôn ghi rõ P2/P3 về UX vận hành artifact; sau đó backlog hóa fix script để giảm nhầm lẫn ở phiên sau.
