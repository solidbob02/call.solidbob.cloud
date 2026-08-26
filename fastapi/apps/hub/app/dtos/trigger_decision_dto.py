# Requirement: B-1
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TriggerDecision:
    """트리거 판정 결과. at_ms 는 발동 시각(통화 기준 ms) — 허용 창(0~1,500ms) 채점과 p50/p95 분포의 재료다."""

    fire: bool
    at_ms: int | None = None  # fire=False 면 None
