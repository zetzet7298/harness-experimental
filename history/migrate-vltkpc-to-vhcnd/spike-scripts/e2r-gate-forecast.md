# E2R Gate Forecast

Generated (UTC): `2026-05-19T15:29:47.584556+00:00`

| Scenario | Remaining | Map issues | Accept provisional | Forecast |
|---|---:|---:|:---:|---|
| current-state | 100 | 48 | False | **blocked** |
| after-apply-proposals-without-provisional-accept | 100 | 0 | False | **blocked** |
| after-apply-proposals-with-provisional-accept | 100 | 0 | True | **ready-provisional-approved** |

Interpretation nhanh:
- Nếu apply proposals và human bật accept provisional => có thể chuyển sang `ready-provisional-approved`.
- Nếu không accept provisional thì vẫn blocked do còn 100 dòng chưa canonical.
