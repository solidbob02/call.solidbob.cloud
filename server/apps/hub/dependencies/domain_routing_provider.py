# Requirement: B-0
"""DomainRoutingPort 프로바이더. **B-0 는 선택이라 기본값이 None 이다** — 501 이 아니다.

`_project/decisions/007` 이 정한 설계상, 분류 신뢰도가 낮으면 4개 인덱스를 전부 검색하는 폴백이 있다.
분류기가 아예 없는 상태는 그 폴백이 항상 켜진 것과 같으므로 파이프라인이 멈출 이유가 없다.
도메인 판정 정확도는 평가 하네스가 "측정 불가 — 모듈 미구현"으로 따로 보고한다.
"""

from __future__ import annotations

from hub.app.ports.output.domain_routing_port import DomainRoutingPort


def get_domain_routing_port() -> DomainRoutingPort | None:
    return None
