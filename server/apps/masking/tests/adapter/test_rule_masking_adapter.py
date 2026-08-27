# Requirement: C-5, SEC-1, QUA-1
"""MaskingPort 계약을 실제로 만족하는지. 허브가 이 어댑터만 보고 쓴다."""

from hub.app.ports.output.masking_port import MaskingPort
from masking.adapter.outbound.rule_masking_adapter import (
    SUPPORTED_PATTERNS,
    UNSUPPORTED_PATTERNS,
    RuleMaskingAdapter,
)


def test_MaskingPort_구현이다():
    assert isinstance(RuleMaskingAdapter(), MaskingPort)


def test_허브_DTO_형태로_돌려준다():
    masked, spans = RuleMaskingAdapter().mask("번호는 01012345678 입니다")
    assert "01012345678" not in masked
    assert spans[0].type == "P4"
    assert isinstance(spans[0].span, tuple) and len(spans[0].span) == 2


def test_처리하는_패턴을_숨기지_않는다():
    """P6·P7 은 NER 이 필요해 아직 없다. 평가 하네스가 '무엇을 못 잡는지' 알아야 한다."""
    assert SUPPORTED_PATTERNS == ("P1", "P2", "P3", "P4", "P5")
    assert UNSUPPORTED_PATTERNS == ("P6", "P7")


def test_개인정보가_없으면_빈_구간이다():
    masked, spans = RuleMaskingAdapter().mask("반품 배송비 문의드립니다")
    assert masked == "반품 배송비 문의드립니다" and spans == ()
