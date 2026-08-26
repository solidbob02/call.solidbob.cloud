# Requirement: 7.3절 종결 판정, F-2
"""종결 판정 (F-2 게이트 결과) — 나르기만 한다.

계약 v2 예시:
    {"call_id": "c_001", "closure_type": "해지", "reason": "고지 완료",
     "evidence": {"위약금_안내": true, "잔여할부_안내": false, "고객확인_기록": false},
     "verdict": "blocked", "missing": ["잔여할부_안내", "고객확인_기록"],
     "source": {"doc_id": "POLICY-CANCEL-1", "title": "내부처리규정 해지 필수 근거"}}

- evidence 는 closure_type 별 부분집합만 담는다 (decisions/003 ③). 필드명은 db/schema.sql `closure` 컬럼과 같다.
- verdict·missing 이 evidence 와 맞는지는 이 DTO 가 검사하지 않는다. 그 규칙은 closure_gate 스포크의
  domain/services 가 소유하고(docs/architecture.md §2), 골든셋으로 evaluation 이 채점한다(절대 규칙 — 1건이라도 어긋나면 실패).
  허브는 도메인 로직을 갖지 않는다 (§1).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from .recommendation_card_dto import Source

# 처리유형은 도메인별 내부처리규정(*-POLICY-*)이 정의한다 — 금융보험: 상품해지·사고보상, 쇼핑: 반품·교환.
# 값 집합이 도메인마다 다르므로 Literal 로 고정하지 않는다 (docs/domain.md §4.3).
ClosureType = str
Verdict = Literal["approved", "blocked"]


@dataclass(frozen=True)
class ClosureVerdict:
    call_id: str
    closure_type: ClosureType
    evidence: dict[str, bool]
    verdict: Verdict
    missing: tuple[str, ...] = field(default_factory=tuple)
    reason: str | None = None
    source: Source | None = None  # 판정 근거 규정 (POLICY-*-1)
