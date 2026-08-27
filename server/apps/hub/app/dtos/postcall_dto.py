# Requirement: D-1, D-2, D-3
from __future__ import annotations

from dataclasses import dataclass, field

from .transcript_dto import TranscriptEvent


@dataclass(frozen=True)
class PostcallCommand:
    """통화 종료 요청. 전사는 **마스킹 완료본**만 담는다 (SEC-1)."""

    call_id: str
    segments: tuple[TranscriptEvent, ...] = field(default_factory=tuple)
