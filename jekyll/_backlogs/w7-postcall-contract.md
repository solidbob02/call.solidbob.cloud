---
title: "통화 후 랩업 계약 — postcall 포트 + 종료 배선"
assignee: "장민석"
role: "ai"
status: "done"
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
  - "server/apps/hub/app/ports/output/postcall_port.py"
  - "server/apps/hub/app/dtos/call_summary_dto.py"
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

## 2026-08-27 — 구현 완료

`POST /hub/calls/{call_id}/close`

```
app/dtos/call_summary_dto.py       CallSummaryDraft · FollowUpAction
app/dtos/postcall_dto.py           PostcallCommand
app/ports/output/postcall_port.py  신규 — 기존 9개 포트와 같은 ABC 패턴, async
app/ports/input/postcall_use_case.py
app/use_cases/postcall_interactor.py
adapter/inbound/api/{schemas,v1}/  스키마 · 라우터
dependencies/postcall_provider.py  미등록 시 501
tests/                             12건
```

필드명은 `db/schema.sql` 과 맞췄다 — `call.summary_text`(D-1) · `call.inquiry_type`(D-2) ·
`follow_up_action.action_text`(D-3).

### 「초안」이라는 사실을 타입에 박았다

DTO 이름이 `CallSummaryDraft` 다. **D-2 유형 분류는 모델 판정**이므로 확정으로 취급하지 않는다.

- `confirmed` 는 **모델이 `True` 를 실어 보내도 서버가 `False` 로 덮는다.** 확정은 상담원이 화면에서 한다
- 응답 스키마에도 *"D-2 분류 **제안**. 확정 아님 — 상담원이 바꾼다"* 로 적었다
- 서버가 `confirmed=true` 를 만드는 경로가 **아예 없다** — 테스트로 고정

[절대 원칙 9](https://github.com/solidbob02/call.solidbob.cloud/blob/main/CLAUDE.md)("판정은 규칙이, 설명만 LLM이")를
계약 형태로 옮긴 것이다.

### 요약을 다시 다듬지 않는다

인터랙터가 `summary_text` 에 손대지 않는다. 손대면 **모델 출력과 화면 표시가 달라져 환각 추적이 끊긴다** —
6주차 환각 건수 비교(150문항 중 5건 이하)가 무의미해진다.

### SEC-1

받는 것도 돌려주는 것도 **마스킹 완료본뿐**이다. 통화 후 처리라고 원문을 다시 꺼내오지 않는다 —
애초에 저장돼 있지 않다. 요청 스키마에 원문 필드가 없다.

### 스포크 부재 시 501

빈 요약을 주면 화면에는 **"요약이 생성됐는데 내용이 없는 것"**으로 보여 모듈 미구현과 구분되지 않는다.

**검증**: `cd server && pytest` 87개 통과(75→87) · 계약 3종 KEPT.

**남은 것**: `follow_up_action` 테이블 저장은 [영속성 계층](/backlog/w2-mysql-persistence/) 뒤에 붙인다.
D-4 공백 리포트는 별도 티켓([w4](/backlog/w4-knowledge-gap-intake/)).
