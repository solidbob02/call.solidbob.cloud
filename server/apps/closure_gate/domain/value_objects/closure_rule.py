# Requirement: F-2
"""처리유형별 필수 근거 규칙표.

**출처는 도메인별 내부처리규정(`*-POLICY-*`)이다.** 이 파일은 그 문서를 코드로 옮긴 것이지
새로 만든 규칙이 아니다 — 규정이 바뀌면 문서를 먼저 고치고 여기를 맞춘다.

    knowledge-base/finance/policy/POLICY.md    FIN-POLICY-CLOSE-1 · FIN-POLICY-COMPENSATE-1
    knowledge-base/shopping/policy/POLICY.md   SHOP-POLICY-RETURN-1 · SHOP-POLICY-EXCHANGE-1

다산·질병관리본부 도메인은 **F-2 미적용**이다(안내형 업무라 종결 개념이 없다).
그쪽 규정 문서가 미적용 사유와 대체 수단(D-4)을 명시한다 — 여기에 빈 규칙을 만들지 않는다.

순수 파이썬이다(계약 4 — domain 은 pydantic 도 모른다).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ClosureRule:
    """처리유형 하나의 판정 스펙.

    `required` 의 **선언 순서가 곧 `missing` 의 출력 순서**다. 규정 문서의 표 순서와 같게 둔다 —
    상담원이 화면에서 보는 순서와 규정을 읽는 순서가 어긋나면 무엇을 빠뜨렸는지 찾기 어렵다.
    """

    closure_type: str
    required: tuple[str, ...]
    source_doc_id: str
    source_title: str

    def __post_init__(self) -> None:
        if not self.required:
            raise ValueError(f"필수 근거가 없는 규칙은 만들지 않는다: {self.closure_type}")


# `closure_type` 값은 db/schema.sql 의 CHECK 제약과 같아야 한다 —
# CHECK ("closure_type" IN ('상품해지','보상','반품','교환'))
RULES: dict[str, ClosureRule] = {
    rule.closure_type: rule
    for rule in (
        ClosureRule(
            closure_type="상품해지",
            required=("중도해지수수료_안내", "약정혜택소멸_안내", "고객확인_기록"),
            source_doc_id="FIN-POLICY-CLOSE-1",
            source_title="내부처리규정 — 상품 해지 필수 근거",
        ),
        ClosureRule(
            closure_type="보상",
            required=("사고경위_확인", "귀책여부_확인"),
            source_doc_id="FIN-POLICY-COMPENSATE-1",
            source_title="내부처리규정 — 사고·보상 필수 근거",
        ),
        ClosureRule(
            closure_type="반품",
            required=("환불금액_안내", "환불기간_안내", "상품상태_확인"),
            source_doc_id="SHOP-POLICY-RETURN-1",
            source_title="내부처리규정 — 반품 필수 근거",
        ),
        ClosureRule(
            closure_type="교환",
            required=("교환가능_확인", "재고_확인"),
            source_doc_id="SHOP-POLICY-EXCHANGE-1",
            source_title="내부처리규정 — 교환 필수 근거",
        ),
    )
}
