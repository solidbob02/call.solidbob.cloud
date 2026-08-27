# Requirement: B-2
"""순위 병합 (RRF) — 순수 규칙 계산이라 domain 계층에 둔다.

**왜 여기서 계산하나.** ES 의 `retriever.rrf` 는 유료다 — 8.15.3·9.5.1 양쪽 다 basic
라이선스에서 `403 non-compliant for [Reciprocal Rank Fusion (RRF)]` 이고 버전을 올려도
풀리지 않는다. 30일 trial 은 2026-09-26 에 만료돼 프로젝트 종료(10-27)를 못 넘긴다.
근거·선택지 전체: `_project/decisions/021`.

**막힌 것은 순위 병합 하나뿐이다** — BM25·kNN·nori·`dense_vector`·`collapse` 는 basic 에서
전부 된다. 그리고 RRF 는 원래 순위의 역수 합이 전부라, 서버가 대신 해 주던 것을 여기서 한다.

`ai/CLAUDE.md` 4번("랭킹 산식은 순수 파이썬")대로 `domain/` 에 두었다. `.importlinter`
계약 3 이 이 계층의 라이브러리 import 를 막으므로 구조로도 고정된다 — LangChain 의
`EnsembleRetriever` 를 쓰지 않은 이유이기도 하다(`decisions/021` 선택지 E).

## 아직 배선되지 않았다

2주차 베이스라인은 BM25 **단독**이라 병합할 순위가 하나뿐이다. 이 모듈은 4주차
하이브리드 검색(BM25 + kNN)에서 쓰인다 — 그때 `dense_vector` 매핑과 임베딩이 붙는다.
미리 만들어 둔 이유는 **알고리즘을 단위 테스트로 고정해 두면 4주차에 `k` 를 바꿔 가며
Recall@5 변화를 잴 수 있기** 때문이다(절대 원칙 1 — 재현 가능해야 한다).
"""

from __future__ import annotations

# Cormack et al. (2009) 이 제안한 값. **우리 데이터에서 검증한 값이 아니다** —
# 4주차에 하이브리드를 붙일 때 함께 재고, 그 전에는 이 값을 바꾸지 않는다(절대 원칙 2).
DEFAULT_K = 60


def reciprocal_rank_fusion(
    rankings: list[list[str]],
    *,
    k: int = DEFAULT_K,
    weights: list[float] | None = None,
) -> list[tuple[str, float]]:
    """여러 순위를 하나로 합친다. 점수가 높은 순으로 `(doc_id, 점수)` 를 돌려준다.

        score(d) = Σ_i  weight_i / (k + rank_i(d))

    **점수 스케일이 달라도 되는 게 요점이다.** BM25 점수(상한 없음)와 코사인 유사도(0~1)를
    그냥 더하면 한쪽이 지배한다. 순위만 쓰면 그 문제가 사라진다 — RRF 가 존재하는 이유다.

    `k` 가 클수록 상위권과 하위권의 점수 차가 평평해진다. 즉 "1등을 얼마나 더
    믿을 것인가"를 정하는 값이다.

    규칙 몇 가지:
    - **한 순위 안에 같은 문서가 두 번 나오면 더 높은(작은) 등수만 센다.** 조항이 쪼개진
      청크가 각각 올라와 같은 조항을 두 번 더하면 그 조항만 부당하게 유리해진다.
    - **동점은 `doc_id` 오름차순으로 가른다.** 실행할 때마다 순서가 달라지면 채점이 흔들린다.
    - 빈 순위는 그냥 건너뛴다(그 검색이 결과를 못 냈다는 뜻이지 오류가 아니다).
    """
    if k <= 0:
        raise ValueError(f"k 는 양수여야 한다: {k}")
    if weights is None:
        weights = [1.0] * len(rankings)
    if len(weights) != len(rankings):
        raise ValueError(f"weights {len(weights)}개 ≠ rankings {len(rankings)}개")

    scores: dict[str, float] = {}
    for ranking, weight in zip(rankings, weights):
        seen: set[str] = set()
        for rank, doc_id in enumerate(ranking, start=1):
            if doc_id in seen:  # 같은 순위 안의 중복은 첫 등장(= 가장 높은 등수)만 센다
                continue
            seen.add(doc_id)
            scores[doc_id] = scores.get(doc_id, 0.0) + weight / (k + rank)

    # 동점을 doc_id 로 갈라 실행마다 같은 순서가 나오게 한다.
    return sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))


def fuse_ids(
    rankings: list[list[str]],
    *,
    top_k: int | None = None,
    k: int = DEFAULT_K,
    weights: list[float] | None = None,
) -> list[str]:
    """`reciprocal_rank_fusion` 의 결과에서 문서 ID 만, 필요하면 상위 몇 개만."""
    fused = [doc_id for doc_id, _ in reciprocal_rank_fusion(rankings, k=k, weights=weights)]
    return fused if top_k is None else fused[:top_k]
