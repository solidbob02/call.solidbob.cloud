---
title: "잠정 베이스라인 측정 — Recall@5 · MRR"
assignee: "류준·장민석"
role: "ai"
status: "done"
sprint: 2
priority: 5
date: 2026-08-26
requirement:
  - "B-2"
  - "E-1"
---

단순 RAG + 골든셋 50건으로 **첫 실측치**를 낸다. 이 프로젝트에서 처음으로 숫자가 기록되는 시점이다.

## 지켜야 할 것

- **여러 번 실행한 값 중 최저치**를 기록한다([6.2절](/docs/06/) 원칙 2)
- 값 하나에 **측정일 · 커밋 · 재현 명령 · 표본 수**가 함께 남아야 한다. 넷 중 하나라도
  못 채우면 그 숫자는 아직 기록할 준비가 안 된 것이다
- 이 값은 **잠정**이다. CI 기준선으로 고정하지 않는다 — 3주차 150건 재측정값이 공식 기준선

## 기록 위치

`db` 의 `eval_run`/`eval_result`, [진행상황](/progress/), 그리고 [6.1절](/docs/06/) 지표 표.

## 완료 조건

`services/core/eval/` 하네스가 "측정 불가 — 모듈 미구현" 대신 실제 수치를 출력한다.

---

## 2026-08-27 측정 완료 (류준)

| 지표 | 값 | 목표 | |
|---|---|---|---|
| 검색 Recall@5 | **0.857** (12/14) | ≥0.70 | ✅ |
| 검색 MRR | **0.702** | ≥0.55 | ✅ |
| B-0 도메인 분류 정확도 | **0.647** (22/34) | ≥0.95 | ❌ |

**측정일** 2026-08-27 · **커밋** `39cbe68` 기준 작업분 · **표본** `golden-set/v1-50.json`
(검색 14건 / 도메인 34건) · **재현 명령**:

```bash
cd infra && docker compose up -d elasticsearch && cd ..
export ELASTICSEARCH_URL=http://localhost:9200
.venv/bin/python scripts/index_knowledge_base.py --to-es --recreate
.venv/bin/python scripts/run_eval.py --golden-set golden-set/v1-50.json --runs 3
```

**3회 실행 최저치 = 1회 값.** BM25 도 검색 기반 도메인 판정도 결정적이라 흔들리지 않는다 —
절대 원칙 4의 "최저치 고정"이 여기서는 자명하게 성립한다. 임베딩이 들어가는 4주차부터는 다시 본다.

**잠정치다.** 공식 기준선은 3주차 150건이고 CI 게이트로 고정하지 않는다([w2-baseline-gate](/backlog/w2-baseline-gate/)).

### B-0 이 목표에 못 미치는 이유 — 오분류가 전부 `finance` 로 쏠린다

```
정답\예측   finance  dasan  shopping  health
finance         9      0        0        0     ← 9/9
dasan           2      6        0        1     ← 6/9
shopping        4      0        4        1     ← 4/9
health          3      1        0        3     ← 3/7
```

**문서 수 불균형**(finance 34 · shopping 27 · health 21 · dasan 20)이 그대로 편향이 됐다.
지금 구현은 분류 모델이 아니라 **검색 결과의 도메인 분포**로 판정하는 v1 이라, 문서가 많은
도메인이 상위를 더 자주 차지한다. 이 값은 KcELECTRA 분류기가 **넘어야 할 기준선**이다.

### 기록하지 않은 것

`db` 의 `eval_run`/`eval_result` 적재는 **하지 않았다.** PostgreSQL 전환(`decisions/018`)
직후라 스키마와 접속 경로를 `server/` 와 맞춰야 하고, 그건 이 티켓 범위 밖이다.
[6.1절 지표 표](/docs/06/)와 이 티켓에 네 가지(측정일·커밋·명령·표본 수)를 모두 남겼다.
