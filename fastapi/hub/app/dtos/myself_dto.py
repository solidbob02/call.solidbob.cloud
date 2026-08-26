# Requirement: 부록 A-1 (발언 범위)
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MyselfQuery:
    name: str


@dataclass(frozen=True)
class MyselfResult:
    name: str
    introduction: str
    endpoints: tuple[str, ...]
    does_not: tuple[str, ...]  # "하지 않는 것" — 부록 A-1 에 따라 범위를 먼저 말한다
