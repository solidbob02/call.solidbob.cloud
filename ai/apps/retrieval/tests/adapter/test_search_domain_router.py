# Requirement: B-0
"""도메인 라우팅 v1 (검색 기반). 판정 계산은 ES 없이 돈다."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

import pytest

from hub.app.ports.output.domain_routing_port import DomainRoutingPort
from retrieval.adapter.outbound import es_index
from retrieval.adapter.outbound.es_bm25_retriever import EsBm25Retriever
from retrieval.adapter.outbound.knowledge_base_loader import load_chunks
from retrieval.adapter.outbound.search_domain_router import (
    SearchDomainRouter,
    classify_by_votes,
)

KB_ROOT = Path(__file__).resolve().parents[4].parent / "knowledge-base"


# ─────────────────────────────────────── 판정 계산 (ES 없이)

def test_상위를_독식하면_그_도메인이다():
    r = classify_by_votes(["FIN-TERM-2.2", "FIN-TERM-2.3", "FIN-MANUAL-1.1"])
    assert r.domain == "finance"
    assert r.confidence == pytest.approx(1.0)


def test_1등이_더_무겁다():
    """`1/rank` 라 1등 1.0 · 2등 0.5 · 3등 0.33. 상위 문서일수록 도메인을 강하게 시사한다."""
    r = classify_by_votes(["SHOP-TERM-4.2", "FIN-TERM-1.1", "FIN-TERM-1.2"])
    assert r.domain == "shopping"  # 1.0 vs 0.5+0.33=0.83


def test_팽팽하면_신뢰도가_낮다():
    tie = classify_by_votes(["FIN-TERM-1.1", "SHOP-TERM-1.1"])
    clear = classify_by_votes(["FIN-TERM-1.1", "FIN-TERM-1.2"])
    assert tie.confidence < clear.confidence
    assert clear.confidence == pytest.approx(1.0)


@pytest.mark.parametrize(
    "doc_id, domain",
    [("FIN-TERM-1.1", "finance"), ("DASAN-TERM-1.1", "dasan"),
     ("SHOP-TERM-1.1", "shopping"), ("HLT-TERM-1.1", "health")],
)
def test_네_도메인_접두어를_모두_안다(doc_id, domain):
    assert classify_by_votes([doc_id]).domain == domain


def test_모르는_접두어는_세지_않는다():
    """폐기된 통신 도메인(TELCO-) 같은 것이 섞여도 조용히 한 표를 주지 않는다."""
    r = classify_by_votes(["TELCO-TERM-3.2", "FIN-TERM-1.1"])
    assert r.domain == "finance"


def test_결과가_없으면_도메인을_정하지_않는다():
    """지어내지 않는다 — 아무 도메인이나 고르면 라우팅이 조용히 틀린다."""
    r = classify_by_votes([])
    assert r.domain is None
    assert r.confidence == 0.0
    assert classify_by_votes(["TELCO-TERM-3.2"]).domain is None


def test_동점은_도메인_이름순으로_가른다():
    """실행마다 답이 달라지면 채점이 흔들린다."""
    for _ in range(5):
        assert classify_by_votes(["FIN-TERM-1.1", "DASAN-TERM-1.1"]).domain == "finance"


def test_신뢰도는_0과_1_사이다():
    for ids in (["FIN-TERM-1.1"], ["FIN-TERM-1.1", "SHOP-TERM-1.1", "HLT-TERM-1.1"]):
        c = classify_by_votes(ids).confidence
        assert 0.0 <= c <= 1.0


def test_포트를_실제로_구현한다():
    assert isinstance(SearchDomainRouter(EsBm25Retriever(None)), DomainRoutingPort)


def test_투표_깊이가_0이하면_거부한다():
    with pytest.raises(ValueError):
        SearchDomainRouter(EsBm25Retriever(None), vote_depth=0)


# ─────────────────────────────────────── 실제 ES 가 있을 때만

@pytest.fixture(scope="module")
def router():
    url = os.environ.get("ELASTICSEARCH_URL")
    if not url:
        pytest.skip("ELASTICSEARCH_URL 이 없다")
    es = pytest.importorskip("elasticsearch")
    c = es.Elasticsearch(url)
    if not c.ping():
        pytest.skip(f"ES 에 붙지 못했다: {url}")
    es_index.create_indices(c, "single", recreate=True)
    es_index.index_chunks(c, load_chunks(KB_ROOT), "single")
    return SearchDomainRouter(EsBm25Retriever(c))


@pytest.mark.integration
@pytest.mark.parametrize(
    "utterance, expected",
    [
        ("이거 그냥 마음에 안 들어서 반품하려는데 배송비는 제가 내야 하나요", "shopping"),
        ("이번 달 하수도 요금이 갑자기 많이 나왔는데 어떻게 계산되는 건가요", "dasan"),
    ],
)
def test_골든셋_발화의_도메인을_맞힌다(router, utterance, expected):
    """골든셋 원문(GS-003·GS-015). 전수 정확도는 평가 하네스가 잰다 — 여기는 연기 감지다."""
    assert asyncio.run(router.classify(utterance)).domain == expected


@pytest.mark.integration
def test_빈_발화는_판정하지_않는다(router):
    assert asyncio.run(router.classify("   ")).domain is None
