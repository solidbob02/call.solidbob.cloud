# Requirement: C-5
"""탐지 파이프라인 ③ — 패턴 매칭. P1~P5 는 숫자 정규식, P6·P7 은 문맥·토큰 규칙이다.

P6(인명)·P7(상세주소)은 [2.4절](/docs/02/)이 NER 로 정했지만 모델은 `ai/` 몫이라
(계약 2 가 `server/` 의 `transformers` import 를 막는다) **규칙으로 바닥을 깔았다.**
각 모듈의 docstring 이 무엇을 못 잡는지 적어 두었다 — NER 이 붙으면 폴백으로 남는다.

**지표 우선순위를 코드에 고정한다** ([2.4절](/docs/02/)):

    누락 0건  >  과잉 마스킹 억제.  애매하면 가린다.

그래서 겹치는 구간이 생기면 **더 넓은 쪽**을 남긴다. 자릿수 범위가 겹치는 패턴
(카드 14~16 / 계좌 10~14)에서 좁은 쪽을 고르면 뒷자리가 노출된다.

**정규화된 문자열 위에서 찾고, 원문 오프셋으로 되돌린다.** 구분자가 있든 없든
같은 번호를 잡기 위해서다 — `"123456 1234567"` 과 `"1234561234567"` 둘 다 포착한다.
"""

from __future__ import annotations

import re

from ..value_objects.pii_pattern import PiiSpan
from .address_detector import detect_addresses
from .name_detector import detect_names
from .number_normalizer import sino_to_digits, strip_separators

# P5 인증번호는 문맥이 있을 때만 잡는다 — 4~6자리 숫자는 금액·개수와 구분이 안 된다.
# 애매하면 가린다는 원칙과 충돌하지 않는다: 문맥 없는 4자리를 전부 가리면
# "3천원"·"2개" 까지 지워져 자막이 읽히지 않는다(자막 자체가 못 쓰게 되는 것이 더 큰 손실).
AUTH_CONTEXT = ("인증", "승인", "확인번호", "코드", "otp", "OTP", "비밀번호", "핀번호")

# 정규화된(구분자 없는) 숫자열 기준. 긴 것부터 본다 — 겹치면 넓은 쪽이 이긴다.
_NUMERIC_RULES: list[tuple[str, re.Pattern[str]]] = [
    ("P1", re.compile(r"\d{13}")),           # 주민등록번호 13자리
    ("P2", re.compile(r"\d{14,16}")),        # 카드번호 14~16자리
    ("P4", re.compile(r"01\d{8,9}")),        # 휴대전화 010/011… 10~11자리
    ("P3", re.compile(r"\d{10,14}")),        # 계좌번호 10~14자리
]


def _to_source_span(pattern: str, start: int, end: int, index_map: list[int]) -> PiiSpan:
    """정규화 문자열의 [start, end) 를 원문 오프셋으로 되돌린다."""
    return PiiSpan(pattern=pattern, start=index_map[start], end=index_map[end - 1] + 1)


def _detect_numeric(text: str) -> list[PiiSpan]:
    normalized, index_map = strip_separators(text)
    digits, _ = sino_to_digits(normalized)  # ② 보조 — 낭독형 숫자를 잡기 위해서만 쓴다

    found: list[PiiSpan] = []
    for name, rule in _NUMERIC_RULES:
        for m in rule.finditer(digits):
            found.append(_to_source_span(name, m.start(), m.end(), index_map))
    return found


def _detect_auth_code(text: str) -> list[PiiSpan]:
    """P5 — 문맥 단어가 같은 발화에 있을 때만 4~6자리를 잡는다."""
    lowered = text.lower()
    if not any(k.lower() in lowered for k in AUTH_CONTEXT):
        return []

    normalized, index_map = strip_separators(text)
    digits, _ = sino_to_digits(normalized)
    return [
        _to_source_span("P5", m.start(), m.end(), index_map)
        for m in re.finditer(r"(?<!\d)\d{4,6}(?!\d)", digits)
    ]


def _resolve_overlaps(spans: list[PiiSpan]) -> list[PiiSpan]:
    """겹치면 **넓은 쪽**을 남긴다 — 좁은 쪽을 고르면 뒷자리가 노출된다(누락 0건 우선)."""
    ordered = sorted(spans, key=lambda s: (-s.length, s.start))
    kept: list[PiiSpan] = []
    for span in ordered:
        if not any(span.overlaps(k) for k in kept):
            kept.append(span)
    return sorted(kept, key=lambda s: s.start)


def detect(text: str) -> list[PiiSpan]:
    """P1~P7 을 찾는다. 결과는 원문 오프셋 기준이고 시작 위치 순으로 정렬된다."""
    return _resolve_overlaps(
        _detect_numeric(text)
        + _detect_auth_code(text)
        + detect_names(text)
        + detect_addresses(text)
    )
