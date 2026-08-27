# Requirement: B-1, B-2
"""스포크를 hub 포트에 꽂기 위한 팩토리. **이 파일은 `server/main.py` 를 위한 것이다.**

`server/` 는 `ai/` 를 import 할 수 없다(`server/.importlinter` 계약 2 — 두 서브도메인을 따로
배포하기 위한 경계다). 그 경계 밖에 있는 유일한 곳이 **합성 루트 `server/main.py`** 이고,
거기서 아래 팩토리를 불러 `dependency_overrides` 에 꽂는다.

    # server/main.py — sys.path 에 ai/apps 와 ai 를 함께 올린다
    from provider import build_retrieval_provider, build_trigger_provider
    from hub.dependencies.retrieval_provider import get_retrieval_port
    from hub.dependencies.trigger_provider import get_trigger_port

    if settings.elasticsearch_configured:
        app.dependency_overrides[get_retrieval_port] = build_retrieval_provider(
            settings.elasticsearch_url, api_key=settings.elasticsearch_api_key
        )
        SPOKES.append("retrieval")

    app.dependency_overrides[get_trigger_port] = build_trigger_provider()
    SPOKES.append("trigger")

    # B-0 은 선택이라 허브 기본값이 None 이다(501 이 아니다). v1 정확도가 0.647 이라
    # 켜면 틀린 도메인으로 검색이 좁아진다 — 켤지는 팀 판단이다.
    # app.dependency_overrides[get_domain_routing_port] = build_domain_routing_provider(...)

`sys.path` 에 **`ai/apps` 와 `ai` 둘 다** 올린다 — 앞의 것은 `retrieval`·`training` 을 최상위
패키지로 보이게 하고, 뒤의 것은 이 파일 자체를 `provider` 로 import 하기 위해서다.
`main.py` 가 이미 `server/apps` 에 대해 하는 일과 같다.

**이 파일이 `apps/` 밖에 있는 이유**: `retrieval`(검색 기반 B-0)과 `training`(모델 기반 B-0)을
동시에 알아야 하는데, 두 모듈이 서로를 import 하면 `.importlinter` 계약 2 가 깨진다.
합성은 계약 밖에서 한다 — `ai/tests/` 와 같은 자리다.

**설정은 인자로 받는다.** 여기서 `os.environ` 을 읽지 않는다 — `ai/` 에는 config 모듈이 없고,
서버의 설정은 `server/core/config.py` 한 곳에서만 읽는다는 규칙(`server/CLAUDE.md` 3번)을
스포크가 우회하면 안 된다.
"""

from __future__ import annotations

from typing import Any, Callable

from hub.app.ports.output.domain_routing_port import DomainRoutingPort
from hub.app.ports.output.retrieval_port import RetrievalPort
from hub.app.ports.output.trigger_port import TriggerPort

from retrieval.adapter.outbound.es_bm25_retriever import EsBm25Retriever
from retrieval.adapter.outbound.es_index import SINGLE_INDEX
from retrieval.adapter.outbound.is_final_trigger import IsFinalTrigger
from retrieval.adapter.outbound.search_domain_router import SearchDomainRouter


def build_es_client(url: str, api_key: str | None = None) -> Any:
    """ES 클라이언트 하나. 요청마다 새로 만들지 않는다 — 연결 풀이 매번 버려진다."""
    if not url:
        raise ValueError("elasticsearch_url 이 비어 있다")
    try:
        from elasticsearch import Elasticsearch
    except ModuleNotFoundError as e:  # pragma: no cover - 설치 안내
        raise RuntimeError("elasticsearch 패키지가 없다: pip install -r ai/requirements.txt") from e

    return Elasticsearch(url, api_key=api_key) if api_key else Elasticsearch(url)


def build_retrieval_provider(
    url: str,
    *,
    api_key: str | None = None,
    index: str = SINGLE_INDEX,
    client: Any | None = None,
) -> Callable[[], RetrievalPort]:
    """`get_retrieval_port` 를 대체할 프로바이더.

    클라이언트를 **기동 시 한 번** 만들어 재사용한다. `client=` 로 갈아끼울 수 있어
    테스트에서 실제 ES 없이도 배선을 확인할 수 있다.

    ⚠ 동기 클라이언트를 쓰므로 `EsBm25Retriever` 가 `asyncio.to_thread` 로 감싼다.
    요청량이 늘면 `AsyncElasticsearch` 로 바꾸는 편이 낫다 — 그때 이 팩토리만 고치면 된다.
    """
    port = EsBm25Retriever(client or build_es_client(url, api_key), index=index)
    return lambda: port


def build_domain_routing_provider(
    url: str,
    *,
    api_key: str | None = None,
    index: str = SINGLE_INDEX,
    client: Any | None = None,
) -> Callable[[], DomainRoutingPort]:
    """`get_domain_routing_port` 를 대체할 프로바이더 (B-0 v1).

    ⚠ **분류 모델이 아니다.** 검색 결과의 도메인 분포로 판정한다 — 학습 데이터가 없어서다.
    2026-08-27 실측 정확도 **0.647** 로 목표(≥0.95)에 못 미친다. 켜기 전에
    `SearchDomainRouter` docstring 과 `w1-domain-routing` 티켓을 읽는다.
    """
    port = SearchDomainRouter(EsBm25Retriever(client or build_es_client(url, api_key), index=index))
    return lambda: port


def build_model_domain_routing_provider(
    model_dir: str = "models/domain-classifier",
) -> Callable[[], DomainRoutingPort]:
    """`decisions/007` 설계 ① — 파인튜닝한 KcELECTRA 분류기.

    모델은 **처음 판정할 때** 올라간다(생성자에서는 경로만 확인). 기동을 느리게 하지 않는다.
    """
    from training.adapter.outbound.model_domain_router import ModelDomainRouter

    port = ModelDomainRouter(model_dir)
    return lambda: port


def build_trigger_provider(**kwargs: Any) -> Callable[[], TriggerPort]:
    """`get_trigger_port` 를 대체할 프로바이더. 규칙 계산뿐이라 외부 자원이 필요 없다.

    ⚠ `at_ms`(발동 시각)를 무엇으로 채우는지는 `IsFinalTrigger` 의 주석을 반드시 읽는다 —
    포트 시그니처에 도착 시각이 없어서 지금은 **실측 상수로 모형화**하고 있다.
    """
    port = IsFinalTrigger(**kwargs)
    return lambda: port
