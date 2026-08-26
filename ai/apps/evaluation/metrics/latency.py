# Requirement: E-3
"""레이턴시 분포. [핵심 기술 난제 4.3절] 내부 처리와 E2E 체감을 분리해서 각각 p50/p95/p99
로 기록한다. 내부 처리 p95 목표만 ≤1,000ms이고, E2E는 목표 없이 측정·기록만 한다."""

from __future__ import annotations

import math


def percentile(values: list[float], p: float) -> float:
    """p는 0~100. 선형 보간 방식(가장 흔한 정의)을 쓴다."""
    if not values:
        return float("nan")
    s = sorted(values)
    if len(s) == 1:
        return s[0]
    rank = (p / 100) * (len(s) - 1)
    lower = math.floor(rank)
    upper = math.ceil(rank)
    if lower == upper:
        return s[int(rank)]
    weight = rank - lower
    return s[lower] * (1 - weight) + s[upper] * weight


def summarize_latency(values_ms: list[float]) -> dict[str, float]:
    return {
        "p50": percentile(values_ms, 50),
        "p95": percentile(values_ms, 95),
        "p99": percentile(values_ms, 99),
        "n": len(values_ms),
    }
