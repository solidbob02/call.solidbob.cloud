# Requirement: B-1, QUA-1
from services.core.eval.metrics.trigger import aggregate_trigger, classify_trigger


def test_on_time_at_lower_bound():
    assert classify_trigger(utterance_end_ms=3100, trigger_at_ms=3100) == "on_time"


def test_on_time_at_upper_bound_800ms():
    assert classify_trigger(utterance_end_ms=3100, trigger_at_ms=3900) == "on_time"


def test_late_just_over_800ms():
    assert classify_trigger(utterance_end_ms=3100, trigger_at_ms=3901) == "late"


def test_early_before_utterance_ends():
    assert classify_trigger(utterance_end_ms=3100, trigger_at_ms=2900) == "early"


def test_aggregate_trigger_rates():
    labels = ["on_time", "on_time", "early", "late"]
    result = aggregate_trigger(labels)
    assert result["on_time_rate"] == 0.5
    assert result["early_rate"] == 0.25
    assert result["late_rate"] == 0.25
    assert result["n"] == 4
