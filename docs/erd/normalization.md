# 스키마 정규화 기록

> 대상: `docs/erd/schema.mmd`
> 초안(5개 테이블, JSON 컬럼 다수) → **3NF 기준 16개 테이블**로 분해한 과정과 근거.
> 초안의 출처는 기획서 rev.4 3절(테이블 이름 5종)과 7.3절 인터페이스 계약이며, 컬럼은 계약에서 유도하거나 추론한 것이다.

---

## 1. 1NF — 반복 그룹 제거

한 컬럼에 값이 여러 개 들어 있으면 조회·집계·무결성이 전부 애플리케이션 책임이 된다.

| 초안 | 문제 | 조치 |
|---|---|---|
| `transcript.masked_spans` (JSON 배열) | 마스킹 구간이 N개. "P2가 몇 건 마스킹됐나"를 SQL로 셀 수 없다 | → **`transcript_mask`** (1:N). `pattern_code`, `span_start`, `span_end` |
| `recommendation.cards` (JSON 배열) | 카드가 N개. 카드별 유사도 분포·출처 집계 불가 | → **`recommendation_card`** (1:N). `rank_no`로 표시 순서 보존 |
| `closure.evidence` (JSON 객체) | 요건별 충족 여부가 키-값 뭉치. 요건이 추가되면 기존 행의 구조가 달라진다 | → **`closure_evidence`** (1:N) |
| `card.source` (중첩 객체) | `{doc, clause}` 중첩 | → `doc_id` FK + `clause_ref` 두 컬럼으로 평탄화 |

### 파생 컬럼 제거

| 초안 | 문제 | 조치 |
|---|---|---|
| `closure.missing` | `evidence` 중 `false`인 것의 목록. **같은 사실을 두 번 저장** → 한쪽만 갱신되면 모순 | **삭제.** `closure_evidence WHERE is_satisfied = false` 로 얻는다 |

> 카드·마스킹 구간을 JSON으로 두면 쓰기는 한 번에 끝나지만, 5주차 "오류율별 마스킹 재현율 곡선"과 7주차 "지식베이스 공백 리포트"가 전부 애플리케이션 코드로 JSON을 풀어야 하는 작업이 된다. **집계가 목적인 데이터는 정규화한다.**

---

## 2. 2NF — 부분 함수 종속 제거

| 초안 | 문제 | 조치 |
|---|---|---|
| `eval_result` | 실질 키가 (`run_id`, `metric`)인데 `commit_sha` · `command` · `golden_set_ver` · `n` · `error_rate` · `measured_at`은 **`run_id`에만 종속**한다. 한 실행에서 지표 8개를 재면 같은 커밋 해시가 8번 반복되고, 하나만 고치면 모순이 생긴다 | → **`eval_run`**(실행 단위 속성) + **`eval_metric`**(지표 값)으로 분해 |

이 분해는 이 저장소의 규칙과도 맞물린다. `CLAUDE.md` 4.4는 측정값 한 건에 `value / measured_at / commit / command / n`을 강제하는데, 정규화하면 **뒤 네 가지가 `eval_run` 한 행에 한 번만** 남는다.

### 함께 정리한 것

| 초안 | 문제 | 조치 |
|---|---|---|
| `eval_result.call_id` | 지표는 골든셋 **전체**에 대한 집계인데 통화 하나를 참조하고 있었다. 카디널리티가 맞지 않는다 | **삭제.** 통화 단위 상세 결과가 필요해지면 `eval_case_result` 층을 따로 만든다 (현재 범위 밖) |

---

## 3. 3NF — 이행 종속 제거

키가 아닌 컬럼이 다른 비키 컬럼을 결정하면 분리한다.

| 초안 | 이행 종속 | 조치 |
|---|---|---|
| `call.agent_id` | 상담원 이름·소속이 통화 행마다 반복된다 | → **`agent`** 마스터 |
| `masked_spans[].type` (P1~P7) | 패턴 코드가 정해지면 이름과 탐지 방식(정규식/NER)이 따라온다 | → **`pii_pattern`** 룩업. `in_absolute_scope`로 "절대 규칙 범위"(P1~P5냐 P1~P7이냐)를 데이터로 표현 |
| `closure.source_doc` (문자열) | 문서명이 여러 행에 반복. 오타·표기 흔들림이 그대로 남는다 | → **`kb_document`** 마스터 + `doc_id` FK |
| 컴플라이언스 경고의 `suggestion` | 규칙이 정해지면 권장 대체 표현(C-4)이 따라온다. 경고마다 문구를 복사하면 문구 수정 시 과거 행과 어긋난다 | → **`compliance_rule`** 룩업 + **`compliance_alert`** |
| 요건 이름·필수 여부 | `closure_type`이 정해지면 필요한 요건 목록이 따라온다 | → **`closure_type`** + **`closure_requirement`** (복합키: 유형 + 요건 코드) |

`closure_requirement`가 **F-2 게이트의 판정 기준표**가 된다. 규정 문서에서 이 표를 채우고, 게이트는 이 표와 `closure_evidence`를 대조해 `verdict`를 정한다. 판정 로직이 코드가 아니라 데이터로 표현되므로 규정이 바뀌어도 재배포가 필요 없다.

---

## 4. 정규화하지 않은 것과 그 이유

| 대상 | 판단 |
|---|---|
| `clause_ref` (조항) | 조항 마스터 테이블을 만들지 않았다. **문서 정본은 Elasticsearch**이고, MySQL에 조항 트리를 두면 이중 관리가 된다. 문자열로 유지 |
| 지표 목표치 | `metric_definition` 같은 테이블을 두지 않았다. 목표 기준선의 정본은 `jekyll/_data/metrics.yml` 하나다. DB에 두면 숫자의 출처가 둘이 된다 |
| 골든셋 본문 | 시나리오·정답 라벨을 DB에 넣지 않았다. `eval_run.golden_set_ver` 문자열로만 참조한다. 골든셋을 파일로 둘지 DB로 옮길지는 **미결** |
| `recommendation.mode`, `speaker`, `verdict` 등 | 값이 2~3개로 고정이고 딸린 속성이 없어 `enum` 유지. 룩업 테이블로 만들면 조인만 늘어난다 |

---

## 5. 트레이드오프 — 실시간 경로의 쓰기 비용

정규화의 대가는 **쓰기 횟수**다.

| | 초안 (JSON) | 정규화 후 |
|---|---|---|
| 추천 1건 저장 | INSERT 1회 | `recommendation` 1 + `recommendation_card` N |
| 전사 1건 저장 | INSERT 1회 | `transcript` 1 + `transcript_mask` N |

레이턴시 예산(내부 처리 p95 ≤ 1,000ms)은 **검색·리랭킹·생성**이 대부분을 쓰므로, DB 쓰기는 응답 경로에서 빼는 것이 전제다.

- 카드·전사 저장은 **응답을 보낸 뒤 비동기로** 처리한다. 사용자 응답 경로에 DB 쓰기를 넣지 않는다
- 카드 N은 상위 3~5개로 작다. 배치 INSERT 한 번이면 충분하다
- 그래도 병목으로 측정되면, 그때 **측정값을 근거로** 역정규화를 결정한다. 지금 추측으로 되돌리지 않는다

---

## 6. 적용 우선순위 — 16개를 1주차에 다 만들지 않는다

3인 8주 프로젝트에서 테이블 16개는 부담이다. 코어(A~E, C-5)에 필요한 것부터 만든다.

| 순위 | 테이블 | 이유 |
|---|---|---|
| **1 (3주차 코어)** | `call`, `transcript`, `transcript_mask`, `pii_pattern` | C-5 마스킹이 3주차 코어. 재현율 곡선이 `transcript_mask` 집계에 걸려 있다 |
| **1 (2~4주차)** | `recommendation`, `recommendation_card`, `kb_document` | 추천 이력과 공백 리포트의 근거 |
| **2 (1주차)** | `eval_run`, `eval_metric` | 평가 하네스가 1주차 산출물. 지표를 파일로만 남기면 이력 비교가 안 된다 |
| **3 (6주차)** | `compliance_rule`, `compliance_alert` | C-1~C-4 구현 시점 |
| **4 (조건부)** | `closure*` 4종 | F-2가 7주차 체크포인트를 통과할 때만 |
| **보류** | `agent` | 상담원 속성이 실제로 필요해질 때. 그전까지 `call.agent_id`는 문자열로 두어도 무방 |

---

## 7. 이 정규화가 건드리는 미결 항목

| 항목 | 내용 |
|---|---|
| **OI-13** | 컴플라이언스 경고를 별도 테이블로 둘지 `recommendation`에 통합할지 → **별도 테이블(`compliance_alert`)을 권고한다.** 경고는 추천과 생명주기·카디널리티가 다르고, 통합하면 카드가 없는 경고 행에 NULL이 대량으로 생긴다. 최종 결정은 1주차 스키마 회의 |
| **OI-03** | 코드 저장소 위치가 정해져야 마이그레이션 파일(DDL)을 어디에 둘지 정할 수 있다 |
| 신규 | 골든셋을 파일로 둘지 DB로 옮길지 |

DDL은 아직 작성하지 않았다. **1주차 스키마 회의에서 이 ERD가 승인된 뒤** 마이그레이션을 만든다.
