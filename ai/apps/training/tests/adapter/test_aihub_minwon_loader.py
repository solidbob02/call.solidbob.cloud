# Requirement: B-0
"""AI Hub 민원 데이터 로더. 임시 파일로 돌아 실제 데이터셋(2.7GB)이 없어도 된다."""

from __future__ import annotations

import json
from collections import Counter

import pytest

from training.adapter.outbound.aihub_minwon_loader import (
    Sample,
    load_samples,
    stratified_split,
)


def _dataset(tmp_path, records):
    d = tmp_path / "validation" / "label" / "금융보험"
    d.mkdir(parents=True)
    (d / "x.json").write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")
    return tmp_path


def _rec(text="카드를 잃어버렸어요", speaker="고객", domain="금융/보험"):
    return {"화자": speaker, "고객질문(요청)": text, "도메인": domain}


def test_고객_질문만_쓴다(tmp_path):
    """B-0 은 통화 초반 고객 발화로 판정한다 — 상담사 발화는 그 시점에 아직 없다."""
    root = _dataset(tmp_path, [_rec(), _rec(text="네 확인해 드릴게요", speaker="상담사")])
    samples, dropped = load_samples(root)
    assert [s.text for s in samples] == ["카드를 잃어버렸어요"]
    assert dropped["상담사 발화"] == 1


def test_너무_짧은_발화를_뺀다(tmp_path):
    """"네"·"아니요" 에는 도메인 단서가 없다."""
    root = _dataset(tmp_path, [_rec(), _rec(text="네")])
    samples, dropped = load_samples(root)
    assert len(samples) == 1
    assert dropped["너무 짧음"] == 1


def test_중복_발화를_한_번만_쓴다(tmp_path):
    """콜센터 대화라 같은 문장이 수없이 반복된다 — 흔한 문장이 학습을 지배하면 안 된다."""
    root = _dataset(tmp_path, [_rec(), _rec(), _rec()])
    samples, dropped = load_samples(root)
    assert len(samples) == 1
    assert dropped["중복"] == 2


def test_모르는_도메인을_뺀다(tmp_path):
    root = _dataset(tmp_path, [_rec(), _rec(text="요금제 문의드려요", domain="통신")])
    samples, dropped = load_samples(root)
    assert len(samples) == 1
    assert dropped["모르는 도메인"] == 1


def test_같은_입력이면_같은_순서다(tmp_path):
    root = _dataset(tmp_path, [_rec(text=f"질문 {i} 입니다") for i in range(10)])
    first, _ = load_samples(root)
    second, _ = load_samples(root)
    assert [s.text for s in first] == [s.text for s in second]


def test_표본이_없으면_실패한다(tmp_path):
    root = _dataset(tmp_path, [_rec(text="네")])
    with pytest.raises(ValueError):
        load_samples(root)


def test_경로가_없으면_실패한다(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_samples(tmp_path / "없는경로")


# ─────────────────────────────────────── 분할

def _samples(counts):
    return [Sample(text=f"{d}-{i}", domain=d) for d, n in counts.items() for i in range(n)]


def test_도메인_비율을_유지한다():
    """도메인마다 표본 수가 크게 달라(쇼핑이 다산의 5배) 무작위로 자르면 작은 쪽이 사라진다."""
    train, val = stratified_split(_samples({"finance": 100, "dasan": 20}), val_ratio=0.1)
    assert Counter(s.domain for s in val) == {"finance": 10, "dasan": 2}
    assert len(train) + len(val) == 120


def test_작은_도메인도_검증에_최소_1건은_남는다():
    _, val = stratified_split(_samples({"finance": 100, "dasan": 3}), val_ratio=0.1)
    assert any(s.domain == "dasan" for s in val)


def test_같은_seed_면_같은_분할이다():
    data = _samples({"finance": 50, "shopping": 50})
    a, _ = stratified_split(data, seed=7)
    b, _ = stratified_split(data, seed=7)
    assert [s.text for s in a] == [s.text for s in b]


def test_학습과_검증이_겹치지_않는다():
    train, val = stratified_split(_samples({"finance": 100}))
    assert not ({s.text for s in train} & {s.text for s in val})


@pytest.mark.parametrize("ratio", [0.0, 1.0, -0.1, 1.5])
def test_잘못된_비율은_거부한다(ratio):
    with pytest.raises(ValueError):
        stratified_split(_samples({"finance": 10}), val_ratio=ratio)
