---
title: "React 대시보드 스캐폴딩"
assignee: "조서희"
role: "app"
status: "todo"
sprint: 2
priority: 7
date: 2026-08-26
---

`apps/dashboard` 를 만든다. 1주차 티켓([w1-dashboard-scaffold](/backlog/w1-dashboard-scaffold/))에서
이월된 작업이며, 팀 개편으로 담당이 조서희로 바뀌었다.

**막혔던 전제는 풀렸다** — 인터페이스 계약이 v2 로 확정됐다([7.3절](/docs/07/),
`_project/decisions/003`).

## 화면 구조 ([2.1절](/docs/02/))

3분할 — 실시간 자막 / 추천 카드(출처·유사도) / 경고. F-2 종결 모달은 이 위에 얹힌다.

## 계약에서 미리 알아둘 것

- **`segment_id`** — interim 이 20초에 199건 온다. 누적하지 말고 같은 `segment_id` 의
  마지막 것으로 **교체**해야 한다. 이 필드가 v2 에서 추가된 이유다
- 첫 interim 은 **962ms**, 최종 결과는 발화 종료 후 **+346ms** (V4 실측)
- 카드에 **출처 없는 것은 표시하지 않는다.** 카드가 없으면 "관련 문서 없음"
- **위험도 점수나 "안전합니다" 류 표현을 UI 에 넣지 않는다** ([부록 A-1](/docs/12/))

규칙: `.claude/rules/dashboard.md`

## 완료 조건

3분할 레이아웃이 뜨고, 계약 3종의 JSON 을 목 데이터로 넣으면 화면에 그려진다.
