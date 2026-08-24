---
layout: page
title: 평가 설계
nav_order: 94
updated: 2026-08-24
owner: eval
status: agreed
---

## 채점 원칙 (변경 금지)

1. **LLM 을 채점자로 쓰지 않는다.** 답을 만든 모델이 자기 답을 심판하면 순환이 된다. 모든 지표를 규칙으로 계산해 재현 가능하게 한다.
2. **여러 번 실행한 값 중 최저치를 기준선으로 고정한다.** 생성 모델은 같은 입력에도 답이 달라진다.
3. **기준선 미달은 CI 실패.** 목적은 개선이 아니라 회귀 방지다.
4. **측정하지 않은 수치는 기록하지 않는다.** 미측정은 `null`.

## 목표 기준선

| 영역 | 지표 | 기준선 |
|---|---|---|
| 검색 | Recall@5 | ≥ {{ site.data.metrics.targets.retrieval.recall_at_5_clean }} (오류 0%) / ≥ {{ site.data.metrics.targets.retrieval.recall_at_5_err10 }} (오류 10%) |
| 검색 | MRR | ≥ {{ site.data.metrics.targets.retrieval.mrr }} |
| 트리거 | 적절 시점 발동률 | ≥ {{ site.data.metrics.targets.trigger.fire_precision }} |
| 트리거 | 불필요 발동률 | ≤ {{ site.data.metrics.targets.trigger.false_fire_rate }} |
| 생성 | 환각 수치 발생 | 150문항 중 {{ site.data.metrics.targets.generation.hallucinated_numbers_max }}건 이하 |
| 생성 | 출처 표시율 | 100% |
| 컴플라이언스 | 재현율 | ≥ {{ site.data.metrics.targets.compliance.recall }} |
| 컴플라이언스 | 정밀도 | ≥ {{ site.data.metrics.targets.compliance.precision }} |
| 성능 | p95 레이턴시 | ≤ {{ site.data.metrics.targets.latency.p95_ms }}ms |

컴플라이언스에서 재현율을 정밀도보다 높게 잡은 것은 의도적이다. **누락(FN)이 오탐(FP)보다 위험**하다는 도메인 비대칭을 지표에 반영했다.

## 하네스 구성 (E 블록)

| 기능 | 내용 |
|---|---|
| E-1 | 골든셋 기반 자동 채점 (규칙 기반) |
| E-2 | STT 오류율별 성능 곡선 자동 생성 |
| E-3 | 레이턴시 분포 측정 (p50 / p95 / p99) |
| E-4 | 기준선 미달 시 CI 실패 |

하네스와 CI 는 1주차에 먼저 깔고, 이후 모듈 개발은 각 트랙이 맡는다.
모듈을 고칠 때마다 숫자가 자동으로 나오므로 "제 방식이 더 나은 것 같은데요" 가 측정으로 대체된다.

## 수치 기록 규칙

측정값은 `_data/metrics.yml` 한 곳에만 쓴다. 한 건에는 반드시 다음이 붙는다.

```yaml
value: 0.66
measured_at: 2026-09-20
commit: a1b2c3d
command: "python eval/run.py --error-rate 0.10"
n: 150
```

넷 중 하나라도 못 채우면 그 숫자는 아직 기록할 준비가 되지 않은 것이다.
현재 실측값 현황은 [진행 상황]({{ '/progress/' | relative_url }}) 에서 볼 수 있다.
