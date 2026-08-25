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
    for section in ("retrieval", "trigger", "compliance", "masking", "closure_gate"):
        assert report[section] == "측정 불가 — 모듈 미구현"


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
