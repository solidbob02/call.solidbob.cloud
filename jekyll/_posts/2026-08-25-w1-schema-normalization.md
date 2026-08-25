---
layout: post
title: "W1 — DB 스키마 3NF 정규화 (5개 → 16개 테이블)"
date: 2026-08-25 11:46:00 +0900
categories: log
week: 1
track: [infra, data]
status: done
metrics_touched: false
---

## 한 일

ERD 초안을 1NF → 2NF → 3NF 순으로 검토하고 다시 그렸다. 분해 근거는 `docs/erd/normalization.md`에 단계별로 남겼다.

**1NF — 반복 그룹 제거**

| 초안 | 조치 |
|---|---|
| `transcript.masked_spans` (JSON 배열) | → `transcript_mask` (1:N) |
| `recommendation.cards` (JSON 배열) | → `recommendation_card` (1:N), `rank_no`로 순서 보존 |
| `closure.evidence` (JSON 객체) | → `closure_evidence` (1:N) |
| `closure.missing` | **삭제** — `evidence`에서 파생된 중복 저장 |

**2NF — 부분 함수 종속 제거**

`eval_result`의 실질 키는 (`run_id`, `metric`)인데 `commit_sha`·`command`·`golden_set_ver`·`n`·`error_rate`·`measured_at`이 `run_id`에만 종속했다. 한 실행에서 지표 8개를 재면 같은 커밋 해시가 8번 반복된다. → `eval_run` + `eval_metric`으로 분해.

`eval_result.call_id`도 삭제했다. 지표는 골든셋 전체에 대한 집계인데 통화 하나를 참조하고 있어 카디널리티가 맞지 않았다.

**3NF — 이행 종속 제거**

`agent`(상담원 마스터), `pii_pattern`(P1~P7 룩업), `kb_document`(문서 마스터), `compliance_rule` + `compliance_alert`, `closure_type` + `closure_requirement` 분리.

결과: **5개 → 16개 테이블.**

## 판단과 근거

- **집계가 목적인 데이터는 정규화한다.** JSON으로 두면 쓰기는 한 번에 끝나지만, 5주차 "오류율별 마스킹 재현율 곡선"과 7주차 "지식베이스 공백 리포트"가 전부 애플리케이션에서 JSON을 풀어야 하는 작업이 된다. 두 지표는 프로젝트의 대표 산출물이라 SQL로 집계 가능해야 한다.
- **`closure_requirement`가 F-2 게이트의 판정 기준표가 된다.** 규정 문서에서 이 표를 채우면 게이트는 표와 `closure_evidence`를 대조해 `verdict`를 정한다. **판정 로직이 코드가 아니라 데이터**가 되므로 규정이 바뀌어도 재배포가 필요 없다. rev.4 부록 A-2("판정은 규칙이 한다")와도 맞는다.
- **정규화하지 않은 것도 근거를 적었다.** 조항(`clause_ref`) 마스터를 만들지 않은 것은 문서 정본이 Elasticsearch이기 때문이고, 지표 목표치를 DB에 두지 않은 것은 정본이 `metrics.yml` 하나여야 하기 때문이다. 룩업으로 만들 이유가 없는 2~3값 컬럼(`mode`, `speaker`, `verdict`)은 `enum`으로 남겼다.
- **트레이드오프를 문서에 남겼다.** 정규화의 대가는 쓰기 횟수다. 추천 1건이 INSERT 1회에서 1 + N회가 된다. 레이턴시 예산은 검색·리랭킹·생성이 대부분을 쓰므로 **DB 쓰기는 응답 경로에서 빼고 비동기 처리**하는 것을 전제로 했다. 병목으로 측정되면 그때 역정규화하되, **지금 추측으로 되돌리지는 않는다.**
- **16개를 1주차에 다 만들지 않는다.** 3인 8주에 테이블 16개는 부담이라 적용 순서를 정했다 — 3주차 코어(전사·마스킹) → 추천 → 1주차 평가 계열, 종결 계열은 F-2가 체크포인트를 통과할 때. `agent`는 상담원 속성이 실제로 필요해질 때까지 보류.
- OI-13(컴플라이언스 경고 테이블)에 **권고안을 붙였다** — 별도 테이블. 다만 결정은 1주차 스키마 회의 몫이라 항목은 열어 뒀다.

## 막힌 것

없음. 테이블이 늘어 다이어그램 폭이 부족해져 렌더 폭을 1800 → 2400으로 올렸다(2384×909). 이미지를 열어 16개 테이블과 한글이 정상인지 확인했다.

## 다음 세션 첫 작업

**AI Hub 데이터 신청**과 **V1·V2 확인**(채널 구성 / GPU 가용 여부). 스키마는 1주차 회의에서 `w1.schema`(계약 3종)와 함께 승인받은 뒤 DDL을 작성한다 — 승인 전에 마이그레이션을 만들지 않는다.
