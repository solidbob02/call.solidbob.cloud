---
title: "인터페이스 스키마 3종 확정"
assignee: "류준"
role: "ai"
status: "in-progress"
sprint: 1
priority: 5
date: 2026-08-25
---

전사 · 추천 카드 · 종결 판정 3종. 초안은 기획서 [7.3절](/docs/07/)에 있다.

**왜**: 병렬 작업의 전제 조건이다. 확정되지 않으면 세 담당이 서로를 기다린다.

## 컨펌 결과 (2026-08-25, 정성윤)

초안을 `db/schema.sql`·`golden-set/v1-10.json`·`services/core/eval/` 와 대조했다.
**큰 틀은 컨펌.** 다만 지금 고치지 않으면 다음 주에 되돌려야 하는 불일치가 있다.

### 반드시 고칠 것

| # | 항목 | 현재 초안 | 실제 |
|---|---|---|---|
| 1 | `verdict` 값 | `blocked` / `allowed` 검토 중 | **`approved`** / `blocked` — `db/schema.sql:149` ENUM, 골든셋 `expected_verdict`, `eval/golden_set.py:38` 이 전부 `approved` |
| 2 | `source` 표기 | `{"doc": "요금제약관", "clause": "3.2"}` | **문서 ID** — `recommendation_card.source_doc_id` → `document(document_id)`, 골든셋 `expected_doc_ids: ["TERM-3.2"]`, F-2 `source: "POLICY-CANCEL-1"`. 정답 라벨이 ID 형식이라 이름으로 두면 Recall@5 채점 때마다 변환이 필요하다 |
| 3 | `evidence` 키 | 7개 1:1 로 읽힘 | **유형별 부분집합**. 해지(위약금_안내·잔여할부_안내·고객확인_기록) / 명의변경(본인확인_수단·요청경위_확인) / 보상(사유_근거·승인권한_확인). 나머지는 `NULL`(해당 없음) → `missing` 자동 추출은 **`false` 만** 뽑아야 한다 |
| 4 | 발화 식별자 | 없음 | interim 이 20초에 199건 온다. 프론트가 자막을 **교체**하려면 어느 발화의 갱신인지 알아야 하는데 `call_id` 만으로는 구분 불가. `transcript_segment.segment_id` 에 대응하는 **`segment_id` 추가 필요** |

### 정하면 되는 것

| 질문 | 제안 | 근거 |
|---|---|---|
| `span` 기준 | **문자(코드포인트)** | DB `span_start/end INT` 와 일치. 한글은 UTF-8 에서 3바이트라 byte 기준이면 프론트·백이 어긋난다 |
| `score` 범위 | 최종 점수 하나만. RRF 원점수는 `eval_run` 로그로 | 계약은 표시용, 원점수는 실험용 |
| `score` 이름 | DB 는 `similarity_score` — 둘 중 하나로 통일 | 지금 계약 `score` / DB `similarity_score` 로 갈려 있다 |
| `rank` | 배열 순서 = rank 로 명시하거나 필드 추가 | DB `recommendation_card.rank TINYINT` 존재 |
| latency 정의 | `internal` = 트리거 발동 → 카드 응답 완료<br>`e2e` = `utterance_end_ms` → 화면 표시 | e2e 에는 V4 실측 STT 최종 지연 **+346ms** 가 이미 포함된다 |
| `closure_type` | **`보상`** 으로 통일 | DB ENUM `('해지','명의변경','보상')`. 문서 일부에 "보상·환불"로 적혀 있다 |

### 그대로 좋은 것

`masked[].type` P1~P7 (`masking_event.pattern` 과 일치) · `is_final` · `utterance_end_ms`

### 자막 렌더링 (장민석)

199건/20초 ≒ 평균 100ms 간격.
- interim 은 누적하지 말고 **마지막 것만 교체** (그래서 위 4번 `segment_id` 필요)
- `requestAnimationFrame` 또는 100ms 디바운스로 묶기
- **DB 에는 `is_final: true` 만 저장** — interim 까지 넣으면 통화 하나에 수천 행이 쌓인다

## 남은 것

류준이 위 내용을 반영해 **계약 v2** 를 7.3절에 갱신. 그 뒤 3인 최종 확인.
