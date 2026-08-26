# Requirement: C-5, SEC-1
from __future__ import annotations

from abc import ABC, abstractmethod

from hub.app.dtos.transcript_dto import MaskedSpan


class MaskingPort(ABC):
    """C-5. 파이프라인의 첫 단계 — 이 포트를 거치기 전의 문자열은 허브 밖으로 나가지 않는다."""

    @abstractmethod
    def mask(self, text: str) -> tuple[str, tuple[MaskedSpan, ...]]:
        """원문을 받아 (마스킹된 텍스트, 마스킹 구간 목록)을 돌려준다. CPU-bound → def."""
