# Requirement: 부록 A-1
from __future__ import annotations

from fastapi import APIRouter, Depends

from hub.adapter.inbound.api.schemas.myself_schema import MyselfResponseSchema
from hub.app.dtos.myself_dto import MyselfQuery
from hub.app.ports.input.myself_use_case import MyselfUseCase
from hub.dependencies.myself_provider import get_myself_use_case

myself_router = APIRouter(prefix="/hub", tags=["hub"])


@myself_router.get("/myself", response_model=MyselfResponseSchema)
async def introduce_myself(use_case: MyselfUseCase = Depends(get_myself_use_case)) -> MyselfResponseSchema:
    result = await use_case.introduce_myself(MyselfQuery(name="허브 (hub)"))
    return MyselfResponseSchema(
        name=result.name,
        introduction=result.introduction,
        endpoints=list(result.endpoints),
        does_not=list(result.does_not),
    )
