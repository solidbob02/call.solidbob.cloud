---
title: "약관 패널 칩 전환"
assignee: "조서희"
role: "app"
status: "done"
sprint: 2
priority: 8
date: 2026-08-27
paths:
  - "apps/dashboard/src/components/ArrowSelectChip.tsx"
  - "apps/dashboard/src/components/TermsPanel.tsx"
  - "apps/dashboard/src/components/AppHeader.tsx"
---

오른쪽 패널에서 약관 본문과 종결 충족요건을 한 카드에 붙이지 않고,
화살표 칩으로 「충족요건」/「팝업창」을 고른다. 헤더 도메인 `<select>` 도
같은 칩으로 옮겨 상호작용을 통일한다.

## 완료 조건

- `ArrowSelectChip` 재사용, 동시에 하나만 펼침, 바깥 클릭 시 닫힘
- 기본 보기 「충족요건」, 종결 처리 버튼은 이 뷰에만
- 도메인 칩이 mock 시나리오 재생을 그대로 호출
- `typecheck` · `build` 통과
