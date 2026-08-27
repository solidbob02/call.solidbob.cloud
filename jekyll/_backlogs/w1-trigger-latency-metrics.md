---
title: "평가 하네스에 트리거 지연 분포(p50/p95/p99) 배선"
assignee: "류준"
role: "ai"
status: "done"
sprint: 1
priority: 24
date: 2026-08-25
requirement:
  - "B-1"
  - "E-2"
---

트리거 허용 창을 0~1,500ms 로 확정하면서 함께 들어간 작업이다.

허용 창은 **합격/불합격 판정선일 뿐**이고, 개선 과정을 보여주는 것은 분포다.
"v1 침묵 기반 p50 920ms → 종결어미 하이브리드 p50 610ms" 같은 문장이 지표 하나보다 강하다.

- `services/core/eval/metrics/trigger.py` 에 지연 분포 계산 추가
- `ON_TIME_WINDOW_MS = (0, 1500)` — 800ms 에서 변경한 근거를 독스트링에 명시
- 6.1절 지표 표에 분포 기록 행 추가

관련: [트리거 허용 창 결정](/backlog/w1-trigger-window/)
