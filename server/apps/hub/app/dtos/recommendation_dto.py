# Requirement: B-0, B-1, B-2, B-3, B-4, B-5, B-6
from __future__ import annotations

from dataclasses import dataclass

from .recommendation_card_dto import RecommendationCards
from .transcript_dto import TranscriptEvent


@dataclass(frozen=True)
class RecommendCommand:
    """추천 파이프라인 입력. **마스킹을 이미 거친** 전사 이벤트만 받는다 (SEC-1).

    원문을 받는 시그니처를 만들지 않는 이유는 transcript_ingest 와 같다 — 파이프라인 뒤쪽
    (검색·생성)까지 원문이 흘러가면 마스킹이 앞단에 있는 의미가 없어진다.
    """

    event: TranscriptEvent
    top_k: int = 5


@dataclass(frozen=True)
class RecommendResult:
    """추천 결과. 트리거가 발동하지 않으면 `cards` 는 None 이다 — 빈 카드 묶음과 구분한다.

    - `cards is None`  → 트리거 미발동. 검색조차 하지 않았다
    - `cards.no_relevant_document` → 트리거는 발동했으나 관련 문서 없음 (B-6)

    둘을 같은 값으로 뭉개면 "검색이 안 돈 것"과 "찾았는데 없는 것"을 구분할 수 없다.
    """

    fired: bool
    cards: RecommendationCards | None = None
    domain: str | None = None  # B-0 판정 결과. 스포크가 없으면 None (전 도메인 검색)
