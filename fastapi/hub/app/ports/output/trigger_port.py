# Requirement: B-1
from __future__ import annotations

from abc import ABC, abstractmethod

from hub.app.dtos.transcript_dto import TranscriptEvent
from hub.app.dtos.trigger_decision_dto import TriggerDecision


class TriggerPort(ABC):
    """B-1. 이 전사 이벤트에서 검색을 발동할지, 한다면 언제(at_ms) 발동했는지.
    3주차 v1 은 is_final 도착 기반 (progress 2026-08-25 (12)). 규칙 계산 → def."""

    @abstractmethod
    def decide(self, event: TranscriptEvent) -> TriggerDecision: ...
