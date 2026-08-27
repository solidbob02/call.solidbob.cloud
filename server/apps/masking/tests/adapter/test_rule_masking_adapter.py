# Requirement: C-5, SEC-1, QUA-1
"""MaskingPort 계약을 실제로 만족하는지. 허브가 이 어댑터만 보고 쓴다."""

from hub.app.ports.output.masking_port import MaskingPort
from masking.adapter.outbound.rule_masking_adapter import (
    PARTIAL_PATTERNS,
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
    """2.4절 목록 7개에 전부 경로가 있다. 하나라도 빠지면 절대 규칙을 못 지킨다."""
    assert SUPPORTED_PATTERNS == ("P1", "P2", "P3", "P4", "P5", "P6", "P7")
    assert UNSUPPORTED_PATTERNS == ()


def test_규칙으로만_잡는_패턴을_구분해서_드러낸다():
    """P6·P7 은 명세상 NER 인데 규칙으로 깔았다. 평가 하네스가 수치를 해석하려면
    '어떤 방식으로 잡았는지'를 알아야 한다 — 완전 지원과 뭉뚱그리지 않는다."""
    assert PARTIAL_PATTERNS == ("P6", "P7")
    assert set(PARTIAL_PATTERNS) <= set(SUPPORTED_PATTERNS)


def test_P6_P7_도_어댑터_경로로_나온다():
    masked, spans = RuleMaskingAdapter().mask("제 이름은 김민준이고 주소는 서울시 강남구 테헤란로 123번지예요")
    assert {s.type for s in spans} == {"P6", "P7"}
    assert "김민준" not in masked and "강남구" not in masked


def test_개인정보가_없으면_빈_구간이다():
    masked, spans = RuleMaskingAdapter().mask("반품 배송비 문의드립니다")
    assert masked == "반품 배송비 문의드립니다" and spans == ()
