# Requirement: B-2
from __future__ import annotations

from dataclasses import dataclass

DOMAINS = ("finance", "dasan", "shopping", "health")
DOC_TYPES = ("TERM", "MANUAL", "POLICY")

# 도메인 접두어(knowledge-base 폴더명 ↔ 문서 ID 접두어). domain.md §3 의 표와 같다.
DOMAIN_BY_PREFIX = {"FIN": "finance", "DASAN": "dasan", "SHOP": "shopping", "HLT": "health"}


@dataclass(frozen=True)
class Chunk:
    """색인 단위 1건. 조항 하나가 그대로 청크 하나가 된다(2026-08-26 실측 근거는 티켓 참고).

    `doc_id` 는 골든셋 `expected_doc_ids` 와 대조되는 단위라 **조항 ID 그대로**여야 한다.
    조항이 상한을 넘어 쪼개진 경우에만 `chunk_id` 가 `doc_id` 와 달라진다(`FIN-TERM-3.2#1`).
    """

    chunk_id: str
    doc_id: str
    domain: str  # "finance" | "dasan" | "shopping" | "health"
    doc_type: str  # "TERM" | "MANUAL" | "POLICY"
    title: str
    text: str
    part: int = 0  # 조항 안에서 몇 번째 조각인지. 분할이 없으면 0
