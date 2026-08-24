---
layout: page
title: 시스템 아키텍처
nav_order: 91
updated: 2026-08-24
owner: lead
status: draft
---

```
[상담원 브라우저]  React 대시보드
       │
   WebSocket (양방향)
       │
[Node.js 게이트웨이]
       │  오디오 청크 중계 / 자막·카드·경고 푸시
       ├──→ [Google STT] ──→ 부분 전사 결과
       ▼
[FastAPI 코어]
       ├─ 트리거 판정 모듈   발화 완결성 · 침묵 길이 · 의도 신호
       ├─ 검색 모듈 ──→ [Elasticsearch]  nori(BM25) + dense_vector + RRF
       ├─ 생성 모듈 ──→ [LLM] 근거 기반 요약
       └─ 컴플라이언스 모듈 ──→ [분류기]
       ▼
   [MySQL]  통화 메타 / 상담 이력 / 평가 결과
```

## 도구별 역할

| 도구 | 역할 | 필수도 |
|---|---|---|
| Python / FastAPI | 검색·생성 API, 백엔드 전체 | 필수 |
| Node.js / WebSocket | 실시간 양방향 게이트웨이 | 필수 |
| Google STT | 스트리밍 음성인식 + 화자 분리 | 필수 |
| Elasticsearch | nori + dense_vector 하이브리드 검색 | 필수 |
| HuggingFace Transformers | 임베딩 모델, 컴플라이언스 분류기 | 필수 |
| React | 상담원 대시보드 | 필수 |
| MySQL | 통화 메타·이력·평가 결과 | 필수 |
| Docker | 서비스 컨테이너화 | 필수 |
| matplotlib | 성능 곡선, 레이턴시 분포 | 필수 |
| Kubernetes / AWS / VirtualBox | 배포·테스트 (여유 시) | 선택 |

OpenCV 는 이 주제에 활용처가 없어 사용하지 않는다.

## 화면 구성 (3분할)

| 영역 | 내용 |
|---|---|
| 좌 | 실시간 자막 (화자 구분) |
| 중 | 추천 카드 — 제목 / 근거 요약 / 출처(문서·조항) / 유사도 |
| 우 | 컴플라이언스 경고 — 감지 문구, 시각, 권장 대체 표현 |

## 현재 구현 상태

아직 아무 컴포넌트도 세팅되지 않았다. 진행 상태는 [진행 상황]({{ '/progress/' | relative_url }}) 참조.
