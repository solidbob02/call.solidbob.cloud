# Requirement: B-1, E-1
"""트리거 판정 채점. [핵심 기술 난제 4.1절] 발화 종료 후 0~1,500ms 이내 발동을 "적절"로,
그 전을 "조기", 1,500ms 초과를 "지연"으로 판정한다. [평가 설계 6.1절] 목표: 적절 발동률
≥0.85, 조기/지연은 별도 집계.

800ms → 1,500ms: 보완지시서 1번(안 A) — 침묵 기반 트리거(700~1,000ms 대기)가
800ms 창 안에서는 구조적으로 "지연"으로만 집계돼 0.85 목표가 애초에 불가능했다.
2026-08-25 팀 컨펌으로 확정. `_project/decisions/001-기획서-rev4-채택.md` 참고."""

from __future__ import annotations

from typing import Literal

TriggerLabel = Literal["early", "on_time", "late"]

ON_TIME_WINDOW_MS = (0, 1500)


def classify_trigger(utterance_end_ms: int, trigger_at_ms: int) -> TriggerLabel:
    delta = trigger_at_ms - utterance_end_ms
    if delta < ON_TIME_WINDOW_MS[0]:
        return "early"
    if delta > ON_TIME_WINDOW_MS[1]:
        return "late"
    return "on_time"


def aggregate_trigger(labels: list[TriggerLabel]) -> dict[str, float]:
    if not labels:
        return {"on_time_rate": float("nan"), "early_rate": float("nan"), "late_rate": float("nan"), "n": 0}
    n = len(labels)
    return {
        "on_time_rate": labels.count("on_time") / n,
        "early_rate": labels.count("early") / n,
        "late_rate": labels.count("late") / n,
        "n": n,
    }
