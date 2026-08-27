---
title: "트리거 허용 창 — 안 A(0~1,500ms) 반영"
assignee: "류준"
role: "ai"
status: "done"
sprint: 1
priority: 14
date: 2026-08-25
requirement:
  - "B-1"
---

## 결정 (2026-08-25) — 안 A 채택

허용 창을 **0 ~ 1,500ms** 로 올린다. 근거: 침묵 대기(최대 1,000ms) + 판정·큐잉 여유(500ms).

### 왜 800ms 로는 안 되나

침묵 기반 트리거는 정의상 무음 N(일반적으로 700~1,000ms)을 기다린 뒤에 발동한다.
여기에 판정 지연이 더해지면 대부분의 발동이 800ms 를 넘겨 "지연"으로 집계된다.
즉 지표가 구현을 평가하는 게 아니라 **침묵 기반이라는 선택지 자체를 사전에 탈락**시킨다.

**V4 실측이 이를 뒷받침한다** — STT 최종 결과가 발화 종료 **+346ms** 에 도착한다.
트리거가 `is_final` 을 기다리는 한 출발선이 이미 +346ms 이고, 800ms 창의 여유는 450ms 뿐이다.

또한 `CLAUDE.md` 규칙상 **rev.4 보완지시서가 기획서 본문보다 우선**한다.
현재 800ms 는 결정의 결과가 아니라 **패치 반영 누락** 상태다.

### 안 B 를 택하지 않은 이유

정확도가 아니라 **비교 가능성** 때문이다. 허용 창은 8주 내내 고정돼야 2주차 값과 7주차 값을
비교할 수 있다. 실측으로 정한 뒤 3주차에 다시 바꾸면 그전 측정치가 무의미해진다.

> 참고: 안 B 의 실측 비용은 생각보다 작다. `scripts/test_stt_v4_streaming.py` 로 이미 측정이 가능하다.
> 그럼에도 한 번 넉넉히 정하고 분포로 개선을 보여주는 편이 낫다고 판단했다.

## 함께 가야 할 조건 3가지 — 전부 반영 완료 (2026-08-25)

1. **지연 분포(p50/p95) 기록** — `services/core/eval/harness.py`의 `run_eval`이 트리거 delta를 모아
   `metrics/latency.py`(`summarize_latency`)로 계산, `report["trigger"]["latency_ms"]`에 싣는다.
   가짜 predictor로 배선 테스트 추가(`test_harness.py`)
2. **3주차 v1 은 STT `is_final` 기반으로** — [4.1절](/docs/04/)에 "STT 엔드포인팅 기반" 전략으로 반영
3. **1,500ms 의 산식을 문서에 남길 것** — [4.1절](/docs/04/)에 "STT 엔드포인팅 +346ms 실측 + 판정·큐잉 여유 500ms" 명시

## 반영 위치 (류준) — 전부 완료

- `jekyll/docs/04-핵심기술난제.markdown` 4.1절 ✓
- `jekyll/docs/06-평가설계.markdown` 6.1절 트리거 행 + p50/p95 기록 행 ✓
- `services/core/eval/metrics/trigger.py` — `ON_TIME_WINDOW_MS` 상수와 파일 상단 독스트링 모두 1,500ms로 갱신 ✓
- `jekyll/open-items.markdown` 해당 항목 체크 ✓

결정 기록: `_project/decisions/001-기획서-rev4-채택.md`, `_project/decisions/003-인터페이스-스키마-v2.md`
