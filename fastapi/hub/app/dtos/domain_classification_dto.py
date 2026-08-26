# Requirement: B-0
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DomainClassification:
    """B-0. 통화가 [4개 도메인](/docs/01/) 중 어디에 속하는지 판정한 결과."""

    domain: str  # "finance" | "dasan" | "shopping" | "health"
    confidence: float
