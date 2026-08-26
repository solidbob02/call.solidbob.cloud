# Requirement: B-2, QUA-1
from evaluation.metrics.retrieval import aggregate_recall_mrr, hit_at_k, reciprocal_rank


def test_hit_at_k_true_when_expected_doc_in_top_k():
    assert hit_at_k(["TERM-3.2"], ["TERM-1.1", "TERM-3.2", "TERM-2.1"], k=5) is True


def test_hit_at_k_false_when_expected_doc_missing():
    assert hit_at_k(["TERM-3.2"], ["TERM-1.1", "TERM-2.1"], k=5) is False


def test_hit_at_k_true_when_no_expected_doc():
    # F-2/C 전용 항목처럼 정답 문서가 없는 케이스는 검색 채점 대상이 아니다.
    assert hit_at_k([], ["TERM-1.1"], k=5) is True


def test_reciprocal_rank_first_position():
    assert reciprocal_rank(["TERM-3.2"], ["TERM-3.2", "TERM-1.1"]) == 1.0


def test_reciprocal_rank_third_position():
    assert reciprocal_rank(["TERM-3.2"], ["TERM-1.1", "TERM-2.1", "TERM-3.2"]) == 1 / 3


def test_reciprocal_rank_not_found():
    assert reciprocal_rank(["TERM-3.2"], ["TERM-1.1"]) == 0.0


def test_aggregate_recall_mrr_excludes_items_without_expected_docs():
    pairs = [
        (["TERM-3.2"], ["TERM-3.2"]),
        ([], ["TERM-1.1"]),  # F-2 전용 케이스 — 분모에서 빠져야 한다
    ]
    result = aggregate_recall_mrr(pairs)
    assert result["n"] == 1
    assert result["recall_at_k"] == 1.0
    assert result["mrr"] == 1.0
