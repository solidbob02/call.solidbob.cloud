# Requirement: C-5, SEC-1
"""MaskingPort 구현 — 허브 계약과 masking 도메인을 잇는다.

도메인의 `PiiSpan` 을 허브 DTO `MaskedSpan` 으로 옮기는 것이 전부다. 판정은 도메인이 한다
(절대 원칙 9). **P6·P7(인명·상세주소)은 아직 없다** — NER 모델이 필요하고, 그 전까지
이 어댑터는 P1~P5 만 처리한다는 사실을 숨기지 않는다.
"""

from __future__ import annotations

from hub.app.dtos.transcript_dto import MaskedSpan
from hub.app.ports.output.masking_port import MaskingPort

from ...domain.services.masker import mask_text

# 이 어댑터가 실제로 처리하는 패턴. 평가 하네스가 "무엇을 못 잡는지" 알아야 한다.
SUPPORTED_PATTERNS = ("P1", "P2", "P3", "P4", "P5")
UNSUPPORTED_PATTERNS = ("P6", "P7")  # NER 필요 — 미구현


class RuleMaskingAdapter(MaskingPort):
    def mask(self, text: str) -> tuple[str, tuple[MaskedSpan, ...]]:
        masked, spans = mask_text(text)
        return masked, tuple(
            MaskedSpan(type=s.pattern, span=(s.start, s.end)) for s in spans
        )
