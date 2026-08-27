# Requirement: D-4, SEC-2
"""KnowledgeGapQueryPort 프로바이더. PostgreSQL 이 없으면 501.

읽는 쪽이라 "빈 목록"을 돌려주고 싶어지지만 그러지 않는다 — **신고가 0건인 것과
데이터베이스에 못 붙은 것은 다르다.** 빈 목록을 주면 화면에 "공백 없음"으로 보이고,
지식베이스가 완벽하다는 잘못된 신호가 된다.
"""

from __future__ import annotations

from fastapi import Depends, HTTPException, Request, status

from hub.adapter.outbound.postgres.connection import build_connection_factory
from hub.adapter.outbound.postgres.knowledge_gap_query_repository import (
    PostgresKnowledgeGapQueryRepository,
)
from hub.app.ports.input.knowledge_gap_query_use_case import KnowledgeGapQueryUseCase
from hub.app.ports.output.knowledge_gap_query_port import KnowledgeGapQueryPort
from hub.app.use_cases.knowledge_gap_query_interactor import KnowledgeGapQueryInteractor


def get_knowledge_gap_query_port(request: Request) -> KnowledgeGapQueryPort:
    settings = request.app.state.settings
    if not settings.postgres_configured:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="PostgreSQL 이 설정되지 않았습니다 — 쌓인 신고를 읽을 곳이 없습니다 (infra/README.md)",
        )
    return PostgresKnowledgeGapQueryRepository(build_connection_factory(settings))


def get_knowledge_gap_query_use_case(
    gaps: KnowledgeGapQueryPort = Depends(get_knowledge_gap_query_port),
) -> KnowledgeGapQueryUseCase:
    return KnowledgeGapQueryInteractor(gaps=gaps)
