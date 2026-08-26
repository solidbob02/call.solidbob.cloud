# Requirement: 7.3절 전사 이벤트, C-5
"""HTTP 표면 스키마. 응답 필드명은 7.3절 계약 JSON 과 같다."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class TranscriptIngestRequest(BaseModel):
    call_id: str
    segment_id: int
    speaker: Literal["customer", "agent"]
    text: str = Field(description="마스킹 전 원문. 응답 이후 서버 어디에도 남지 않는다 (SEC-1)")
    is_final: bool
    utterance_end_ms: int | None = None


class MaskedSpanSchema(BaseModel):
    type: str
    span: tuple[int, int]


class TranscriptEventSchema(BaseModel):
    call_id: str
    segment_id: int
    speaker: Literal["customer", "agent"]
    text: str
    masked: list[MaskedSpanSchema]
    is_final: bool
    utterance_end_ms: int | None = None
