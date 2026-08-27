# Requirement: A-1, SEC-1
"""HTTP 표면 스키마. 전사 이벤트 필드명은 7.3절 계약과 같다."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class MaskedSpanSchema(BaseModel):
    type: str
    span: tuple[int, int] = Field(description="문자(코드포인트) 오프셋 — byte 아님 (7.3절)")


class TranscriptSegmentSchema(BaseModel):
    segment_id: int
    speaker: Literal["customer", "agent"]
    text: str = Field(description="마스킹 완료본만 (SEC-1)")
    masked: list[MaskedSpanSchema]
    is_final: bool
    utterance_end_ms: int | None = None


class TranscriptPageResponse(BaseModel):
    call_id: str
    segments: list[TranscriptSegmentSchema]
    total: int = Field(description="확정 발화 총수. interim 은 저장되지 않으므로 세어지지 않는다")
    limit: int
    offset: int
