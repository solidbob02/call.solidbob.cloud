---
title: "상담원 화면 패널별 헤더 셸"
assignee: "조서희"
role: "app"
status: "done"
sprint: 2
priority: 7
date: 2026-08-27
paths:
  - "apps/dashboard/src/App.tsx"
  - "apps/dashboard/src/components/AppHeader.tsx"
  - "apps/dashboard/src/components/TranscriptPanel.tsx"
  - "apps/dashboard/src/components/TermsPanel.tsx"
  - "apps/dashboard/src/components/ManualSearchBar.tsx"
  - "apps/dashboard/src/index.css"
---

통합 헤더를 없애고 왼쪽(로고)·오른쪽(세션)으로 나눈다. 자막 패널은 크림
배경, 수동 검색바는 왼쪽 하단, 점무늬는 오른쪽 캔버스에만 둔다.

## 완료 조건

- 두 헤더가 패널 경계에서 갈라지고 배경이 각 패널과 이어진다
- 검색바가 왼쪽 패널 너비 안에만 있다
- 카드·칩·도메인 전환 로직은 그대로
