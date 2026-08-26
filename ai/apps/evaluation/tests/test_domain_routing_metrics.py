# Requirement: B-0, QUA-1
from evaluation.metrics.domain_routing import DOMAINS, score_domain_routing


def test_perfect_predictions_score_1():
    result = score_domain_routing(
        ["finance", "dasan", "shopping", "health"],
        ["finance", "dasan", "shopping", "health"],
    )
    assert result["accuracy"] == 1.0
    assert result["n"] == 4


def test_misclassification_lowers_accuracy():
    result = score_domain_routing(
        ["finance", "shopping"],
        ["finance", "finance"],  # 쇼핑을 금융보험으로 오분류
    )
    assert result["accuracy"] == 0.5
    assert result["confusion"]["shopping"]["finance"] == 1
    assert result["confusion"]["shopping"]["shopping"] == 0


def test_empty_input_reports_nan_not_zero():
    result = score_domain_routing([], [])
    assert result["n"] == 0
    import math

    assert math.isnan(result["accuracy"])


def test_length_mismatch_raises():
    import pytest

    with pytest.raises(ValueError):
        score_domain_routing(["finance"], [])


def test_confusion_matrix_covers_all_four_domains():
    result = score_domain_routing(["finance"], ["finance"])
    assert set(result["confusion"].keys()) == set(DOMAINS)
