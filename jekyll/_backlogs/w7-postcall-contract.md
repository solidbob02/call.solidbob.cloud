---
title: "통화 후 랩업 계약 — postcall 포트 + 종료 배선"
assignee: "장민석"
role: "ai"
status: "todo"
sprint: 7
priority: 6
date: 2026-08-26
requirement:
  - "D-1"
  - "D-2"
  - "D-3"
depends_on:
  - "w2-mysql-persistence"
paths:
  - "server/apps/hub/app/ports/output/*"
  - "server/apps/hub/app/dtos/*"
---

[2.5절 D](/docs/02/)(D-1 요약 · D-2 유형 분류 · D-3 후속조치 추출)는 기능 명세에 있는데
**포트가 아예 없다.** 지금 있는 아웃바운드 포트 9개 중 D 계열은 하나도 없다.

Genesys Agent Copilot 도 통화 종료 시 요약을 만들고 wrap-up 코드를 **추천**해서 상담원이
고르게 한다 — 우리 D-1·D-2 와 같은 구조다.

## 할 것

```
app/ports/output/postcall_port.py     ← 신규 (D-1·D-2·D-3)
app/dtos/call_summary_dto.py          ← 신규
adapter/inbound/api/v1/               POST /calls/{call_id}/close
                                      follow_up_action 테이블 저장 (이미 존재)
```

기존 6개 포트와 같은 ABC 패턴을 따른다. 모델 추론이므로 `async`.

## ⚠ 부록 A-1 — 확정이 아니라 초안이다

**D-2 문의 유형 분류는 모델 판정이다.** 자동 확정하지 않고 **"제안 — 상담원이 수정 가능"**
으로 계약에 명시한다. [절대 원칙 9](https://github.com/solidbob02/call.solidbob.cloud/blob/main/CLAUDE.md)
("판정은 규칙이, 설명만 LLM이")를 DTO 필드 이름과 주석에 반영한다.

## 경계

요약·분류를 **실제로 하는 것은 `ai/`** 다. `server/` 는 계약·배선·저장까지다
([영역 규칙](https://github.com/solidbob02/call.solidbob.cloud/blob/main/server/CLAUDE.md)).

## 완료 조건

포트·DTO 가 기존 패턴과 같은 형태로 정의되고, 구현체 미등록 시 501.
`evaluation.harness.Ports(...)` 에도 꽂을 자리가 생긴다.
