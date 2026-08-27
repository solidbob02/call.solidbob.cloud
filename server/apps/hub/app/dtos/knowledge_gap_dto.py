# Requirement: D-4
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

# db `knowledge_gap.module` ENUM 과 같다. [2.5절 D-4 확장](/docs/02/)의 세 갈래:
#   B 검색 실패 · C 놓친 위반 · F 통과했으나 사후 문제
GapModule = Literal["B", "C", "F"]


@dataclass(frozen=True)
class KnowledgeGapReport:
    """상담원이 직접 누른 신고 1건.

    시스템이 검색 실패를 추정하는 것보다 정확한 라벨이 쌓인다 — [평가 하네스](/docs/06/)가
    골든셋을 늘릴 실사용 후보로 쓴다.
    """

    module: GapModule
    description: str
    call_id: str | None = None
    segment_id: int | None = None
    closure_id: int | None = None


@dataclass(frozen=True)
class KnowledgeGapReceipt:
    """접수 결과. 집계·분석은 `ai/` 몫이라 여기서는 접수 사실만 돌려준다."""

    gap_id: int
    module: GapModule
