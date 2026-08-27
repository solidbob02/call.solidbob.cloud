# Requirement: A-1, SEC-1
"""전사 조회 인터랙터. 페이지 경계만 검사하고 포트를 부른다.

**정렬을 여기서 하지 않는다** — 리포지토리가 `segment_id` 순으로 준다. 허브가 다시 정렬하면
DB 인덱스를 못 쓰고, 페이지 경계에서 순서가 어긋난다.
"""

from __future__ import annotations

from hub.app.dtos.transcript_query_dto import MAX_LIMIT, TranscriptPage, TranscriptQuery
from hub.app.ports.input.transcript_query_use_case import TranscriptQueryUseCase
from hub.app.ports.output.transcript_query_port import TranscriptQueryPort


class TranscriptQueryInteractor(TranscriptQueryUseCase):
    def __init__(self, query_port: TranscriptQueryPort) -> None:
        self._query = query_port

    async def list(self, query: TranscriptQuery) -> TranscriptPage:
        if not query.call_id:
            raise ValueError("call_id 가 비어 있습니다")
        if not 1 <= query.limit <= MAX_LIMIT:
            raise ValueError(f"limit 은 1~{MAX_LIMIT} 사이여야 합니다: {query.limit}")
        if query.offset < 0:
            raise ValueError(f"offset 은 0 이상이어야 합니다: {query.offset}")

        segments = await self._query.list_segments(query.call_id, query.limit, query.offset)
        total = await self._query.count_segments(query.call_id)
        return TranscriptPage(
            call_id=query.call_id,
            segments=tuple(segments),
            total=total,
            limit=query.limit,
            offset=query.offset,
        )
