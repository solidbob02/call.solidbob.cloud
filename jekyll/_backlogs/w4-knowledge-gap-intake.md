---
title: "「못 찾았다」 신고 수집 — D-4 공백 리포트 입력 경로"
assignee: "장민석"
role: "ai"
status: "todo"
sprint: 4
priority: 4
date: 2026-08-26
requirement:
  - "D-4"
depends_on:
  - "w2-mysql-persistence"
paths:
  - "server/apps/hub/adapter/inbound/api/v1/*"
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
