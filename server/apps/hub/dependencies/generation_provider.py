# Requirement: B-4, B-5, B-6
"""GenerationPort 프로바이더. 기본값은 **폴백(스니펫 그대로)** 이다 — 여기만 501 이 아니다.

다른 포트와 달리 폴백을 두는 이유: 스니펫 전달은 [7.3절](/docs/07/)이 정의한 정식 모드이고,
지어내지 않으므로 **환각이 구조적으로 0**이다. 검색만 붙은 상태에서도 파이프라인 전체를 돌려볼 수 있고,
generation 스포크가 붙은 뒤에는 환각 건수 비교의 기준선이 된다.

스포크가 생기면 main.py 에서 `app.dependency_overrides[get_generation_port] = ...` 로 교체한다.
"""

from __future__ import annotations

from hub.adapter.outbound.snippet_card_adapter import SnippetCardAdapter
from hub.app.ports.output.generation_port import GenerationPort


def get_generation_port() -> GenerationPort:
    return SnippetCardAdapter()
