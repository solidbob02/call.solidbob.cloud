---
title: "상담원 화면 떠있는 패널 셸"
assignee: "조서희"
role: "app"
status: "done"
sprint: 2
priority: 8
date: 2026-08-26
paths:
  - "apps/dashboard/src/App.tsx"
  - "apps/dashboard/src/index.css"
  - "apps/dashboard/src/components/AppHeader.tsx"
---

페이지 배경·여백·떠있는 카드 셸만 적용한다. 자막 패널 내부와 카드 스타일은 건드리지 않는다.

## 완료 조건

- 배경 `#EDECE7`, 블러 블롭 2개, 본체가 흰 카드로 뜸
- `typecheck` · `build` 통과, 1024px 이하에서 padding 축소 확인
