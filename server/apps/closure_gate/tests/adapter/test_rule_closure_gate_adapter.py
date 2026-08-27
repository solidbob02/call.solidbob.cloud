# Requirement: F-2, QUA-1
"""ClosureGatePort 계약을 실제로 만족하는지. 허브가 이 어댑터만 보고 쓴다."""

import pytest

from closure_gate.adapter.outbound.rule_closure_gate_adapter import (
    SUPPORTED_CLOSURE_TYPES,
    RuleClosureGateAdapter,
)
from closure_gate.domain.services.gate import UnknownClosureType
from hub.app.ports.output.closure_gate_port import ClosureGatePort


def test_ClosureGatePort_구현이다():
    assert isinstance(RuleClosureGateAdapter(), ClosureGatePort)


def test_판정할_수_있는_처리유형을_숨기지_않는다():
    """평가 하네스가 '무엇을 못 보는지' 알아야 한다. 다산·질병관리본부는 F-2 미적용이다."""
    assert SUPPORTED_CLOSURE_TYPES == ("상품해지", "보상", "반품", "교환")


def test_허브_DTO_형태로_돌려준다():
    v = RuleClosureGateAdapter().evaluate(
        "c_001", "반품",
        {"환불금액_안내": True, "환불기간_안내": True, "상품상태_확인": False},
        reason="수거 전",
    )
    assert v.call_id == "c_001" and v.closure_type == "반품"
    assert v.verdict == "blocked" and v.missing == ("상품상태_확인",)
    assert v.source.doc_id == "SHOP-POLICY-RETURN-1"
    assert v.reason == "수거 전"          # 상담원이 적은 사유를 그대로 나른다


def test_게이트가_설명_문장을_만들지_않는다():
    """판정은 규칙이, 설명만 LLM이 한다(절대 원칙 9). `reason` 을 안 주면 비어 있어야 한다 —
    게이트가 문장을 지어내면 그게 판정 근거처럼 읽힌다."""
    v = RuleClosureGateAdapter().evaluate("c_002", "교환", {"교환가능_확인": True, "재고_확인": True})
    assert v.reason is None


def test_판정할_수_없는_처리유형은_예외다():
    with pytest.raises(UnknownClosureType):
        RuleClosureGateAdapter().evaluate("c_003", "민원접수", {"아무거나": True})


def test_받은_근거를_그대로_되돌려준다():
    """화면이 '무엇을 근거로 이 판정이 났는지' 보여줘야 한다."""
    evidence = {"사고경위_확인": True, "귀책여부_확인": False}
    v = RuleClosureGateAdapter().evaluate("c_004", "보상", evidence)
    assert v.evidence == evidence
    evidence["귀책여부_확인"] = True          # 호출자가 나중에 고쳐도
    assert v.evidence["귀책여부_확인"] is False   # 판정 결과는 안 흔들린다
