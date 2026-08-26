---
title: "수동 검색 폴백 — POST /search HTTP 표면"
assignee: "장민석"
role: "ai"
status: "done"
sprint: 2
priority: 2
date: 2026-08-26
paths:
  - "server/apps/hub/adapter/inbound/api/v1/*"
---

추천이 빗나갔을 때 상담원이 직접 검색하는 경로. **[Recall@5 목표가 0.70](/docs/06/) 이라는 건
10건 중 3건은 못 찾는다는 뜻**이므로, 폴백이 없으면 그 3건에서 상담원이 막힌다.
Genesys Agent Copilot·Amazon Connect 둘 다 자동 추천과 **함께** 검색을 제공한다.

## 지금 당장 할 수 있다

`RetrievalPort` 는 **이미 있다**(`app/ports/output/retrieval_port.py`). DB 도 필요 없다.

```python
async def retrieve(self, utterance: str, top_k: int = 5) -> list[RetrievedDoc]: ...
```

`server/` 가 할 일은 **HTTP 경계뿐**이다 — 라우터·스키마·유스케이스. 실제 검색은 `ai/` 쪽
구현체가 꽂히면 동작한다. 구현체가 없는 동안은 `POST /hub/transcripts` 와 같은 방식으로
**501** 을 돌려준다(임시 통과 경로를 만들지 않는다).

## 할 것

[`architecture.md` §3](https://github.com/solidbob02/call.solidbob.cloud/blob/main/docs/architecture.md) 프랙탈 단면대로:

```
adapter/inbound/api/schemas/search_schema.py
adapter/inbound/api/v1/search_router.py
app/dtos/search_dto.py
app/ports/input/search_use_case.py
app/use_cases/search_interactor.py
dependencies/search_provider.py
tests/app/use_cases/test_search_interactor.py      스텁 포트로
tests/adapter/test_search_router.py                구현체 미등록 시 501
```

## 완료 조건

`POST /search` 가 `RetrievedDoc` 목록을 돌려주고, 구현체 미등록 시 501. 스텁 포트로 인터랙터
테스트 통과. `PYTHONPATH=apps lint-imports` 계약 3종 KEPT.

## 2026-08-26 — 구현 완료

[§3 프랙탈 단면](https://github.com/solidbob02/call.solidbob.cloud/blob/main/docs/architecture.md) 그대로 8개 파일.

```
adapter/inbound/api/schemas/search_schema.py    SearchRequest · RetrievedDocSchema · SearchResponse
adapter/inbound/api/v1/search_router.py         POST /hub/search
app/dtos/search_dto.py                          SearchQuery · SearchResult (frozen)
app/ports/input/search_use_case.py              SearchUseCase ABC
app/use_cases/search_interactor.py              RetrievalPort 호출 + 입력 검증
dependencies/retrieval_provider.py              미등록 시 501
dependencies/search_provider.py                 DI
tests/app/use_cases/ · tests/adapter/           17건
```

**빈 목록으로 통과시키지 않고 501 을 돌려준다.** 빈 결과는 "관련 문서 없음"(B-6)과 구분되지
않아서, 200 으로 통과시키면 검색이 죽은 것인지 정말 없는 것인지 알 수 없게 된다
(절대 원칙 10 — 측정할 수 없는 상태를 만들지 않는다). `masking_provider` 가 같은 이유로 501 인 것과 같다.

**순위를 허브가 다시 매기지 않는다** — retrieval 스포크가 준 순서를 그대로 유지한다.
허브가 정렬에 손대면 자동 추천과 수동 검색이 서로 다른 순위를 내놓는다. 테스트로 고정했다.

**의존성 해석이 본문 검증보다 먼저다.** 스포크 미등록 상태에서는 입력이 잘못돼도 422 가
아니라 501 이 난다 — 구현이 없다는 사실이 먼저 알려지는 쪽이 맞다고 보고 그대로 뒀고,
테스트로 그 순서를 문서화했다.

**검증**: `cd server && pytest` 28개 통과(11→28) · `lint-imports` 계약 3종 KEPT ·
라우트 표에 `POST /hub/search` 확인.

**남은 것**: `ai/apps/retrieval/` 이 `RetrievalPort` 를 구현하면 `main.py` 의
`dependency_overrides[get_retrieval_port]` 에 꽂는다. 그 전까지 이 엔드포인트는 501 이다.
