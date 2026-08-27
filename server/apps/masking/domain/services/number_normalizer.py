# Requirement: C-5
"""탐지 파이프라인 ①② — 정규화. [2.4절](/docs/02/) 순서를 그대로 따른다.

    ① 구분자·공백 제거 후 연속 숫자열 판정   ← 주 실패 모드
    ② 한글 수사 → 숫자 변환 (보조)

**①이 ②보다 앞이다.** Google STT 한국어는 긴 숫자열을 대체로 아라비아 숫자로 정규화하므로,
한글 수사보다 **구분자 부재·띄어쓰기 붕괴**가 지배적 실패 모드다([V3 실측](/docs/05/)).

정규화는 원문을 바꾸지 않는다 — **원문 오프셋으로 되돌릴 지도를 함께 만든다.**
바꾼 문자열 위에서 찾은 위치를 원문에 그대로 쓰면 엉뚱한 곳을 가린다.
"""

from __future__ import annotations

# 숫자 사이에 흔히 끼는 구분자. STT 가 넣기도 하고 안 넣기도 한다.
SEPARATORS = " -–—.()·,/\t"

# ② 한글 수사. "공"·"영" 둘 다 0 으로 읽는다.
SINO_DIGITS = {
    "공": "0", "영": "0", "일": "1", "이": "2", "삼": "3", "사": "4",
    "오": "5", "육": "6", "륙": "6", "칠": "7", "팔": "8", "구": "9",
}


def strip_separators(text: str) -> tuple[str, list[int]]:
    """① 구분자·공백을 없앤 문자열과, 각 문자의 **원문 인덱스** 목록을 함께 돌려준다.

        "010-1234-5678" → ("01012345678", [0,1,2,4,5,6,7,9,10,11,12])

    두 번째 값이 없으면 마스킹 위치를 원문으로 되돌릴 수 없다.
    """
    kept: list[str] = []
    index_map: list[int] = []
    for i, ch in enumerate(text):
        if ch in SEPARATORS:
            continue
        kept.append(ch)
        index_map.append(i)
    return "".join(kept), index_map


# 낭독형으로 인정할 최소 연속 길이. 한글 수사는 일상어와 겹친다 —
# "이"(그리고/이것), "사"(사다), "구"(오래된), "오"(감탄) 가 대표적이다.
# 단독 글자를 바꾸면 "01012345678이고" 의 "이" 가 2 가 되어 번호 구간이 뒤로 번진다(2026-08-27 실제로 발생).
MIN_SINO_RUN = 3


def sino_to_digits(text: str, min_run: int = MIN_SINO_RUN) -> tuple[str, list[int]]:
    """② 한글 수사를 숫자로 바꾼다. 길이가 1:1 이라 인덱스가 보존된다.

    **연속 `min_run` 자 이상일 때만 바꾼다.** "구일공일이삼사" 같은 낭독형은 잡히고,
    "이고"·"이사" 처럼 일상어에 섞인 한 글자는 그대로 둔다.

    보조 수단이다 — 단독으로 쓰지 않는다. 이 변환 결과는 **연속 숫자열 판정에만** 쓰고,
    변환됐다는 사실 자체를 개인정보 근거로 삼지 않는다.
    """
    out = list(text)
    run_start = None
    for i, ch in enumerate(text + "\0"):  # 보초값으로 마지막 런을 닫는다
        if ch in SINO_DIGITS:
            if run_start is None:
                run_start = i
            continue
        if run_start is not None and i - run_start >= min_run:
            for j in range(run_start, i):
                out[j] = SINO_DIGITS[text[j]]
        run_start = None
    return "".join(out), list(range(len(text)))
