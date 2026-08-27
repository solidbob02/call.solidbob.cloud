# Requirement: C-5
"""탐지 파이프라인 ③ 확장 — P7 상세주소.

[2.4절](/docs/02/)은 P7 을 **NER** 로 적었지만, 확보한 데이터셋에 주소 태그가 없어
학습·평가가 불가능하다([미결 항목](/open-items/)). 그래서 **규칙으로 먼저 바닥을 깐다** —
0% 로 두는 것보다 낫고, 「누락 0건 > 과잉 마스킹 억제」 원칙에도 맞는다.
NER 이 붙으면 이 규칙은 폴백으로 남는다.

**토큰 연속성으로 잡는다.** 주소는 행정구역이 큰 단위에서 작은 단위로 이어지는
연속된 어절이다. 한 토큰만 보고 판단하면 "새로"·"그러므로" 같은 일상어의 `로` 에
걸린다 — **2어절 이상 이어지고 행정구역 표지가 하나라도 있을 때만** 주소로 본다.
"""

from __future__ import annotations

import re

from ..value_objects.pii_pattern import PiiSpan

# 광역단체는 **닫힌 목록**으로 둔다. `도` 를 접미로 열어두면 `"보내도"`·`"어디로 보내도"` 같은
# 어미가 전부 주소가 된다(실제로 걸렸다). 광역단체는 17개뿐이라 열거가 정확하고 싸다.
_WIDE_NAMES = ("서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종", "경기",
               "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주",
               "충청북", "충청남", "전라북", "전라남", "경상북", "경상남")
_AREA_WIDE = re.compile(
    r"^(?:%s)(?:특별시|광역시|특별자치시|특별자치도|시|도)?$" % "|".join(_WIDE_NAMES))
# 기초단체·법정동. `도` 는 위에서만 인정한다. 한 글자 동네(`우동`)를 살리려 {1,10} 이지만,
# 어절이 2개 이상 이어져야 주소로 보므로 `"운동 하세요"` 는 걸리지 않는다.
_AREA_LOCAL = re.compile(r"^[가-힣]{1,10}(시|군|구|읍|면|동|리)$")
# 도로명. `로`·`길` 은 일상어에도 흔해 단독으로는 신호가 약하다.
_ROAD = re.compile(r"^[가-힣]{2,10}(대로|로|길)$")
# 번지·호·층·동. 숫자로 시작하므로 오탐이 적고, 주소의 끝을 알려준다.
_NUMBERED = re.compile(r"^\d+(번지|호|층|동|가)")

# 행정구역 표지 — 이것이 하나도 없으면 주소로 보지 않는다(`로`·`길` 만으로는 약하다).
_STRONG = (_AREA_WIDE, _AREA_LOCAL, _NUMBERED)


def _classify(token: str) -> bool:
    return bool(_AREA_WIDE.match(token) or _AREA_LOCAL.match(token)
                or _ROAD.match(token) or _NUMBERED.match(token))


def _tokens(text: str) -> list[tuple[int, str]]:
    """(시작 오프셋, 토큰). 문자 오프셋이므로 한글이 섞여도 어긋나지 않는다."""
    return [(m.start(), m.group()) for m in re.finditer(r"\S+", text)]


def _trim_tail(token: str) -> int:
    """마지막 토큰에 붙은 조사를 잘라낸다.

    `"456호예요"` 에서 `"예요"` 까지 가리면 자막이 `"456호***"` 처럼 읽히지 않는다.
    번호 뒤 조사가 번호에 먹히던 문제(한글 수사)와 같은 종류다.
    """
    m = _NUMBERED.match(token)
    if m:
        return m.end()
    m = _AREA_WIDE.match(token) or _AREA_LOCAL.match(token) or _ROAD.match(token)
    return m.end() if m else len(token)


def detect_addresses(text: str) -> list[PiiSpan]:
    """P7 구간 목록. 주소 어절이 2개 이상 이어지고 행정구역 표지가 있을 때만 잡는다."""
    tokens = _tokens(text)
    found: list[PiiSpan] = []

    run: list[tuple[int, str]] = []
    for offset, token in tokens + [(-1, "")]:          # 보초값으로 마지막 run 을 닫는다
        if offset >= 0 and _classify(token):
            run.append((offset, token))
            continue
        if len(run) >= 2 and any(p.match(t) for _, t in run for p in _STRONG):
            start = run[0][0]
            last_offset, last_token = run[-1]
            found.append(PiiSpan(pattern="P7", start=start,
                                 end=last_offset + _trim_tail(last_token)))
        run = []
    return found
