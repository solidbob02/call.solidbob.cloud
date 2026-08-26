# Requirement: B-2, B-3
"""POST /hub/search — 상담원 수동 검색. 스키마 ↔ DTO 변환은 여기서만 한다."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from hub.adapter.inbound.api.schemas.search_schema import (
    RetrievedDocSchema,
    SearchRequest,
    SearchResponse,
)
from hub.app.dtos.search_dto import SearchQuery
from hub.app.ports.input.search_use_case import SearchUseCase
from hub.dependencies.search_provider import get_search_use_case

search_router = APIRouter(prefix="/hub", tags=["hub"])


@search_router.post("/search", response_model=SearchResponse)
async def search(
    body: SearchRequest,
    use_case: SearchUseCase = Depends(get_search_use_case),
) -> SearchResponse:
    try:
        result = await use_case.search(SearchQuery(utterance=body.utterance, top_k=body.top_k))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc

    return SearchResponse(
        query=result.query,
        docs=[
            RetrievedDocSchema(doc_id=d.doc_id, title=d.title, snippet=d.snippet, score=d.score)
            for d in result.docs
        ],
    )
