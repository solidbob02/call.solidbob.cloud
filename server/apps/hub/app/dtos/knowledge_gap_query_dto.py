# Requirement: D-4
"""공백 리포트 조회·집계 DTO.

[2.5절 D-4 확장](/docs/02/)은 **B(검색 실패)·C(놓친 위반)·F(사후 문제)를 같은 루프로
누적**하라고 정했다. 지금까지는 입구(`POST /hub/knowledge-gaps`)만 있어 신고가 쌓이기만 하고
**아무도 볼 수 없었다** — 루프가 닫히지 않았다. 이 DTO 들이 읽는 쪽을 연다.

**여기서 하지 않는 것**: 무엇이 진짜 공백인지, 어느 것을 골든셋으로 승격할지 판정.
그건 품질을 재는 일이라 `ai/` 몫이다(`server/CLAUDE.md` §0). 서버는 **세고 나를 뿐이다.**
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from .knowledge_gap_dto import GapModule

DEFAULT_LIMIT = 50
MAX_LIMIT = 200

GapStatus = str  # db `knowledge_gap.status` CHECK: 'open' | 'resolved'
OPEN = "open"
RESOLVED = "resolved"


@dataclass(frozen=True)
class KnowledgeGapQuery:
    """조회 조건. 필터를 주지 않으면 전부 본다.

    `module`·`status` 로만 좁힌다 — 설명 본문 검색은 넣지 않았다. 신고가 300자짜리
    자유 서술이라 부분일치 검색은 인덱스를 타지 못하고, **무엇이 같은 공백인지 묶는 일은
    `ai/` 가 할 일**이다(문자열 매칭으로 흉내내면 그 판단이 두 곳에 생긴다).
    """

    module: GapModule | None = None
    status: GapStatus | None = None
    limit: int = DEFAULT_LIMIT
    offset: int = 0


@dataclass(frozen=True)
class KnowledgeGapRecord:
    """쌓인 신고 1건. `domain` 은 통화에서 따라온다 — 신고 자체는 도메인을 모른다."""

    gap_id: int
    module: GapModule
    description: str
    status: GapStatus
    created_at: datetime
    call_id: str | None = None
    segment_id: int | None = None
    closure_id: int | None = None
    domain: str | None = None


@dataclass(frozen=True)
class KnowledgeGapPage:
    gaps: tuple[KnowledgeGapRecord, ...] = field(default_factory=tuple)
    total: int = 0
    limit: int = DEFAULT_LIMIT
    offset: int = 0


@dataclass(frozen=True)
class GapCount:
    """한 축의 집계 한 칸. `key` 는 모듈명이거나 도메인명이다."""

    key: str
    open: int = 0
    resolved: int = 0

    @property
    def total(self) -> int:
        return self.open + self.resolved


@dataclass(frozen=True)
class KnowledgeGapSummary:
    """공백 리포트 요약 — **세기만 한다.**

    ⚠ 우선순위·심각도·"위험" 같은 필드를 두지 않는다([부록 A-1](/docs/12/)). 건수가 많다는
    사실과 그것이 중요하다는 판단은 다르고, 후자는 사람이 지식베이스를 보고 정한다.
    """

    by_module: tuple[GapCount, ...] = field(default_factory=tuple)
    by_domain: tuple[GapCount, ...] = field(default_factory=tuple)
    total: int = 0


@dataclass(frozen=True)
class GapResolution:
    """상태 전이 요청. 되돌리기(`resolved` → `open`)도 허용한다 —
    보강했다고 눌렀는데 아니었던 경우를 기록에서 지우지 않고 되돌릴 수 있어야 한다."""

    gap_id: int
    status: GapStatus
