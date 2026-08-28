# Requirement: B-0
"""AI Hub 표기 ↔ 도메인 코드 매핑. 순수 계산이라 전부 ES·모델 없이 돈다."""

from __future__ import annotations

import pytest

from training.domain.services.domain_labels import (
    DOMAIN_BY_AIHUB_LABEL,
    LABEL_ORDER,
    index_to_label,
    label_to_index,
    to_domain,
)


@pytest.mark.parametrize(
    "aihub, domain",
    [("금융/보험", "finance"), ("다산콜센터", "dasan"), ("K쇼핑", "shopping"), ("질병관리본부", "health")],
)
def test_네_도메인_표기를_모두_옮긴다(aihub, domain):
    assert to_domain(aihub) == domain


def test_앞뒤_공백을_견딘다():
    assert to_domain("  K쇼핑 ") == "shopping"


def test_모르는_표기는_None_이다():
    """폐기된 통신 도메인 같은 것이 섞이면 조용히 아무 라벨이나 주지 않는다."""
    assert to_domain("통신") is None
    assert to_domain("") is None


def test_라벨_순서가_고정돼_있다():
    """학습과 추론이 같은 순서를 봐야 한다. 딕셔너리 순서에 기대면 조용히 어긋난다."""
    assert LABEL_ORDER == ("dasan", "finance", "health", "shopping")
    assert LABEL_ORDER == tuple(sorted(LABEL_ORDER))


def test_인덱스_변환이_왕복한다():
    for d in LABEL_ORDER:
        assert index_to_label(label_to_index(d)) == d


def test_모르는_도메인_인덱스는_거부한다():
    with pytest.raises(ValueError):
        label_to_index("telco")
    with pytest.raises(ValueError):
        index_to_label(len(LABEL_ORDER))


# `retrieval` 쪽 DOMAINS 와 값이 같은지는 여기서 보지 않는다 — `training.tests` 가
# `retrieval` 을 import 하면 module-independence 계약이 깨진다(테스트도 계약 대상이다).
# 교차 검증은 두 모듈 밖인 `ai/tests/test_domain_label_consistency.py` 에 있다.
