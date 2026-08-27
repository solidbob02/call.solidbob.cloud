# Requirement: A-1, SEC-1
from __future__ import annotations

from dataclasses import dataclass, field

from .transcript_dto import TranscriptEvent

DEFAULT_LIMIT = 100
MAX_LIMIT = 500


@dataclass(frozen=True)
class TranscriptQuery:
    call_id: str
    limit: int = DEFAULT_LIMIT
    offset: int = 0


@dataclass(frozen=True)
class TranscriptPage:
    """한 페이지. `total` 은 그 통화의 확정 발화 총수다.

    interim 은 애초에 저장되지 않으므로([7.3절](/docs/07/)) 여기 세어지지 않는다 —
    20초에 199건씩 오던 것이 화면에서만 교체되고 DB 에는 확정본만 남는다.
    """

    call_id: str
    segments: tuple[TranscriptEvent, ...] = field(default_factory=tuple)
    total: int = 0
    limit: int = DEFAULT_LIMIT
    offset: int = 0
