# Requirement: B-0, B-1, B-2, B-3, B-4, B-5, B-6
from __future__ import annotations

from abc import ABC, abstractmethod

from hub.app.dtos.recommendation_dto import RecommendCommand, RecommendResult


class RecommendationUseCase(ABC):
    """전사 1건 → (트리거 판정) → 도메인 판별 → 검색 → 카드. 코어 파이프라인이다.

    이 인터랙터가 [4.1절](/docs/04/) "내부 처리 p95 ≤1,000ms" 를 재는 구간이다 —
    트리거 발동 시점부터 카드 완성까지가 `internal_latency_ms` 다.
    """

    @abstractmethod
    async def recommend(self, command: RecommendCommand) -> RecommendResult: ...
