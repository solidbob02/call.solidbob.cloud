# Requirement: E-1, E-2, E-4
"""평가 하네스 골격 — [팀 분업 7.2절] 1주차엔 류준이 설계만 하고 이후 운영은 정성윤이
맡는다. 이 파일이 그 "설계"에 해당한다.

지금은 services/core의 실제 검색·트리거·컴플라이언스·마스킹·F-2 모듈이 없다
([Task 1] 스캐폴딩 전). 그래서 각 모듈을 `Predictor` 프로토콜로 추상화해두고,
실제 구현이 붙기 전까지는 `None`으로 둬 "측정 불가 — 미구현"으로 정직하게
보고한다(목표 수치를 지어내지 않는다 — testing.md, 6.2절 원칙 5).

실제 모듈이 생기면 이 프로토콜을 구현하는 클래스를 만들어 `Predictors(...)`에
꽂기만 하면 된다. 채점 로직 자체(metrics/)는 지금 이미 완성돼 있고 단위 테스트로
검증됐다 — services/core/tests/.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from .golden_set import GoldenItem, load_golden_set
from .metrics import closure_gate as closure_gate_metrics
from .metrics import compliance as compliance_metrics
from .metrics import masking as masking_metrics
from .metrics import retrieval as retrieval_metrics
from .metrics import trigger as trigger_metrics


class RetrievalPredictor(Protocol):
    """B-2. 발화를 받아 순위가 매겨진 문서 ID 목록을 반환한다."""

    def retrieve(self, utterance: str) -> list[str]: ...


class TriggerPredictor(Protocol):
    """B-1. 골든셋 항목을 받아 트리거가 발동된 시각(ms)을 반환한다."""

    def trigger_at(self, item: GoldenItem) -> int: ...


class CompliancePredictor(Protocol):
    """C-1~C-4. 발화를 받아 위반 여부를 반환한다."""

    def detect_violation(self, utterance: str) -> bool: ...


class MaskingPredictor(Protocol):
    """C-5. 발화를 받아 실제로 마스킹된 패턴 목록(P1~P7)을 반환한다."""

    def masked_patterns(self, utterance: str) -> list[str]: ...


class ClosureGatePredictor(Protocol):
    """F-2. 처리 유형과 근거 필드를 받아 (판정, 미충족 필드 목록)을 반환한다."""

    def evaluate(self, closure_type: str, evidence: dict[str, bool]) -> tuple[str, list[str]]: ...


@dataclass
class Predictors:
    """구현되지 않은 모듈은 None으로 둔다 — 해당 지표는 리포트에서 "미구현"으로 표시된다."""

    retrieval: RetrievalPredictor | None = None
    trigger: TriggerPredictor | None = None
    compliance: CompliancePredictor | None = None
    masking: MaskingPredictor | None = None
    closure_gate: ClosureGatePredictor | None = None


NOT_IMPLEMENTED = "측정 불가 — 모듈 미구현"


def run_eval(items: list[GoldenItem], predictors: Predictors) -> dict:
    report: dict = {}

    # B: 검색 (Recall@5, MRR)
    b_items = [it for it in items if it.module == "B"]
    if predictors.retrieval is None:
        report["retrieval"] = NOT_IMPLEMENTED
    else:
        pairs = [
            (it.expected_doc_ids, predictors.retrieval.retrieve(it.customer_utterance or ""))
            for it in b_items
        ]
        report["retrieval"] = retrieval_metrics.aggregate_recall_mrr(pairs)

    # B-1: 트리거 (GS-001처럼 trigger_examples가 있는 항목만 채점 가능)
    if predictors.trigger is None:
        report["trigger"] = NOT_IMPLEMENTED
    else:
        labels = []
        for it in items:
            if it.utterance_end_ms is None:
                continue
            trigger_at = predictors.trigger.trigger_at(it)
            labels.append(trigger_metrics.classify_trigger(it.utterance_end_ms, trigger_at))
        report["trigger"] = trigger_metrics.aggregate_trigger(labels)

    # C-1~C-4: 컴플라이언스 (재현율/정밀도)
    c_items = [it for it in items if it.module in ("C-1", "C-2", "C-3", "C-4")]
    if predictors.compliance is None:
        report["compliance"] = NOT_IMPLEMENTED
    else:
        expected = [it.compliance_violation is not None for it in c_items]
        predicted = [
            predictors.compliance.detect_violation(it.agent_utterance or it.customer_utterance or "")
            for it in c_items
        ]
        report["compliance"] = compliance_metrics.score_binary_predictions(expected, predicted)

    # C-5: 마스킹 (절대 규칙)
    if predictors.masking is None:
        report["masking"] = NOT_IMPLEMENTED
    else:
        cases = []
        for it in items:
            if not it.pii_patterns:
                continue
            predicted_patterns = predictors.masking.masked_patterns(it.customer_utterance or "")
            for pii in it.pii_patterns:
                cases.append(
                    masking_metrics.MaskingCase(
                        item_id=it.id,
                        pattern=pii.pattern,
                        should_be_masked=pii.masked_expected,
                        was_masked=pii.pattern in predicted_patterns,
                    )
                )
        report["masking"] = masking_metrics.score_masking(cases)

    # F-2: 종결 게이트 (절대 규칙)
    f2_items = [it for it in items if it.f2_case is not None]
    if predictors.closure_gate is None:
        report["closure_gate"] = NOT_IMPLEMENTED
    else:
        predictions = []
        for it in f2_items:
            case = it.f2_case
            verdict, missing = predictors.closure_gate.evaluate(case.closure_type, case.evidence)
            predictions.append(
                closure_gate_metrics.F2Prediction(
                    item_id=it.id,
                    expected_verdict=case.expected_verdict,
                    predicted_verdict=verdict,
                    expected_missing=case.expected_missing,
                    predicted_missing=missing,
                )
            )
        report["closure_gate"] = closure_gate_metrics.score_closure_gate(predictions)

    return report


def main() -> None:  # pragma: no cover — 수동 실행용
    from .report import print_report

    items = load_golden_set()
    report = run_eval(items, Predictors())  # 전부 미구현 상태로 골격만 확인
    print_report(report, golden_set_path=Path(__file__).resolve().parents[3] / "golden-set" / "v1-10.json")


if __name__ == "__main__":  # pragma: no cover
    main()
