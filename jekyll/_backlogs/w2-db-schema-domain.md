---
title: "DB 스키마 도메인 재검토 — 통신 특화 테이블 정리"
assignee: "류준·장민석"
role: "ai"
status: "in-progress"
sprint: 2
priority: 8
date: 2026-08-26
---

도메인 4종 전환(`_project/decisions/004`) 후속. 스키마 일부가 통신 도메인 가정에 묶여 있다.

| 대상 | 문제 |
|---|---|
| `subscriber` · `plan` | 통신 가입자·요금제 전용. 4개 도메인에 그대로 쓸 수 없다 |
| `closure` evidence 컬럼 | `위약금_안내`·`잔여할부_안내` 가 통신 해지 기준. 금융보험(상품해지·보상)·쇼핑(반품·교환) 요건으로 다시 정의 |
| `document` | 도메인 구분 컬럼이 필요한지 — [도메인 라우팅 결정](/backlog/w2-domain-routing/)에 달려 있다 |

F-2 는 금융보험·쇼핑에만 적용되고 다산콜센터·질병관리본부는 미적용이므로, `closure` 계열은
그 전제로 재검토한다.

## 주의

인터페이스 계약 v2 의 `evidence` 정의가 이 컬럼들과 1:1 로 묶여 있다. 스키마를 바꾸면
[7.3절](/docs/07/) 계약도 함께 고쳐야 한다 — 한쪽만 바꾸면 어긋난다.

## 완료 조건

`db/schema.sql` · ERD 갱신 + 계약 반영 여부 확인 + 팀 승인([w1-db-schema](/backlog/w1-db-schema/)와 함께).

## 2026-08-26 — 스키마 정리 완료, 팀 승인 남음

위 표의 세 항목을 처리했다. 결정 기록: `_project/decisions/006-db-스키마-도메인-정리.md`.

| 대상 | 처리 결과 |
|---|---|
| `subscriber` · `plan` | `plan` 테이블 삭제, `subscriber` → `customer` 로 정리(체납·분실신고 플래그 삭제 — 폐기된 명의변경 처리유형에만 쓰이던 필드) |
| `closure` evidence 컬럼 | `closure_type`·evidence 를 금융보험(상품해지·보상)·쇼핑(반품·교환) 기준으로 교체 |
| `document` | 별도 도메인 컬럼을 두지 않았다. `document_id` 접두어(`FIN-`/`DASAN-`/`SHOP-`/`HLT-`)가 도메인을 담는다 |

`call` 에 `domain ENUM('finance','dasan','shopping','health')` 컬럼을 신설했다 — 라우팅
정보가 스키마에 아예 없던 공백을 메운 것이다. 17개 → 16개 테이블.
`db/generate_schema_docs.py` 수정 후 재실행해 `schema.sql`·`erd.dot`·`ERD.png` 재생성,
[7.3절](/docs/07/) 계약 JSON 예시도 새 스키마 값으로 교체, `cd fastapi && pytest` 통과.

**아직 `done` 이 아닌 이유**: 완료 조건의 **팀 승인**이 남았다.
[w1-db-schema](/backlog/w1-db-schema/)(류준)와 같은 회의에서 정하기로 돼 있고, 그 티켓도
아직 승인 전이다.
