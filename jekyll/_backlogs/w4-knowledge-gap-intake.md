---
title: "「못 찾았다」 신고 수집 — D-4 공백 리포트 입력 경로"
assignee: "장민석"
role: "ai"
status: "done"
sprint: 4
priority: 4
date: 2026-08-26
requirement:
  - "D-4"
depends_on:
  - "w2-mysql-persistence"
paths:
  - "server/apps/hub/adapter/inbound/api/v1/knowledge_gap_router.py"
---

[D-4 지식베이스 공백 리포트](/docs/02/)는 지금 **시스템이 검색 실패를 추정**하는 구조다.
상담원이 직접 "이 답을 못 찾았다"를 누르는 경로를 두면 훨씬 정확한 라벨이 쌓인다.

**이게 우리만의 고리다.** 레퍼런스 제품(Genesys·Amazon Connect)에 없는데, 우리는
[평가 하네스(E)](/docs/06/)가 있어서 **골든셋을 늘릴 실사용 후보**가 자동으로 모인다.
2주차 50건 → 3주차 150건 확장의 재료가 된다.

## 할 것

```
POST /knowledge-gaps    →  knowledge_gap 테이블 (이미 존재)
```

`knowledge_gap` 테이블은 `db/schema.sql` 에 이미 있다. **수집 경로만 없다.**
[D-4 확장](/docs/02/)이 B(검색 실패)/C(놓친 위반)/F(사후 문제)를 같은 루프에 넣기로 했으므로,
신고 유형을 그 셋으로 받는다.

## ⚠ 수집만 한다

집계·분석은 `ai/` 쪽 일이다([영역 규칙](https://github.com/solidbob02/call.solidbob.cloud/blob/main/server/CLAUDE.md) —
"품질을 만들거나 재는 코드인가?" → `ai/`). `server/` 는 받아서 저장하는 데까지다.

## 완료 조건

세 유형(B/C/F)의 신고가 `knowledge_gap` 에 저장되고, 통화·발화와 연결된다.

## 2026-08-27 — 구현 완료

`POST /hub/knowledge-gaps` → 201 + `gap_id`

```
app/dtos/knowledge_gap_dto.py          KnowledgeGapReport · KnowledgeGapReceipt
app/ports/output/knowledge_gap_port.py
app/use_cases/knowledge_gap_interactor.py
adapter/outbound/mysql/knowledge_gap_repository.py
adapter/inbound/api/{schemas,v1}/
dependencies/knowledge_gap_provider.py  MySQL 미설정 시 501
tests/                                  10건
```

`module` 은 **B·C·F** 세 갈래다 — db `knowledge_gap.module` ENUM 과 [2.5절 D-4 확장](/docs/02/)
표가 정확히 일치해서 그대로 따랐다.

### 신고를 걸러내지 않는다

중복이든 애매하든 그대로 받는다. **무엇이 공백인지 판단하는 것은 집계 단계(`ai/`) 일**이고,
입구에서 거르면 그 판단의 재료가 사라진다. 통화 연결(`call_id`) 없이도 접수된다.

### 설명 길이를 입구에서 막는다

db 가 `VARCHAR(300)` 이라 넘기면 **소리 없이 잘린다** — 신고 내용이 사라지는 것이라 422 로 돌려준다.

### MySQL 없으면 501

접수했다고 응답한 뒤 아무 데도 안 남으면, 상담원은 신고했다고 믿고 우리는 데이터가 없다.
**D-4 를 만든 목적과 정반대**다.

**검증**: `cd server && pytest` 114개 통과 · 계약 3종 KEPT.
