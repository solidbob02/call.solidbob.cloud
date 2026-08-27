# Requirement: D-1, D-2, D-3
"""통화 후 처리 결과 — 나르기만 한다. 필드명은 `db/schema.sql` 의 `call`·`follow_up_action` 과 같다.

**전부 초안이다.** D-1~D-3 은 모델이 만든 것이고, 확정은 상담원이 한다.
부록 A-1 이 금지한 것은 "모델이 정한 것을 시스템이 확정한 것처럼 보이게 하는 것"이라,
필드 이름과 주석에 그 성격을 남긴다.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class FollowUpAction:
    """D-3 후속조치 1건. `action_text` 는 db `follow_up_action.action_text` 와 같다."""

    action_text: str


@dataclass(frozen=True)
class CallSummaryDraft:
    """D-1·D-2·D-3 결과 묶음. 이름이 `Draft` 인 것이 계약의 일부다.

    `inquiry_type` 은 **분류 제안**이지 확정된 유형이 아니다 — 상담원이 바꿀 수 있다.
    화면도 "제안"으로 표시해야 한다(부록 A-1). 자동 확정하는 경로를 만들지 않는다.
    """

    call_id: str
    summary_text: str  # D-1
    inquiry_type: str | None = None  # D-2 — 제안. 확정 아님
    follow_up_actions: tuple[FollowUpAction, ...] = field(default_factory=tuple)  # D-3
    confirmed: bool = False  # 상담원이 확정했는가. 모델 출력은 항상 False 로 들어온다
