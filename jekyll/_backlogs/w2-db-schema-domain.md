---
title: "DB 스키마 도메인 재검토 — 통신 특화 테이블 정리"
assignee: "류준·장민석"
role: "ai"
status: "done"
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

**2026-08-26 완료.** `plan` 테이블 제거, `subscriber`→`customer`로 정리, `call`에 `domain`
ENUM('finance','dasan','shopping','health') 컬럼 신설(위 표의 `document` 도메인 구분 질문에
대한 답 — `document`가 아니라 `call` 레벨에 둠), `closure.closure_type`/evidence 컬럼을
금융보험(상품해지·보상)·쇼핑(반품·교환) 기준으로 교체. 17개→16개 테이블. `db/schema.sql`·
`db/docs/ERD.md`·[16절 ERD](/docs/16/)·[7.3절 인터페이스 계약](/docs/07/) 예시까지 함께
갱신해 계약과 어긋나지 않게 맞췄다. 결정 기록: `_project/decisions/006-db-스키마-도메인-정리.md`.

## 완료 조건

`db/schema.sql` · ERD 갱신 + 계약 반영 여부 확인 + 팀 승인([w1-db-schema](/backlog/w1-db-schema/)와 함께).

**스키마·ERD·계약 갱신은 완료.** 팀 정식 승인(4인)은 [w1-db-schema](/backlog/w1-db-schema/)에서
계속 추적 — 그 티켓은 아직 `in-progress`다. 실제 MySQL 마이그레이션 적용도 미착수.
