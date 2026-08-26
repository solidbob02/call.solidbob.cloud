---
title: "B-0 도메인 라우팅(자동 분류) — 평가 하네스 배선"
assignee: "류준·장민석"
role: "ai"
status: "in-progress"
sprint: 1
priority: 9
date: 2026-08-26
---

[3.2절](/docs/03/) 도메인 라우팅을 자동 분류로 확정(수동 선택 안 함) — 근거·설계:
`_project/decisions/007-도메인-라우팅-자동분류-확정.md`.

**[w2-domain-routing](/backlog/w2-domain-routing/)와 범위가 다르다** — 그 티켓은 A안(수동)
vs B안(자동) **결정** 자체(완료)이고, 이 티켓은 그 결정을 실제로 구현하는 **작업**
(하네스 배선 완료, 분류기 구현은 미착수)이다. 슬러그가 비슷해 보이지만 중복이 아니다.

**끝낸 것**: 평가 하네스에 B-0 배선 완료. `services/core/eval/metrics/domain_routing.py`
(정확도 + 오분류 행렬, 규칙 기반), `harness.py`에 `DomainPredictor` Protocol 추가(아직
`None` — "측정 불가 — 모듈 미구현"으로 정직하게 보고), 골든셋 `domain` 필드를 정답
라벨로 재사용. 테스트(`test_domain_routing_metrics.py`, `test_harness.py` 배선 검증)
포함 `pytest services/core` 33개 통과. [6.1절](/docs/06/)에 목표(정확도 ≥0.95) 반영.

**남은 것**: 실제 KcELECTRA 계열 분류기 구현·학습은 미착수 — 골든셋 7건(F-2 케이스
제외)만으로는 분류기를 학습시킬 수 없다. 2주차 이후 골든셋이 50개로 늘어나면 착수.
신뢰도 낮을 때 폴백(4개 인덱스 전체 검색)은 B-2 하이브리드 검색이 먼저 있어야 구현
가능 — 아직 그 모듈도 없음.

## [w2-domain-routing](/backlog/w2-domain-routing/) 과의 관계

이름이 겹쳐 보드에 두 장으로 보이지만 **다른 일**이다. 세션 종료 검사(③ 중복 티켓)가
슬러그로 경고하는 것이라 합치지 않는다.

| 티켓 | 무엇 | 상태 |
|---|---|---|
| `w2-domain-routing` | **방식 결정** — 수동 선택(A) vs 자동 분류(B) | `done` (B안 확정, `decisions/007`) |
| **이 티켓** | **구현** — 하네스 배선 + 분류기 학습 | `in-progress` (배선만 끝남) |

**2026-08-26 갱신**: 전제였던 골든셋 50건은 확보됐다(`golden-set/v1-50.json`, 도메인
라벨 있는 채점 표본 34건 — F-2 16건은 발화 텍스트가 없어 제외). 남은 전제는 B-2 검색이며,
그건 [ES 인덱스 분할 결정](/open-items/)이 나야 시작할 수 있다.
