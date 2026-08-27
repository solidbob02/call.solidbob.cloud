# Requirement: C-5, QUA-2, SEC-1
"""골든셋 C-5 케이스 회귀 — **누락은 1건이라도 실패**다.

[6.2절](/docs/06/)이 정한 대로 평균이 아니라 **건 단위**로 본다. 단위 테스트는 내가 상상한
입력을 보지만, 이 테스트는 **팀이 정답을 붙인 실제 발화**를 본다 — 골든셋이 커지면
(50 → 150건) 자동으로 커버리지가 늘어난다.

채점은 규칙 기반이다(절대 원칙 1) — 정답 구간의 모든 문자가 마스킹됐는지만 본다.
"""

import json
from pathlib import Path

import pytest

from masking.domain.services.masker import mask_text

GOLDEN_SET = Path(__file__).resolve().parents[4].parent / "golden-set" / "v1-50.json"


def _c5_cases():
    if not GOLDEN_SET.exists():                      # 골든셋이 없는 체크아웃에서는 건너뛴다
        return []
    raw = json.loads(GOLDEN_SET.read_text(encoding="utf-8"))
    items = raw if isinstance(raw, list) else raw.get("cases", raw.get("items", []))
    return [
        pytest.param(c["id"], c["customer_utterance"], p, id=f"{c['id']}-{p['pattern']}")
        for c in items if c.get("module") == "C-5"
        for p in c.get("pii_patterns", []) if p.get("masked_expected")
    ]


CASES = _c5_cases()


def test_골든셋에_C5_케이스가_실려있다():
    """케이스가 0건이면 아래 테스트가 전부 통과해버린다 — 빈 채로 초록불이 되는 것을 막는다."""
    assert GOLDEN_SET.exists(), f"골든셋이 없다: {GOLDEN_SET}"
    assert CASES, "골든셋에 C-5 케이스가 없다 — 채점 대상이 사라졌다"


@pytest.mark.parametrize("case_id, utterance, expected", CASES)
def test_골든셋_정답구간이_한_글자도_빠짐없이_가려진다(case_id, utterance, expected):
    raw = expected["raw_span"]
    start = utterance.find(raw)
    assert start >= 0, f"{case_id}: 정답 구간이 발화에 없다 — 골든셋이 어긋났다"

    masked, _ = mask_text(utterance)
    leaked = [utterance[i] for i in range(start, start + len(raw)) if masked[i] != "*"]
    assert not leaked, (
        f"{case_id} [{expected['pattern']}] 누락 — 절대 규칙 위반\n"
        f"  원문: {utterance}\n  결과: {masked}\n  샌 문자: {''.join(leaked)!r}"
    )


@pytest.mark.parametrize("case_id, utterance, expected", CASES)
def test_원문이_결과에_남지_않는다(case_id, utterance, expected):
    """SEC-1 — 마스킹 결과에 원본 값이 그대로 들어 있으면 안 된다."""
    masked, _ = mask_text(utterance)
    assert expected["raw_span"] not in masked, f"{case_id}: 원문이 그대로 남았다"
