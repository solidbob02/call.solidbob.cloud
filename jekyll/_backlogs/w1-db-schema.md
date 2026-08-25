---
title: "MySQL 스키마 확정"
assignee: "류준"
role: "ai"
status: "in-progress"
sprint: 1
priority: 6
date: 2026-08-25
---

`db/schema.sql`(17개 테이블) + `db/docs/ERD.md`. 팀 교차검증 1회 완료.

**완료 조건**: 3인 승인 후 마이그레이션 확정. 인터페이스 계약과 같은 회의에서 정한다.

추가(2026-08-25): 인터페이스 계약 v2 확정 과정에서 `closure` evidence는 실제로 넓은 표(`closure_type`별
부분집합 컬럼)로 쓰이고 있음을 재확인 — [7.3절](/docs/07/), `_project/decisions/003-인터페이스-스키마-v2.md`.
다만 이건 현재 구현 확인이지 3인 정식 승인은 아니다.

미결: 컴플라이언스 경고를 별도 테이블로 둘지, F-2 evidence를 넓은 표로 둘지 EAV로 둘지.
※ 기획서 [7.1절](/docs/07/)상 MySQL 스키마 담당은 정성윤이나 실제 작성은 류준이 했다. 역할 표기 정리 필요.
