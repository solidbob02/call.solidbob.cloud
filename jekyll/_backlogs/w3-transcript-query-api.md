---
title: "자막 스크롤백 조회 API + interim 중복 흡수"
assignee: "장민석"
role: "ai"
status: "done"
sprint: 3
priority: 3
date: 2026-08-26
requirement:
  - "A-1"
  - "SEC-1"
depends_on:
  - "w2-mysql-persistence"
paths:
  - "server/apps/hub/adapter/inbound/api/v1/transcript_query_router.py"
---

상담원이 지나간 발화를 다시 보는 경로. Genesys Agent Copilot 도 같은 이유로 전사를 남긴다 —
*"agents can refer to it if they miss something"*.

우리는 이게 특히 중요하다. [V4 실측](/docs/05/)상 **20초에 interim 이 199건** 오고
`segment_id` 로 교체되는 구조라, 되돌아보는 경로가 없으면 상담원이 놓친 내용을 복구할 수 없다.

## interim 중복은 서버가 흡수한다

199건을 그대로 저장하면 `transcript_segment` 가 터지고, 안 하면 프론트가 중복 제거를 떠안는다.
**같은 `segment_id` 는 마지막 것(`is_final`)만 남긴다** — 이 규칙을 서버가 갖는다.
`segment_id` 가 [7.3절 계약 v2](/docs/07/)에 추가된 이유가 이것이다(`_project/decisions/003`).

## 할 것

```
GET /calls/{call_id}/transcript      페이징. 마스킹된 텍스트만 나간다(SEC-1)
```

프랙탈 단면 그대로 + 조회 포트. 저장은 `w2-mysql-persistence` 가 먼저다.

## 완료 조건

같은 `segment_id` 로 interim 을 여러 번 넣어도 조회 결과가 1건이고 그것이 final 이다.
응답 어디에도 마스킹 전 원문이 없다.

## 2026-08-27 — 구현 완료

`GET /hub/calls/{call_id}/transcript?limit=&offset=`

```
app/ports/output/transcript_query_port.py       조회 전용 포트 (기록 포트와 분리)
app/dtos/transcript_query_dto.py                TranscriptQuery · TranscriptPage
app/use_cases/transcript_query_interactor.py
adapter/outbound/mysql/transcript_query_repository.py
adapter/inbound/api/{schemas,v1}/
dependencies/transcript_query_provider.py       MySQL 미설정 시 501
tests/                                          14건
```

### 기록 포트와 조회 포트를 나눴다

쓰기는 파이프라인 입구(마스킹 직후)에서, 읽기는 상담원이 화면에서 되돌아볼 때 일어난다.
한 포트에 묶으면 쓰기만 필요한 곳도 조회 구현을 갖게 된다.

### interim 중복은 이미 흡수돼 있다

[영속성 계층](/backlog/w2-mysql-persistence/)이 `is_final=true` 만 저장하므로([7.3절](/docs/07/)),
조회 쪽에서 따로 걸러낼 것이 없다. `total` 은 확정 발화 총수다 — 20초에 199건씩 오던 interim 은
화면에서만 교체되고 DB 에 남지 않는다.

### N+1 을 피했다

마스킹 구간은 별도 테이블(`masking_event`)이라 세그먼트마다 쿼리하면 N+1 이 된다.
페이지의 `segment_id` 를 모아 한 번에 읽고 메모리에서 붙인다.

### 정렬은 리포지토리가 한다

`ORDER BY segment_id` — 허브가 다시 정렬하면 인덱스를 못 쓰고 페이지 경계에서 순서가 어긋난다.

**검증**: `cd server && pytest` 114개 통과 · 계약 3종 KEPT · 응답에 마스킹 완료본만 나가는 것 확인(SEC-1).
