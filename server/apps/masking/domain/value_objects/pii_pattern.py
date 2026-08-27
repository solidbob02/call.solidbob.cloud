# Requirement: C-5
"""P1~P7 패턴 정의. [2.4절](/docs/02/) 목록을 그대로 옮긴다 — 여기에 없는 패턴은 만들지 않는다.

순수 파이썬이다. 정규식·표준 라이브러리만 쓴다(.importlinter 계약 4 — domain 은 pydantic 도 모른다).
"""

from __future__ import annotations

from dataclasses import dataclass

# 화면·DB 에 나갈 대체 문자. 자리수를 보존해 "몇 자리였는지"는 남기되 값은 지운다.
MASK_CHAR = "*"


@dataclass(frozen=True)
class PiiSpan:
    """찾아낸 개인정보 구간 1건. `start`/`end` 는 **문자(코드포인트) 오프셋**이다.

    [7.3절](/docs/07/)이 byte 가 아니라 문자 기준으로 못박았다 — 한글은 UTF-8 에서 3바이트라
    byte 로 재면 프론트와 어긋난다.
    """

    pattern: str  # "P1" ~ "P7"
    start: int
    end: int

    def __post_init__(self) -> None:
        if self.start < 0 or self.end <= self.start:
            raise ValueError(f"구간이 올바르지 않습니다: {self.pattern} ({self.start}, {self.end})")

    @property
    def length(self) -> int:
        return self.end - self.start

    def overlaps(self, other: "PiiSpan") -> bool:
        return self.start < other.end and other.start < self.end
