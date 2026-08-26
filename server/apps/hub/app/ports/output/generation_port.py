# Requirement: B-4, B-5, B-6
from __future__ import annotations

from abc import ABC, abstractmethod

from hub.app.dtos.recommendation_card_dto import Card
from hub.app.dtos.retrieved_doc_dto import RetrievedDoc


class GenerationPort(ABC):
    """B-4~B-6. 검색 결과를 카드로 만든다. 근거가 없으면 빈 목록 (B-6) — 지어내지 않는다.
    폴백 구현은 snippet 을 summary 로 그대로 옮긴다. 모델 추론 → async."""

    @abstractmethod
    async def to_cards(self, utterance: str, docs: list[RetrievedDoc]) -> list[Card]: ...
