# Requirement: B-0
"""`retrieval` 과 `training` 이 같은 네 도메인을 보는지 확인한다.

**여기가 `apps/` 밖인 이유**: 두 모듈은 서로를 import 할 수 없다(`.importlinter` 계약 2 —
테스트도 계약 대상이다). 그래서 값이 어긋나도 어느 쪽도 알아채지 못한다.
계약 밖인 이 자리에서만 양쪽을 함께 볼 수 있다.

어긋나면 조용히 무너진다 — 학습은 4클래스로 하는데 라우팅이 다른 이름을 기대하거나,
색인의 도메인 필드 값과 분류기 출력이 달라 필터가 아무것도 못 거른다.
"""

from __future__ import annotations

from retrieval.domain.value_objects.chunk import DOMAIN_BY_PREFIX, DOMAINS
from training.domain.services.domain_labels import (
    DOMAIN_BY_AIHUB_LABEL,
    LABEL_ORDER,
)


def test_두_모듈이_같은_네_도메인을_본다():
    assert set(LABEL_ORDER) == set(DOMAINS)


def test_AI_Hub_표기가_그_네_도메인으로만_간다():
    assert set(DOMAIN_BY_AIHUB_LABEL.values()) == set(DOMAINS)


def test_문서_ID_접두어도_같은_네_도메인을_가리킨다():
    """색인의 `domain` 필드 값과 분류기 출력이 같아야 필터가 듣는다."""
    assert set(DOMAIN_BY_PREFIX.values()) == set(LABEL_ORDER)


def test_라벨_순서가_결정적이다():
    """학습이 본 순서와 추론이 보는 순서가 같아야 한다 — 다르면 정확도가 조용히 무너진다."""
    assert LABEL_ORDER == tuple(sorted(LABEL_ORDER))
    assert len(LABEL_ORDER) == len(set(LABEL_ORDER)) == 4
