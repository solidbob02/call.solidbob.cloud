# Requirement: E-1, E-2, E-4, QUA-1
"""하네스 배선(wiring) 검증. 실제 검색/트리거/컴플라이언스/마스킹/게이트 스포크는 아직
없으므로, ①전부 미구현 상태에서 크래시 없이 "N/A"를 정직하게 보고하는지, ②hub 포트를
구현한 가짜 객체를 꽂았을 때 golden-set → metrics로 데이터가 올바르게 흘러가는지 두 가지만
확인한다. 실제 정확도 수치를 여기서 하드코딩하지 않는다 (6.2절 원칙 5)."""

from evaluation.golden_set import load_golden_set
from evaluation.harness import Ports, run_eval
from hub.app.dtos import ClosureVerdict, MaskedSpan, TranscriptEvent, TriggerDecision
from hub.app.ports.output import ClosureGatePort, MaskingPort, TriggerPort


def test_all_ports_none_reports_not_implemented():
    items = load_golden_set()
    report = run_eval(items, Ports())
    for section in ("retrieval", "trigger", "compliance", "masking", "closure_gate"):
        assert report[section] == "측정 불가 — 모듈 미구현"


class _PerfectClosureGate(ClosureGatePort):
    """골든셋의 기대값을 그대로 돌려주는 가짜 포트 구현 — 배선만 검증한다."""

    def evaluate(self, call_id, closure_type, evidence, reason=None) -> ClosureVerdict:
        missing = tuple(field for field, ok in evidence.items() if not ok)
        return ClosureVerdict(
            call_id=call_id, closure_type=closure_type, evidence=evidence,
            verdict="approved" if not missing else "blocked", missing=missing,
        )


def test_closure_gate_wiring_with_fake_port():
    items = load_golden_set()
    report = run_eval(items, Ports(closure_gate=_PerfectClosureGate()))
    result = report["closure_gate"]
    assert result["n"] == 3  # GS-008, GS-009, GS-010
    assert result["absolute_rule_passed"] is True


class _FixedDelayTrigger(TriggerPort):
    """항상 발화 종료 900ms 뒤에 발동하는 가짜 포트 — 배선과 지연 분포 계산만 검증한다."""

    def decide(self, event: TranscriptEvent) -> TriggerDecision:
        return TriggerDecision(fire=True, at_ms=event.utterance_end_ms + 900)


def test_trigger_wiring_reports_latency_distribution():
    items = load_golden_set()
    report = run_eval(items, Ports(trigger=_FixedDelayTrigger()))
    result = report["trigger"]
    assert result["n"] == 3  # utterance_end_ms가 있는 GS-001~GS-003
    assert result["on_time_rate"] == 1.0  # 900ms는 0~1,500ms 허용 창 안
    assert result["latency_ms"]["p50"] == 900
    assert result["latency_ms"]["p95"] == 900
    assert result["latency_ms"]["n"] == 3
    assert result["not_fired"] == 0


class _DigitsOnlyMasking(MaskingPort):
    """연속 숫자 11자리(P4)만 가리는 가짜 — 절대 규칙이 '1건 누락 = 실패'로 뚫리는지 배선 검증."""

    def mask(self, text: str):
        idx = text.find("01012345678")
        if idx < 0:
            return text, ()
        return text[:idx] + "*" * 11 + text[idx + 11:], (MaskedSpan(type="P4", span=(idx, idx + 11)),)


def test_masking_wiring_reports_misses_per_pattern():
    items = load_golden_set()
    result = run_eval(items, Ports(masking=_DigitsOnlyMasking()))["masking"]
    # GS-006(P1, P2)은 못 가리고 GS-007(P4)만 가린다 → 누락 2건, 절대 규칙 실패
    assert result["absolute_rule_passed"] is False
    assert result["miss_count"] == 2 and result["missed_items"] == ["GS-006", "GS-006"]
