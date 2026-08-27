# Requirement: C-5, SEC-1
"""MaskingPort 프로바이더. 2026-08-27 부터 규칙 기반 구현(P1~P5)이 기본이다.

그 전까지는 501 이었다 — 마스킹 없이 원문을 흘려보내는 '임시 통과' 구현을 만들지 않기
위해서였다(SEC-1: 그 경로가 생기는 순간 원문이 새는 길이 된다). 이제 실제 구현이 있으므로
501 이 아니다.

**P6·P7(인명·상세주소)은 아직 없다.** NER 모델이 필요하고, 그때까지 이 프로바이더는
P1~P5 만 처리한다 — 평가 하네스가 그 사실을 그대로 보고한다.
"""

from __future__ import annotations

from hub.app.ports.output.masking_port import MaskingPort
from masking.adapter.outbound.rule_masking_adapter import RuleMaskingAdapter


def get_masking_port() -> MaskingPort:
    return RuleMaskingAdapter()
