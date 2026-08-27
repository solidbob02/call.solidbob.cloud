# Requirement: D-4
"""HTTP 표면 스키마 — 공백 리포트 조회·집계·상태 전이."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class KnowledgeGapItemSchema(BaseModel):
    gap_id: int
    module: Literal["B", "C", "F"] = Field(
        description="B 검색 실패 · C 놓친 위반 · F 통과했으나 사후 문제 (2.5절)"
    )
    description: str
    status: Literal["open", "resolved"]
    created_at: datetime
    call_id: str | None = None
    segment_id: int | None = None
    closure_id: int | None = None
    domain: str | None = Field(default=None, description="통화에서 따라온다. 통화가 없는 신고는 null")


class KnowledgeGapPageResponse(BaseModel):
    gaps: list[KnowledgeGapItemSchema]
    total: int = Field(description="필터를 적용한 전체 건수. 이 페이지의 건수가 아니다")
    limit: int
    offset: int


class GapCountSchema(BaseModel):
    key: str
    open: int
    resolved: int
    total: int


class KnowledgeGapSummaryResponse(BaseModel):
    """⚠ 세기만 한다. 우선순위·심각도 필드를 두지 않는다 (부록 A-1)."""

    by_module: list[GapCountSchema]
    by_domain: list[GapCountSchema] = Field(
        description="통화가 연결된 신고만 세어진다 — by_module 총합과 다를 수 있다"
    )
    total: int = Field(description="모듈 축 기준 총계")


class GapResolutionRequest(BaseModel):
    status: Literal["open", "resolved"] = Field(
        description="되돌리기(resolved→open)도 허용한다 — 잘못 닫은 것을 기록에서 지우지 않는다"
    )


class GapResolutionResponse(BaseModel):
    gap_id: int
    status: Literal["open", "resolved"]
