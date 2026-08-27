# Requirement: C-5, SEC-1
"""MaskingPort 구현 — 허브 계약과 masking 도메인을 잇는다.

도메인의 `PiiSpan` 을 허브 DTO `MaskedSpan` 으로 옮기는 것이 전부다. 판정은 도메인이 한다
(절대 원칙 9).

**P1~P7 을 전부 처리하지만, P6·P7 은 NER 이 아니라 규칙이다.** [2.4절](/docs/02/)이 정한
방식은 NER 이고 그 판단은 유효하다 — 모델은 `ai/` 몫이라(계약 2) 여기서는 규칙으로
바닥을 깔았다. 규칙이 못 잡는 범위가 있으므로 **완전 지원과 구분해서 노출한다** —
평가 하네스가 "무엇을 어떤 방식으로 잡는지" 알아야 수치를 해석할 수 있다.
"""

from __future__ import annotations

from hub.app.dtos.transcript_dto import MaskedSpan
from hub.app.ports.output.masking_port import MaskingPort

from ...domain.services.masker import mask_text

# 이 어댑터가 실제로 처리하는 패턴. 평가 하네스가 "무엇을 어떻게 잡는지" 알아야 한다.
SUPPORTED_PATTERNS = ("P1", "P2", "P3", "P4", "P5", "P6", "P7")

# 규칙만으로 처리하는 패턴 — 명세상 방식(NER)과 다르다. 놓치는 범위가 있다:
#   P6 인명     이름을 밝히는 문맥이 있을 때만. `"그 김민준 씨가"` 는 못 잡는다
#   P7 상세주소 주소 어절이 2개 이상 이어질 때만. `"테헤란로요"` 단독은 못 잡는다
# NER(`ai/`)이 붙으면 이 규칙은 폴백으로 남고 이 목록은 비워진다.
PARTIAL_PATTERNS = ("P6", "P7")
UNSUPPORTED_PATTERNS = ()  # 목록의 모든 패턴에 최소 한 경로는 있다


class RuleMaskingAdapter(MaskingPort):
    def mask(self, text: str) -> tuple[str, tuple[MaskedSpan, ...]]:
        masked, spans = mask_text(text)
        return masked, tuple(
            MaskedSpan(type=s.pattern, span=(s.start, s.end)) for s in spans
        )
