---
title: "카드 채택·무시 기록 — 실사용 신호 수집"
assignee: "장민석"
role: "ai"
status: "todo"
sprint: 7
priority: 5
date: 2026-08-26
requirement:
  - "E-1"
depends_on:
  - "w2-mysql-persistence"
paths:
  - "server/apps/hub/adapter/inbound/api/v1/card_feedback_router.py"
---

상담원이 추천 카드를 실제로 썼는지 기록한다. 골든셋 기반 Recall@5 와 별개로
**"현장에서 실제로 쓸모 있었는가"** 를 재는 신호가 된다 — [평가 하네스(E)](/docs/06/)와 연결된다.

7주차(운영 관점)에 두는 이유: 카드 생성(B-4~B-6, 6주차)이 먼저 있어야 채택할 카드가 생긴다.

## ⚠ 스키마 변경이 따라온다 — 팀 승인 필요

`recommendation_card` 테이블에 **채택 여부 컬럼이 없다**(2026-08-26 확인).

```sql
card_id · recommendation_id · source_doc_id · title · summary · similarity_score · rank
```

컬럼을 더할지, 별도 테이블(`card_feedback`)로 뺄지 정해야 한다. 스키마 변경은
`db/generate_schema_docs.py` 를 고쳐 재생성하고 ERD·[16절](/docs/16/)까지 함께 갱신하는 작업이며,
[w1-db-schema](/backlog/w1-db-schema/) 와 같은 팀 승인 절차를 탄다.

## 할 것

```
POST /cards/{card_id}/feedback    adopted | ignored
```

## ⚠ 부록 A-1 — 점수를 만들지 않는다

채택률을 상담원별로 집계해 **점수·순위로 쓰지 않는다.** Cresta 식 실시간 코칭 점수는
[부록 A-1](/docs/12/) 금지 범위다. 이 데이터는 **카드 품질**을 재는 용도지 사람을 재는 용도가 아니다.

## 완료 조건

채택·무시가 저장되고, 어느 `doc_id` 의 카드가 얼마나 채택됐는지 조회할 수 있다.
상담원 단위 집계는 만들지 않는다.
