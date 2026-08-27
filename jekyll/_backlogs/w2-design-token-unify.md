---
title: "대시보드 간격·테두리·아이콘 토큰 통일"
assignee: "조서희"
role: "app"
status: "done"
sprint: 2
priority: 7
date: 2026-08-27
paths:
  - "apps/dashboard/src/index.css"
  - "apps/dashboard/src/components/TermsPanel.tsx"
---

오늘 여러 번에 걸쳐 고치다 카드·검색창·버튼마다 padding·border·radius가 살짝씩 달랐다. 기능은 건드리지 않고 보이는 값만 맞춘다.

## 완료 조건

- 카드(일반·충족요건 있음·랩업) padding이 같다
- 테두리 색은 `#ECECE7` 하나, radius는 요소 종류별로 하나
- 충족요건 아이콘은 원형 배경 없이 초록 체크 / 빨간 X
- 헤더 링과 카드 안 링의 stroke가 같다
- `typecheck` · `build` 통과
