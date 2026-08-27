---
title: "F-2 종결 게이트 배선 — 검증 없이 통과시키지 않는다"
assignee: "장민석"
role: "ai"
status: "done"
sprint: 7
priority: 4
date: 2026-08-27
requirement:
  - "F-2"
paths:
  - "server/apps/hub/app/use_cases/closure_check_interactor.py"
  - "server/apps/hub/adapter/inbound/api/v1/closure_router.py"
---

`ClosureGatePort` 도 있었는데 부르는 곳이 없었다. `POST /hub/closure-checks`.

F-2 는 [조건부 모듈](/docs/08/)(7주차 체크포인트)이지만, **배선은 스포크와 무관하게 먼저 만들 수 있다.**
게이트 판정 규칙이 아니라 요청을 나르는 경로이기 때문이다.

## 허브가 판정하지 않는다

`evidence` 를 보고 스스로 approved/blocked 를 정하지 않는다. 그 규칙표는 도메인별
내부처리규정(`*-POLICY-*`)이 갖고 closure_gate 스포크의 `domain/services` 가 소유한다
([architecture.md §2](https://github.com/solidbob02/call.solidbob.cloud/blob/main/docs/architecture.md)).
어떤 키가 필수인지도 허브는 모른다 — 여기서 검사하면 규칙이 두 곳에 생긴다.

## 스포크가 없으면 501 — 통과시키지 않는다

F-2 는 **"필수 근거 미기재 시 종결 100% 차단"이 절대 규칙**이다. 게이트가 없는 상태를
`approved` 로 돌려주면 차단해야 할 건을 통과시키는 것이고, **그건 F-2 를 안 만든 것보다 나쁘다** —
화면에는 검증을 통과한 것처럼 보이기 때문이다.

같은 이유로 **빈 근거(`evidence: {}`)는 422 로 막았다.** 빈 근거로 판정을 요청하는 것은
근거 없이 승인을 받으려는 것과 같다.

## 완료 조건

`cd server && pytest` 75개 통과 · 스포크 미등록 시 501 이고 응답에 `approved` 가 없음을 테스트가 검증.
