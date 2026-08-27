---
title: "D-4 공백 리포트 조회·집계 — 쌓인 신고를 읽는 경로"
assignee: "장민석"
role: "ai"
status: "done"
sprint: 4
priority: 3
date: 2026-08-27
depends_on:
  - "w4-knowledge-gap-intake"
requirement:
  - "D-4"
paths:
  - "server/apps/hub/adapter/inbound/api/v1/knowledge_gap_query_router.py"
  - "server/apps/hub/adapter/outbound/postgres/knowledge_gap_query_repository.py"
---

## 무엇을

[w4-knowledge-gap-intake](/backlog/w4-knowledge-gap-intake/)가 **입구만** 만들었다.
신고는 쌓이는데 **읽는 경로가 없어 아무도 볼 수 없었다** — `status` 컬럼(open/resolved)까지
있는데 옮길 방법도 없었다. [2.5절 D-4](/docs/02/)가 정한 *"B·C·F 를 같은 루프로 누적"* 에서
**루프가 닫히지 않은 상태**였다.

```
GET   /hub/knowledge-gaps           목록 (module·status 필터 + 페이지네이션)
GET   /hub/knowledge-gaps/summary   모듈 축 · 도메인 축 집계
PATCH /hub/knowledge-gaps/{id}      open ↔ resolved
```

엔드포인트 11 → **14개**.

## 판단한 것

- **집계는 SQL 이 한다.** 애플리케이션이 읽어와 세면 페이지네이션과 집계가 어긋난다 —
  한쪽은 50건만 보고 센다
- **`domain` 은 LEFT JOIN 이다.** `knowledge_gap.call_id` 는 NULL 을 허용하므로
  INNER JOIN 하면 통화와 무관한 신고가 **조용히 사라진다**
- **총계는 모듈 축에서만 센다.** 도메인 축은 통화 없는 신고를 놓쳐 합이 다르다 —
  다른 값을 같은 이름으로 쓰지 않는다
- **신고를 묶거나 걸러내지 않는다.** 중복이든 애매하든 그대로 보여준다. 무엇이 같은
  공백인지 판단하는 것은 `ai/` 일이고, **입구에서 거르지 않기로 한 것과 같은 이유**다
- **DB 에 못 붙으면 빈 목록이 아니라 501.** 신고 0건과 DB 미연결은 다르다 — 빈 목록을 주면
  화면에 "공백 없음"으로 보이고 **지식베이스가 완벽하다는 잘못된 신호**가 된다
- **없는 id 를 옮겼다고 하지 않는다**(404). 화면이 "처리했다"고 표시하면 거짓이 된다
- **되돌리기(resolved→open)를 허용한다.** 잘못 닫은 것을 기록에서 지우지 않고 되돌린다

## ⚠ 집계에 우선순위·심각도를 두지 않는다

[부록 A-1](/docs/12/). **건수가 많다는 사실과 그것이 중요하다는 판단은 다르고**, 후자는
사람이 지식베이스를 보고 정한다. 응답 스키마에 `priority`·`severity`·`risk` 필드가
아예 없어서 화면이 그런 표현을 만들 재료가 없다 — 테스트로 고정했다.

## 검증

`server` **288 → 311개 통과**, 계약 4종 KEPT.
**실제 PostgreSQL 로 integration 통과** — 가짜 커서로는 `FILTER (WHERE ...)` 집계·LEFT JOIN·
필터 조합이 **문법이 틀려도 통과**하므로 실제 DB 로 확인했다(통화 없는 신고가 살아남는 것,
집계 두 축, 상태 전이, 없는 id 가 False 인 것).
