# Requirement: B-0
"""AI Hub 민원(콜센터) 질의응답 → B-0 학습 표본. 파일 I/O 라 adapter 계층.

**골든셋을 학습에 쓰지 않기 위해 존재하는 모듈이다.** 골든셋은 평가 세트다 — 그걸로
학습시키고 그걸로 채점하면 정확도가 1.0 으로 나오는데 아무것도 측정하지 않은 숫자다.

데이터 구조 (`data/raw/aihub-minwon-qa/`, `.gitignore` 대상):

    validation/label/<도메인>/*.json   레코드 배열. 각 레코드에 `도메인`·`화자`·`고객질문(요청)`

**고객 질문만 쓴다.** B-0 은 "통화 초반 고객 발화로 도메인을 판정"하는 것이고
(`decisions/007`), 상담사 발화는 실제 라우팅 시점에 아직 없다.
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from training.domain.services.domain_labels import to_domain

CONVERSATION_FIELD = "대화셋일련번호"
SENTENCE_NO_FIELD = "문장번호"
UTTERANCE_FIELD = "고객질문(요청)"
SPEAKER_FIELD = "화자"
DOMAIN_FIELD = "도메인"
CUSTOMER = "고객"

# 너무 짧은 발화는 도메인 단서가 없다("네", "아니요"). 도메인과 무관한 잡음이라 뺀다.
MIN_CHARS = 4


@dataclass(frozen=True)
class Sample:
    text: str
    domain: str


def load_samples(root: Path, *, min_chars: int = MIN_CHARS) -> tuple[list[Sample], dict[str, int]]:
    """(표본, 걸러낸 이유별 건수). 같은 입력이면 항상 같은 순서로 나온다(정렬 순회)."""
    if not root.is_dir():
        raise FileNotFoundError(f"데이터셋 경로가 없다: {root}")

    dropped: Counter[str] = Counter()
    seen: set[str] = set()
    samples: list[Sample] = []

    for path in sorted(root.rglob("*.json")):
        if "/label/" not in path.as_posix():
            continue
        raw = json.loads(path.read_text(encoding="utf-8"))
        for rec in raw if isinstance(raw, list) else [raw]:
            if rec.get(SPEAKER_FIELD) != CUSTOMER:
                dropped["상담사 발화"] += 1
                continue
            text = (rec.get(UTTERANCE_FIELD) or "").strip()
            if len(text) < min_chars:
                dropped["너무 짧음"] += 1
                continue
            domain = to_domain(rec.get(DOMAIN_FIELD, ""))
            if domain is None:
                dropped["모르는 도메인"] += 1
                continue
            if text in seen:
                # 콜센터 대화라 "네 알겠습니다" 류가 수없이 반복된다. 중복을 그대로 두면
                # 흔한 문장이 학습을 지배하고, 검증 쪽에도 같은 문장이 새어 든다.
                dropped["중복"] += 1
                continue
            seen.add(text)
            samples.append(Sample(text=text, domain=domain))

    if not samples:
        raise ValueError(f"표본이 하나도 없다: {root}")
    return samples, dict(dropped)


def stratified_split(
    samples: list[Sample], *, val_ratio: float = 0.1, seed: int = 42
) -> tuple[list[Sample], list[Sample]]:
    """도메인별 비율을 유지한 채 학습/검증으로 나눈다.

    도메인마다 표본 수가 크게 다르므로(쇼핑이 다산의 5배) 무작위로 자르면 검증 세트에서
    작은 도메인이 사라질 수 있다. **같은 seed 면 항상 같은 분할**이다 — 재현 가능해야 한다.
    """
    if not 0.0 < val_ratio < 1.0:
        raise ValueError(f"val_ratio 는 0~1 사이여야 한다: {val_ratio}")

    import random

    train: list[Sample] = []
    val: list[Sample] = []
    by_domain: dict[str, list[Sample]] = {}
    for s in samples:
        by_domain.setdefault(s.domain, []).append(s)

    for domain in sorted(by_domain):
        group = sorted(by_domain[domain], key=lambda s: s.text)  # 입력 순서에 기대지 않는다
        random.Random(seed).shuffle(group)
        cut = max(1, int(len(group) * val_ratio))
        val += group[:cut]
        train += group[cut:]
    return train, val


# ─────────────────────────────────────── 통화 초반 발화 (골든셋 문체에 맞춘 증강)

# 골든셋 발화는 "통화 초반의 완결된 질문" 한 문장이다
# ("카드를 잃어버렸는데 신고하기 전에 이미 누가 써버린 돈은 저는 못 돌려받는 거예요?").
# AI Hub 의 고객 발화는 같은 질문이 **짧은 턴으로 쪼개져** 있다
# ("카드를 잃어버렸어요" / "그런것 같아요 아무리 찾아도 없네요" / "분실신고 하고 나서 …").
#
# 그래서 **한 대화의 앞쪽 고객 턴을 이어 붙여** 완결된 질문 형태로 만든다.
# 지어낸 문장이 아니라 **실제 전사를 잇는 것**이고, B-0 의 실제 입력(통화 초반 발화)과도
# 더 맞는다 — 지금 학습 표본은 통화 중반·후반 턴까지 섞여 있다.
#
# ⚠ 골든셋 문장을 학습에 쓰지 않는다. 평가 세트라 학습에 쓰면 그 라벨로 다시 잴 수 없다.
MAX_OPENING_TURNS = 3


def load_opening_samples(
    root: Path, *, max_turns: int = MAX_OPENING_TURNS, min_chars: int = MIN_CHARS
) -> list[Sample]:
    """대화마다 앞쪽 고객 턴 1~max_turns 개를 이어 붙인 표본을 만든다.

    1턴짜리는 `load_samples` 와 겹치므로 **2턴 이상만** 돌려준다 — 같은 문장을 두 번 넣으면
    그 문장이 학습을 지배한다.
    """
    if not root.is_dir():
        raise FileNotFoundError(f"데이터셋 경로가 없다: {root}")

    conversations: dict[str, list[tuple[int, str, str]]] = {}
    for path in sorted(root.rglob("*.json")):
        if "/label/" not in path.as_posix():
            continue
        raw = json.loads(path.read_text(encoding="utf-8"))
        for rec in raw if isinstance(raw, list) else [raw]:
            if rec.get(SPEAKER_FIELD) != CUSTOMER:
                continue
            text = (rec.get(UTTERANCE_FIELD) or "").strip()
            domain = to_domain(rec.get(DOMAIN_FIELD, ""))
            conv_id = rec.get(CONVERSATION_FIELD)
            if not text or domain is None or not conv_id:
                continue
            try:
                order = int(rec.get(SENTENCE_NO_FIELD, 0))
            except (TypeError, ValueError):
                continue
            conversations.setdefault(conv_id, []).append((order, text, domain))

    samples: list[Sample] = []
    seen: set[str] = set()
    for conv_id in sorted(conversations):
        turns = sorted(conversations[conv_id])
        for n in range(2, max_turns + 1):
            if len(turns) < n:
                break
            joined = " ".join(t[1] for t in turns[:n])
            if len(joined) < min_chars or joined in seen:
                continue
            seen.add(joined)
            samples.append(Sample(text=joined, domain=turns[0][2]))
    return samples
