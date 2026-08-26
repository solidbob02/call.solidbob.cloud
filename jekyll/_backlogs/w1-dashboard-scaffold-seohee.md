---
title: "React 대시보드 스캐폴딩"
assignee: "조서희"
role: "app"
status: "done"
sprint: 1
priority: 12
date: 2026-08-26
---

`apps/dashboard` 를 Vite + React 18 + TypeScript strict 로 스캐폴딩한다.
**이 티켓은 [w1-dashboard-scaffold](/backlog/w1-dashboard-scaffold/) (장민석, 팀개편 전)를 대체한다.**
기존 티켓의 `assignee` 는 작성 당시 기록이므로 소급 수정하지 않는다.

규칙은 `.claude/rules/dashboard.md` 를 따르되, 그 안의 `RecommendationCard` 예시(`source.doc`/`score`)는 구버전이다.
정본은 [7.3절 인터페이스 계약 v2](/docs/07/) (`source.doc_id`+`title`, `similarity_score`).

## 범위

- 3분할: 실시간 자막 / 추천 카드 / 개인정보 마스킹 로그. F-2 종결 모달
- 게이트웨이 클라이언트 real/mock 동일 인터페이스. `VITE_GATEWAY_WS_URL` 이 없으면 mock.
  mock 데이터는 7.3절 예시값만 사용 (프로모션 할인 카드, 해지 종결 `blocked`)
- **상태관리 zustand — 팀 컨펌 필요.** 칸반·규칙에 합의된 방식이 없어 이번에 도입했다.
  PR 올릴 때 이 선택을 팀에 확인한다.

## 완료 조건

- `npm run typecheck` · `npm run build` 통과
- mock 시나리오가 자막 → 카드 → 마스킹 로그 → 종결 모달(종결 버튼 비활성) 순으로 그려진다
- 출처 없는 카드 미표시, 위험도/"안전합니다" 류 문구 없음

## 2026-08-26 착수 후 범위 (같은 티켓에서 이어짐)

스캐폴딩 완료 조건은 위에서 충족. 이어서 넣은 것: 상단 2분할 + 하단 책갈피, 도메인 4종 mock, F-2 evidence를 §2.7 필드명으로 정정, blocked는 경고 아래 실시간 표시 / approved만 모달. 상태관리는 zustand (팀 컨펌 대기).
