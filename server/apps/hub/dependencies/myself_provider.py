# Requirement: 부록 A-1
from __future__ import annotations

from hub.adapter.outbound.log_myself_record_adapter import LogMyselfRecordAdapter
from hub.app.ports.input.myself_use_case import MyselfUseCase
from hub.app.use_cases.myself_interactor import MyselfInteractor


def get_myself_use_case() -> MyselfUseCase:
    return MyselfInteractor(record=LogMyselfRecordAdapter())
