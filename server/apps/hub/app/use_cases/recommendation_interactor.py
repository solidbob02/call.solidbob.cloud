# Requirement: B-0, B-1, B-2, B-3, B-4, B-5, B-6
"""추천 파이프라인 — 포트를 순서대로 부르는 것이 전부다. 판정은 하나도 하지 않는다.

    TriggerPort(B-1) ─fire?─▶ DomainRoutingPort(B-0) ─▶ RetrievalPort(B-2·B-3) ─▶ GenerationPort(B-4~B-6)

**여기서 하지 않는 것**(절대 원칙 9 — 판정은 규칙이, 설명만 LLM이):
- 발동 여부를 `if` 로 다시 판단하지 않는다. `TriggerDecision.fire` 를 그대로 따른다.
- 검색 결과 순서를 다시 매기지 않는다. 리랭킹은 retrieval 스포크 몫이다.
- 카드를 지어내지 않는다. 생성이 빈 목록을 주면 "관련 문서 없음"(B-6)으로 그대로 나간다.

`internal_latency_ms` 는 **트리거 발동 시점부터 카드 완성까지**다([4.1절](/docs/04/) p95 ≤1,000ms 채점 재료).
발화 종료 → 화면 표시(e2e)는 게이트웨이·대시보드가 채운다.
"""

from __future__ import annotations

from time import perf_counter
from typing import Callable

from hub.app.dtos.recommendation_card_dto import RecommendationCards
from hub.app.dtos.recommendation_dto import RecommendCommand, RecommendResult
from hub.app.ports.input.recommendation_use_case import RecommendationUseCase
from hub.app.ports.output.domain_routing_port import DomainRoutingPort
from hub.app.ports.output.generation_port import GenerationPort
from hub.app.ports.output.retrieval_port import RetrievalPort
from hub.app.ports.output.trigger_port import TriggerPort


class RecommendationInteractor(RecommendationUseCase):
    def __init__(
        self,
        trigger: TriggerPort,
        retrieval: RetrievalPort,
        generation: GenerationPort,
        domain_routing: DomainRoutingPort | None = None,
        clock: Callable[[], float] = perf_counter,
    ) -> None:
        self._trigger = trigger
        self._retrieval = retrieval
        self._generation = generation
        # B-0 는 선택이다. 스포크가 없으면 도메인을 정하지 않고 전 도메인을 검색한다
        # (decisions/007 의 "신뢰도 낮으면 4개 인덱스 전체 검색" 폴백과 같은 상태).
        self._domain_routing = domain_routing
        self._clock = clock

    async def recommend(self, command: RecommendCommand) -> RecommendResult:
        event = command.event

        decision = self._trigger.decide(event)
        if not decision.fire:
            return RecommendResult(fired=False)  # 검색조차 하지 않는다

        started = self._clock()

        domain = None
        if self._domain_routing is not None:
            domain = (await self._domain_routing.classify(event.text)).domain

        docs = await self._retrieval.retrieve(event.text, top_k=command.top_k)
        cards = await self._generation.to_cards(event.text, docs)

        elapsed_ms = int((self._clock() - started) * 1000)
        return RecommendResult(
            fired=True,
            domain=domain,
            cards=RecommendationCards(
                call_id=event.call_id,
                trigger_at_ms=decision.at_ms or 0,
                cards=tuple(cards),
                internal_latency_ms=elapsed_ms,
            ),
        )
