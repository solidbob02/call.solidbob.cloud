---
title: "자막 스크롤백 조회 API + interim 중복 흡수"
assignee: "장민석"
role: "ai"
status: "todo"
sprint: 3
priority: 3
date: 2026-08-26
requirement:
  - "A-1"
  - "SEC-1"
depends_on:
  - "w2-mysql-persistence"
paths:
  - "server/apps/hub/adapter/inbound/api/v1/*"
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
