---
layout: page
title: 3. 주요 개발 수행 지침
nav_order: 3
updated: 2026-08-24
owner: lead
status: agreed
---

## 1) 일반 사항

### 인터페이스 계약 우선

1주차에 모듈 간 메시지 스키마를 확정한다. **이것이 병렬 작업의 전제 조건이다.** 계약이 없으면 다섯 트랙이 서로를 기다리게 된다.
계약 문서가 `agreed` 상태가 된 뒤의 변경은 결정 기록을 남긴다. → [인터페이스 계약]({{ '/docs/interface-contract/' | relative_url }})

### 평가 하네스를 먼저 깔고 손을 뗀다

프로젝트 리드가 1주차에 평가 하네스와 CI 를 구축한 뒤, 모듈 개발은 각 트랙에 넘긴다.

- 각자 모듈을 고칠 때마다 숫자가 자동으로 나온다
- "제 방식이 더 나은 것 같은데요" 같은 논쟁이 측정으로 대체된다
- 대신 짜주지 않고 리뷰로 올린다

### 기록이 곧 산출물

본 저장소는 제품 코드 저장소가 아니라 **기록 저장소**다. 작업의 일부로 기록을 남기며, 규칙은 `CLAUDE.md` 가 정본이다.

| | 무엇 | 시간 축 | 수정 |
|---|---|---|---|
| [개발 로그]({{ '/log/' | relative_url }}) | 그날 무엇을 왜 했는가 | 과거·쌓기만 함 | 안 함 |
| 문서 (본 제안서 각 절) | 지금 무엇이 맞는가 | 현재 | 계속 덮어씀 |
| [진행 상황]({{ '/progress/' | relative_url }}) | 어디까지 왔고 숫자는 얼마인가 | 현재 | 계속 갱신 |
| [미결 항목]({{ '/open-items/' | relative_url }}) | 아직 정하지 못한 것 | 현재 | 해소 시 닫음 |

## 2) 개발 표준 및 산출물

### 트랙별 산출물

| 트랙 | 범위 | 산출물 |
|---|---|---|
| ① 음성 파이프라인 | 오디오 스트리밍, STT 연동, 화자 분리, 발화 구간 검출 | 전사 스트림 API |
| ② 검색 | ES 인덱스 설계, nori·자모 필터, 하이브리드 검색, 리랭킹 | 검색 API + 성능 리포트 |
| ③ 실시간 코어 | 트리거 판정, 생성, 레이턴시 최적화, 캐싱 | 추천 API |
| ④ 분류·후처리 | 컴플라이언스 분류기 파인튜닝, 요약, 유형 분류 | 모델 + 지표 |
| ⑤ 프론트·인프라 | React 대시보드, WebSocket, Docker 구성 | 동작하는 화면 |

### 저장소 구조

```
CLAUDE.md            작업 규칙 (세션 시작 시 필독)
_project/            비공개 — 기획서 원본, STATE.md, 결정 기록, 템플릿 (사이트 미게시)
jekyll/              지킬 사이트 루트 — 지킬 명령은 전부 이 안에서 실행
  _posts/            개발 로그 — 과거, 수정하지 않음
  _docs/             제안서 각 절 + 세부 문서 — 현재 사실, 계속 덮어씀
  _data/             milestones.yml 진행률 · metrics.yml 수치 · open_items.yml 미결 항목
```

저장소 루트에는 지킬 사이트(`jekyll/`)와 함께 앞으로 추가될 애플리케이션 코드가 나란히 놓인다.
브랜치는 역할별로 나눈다 — `PM` / `frontend` / `backend` / `flutter`.

### 커밋 규칙

```
log(w3): 스트리밍 STT 파이프라인 연결
docs(search): 인터페이스 계약 v2 확정
data(metrics): 오류율 10% 구간 Recall@5 실측 반영
```

타입: `log` | `docs` | `data` | `code` | `rule` | `chore`

### 결정 기록

되돌리기 어려운 선택(지식베이스 도메인, 트리거 전략, 청킹 방식, 임베딩 모델, 기획서와 다르게 간 지점)은 `_project/decisions/` 에 **맥락 / 선택지 / 결정 / 근거 / 되돌리는 법** 형식으로 남긴다.

## 3) 품질 관리 및 테스트

### 채점 원칙 (변경 금지)

1. **LLM 을 채점자로 쓰지 않는다.** 답을 만든 모델이 자기 답을 심판하면 순환이 된다. 모든 지표를 규칙으로 계산해 재현 가능하게 한다.
2. **측정하지 않은 수치를 기록하지 않는다.** 미측정은 `null` 로 두고 화면에 "미측정"으로 표시한다.
3. **여러 번 실행한 값 중 최저치를 기준선으로 고정한다.** 생성 모델은 같은 입력에도 답이 달라진다.
4. **기준선 미달은 CI 실패.** 목적은 개선이 아니라 회귀 방지다.
5. **실패를 지우지 않는다.** 미달 지표·안 된 실험·틀린 가설은 그대로 남겨 8주차 실패 사례 분석의 재료로 쓴다.

### 목표 기준선

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
| 성능 | 통화당 토큰 비용 | 측정·기록 |

컴플라이언스에서 재현율을 정밀도보다 높게 잡은 것은 의도적이다. **누락(FN)이 오탐(FP)보다 위험**하다는 도메인 비대칭을 지표에 반영했다.

### 수치 기록 형식

모든 성능 수치는 `jekyll/_data/metrics.yml` 한 곳에서 온다. 값 하나에 다음 네 가지가 반드시 붙는다.

```yaml
value: 0.66
measured_at: 2026-09-20      # 언제
commit: a1b2c3d              # 어느 코드로
command: "python eval/run.py --error-rate 0.10"   # 어떻게 재현하나
n: 150                       # 표본 수
```

넷 중 하나라도 못 채우면 그 숫자는 아직 기록할 준비가 되지 않은 것이다.

상세는 [평가 설계]({{ '/docs/evaluation/' | relative_url }}).
