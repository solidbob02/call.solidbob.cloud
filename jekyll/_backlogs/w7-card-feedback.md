---
title: "카드 채택·무시 기록 — 실사용 신호 수집"
assignee: "장민석"
role: "ai"
status: "done"
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

## 2026-08-27 — 구현 완료 (스키마 변경 포함)

`POST /hub/cards/{card_id}/feedback` → 201

### 스키마 결정: `card_feedback` 테이블 신설 (16 → 17개)

`recommendation_card` 에 컬럼을 더하지 않고 **분리**했다.

```sql
CREATE TABLE `card_feedback` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `card_id` BIGINT NOT NULL,
    `action` ENUM('adopted','ignored') NOT NULL,
    `created_at` DATETIME NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`card_id`) REFERENCES `recommendation_card`(`card_id`)
);
```

이유: 피드백은 **카드 내용과 다른 사실**이고 자체 시각을 갖는다. 카드 하나에 이벤트가 여러 번
붙을 수 있어(채택 → 취소) 이력이 남아야 한다. `masking_event`·`compliance_flag` 와 같은
**이벤트 테이블 패턴**이고 3NF 에도 맞는다. append-only — UPDATE 하지 않는다.

### ⚠ 부록 A-1 — 상담원 식별자를 아예 받지 않는다

이 데이터는 **카드 품질을 재는 것**이지 사람을 재는 것이 아니다. 같은 데이터로 상담원을
줄 세우는 것은 다른 일이고, Cresta 식 실시간 코칭 점수는 [금지 범위](/docs/12/)다.

그래서 `CardFeedback` DTO 와 요청 스키마에 **`agent_id` 가 없다** — 받지 않으면 만들 수도 없다.
요청 본문에 `agent_id` 를 넣어도 무시된다. 테스트로 고정했다.

집계(채택률)도 허브에서 하지 않는다 — `ai/`(평가 하네스) 몫이다.

### 골든셋과 별개 신호다

골든셋 Recall@5 는 **"정답을 찾았는가"**를, 이쪽은 **"현장에서 실제로 쓸모 있었는가"**를 잰다.
둘이 갈리는 지점이 지식베이스 보강 후보가 된다.

**검증**: `cd server && pytest` 125개 통과 · `-m integration` 1개 통과 · 계약 3종 KEPT ·
DB 에 17개 테이블 적용 확인.
