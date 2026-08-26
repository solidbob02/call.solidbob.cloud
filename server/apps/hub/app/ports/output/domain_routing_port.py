# Requirement: B-0
from __future__ import annotations

from abc import ABC, abstractmethod

from hub.app.dtos.domain_classification_dto import DomainClassification


class DomainRoutingPort(ABC):
    """B-0. 통화 초반 발화로 4개 도메인(finance/dasan/shopping/health) 중 하나를 판정한다.
    도메인을 잘못 판정하면 검색 자체가 엉뚱한 인덱스를 보는 셈이라, retrieval보다 먼저
    호출된다. 분류기 추론 → async. 자동 분류로 하기로 한 결정:
    _project/decisions/007-도메인-라우팅-자동분류-확정.md"""

    @abstractmethod
    async def classify(self, utterance: str) -> DomainClassification: ...
