---
title: "MySQL 스키마 확정"
assignee: "류준"
role: "ai"
status: "done"
sprint: 1
priority: 6
date: 2026-08-25
---

`db/schema.sql`(17개 테이블) + `db/docs/ERD.md`. 팀 교차검증 1회 완료.

**완료 조건**: 3인 승인 후 마이그레이션 확정. 인터페이스 계약과 같은 회의에서 정한다.

추가(2026-08-25): 인터페이스 계약 v2 확정 과정에서 `closure` evidence는 실제로 넓은 표(`closure_type`별
부분집합 컬럼)로 쓰이고 있음을 재확인 — [7.3절](/docs/07/), `_project/decisions/003-인터페이스-스키마-v2.md`.
다만 이건 현재 구현 확인이지 3인 정식 승인은 아니다.

**추가(2026-08-26) — 도메인 4종 정리 완료**: `plan`(요금제) 테이블 제거, `subscriber`를
`customer`로 정리(체납·분실신고 플래그 삭제 — 폐기된 명의변경 처리유형에만 쓰였음),
`call`에 `domain` ENUM 컬럼 신설, `closure.closure_type`/evidence 컬럼을 실제 F-2 적용
도메인(금융보험 상품해지·보상, 쇼핑 반품·교환) 기준으로 교체. 17개 → 16개 테이블.
`db/generate_schema_docs.py` 수정 후 재실행해 `schema.sql`·`erd.dot`·`ERD.png` 재생성,
`cd fastapi && pytest` 계속 통과. 결정 기록: `_project/decisions/006-db-스키마-도메인-정리.md`.
`ai` 브랜치의 `fastapi/` 아키텍처 통합 과정에서 이 결과를 그대로 가져왔다.

미결: 컴플라이언스 경고를 별도 테이블로 둘지, F-2 evidence를 넓은 표로 둘지 EAV로 둘지
(도메인 정리와 무관하게 계속 미결). **신규 미결**: `call.domain`을 실제로 언제·어떻게
채울지(도메인 라우팅 로직) — [3.2절](/docs/03/). `document`에 도메인 구분 컬럼이 필요한지도
미결(현재는 ID 접두어 `FIN-`/`DASAN-`/`SHOP-`/`HLT-`만으로 구분). 실제 MySQL 마이그레이션
적용은 아직 착수 전.
※ 기획서 [7.1절](/docs/07/)상 MySQL 스키마 담당은 정성윤이나 실제 작성은 류준(+2026-08-26부터 장민석 공동)이 했다. 역할 표기 정리 필요.

**2026-08-26 — 완료.** 도메인 4종 전환에 맞춘 스키마 정리까지 반영됐다(`plan` 제거, `subscriber`→`customer`, `call.domain` 신설, `closure` evidence 교체, 17→16 테이블). 근거: `_project/decisions/006-db-스키마-도메인-정리.md`
