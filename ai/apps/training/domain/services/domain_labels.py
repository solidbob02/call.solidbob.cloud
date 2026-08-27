# Requirement: B-0
"""AI Hub 민원(콜센터) 데이터셋의 도메인 표기 → 우리 도메인 코드. 순수 매핑이라 domain 계층.

데이터셋은 도메인을 한글로 적고 우리는 영문 코드를 쓴다. 두 표기를 잇는 곳을 **여기 한 곳**으로
모은다 — 로더와 추론기가 각자 매핑을 들고 있으면 한쪽만 바뀌었을 때 라벨이 조용히 어긋난다.

    금융/보험    → finance
    다산콜센터   → dasan
    K쇼핑        → shopping
    질병관리본부 → health

⚠ 데이터셋 표기가 폴더명(`쇼핑`)과 레코드 값(`K쇼핑`)에서 다르다. **레코드 값을 정본으로**
쓴다 — 학습에 들어가는 것은 레코드다.
"""

from __future__ import annotations

# `retrieval.domain.value_objects.chunk.DOMAINS` 와 같은 네 값이어야 하지만 **import 하지 않는다** —
# 모듈끼리 직접 참조하면 `.importlinter` 계약 2 가 깨진다. 두 곳이 어긋나면
# `tests/domain/test_domain_labels.py` 가 잡는다(테스트는 계약 밖이라 양쪽을 볼 수 있다).
DOMAIN_BY_AIHUB_LABEL = {
    "금융/보험": "finance",
    "다산콜센터": "dasan",
    "K쇼핑": "shopping",
    "질병관리본부": "health",
}

# 학습·추론이 같은 순서를 봐야 한다. 정렬해 고정한다 — 딕셔너리 순서에 기대지 않는다.
LABEL_ORDER: tuple[str, ...] = ("dasan", "finance", "health", "shopping")


def to_domain(aihub_label: str) -> str | None:
    """데이터셋 표기 → 도메인 코드. 모르는 표기는 None (조용히 버리지 않고 호출부가 센다)."""
    return DOMAIN_BY_AIHUB_LABEL.get(aihub_label.strip())


def label_to_index(domain: str) -> int:
    if domain not in LABEL_ORDER:
        raise ValueError(f"모르는 도메인: {domain!r} (가능: {', '.join(LABEL_ORDER)})")
    return LABEL_ORDER.index(domain)


def index_to_label(index: int) -> str:
    if not 0 <= index < len(LABEL_ORDER):
        raise ValueError(f"라벨 인덱스 범위 밖: {index}")
    return LABEL_ORDER[index]
