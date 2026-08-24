---
layout: page
title: 5. 부록
nav_order: 5
updated: 2026-08-24
owner: lead
status: agreed
---

## 1) 용어 정의

| 용어 | 정의 |
|---|---|
| **Agent Assist** | 상담원이 통화하는 동안 시스템이 대화를 이해해 답변·문서·다음 행동을 실시간으로 제안하는 제품 범주 |
| **RAG** (Retrieval-Augmented Generation) | 문서를 먼저 검색한 뒤 그 근거만으로 답을 생성하는 방식. 모델의 기억이 아니라 검색된 문서가 답의 출처가 된다 |
| **트리거 판정** | 스트리밍으로 들어오는 미완성 발화 중 **언제 검색을 실행할지** 결정하는 로직. 본 사업의 핵심 난제 |
| **STT** (Speech-to-Text) | 음성 인식. 본 사업에서는 부분 결과를 포함한 스트리밍 인식을 사용 |
| **화자 분리** (Diarization) | 오디오에서 누가 말했는지(고객/상담원) 구분하는 처리 |
| **VAD / 발화 구간 검출** | 침묵과 발화를 구분해 말이 끝난 시점을 판정하는 처리 |
| **BM25** | 단어 빈도 기반 전통적 검색 랭킹 함수. 형태소 분석 결과에 적용된다 |
| **nori** | Elasticsearch 의 한국어 형태소 분석기. 띄어쓰기 오류를 흡수하는 데 사용 |
| **자모 분해 필터** | 한글을 초·중·종성으로 분해해 색인하는 방식. 유사 발음 오인식("해지"→"해제")에 대응 |
| **dense_vector** | 문장을 임베딩한 벡터를 저장하는 ES 필드 타입. 의미 기반 검색에 사용 |
| **하이브리드 검색** | 형태소 검색과 벡터 검색을 함께 실행해 결과를 합치는 방식 |
| **RRF** (Reciprocal Rank Fusion) | 서로 다른 검색 결과의 순위를 역수로 합산해 병합하는 표준 기법 |
| **리랭킹** | 1차 검색 상위 후보를 더 정밀한 모델로 재정렬하는 단계 |
| **청킹** | 긴 문서를 검색 단위로 쪼개는 작업. 쪼개는 방식이 검색 품질을 크게 좌우한다 |
| **골든셋** | 정답이 라벨링된 평가용 시나리오 모음. 자동 채점의 기준 |
| **Recall@5** | 상위 5개 검색 결과 안에 정답 문서가 포함된 비율 |
| **MRR** (Mean Reciprocal Rank) | 정답이 몇 번째에 나왔는지를 역수로 평균한 값. 순위 품질 지표 |
| **재현율 / 정밀도** | 재현율 = 실제 위반 중 잡아낸 비율, 정밀도 = 경고한 것 중 진짜 위반인 비율. 본 사업은 재현율 우선 |
| **환각** (Hallucination) | 근거 문서에 없는 내용을 모델이 지어내는 현상. 특히 수치 환각을 별도 측정한다 |
| **p50 / p95 / p99** | 응답 시간 분포의 백분위. p95 는 100번 중 95번이 그 시간 안에 끝난다는 뜻 |
| **CER** (Character Error Rate) | 음성인식 오류율을 글자 단위로 측정한 값 |
| **기준선** (Baseline) | 개선 전 성능을 고정해둔 수치. 이후 변경이 이보다 나빠지면 CI 가 실패한다 |

## 2) 관련 서식

작업 기록에 사용하는 서식. 규칙 정본은 저장소 루트의 `CLAUDE.md`.

### 개발 로그 (`_posts/YYYY-MM-DD-슬러그.md`)

```yaml
---
layout: post
title: "W{주차} — {한 일}"
date: YYYY-MM-DD HH:MM:SS +0900
categories: log
week: 1
track: [search]     # voice | search | core | classify | frontend | eval | data | infra
status: done        # done | partial | blocked
metrics_touched: false
---
## 한 일
## 판단과 근거      ← 버린 선택지도 한 줄
## 막힌 것
## 다음 세션 첫 작업
```

### 문서 (`_docs/*.md`)

```yaml
---
layout: page
title: 문서 제목
nav_order: 10
updated: 2026-08-24
owner: core         # 담당 트랙
status: draft       # draft | agreed | frozen
---
```

### 결정 기록 (`_project/decisions/NNN-제목.md`)

맥락 / 선택지 / 결정 / 근거 / 결과·되돌리는 법

### 측정값 (`_data/metrics.yml`)

```yaml
value: 0.66
measured_at: 2026-09-20
commit: a1b2c3d
command: "python eval/run.py --error-rate 0.10"
n: 150
```

### 미결 항목 (`_data/open_items.yml`)

```yaml
- id: OI-01
  title: 팀 인원 구성 확정
  why: 5인 분업 전제의 계획. 인원이 적으면 A·C 축소 재계획 필요
  blocks: [w1.schema, w4.chunking]
  owner: user
  status: open        # open | resolved
  opened: 2026-08-24
```

## 3) 참고 자료

### 제품 레퍼런스 (기능 벤치마킹)

| 제품 | 참고 포인트 |
|---|---|
| Amazon Q in Connect | 통화 중 고객 의도 자동 감지 → 실시간 생성 응답·추천 액션·문서 링크. 기능 명세 참고 |
| AWS Live Call Analytics with Agent Assist | **아키텍처 다이어그램과 샘플 코드 공개**. 설계 참고 |
| Google Agent Assist | "Proactive generative knowledge assist" — 본 사업의 트리거 판정과 동일한 문제 |
| LG CNS FCC RT-Advisor | "숙련되지 않은 상담사도" 실시간 지식 제공이라는 가치 제안 |
| KT A'Cen | 불완전판매 방지(STT/TA 모니터링). Barge-in, SAD, 단문발화 등 실시간 음성 처리 난점 목록 |

### 데이터셋

| 출처 | 내용 |
|---|---|
| AI Hub 상담 음성 | 3,000시간. 교육·금융·통신판매, 가상 시나리오, 저작권 해결 |
| AI Hub 고객 응대 음성 | 3,300시간. 감정·의도 태깅 및 요약문 포함 |
| AI Hub 저음질 전화망 음성 | 실제 상담 환경 잡음 포함 |
| AI Hub 민원(콜센터) 질의-응답 | QA 110만쌍 / 음성 440시간+ |
| 서울 열린데이터광장 행정 민원상담 음성 | 56개 시나리오 유형, 8kHz |

### 기술 레퍼런스

| 항목 | 내용 |
|---|---|
| 한국어 STT 벤치마크 | 도메인별 CER 비교 공개 저장소. Google STT 한국어 성능 사전 확인용 |
| Elasticsearch nori | 사용자 사전으로 업계 용어 등록 필수 |
| ES dense_vector + kNN | 하이브리드 검색 구성 |
| RRF | BM25 + 벡터 결과 병합 표준 기법 |
| KLUE 벤치마크 | 한국어 NLU 데이터셋. 분류기 파인튜닝 참고 |

원본 URL 목록은 비공개 기획서(`_project/plan.md` 9절)에 있다.
