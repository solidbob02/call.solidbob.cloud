---
title: "자막 패널 최신 발화 자동 스크롤"
assignee: "조서희"
role: "app"
status: "done"
sprint: 2
priority: 6
date: 2026-08-26
paths:
  - "apps/dashboard/src/components/TranscriptPanel.tsx"
---

자막이 쌓여도 패널이 최신 줄을 따라가지 않는다. 맨 아래 근처에 있을 때만 자동 스크롤한다.

## 완료 조건

- mock 재생 중 최신 발화가 자막 패널에 보인다
- 위로 올려 예전 대화를 보면 강제 스크롤하지 않는다
- 카드 패널 스크롤 로직은 건드리지 않는다
