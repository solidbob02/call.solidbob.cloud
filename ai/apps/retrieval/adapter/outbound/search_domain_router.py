# Requirement: B-0
"""도메인 라우팅 v1 — 지식베이스 검색으로 판정한다. `DomainRoutingPort` 구현.

## 왜 분류 모델이 아닌가

`_project/decisions/007` 의 설계는 **① KcELECTRA 4클래스 분류기 → ② 신뢰도가 낮으면
4개 도메인 전부 검색하는 폴백** 이다. 지금 ①을 만들 수 없다:

**학습 데이터가 없다.** 골든셋은 **평가 세트**다(도메인 라벨이 붙은 채점 표본 34건).
그걸로 학습시키고 그걸로 채점하면 정확도가 1.0 으로 나오는데 **아무것도 측정하지 않은
숫자**다. 라벨을 학습에 쓰는 순간 그 라벨로는 다시 잴 수 없다.

그래서 **②를 먼저 만들어 1차 경로로 쓴다.** 설계에 이미 들어 있는 안전망이고, 새 도구를
들이지 않으며([아키텍처 3.1](/docs/03/) 투입자원 원칙), 학습 데이터 없이 **지금 잴 수 있다.**
①이 생기면 이 구현이 설계대로 폴백 자리로 내려간다 — 그때 이 값이 **비교 기준선**이 된다.

## 판정 방법

발화로 전 도메인을 검색해 상위 문서들의 도메인에 **순위 가중치**(`1/rank`)로 표를 준다.
가장 표를 많이 받은 도메인이 답이고, 신뢰도는 **1등과 2등의 표 차이**다.

점수(BM25 원점수)가 아니라 **순위**를 쓰는 이유는 RRF 와 같다 — BM25 점수는 질의마다
스케일이 달라 "0.8 이면 확신" 같은 임계값을 못 세운다. 순위 기반이면 임계값이 질의와
무관하게 의미를 갖는다.

⚠ 신뢰도는 **교정된 확률이 아니다.** "이 값 이상이면 몇 % 맞다"고 말할 수 없고, 그렇게
쓰지도 않는다 — 임계값은 폴백 여부를 가르는 데만 쓰고, 그 임계값도 실측으로 정해야 한다.
"""

from __future__ import annotations

from collections import defaultdict

from hub.app.dtos.domain_classification_dto import DomainClassification
from hub.app.ports.output.domain_routing_port import DomainRoutingPort

from retrieval.adapter.outbound.es_bm25_retriever import EsBm25Retriever
from retrieval.domain.value_objects.chunk import DOMAIN_BY_PREFIX

# 표를 모으는 데 볼 상위 문서 수. 5는 Recall@5 와 맞춘 값이고 실측으로 정한 값이 아니다.
DEFAULT_VOTE_DEPTH = 5


class SearchDomainRouter(DomainRoutingPort):
    """지식베이스 검색 결과의 도메인 분포로 판정한다.

    `retriever` 를 주입받는다 — 검색 방식이 4주차에 하이브리드로 바뀌어도 여기는 그대로다.
    """

    def __init__(
        self,
        retriever: EsBm25Retriever,
        *,
        vote_depth: int = DEFAULT_VOTE_DEPTH,
    ) -> None:
        if vote_depth < 1:
            raise ValueError(f"vote_depth 는 1 이상이어야 한다: {vote_depth}")
        self._retriever = retriever
        self._vote_depth = vote_depth

    async def classify(self, utterance: str) -> DomainClassification:
        docs = await self._retriever.retrieve(utterance, top_k=self._vote_depth)
        return classify_by_votes([d.doc_id for d in docs])


def classify_by_votes(doc_ids: list[str]) -> DomainClassification:
    """문서 ID 순위 → 도메인 판정. 순수 계산이라 ES 없이 테스트된다.

    표는 `1/rank` 다 — 1등 1.0, 2등 0.5, 3등 0.33…. 상위 문서일수록 도메인을 강하게 시사한다.
    신뢰도는 **1등 표에서 2등 표를 뺀 값을 총표로 나눈 것**(0~1)이다. 한 도메인이 상위를
    독식하면 1에 가깝고, 두 도메인이 팽팽하면 0에 가깝다.

    결과가 없으면 도메인을 정하지 않는다(`domain=None`, 신뢰도 0) — 지어내지 않는다.

    ⚠ `DomainClassification.domain` 의 타입은 `str` 이지 `str | None` 이 아니다. 계약상
    "판정 불가"를 표현할 방법이 없어서 런타임에 `None` 을 넣고 있다. DTO 변경은 `server/`
    소관이라 손대지 않았다 — [미결 항목](/open-items/)에 올렸다. 빈 발화가 아니면 102건
    인덱스에서 결과가 0인 경우는 사실상 없다.
    """
    votes: dict[str, float] = defaultdict(float)
    for rank, doc_id in enumerate(doc_ids, start=1):
        prefix = doc_id.split("-", 1)[0]
        domain = DOMAIN_BY_PREFIX.get(prefix)
        if domain is None:  # 모르는 접두어는 세지 않는다 — 조용히 한 표를 주지 않는다
            continue
        votes[domain] += 1.0 / rank

    if not votes:
        return DomainClassification(domain=None, confidence=0.0)

    ranked = sorted(votes.items(), key=lambda kv: (-kv[1], kv[0]))
    top_domain, top_votes = ranked[0]
    runner_up = ranked[1][1] if len(ranked) > 1 else 0.0
    total = sum(votes.values())
    return DomainClassification(
        domain=top_domain,
        confidence=(top_votes - runner_up) / total,
    )
