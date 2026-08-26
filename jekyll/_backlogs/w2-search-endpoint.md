---
title: "수동 검색 폴백 — POST /search HTTP 표면"
assignee: "장민석"
role: "ai"
status: "todo"
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
