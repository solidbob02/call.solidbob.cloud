---
title: "컴플라이언스 검사 경로 — 상담원 발화 → 위반 목록"
assignee: "장민석"
role: "ai"
status: "done"
sprint: 6
priority: 3
date: 2026-08-27
requirement:
  - "C-1"
  - "C-2"
  - "C-3"
  - "C-4"
paths:
  - "server/apps/hub/app/use_cases/compliance_check_interactor.py"
  - "server/apps/hub/adapter/inbound/api/v1/compliance_router.py"
---

`CompliancePort` 는 있었는데 **부르는 곳이 없었다.** [기능 ID 배지](/kanban/)를 달면서
C-1~C-4 에 티켓이 0건인 것이 드러나 만들었다 — [필수 블록](https://github.com/solidbob02/call.solidbob.cloud/blob/main/CLAUDE.md)이다.

`POST /hub/compliance-checks`

## 추천(B)과 별개 경로다

검색은 **고객 발화**에 반응하고 이쪽은 **상담원 발화**에 반응한다. 한 인터랙터에 묶으면
화자에 따라 분기하는 `if` 가 생기고 두 지표(적절 발동률 / 재현율)가 섞인다.

커맨드가 `agent_utterance` 만 받는 것도 같은 이유다 — 고객이 한 말을 위반으로 잡으면
화면에 **고객을 탓하는 경고**가 뜬다.

## 부록 A-1 을 구조로 막았다

응답 필드가 `call_id` · `segment_id` · `findings` **셋뿐**이다. 등급·점수·"안전" 필드를
아예 두지 않았으므로 화면이 그런 표현을 만들 재료가 없다. 테스트로도 고정했다.

> 발견이 없는 것은 **"잡힌 것이 없음"**이지 **"안전함"**이 아니다.
> 재현율 0.90 목표라는 건 10건 중 1건은 놓친다는 뜻이다.

## 스포크가 없으면 501

빈 목록을 돌려주면 **탐지가 죽은 것이 "깨끗하다"로 읽힌다.** 재현율 우선(애매하면 잡는다)과
정반대 방향의 사고라 통과 경로를 만들지 않았다.

## 완료 조건

`cd server && pytest` 75개 통과 · 계약 3종 KEPT · 응답에 등급 필드 없음을 테스트가 검증.
