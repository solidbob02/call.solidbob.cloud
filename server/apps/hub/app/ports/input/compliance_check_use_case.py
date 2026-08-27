# Requirement: C-1, C-2, C-3, C-4
from __future__ import annotations

from abc import ABC, abstractmethod

from hub.app.dtos.compliance_dto import ComplianceCheckCommand, ComplianceCheckResult


class ComplianceCheckUseCase(ABC):
    """상담원 발화 1건에서 컴플라이언스 위반을 찾는다 (C-1~C-4).

    추천 파이프라인(B)과 **별개 경로**다. 검색은 고객 발화에 반응하고, 이쪽은 상담원 발화에
    반응한다 — 한 인터랙터에 묶으면 화자에 따라 분기하는 if 가 생기고 두 지표가 섞인다.
    """

    @abstractmethod
    async def check(self, command: ComplianceCheckCommand) -> ComplianceCheckResult: ...
