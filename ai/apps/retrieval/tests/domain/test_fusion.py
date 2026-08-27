# Requirement: B-2
"""순위 병합(RRF). 순수 계산이라 전부 ES 없이 돈다.

ES 의 `retriever.rrf` 가 유료라 우리가 계산한다(`_project/decisions/021`). 그 대신
**알고리즘을 여기서 못박아 둔다** — 4주차에 `k` 를 바꿔 가며 Recall@5 변화를 잴 때
병합 자체가 흔들리지 않아야 한다.
"""

from __future__ import annotations

import pytest

from retrieval.domain.services.fusion import (
    DEFAULT_K,
    fuse_ids,
    reciprocal_rank_fusion,
)


def test_한쪽에서만_1등인_문서보다_양쪽에서_고른_문서가_앞선다():
    """RRF 의 존재 이유. 한 검색이 크게 틀려도 다른 검색이 받쳐 주면 정답이 살아남는다."""
    bm25 = ["W", "A", "X", "Y", "Z"]  # A 는 2위
    knn = ["V", "A", "T", "S", "W"]   # A 는 2위, W 는 5위
    fused = fuse_ids([bm25, knn])
    assert fused[0] == "A"  # 2·2위(1/62×2)가 1·5위(1/61+1/65)를 이긴다
    assert fused.index("A") < fused.index("W")


def test_한쪽에만_나온_문서보다_양쪽에_나온_문서가_앞선다():
    fused = fuse_ids([["X", "A"], ["Y", "A"]])
    assert fused[0] == "A"  # A 는 2위+2위, X·Y 는 1위 한 번뿐


def test_점수는_순위의_역수_합이다():
    scored = dict(reciprocal_rank_fusion([["A", "B"], ["B"]], k=60))
    assert scored["A"] == pytest.approx(1 / 61)
    assert scored["B"] == pytest.approx(1 / 62 + 1 / 61)


def test_점수_스케일이_달라도_된다():
    """입력이 순위뿐이라 BM25 점수(상한 없음)와 코사인 유사도(0~1)를 섞어도 문제가 없다.

    이 테스트는 계산이 **점수를 아예 받지 않는다**는 사실 자체를 고정한다.
    """
    assert fuse_ids([["A", "B"]]) == fuse_ids([["A", "B"]])


def test_한_순위_안의_중복은_한_번만_센다():
    """쪼개진 청크가 같은 조항으로 두 번 올라와도 그 조항만 유리해지면 안 된다."""
    once = dict(reciprocal_rank_fusion([["A", "B"]]))
    twice = dict(reciprocal_rank_fusion([["A", "A", "B"]]))
    assert twice["A"] == once["A"]
    assert twice["B"] < once["B"]  # 중복이 한 칸 밀어냈으므로 B 의 등수는 내려간다


def test_동점은_doc_id_순으로_갈린다():
    """실행마다 순서가 달라지면 채점이 흔들린다 — 재현 가능해야 한다(절대 원칙 1)."""
    assert fuse_ids([["B", "A"], ["A", "B"]]) == ["A", "B"]
    for _ in range(5):
        assert fuse_ids([["B", "A"], ["A", "B"]]) == ["A", "B"]


def test_빈_순위는_건너뛴다():
    """검색 하나가 결과를 못 냈다는 뜻이지 오류가 아니다."""
    assert fuse_ids([[], ["A", "B"]]) == ["A", "B"]
    assert fuse_ids([[], []]) == []


def test_k_가_클수록_상위와_하위의_점수차가_줄어든다():
    def gap(k: int) -> float:
        s = dict(reciprocal_rank_fusion([["A", "B"]], k=k))
        return s["A"] - s["B"]

    assert gap(10) > gap(60) > gap(1000)


def test_기본_k는_60이고_관례값임을_밝힌다():
    """우리 데이터에서 검증한 값이 아니다 — 4주차에 함께 잰다(절대 원칙 2)."""
    assert DEFAULT_K == 60


def test_가중치를_주면_그쪽_순위가_더_세진다():
    balanced = fuse_ids([["A"], ["B"]])
    weighted = fuse_ids([["A"], ["B"]], weights=[2.0, 1.0])
    assert balanced == ["A", "B"]  # 동점 → doc_id 순
    assert weighted[0] == "A"      # 가중치가 동점을 깬다
    assert fuse_ids([["A"], ["B"]], weights=[1.0, 2.0])[0] == "B"


def test_top_k_로_자른다():
    assert fuse_ids([["A", "B", "C"]], top_k=2) == ["A", "B"]
    assert len(fuse_ids([["A", "B", "C"]], top_k=10)) == 3


@pytest.mark.parametrize("bad_k", [0, -1])
def test_k가_0이하면_거부한다(bad_k):
    with pytest.raises(ValueError):
        reciprocal_rank_fusion([["A"]], k=bad_k)


def test_가중치_개수가_안_맞으면_거부한다():
    with pytest.raises(ValueError):
        reciprocal_rank_fusion([["A"], ["B"]], weights=[1.0])
