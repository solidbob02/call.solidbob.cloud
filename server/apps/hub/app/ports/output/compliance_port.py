# Requirement: C-1, C-2, C-3, C-4
from __future__ import annotations

from abc import ABC, abstractmethod

from hub.app.dtos.compliance_finding_dto import ComplianceFinding


class CompliancePort(ABC):
    """C-1~C-4. 상담원 발화에서 위반을 찾는다. 재현율 우선 — 애매하면 잡는다. 분류기 추론 → async."""

    @abstractmethod
    async def detect(self, agent_utterance: str) -> list[ComplianceFinding]: ...
