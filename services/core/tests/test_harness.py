# Requirement: E-1, E-2, E-4, QUA-1
"""하네스 배선(wiring) 검증. 실제 검색/트리거/컴플라이언스/마스킹/게이트 모듈은 아직
없으므로, ①전부 미구현 상태에서 크래시 없이 "N/A"를 정직하게 보고하는지, ②가짜
predictor를 꽂았을 때 golden-set → metrics로 데이터가 올바르게 흘러가는지 두 가지만
확인한다. 실제 정확도 수치를 여기서 하드코딩하지 않는다 (6.2절 원칙 5)."""

from services.core.eval.golden_set import load_golden_set
from services.core.eval.harness import Predictors, run_eval


def test_all_predictors_none_reports_not_implemented():
    items = load_golden_set()
    report = run_eval(items, Predictors())
    for section in ("domain_routing", "retrieval", "trigger", "compliance", "masking", "closure_gate"):
        assert report[section] == "측정 불가 — 모듈 미구현"


class _EchoDomainPredictor:
    """발화 안에 domain 이름이 그대로 있으면 정답을 맞히는 가짜 predictor — 배선만 검증한다."""

    def classify(self, utterance: str) -> str:
        for domain in ("finance", "dasan", "shopping", "health"):
            if domain in utterance:
                return domain
        return "finance"  # 못 찾으면 임의 기본값


def test_domain_routing_wiring_with_fake_predictor():
    items = load_golden_set()
    report = run_eval(items, Predictors(domain=_EchoDomainPredictor()))
    result = report["domain_routing"]
    # 골든셋 10건 전부 domain 필드는 있지만, F-2 케이스(GS-008~010)는 발화 텍스트가
    # 없고 closure_intent만 있어 분류 대상에서 빠진다 — 실제로 분류할 텍스트가 있는
    # 7건만 채점된다.
    assert result["n"] == 7
    # 가짜 predictor는 발화에 도메인 이름이 안 박혀 있으니 대부분 못 맞힌다 —
    # 여기서 검증하는 건 정확도 수치가 아니라 배선(크래시 없이 흘러가는지)이다.
    assert 0.0 <= result["accuracy"] <= 1.0


class _PerfectClosureGate:
    """골든셋의 기대값을 그대로 돌려주는 가짜 predictor — 배선만 검증한다."""

    def evaluate(self, closure_type: str, evidence: dict[str, bool]) -> tuple[str, list[str]]:
        missing = [field for field, ok in evidence.items() if not ok]
        verdict = "approved" if not missing else "blocked"
        return verdict, missing


def test_closure_gate_wiring_with_fake_predictor():
    items = load_golden_set()
    report = run_eval(items, Predictors(closure_gate=_PerfectClosureGate()))
    result = report["closure_gate"]
    assert result["n"] == 3  # GS-008, GS-009, GS-010
    assert result["absolute_rule_passed"] is True


class _FixedDelayTrigger:
    """항상 발화 종료 900ms 뒤에 발동하는 가짜 predictor — 배선과 지연 분포 계산만 검증한다."""

    def trigger_at(self, item) -> int:
        return item.utterance_end_ms + 900


def test_trigger_wiring_reports_latency_distribution():
    items = load_golden_set()
    report = run_eval(items, Predictors(trigger=_FixedDelayTrigger()))
    result = report["trigger"]
    assert result["n"] == 3  # utterance_end_ms가 있는 GS-001~GS-003
    assert result["on_time_rate"] == 1.0  # 900ms는 0~1,500ms 허용 창 안
    assert result["latency_ms"]["p50"] == 900
    assert result["latency_ms"]["p95"] == 900
    assert result["latency_ms"]["n"] == 3
