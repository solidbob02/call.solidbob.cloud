# Requirement: B-2
"""청크 → Elasticsearch 색인. ES 클라이언트를 부르므로 adapter 계층에 둔다.

`ai/.importlinter` 의 domain-purity 계약이 `retrieval.domain → elasticsearch` 를 막는다.
청킹 규칙(순수 파이썬)은 domain 에, ES 방언은 여기에.

**지금은 `single` 로 간다** (`_project/decisions/017`). 조항이 102개뿐이라 도메인별로 나누면
인덱스당 20~34건이 되어 BM25 IDF 가 불안정해지고, 얻는 이점(도메인별 독립 재적재)은 전체
재적재가 1초도 안 걸리는 지금 있으나 마나다.

    single      callguard-kb-single                      ← 현재 쓰는 것
    per-domain  callguard-kb-{finance,dasan,shopping,health}   ← 전환 대비로 남겨둔 경로

`per-domain` 을 지우지 않은 이유: **이 결정은 지금 규모에 대한 것**이다. 도메인이 4개를 넘어
크게 늘거나(필터 선택도가 떨어져 filtered HNSW 가 무너진다), 단일 인덱스가 샤드 2개 이상을
필요로 하면(BM25 점수는 인덱스가 아니라 **샤드 단위**라 "전역 IDF" 장점이 그때 사라진다)
`--layout per-domain` 으로 전환한다. 전환 조건 전체는 `decisions/017` 참고.

**두 레이아웃의 문서와 매핑을 동일하게 유지한다** — per-domain 에도 `domain` 필드를 그대로
넣는다. 샤드 수도 1로 고정한다. 덕분에 전환이 **재적재 한 번**으로 끝나고, 나중에 양쪽을
실측 비교할 때도 인덱스 토폴로지 말고는 달라지는 것이 없다.

⚠ `callguard-kb-*` 와일드카드는 **두 레이아웃을 한꺼번에 잡는다.** 양쪽을 동시에 적재해 둔
상태라면 같은 조항이 두 번 세어진다. 인덱스 이름은 반드시 `index_names(layout)` 로 얻는다.
"""

from __future__ import annotations

from typing import Any, Literal

from retrieval.domain.value_objects.chunk import DOMAINS, Chunk

Layout = Literal["single", "per-domain"]
LAYOUTS: tuple[Layout, ...] = ("single", "per-domain")

INDEX_PREFIX = "callguard-kb"
SINGLE_INDEX = f"{INDEX_PREFIX}-single"

# 색인에 넣는 필드. Chunk 의 필드와 1:1 이다.
_SOURCE_FIELDS = ("chunk_id", "doc_id", "domain", "doc_type", "title", "text", "part")


def _check_layout(layout: str) -> None:
    if layout not in LAYOUTS:
        raise ValueError(f"모르는 레이아웃: {layout!r} (가능: {', '.join(LAYOUTS)})")


def index_names(layout: Layout) -> tuple[str, ...]:
    """이 레이아웃이 쓰는 인덱스 이름 전부. 검색·삭제 모두 이걸 거쳐 얻는다."""
    _check_layout(layout)
    if layout == "single":
        return (SINGLE_INDEX,)
    return tuple(f"{INDEX_PREFIX}-{d}" for d in DOMAINS)


def index_name_for(chunk: Chunk, layout: Layout) -> str:
    """청크 하나가 들어갈 인덱스."""
    _check_layout(layout)
    if layout == "single":
        return SINGLE_INDEX
    if chunk.domain not in DOMAINS:
        raise ValueError(f"모르는 도메인: {chunk.domain!r} ({chunk.chunk_id})")
    return f"{INDEX_PREFIX}-{chunk.domain}"


def build_settings() -> dict[str, Any]:
    """nori 형태소 분석 + 샤드 1개.

    `decompound_mode: mixed` 는 복합명사를 원형과 조각 양쪽으로 남긴다("중도해지수수료" →
    원형 + 중도/해지/수수료). 상담 발화는 조각으로, 약관 조항은 원형으로 쓰이는 일이 많아
    한쪽만 남기면 매칭이 끊긴다.

    ⚠ nori 는 `analysis-nori` 플러그인이다. 기본 이미지에 없으면 인덱스 생성이 실패한다
    (`infra/docker-compose.yml` 주석 참고).
    """
    return {
        "number_of_shards": 1,  # BM25 term statistics 가 샤드 단위 — 비교의 교란 변수를 없앤다
        "number_of_replicas": 0,  # 단일 노드 로컬/데모. 복제본을 두면 상태가 yellow 로 남는다
        "analysis": {
            "tokenizer": {
                "kb_nori": {"type": "nori_tokenizer", "decompound_mode": "mixed"},
            },
            "analyzer": {
                "korean": {
                    "type": "custom",
                    "tokenizer": "kb_nori",
                    "filter": ["nori_readingform", "lowercase"],
                },
            },
        },
    }


def build_mapping() -> dict[str, Any]:
    """지금 적재하는 것만 넣는다.

    `doc_id` 는 반드시 `keyword` 다 — 평가 하네스가 이 값을 **정확 일치**로 대조한다
    (`evaluation/metrics/retrieval.py`). `text` 로 분석되면 채점이 조용히 깨진다.

    임베딩(`dense_vector`, KoE5 1024차원)은 아직 넣지 않는다. 4주차에 임베딩을 실제로 만들 때
    매핑을 늘리고 재적재한다 — 102건 재적재는 순식간이라 미리 잡아둘 이유가 없다.
    """
    return {
        "properties": {
            "chunk_id": {"type": "keyword"},
            "doc_id": {"type": "keyword"},
            "domain": {"type": "keyword"},
            "doc_type": {"type": "keyword"},
            "title": {"type": "text", "analyzer": "korean"},
            "text": {"type": "text", "analyzer": "korean"},
            "part": {"type": "integer"},
        },
    }


def to_source(chunk: Chunk) -> dict[str, Any]:
    """청크 → 색인 문서 본문. 두 레이아웃이 같은 문서를 쓴다."""
    return {f: getattr(chunk, f) for f in _SOURCE_FIELDS}


def create_indices(client: Any, layout: Layout, *, recreate: bool = False) -> list[str]:
    """레이아웃의 인덱스를 만든다. 이미 있으면 건너뛴다(`recreate=True` 면 지우고 다시).

    client 는 주입받는다 — `elasticsearch` 를 이 모듈이 직접 import 하지 않으므로 패키지가
    없는 환경(CI)에서도 위쪽 순수 함수들과 이 모듈 자체는 import 된다.
    """
    _check_layout(layout)
    created = []
    for name in index_names(layout):
        if recreate:
            client.indices.delete(index=name, ignore_unavailable=True)
        if not client.indices.exists(index=name):
            client.indices.create(index=name, settings=build_settings(), mappings=build_mapping())
            created.append(name)
    return created


def index_chunks(client: Any, chunks: list[Chunk], layout: Layout) -> dict[str, int]:
    """청크를 적재하고 인덱스별 문서 수를 돌려준다.

    **재적재가 재현된다** — `_id` 를 `chunk_id` 로 고정한 `index` 연산(upsert)이라 같은 입력을
    몇 번 돌려도 문서 수와 `_id` 집합이 같다. 이게 `w2-kb-index` 의 완료 조건이다.

    `helpers.bulk` 를 쓰지 않는 이유: 지식베이스 전체가 39KB(청크 102개)라 한 번의 `bulk`
    요청에 들어간다. 굳이 `elasticsearch` 를 import 하지 않아도 되고, 실패도 한 응답에서
    다 보인다. 지식베이스가 수 MB 로 커지면 그때 `helpers.bulk` 로 바꾼다.
    """
    _check_layout(layout)
    if not chunks:
        raise ValueError("적재할 청크가 없다")

    operations: list[dict[str, Any]] = []
    for c in chunks:
        operations.append({"index": {"_index": index_name_for(c, layout), "_id": c.chunk_id}})
        operations.append(to_source(c))

    resp = client.bulk(operations=operations, refresh=True)
    if resp.get("errors"):
        failed = [
            item["index"]
            for item in resp["items"]
            if item.get("index", {}).get("error") is not None
        ]
        raise RuntimeError(f"색인 실패 {len(failed)}건 — 첫 건: {failed[0] if failed else '?'}")

    return {name: client.count(index=name)["count"] for name in index_names(layout)}
