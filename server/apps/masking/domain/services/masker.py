# Requirement: C-5, SEC-1
"""탐지 파이프라인 ④ — 마스킹. 찾은 구간을 대체 문자로 덮는다.

**자리수를 보존한다.** `01012345678` → `***********` 로, 몇 자리였는지는 남기고 값만 지운다.
길이가 바뀌면 [7.3절](/docs/07/) `span` 오프셋이 화면 텍스트와 어긋난다.

이 함수는 **원문을 돌려주지 않는다** — 마스킹 결과와 구간만 나간다(SEC-1).
"""

from __future__ import annotations

from ..value_objects.pii_pattern import MASK_CHAR, PiiSpan
from .pii_detector import detect


def mask_text(text: str) -> tuple[str, tuple[PiiSpan, ...]]:
    """(마스킹된 텍스트, 구간 목록)을 돌려준다. 찾은 것이 없으면 원문 그대로와 빈 튜플."""
    spans = detect(text)
    if not spans:
        return text, ()

    chars = list(text)
    for span in spans:
        for i in range(span.start, span.end):
            chars[i] = MASK_CHAR
    return "".join(chars), tuple(spans)
