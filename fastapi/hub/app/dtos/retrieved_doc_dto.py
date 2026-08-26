# Requirement: B-2, B-3
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievedDoc:
    """검색 스포크가 돌려주는 조항 1건. 카드(B-4)로 다듬기 전 단계."""

    doc_id: str  # knowledge-base 조항 ID (TERM-3.2 …)
    title: str
    snippet: str  # 폴백 모드에서 카드 summary 로 그대로 쓰인다
    score: float
