# Requirement: 부록 A-1
from __future__ import annotations

from pydantic import BaseModel


class MyselfResponseSchema(BaseModel):
    name: str
    introduction: str
    endpoints: list[str]
    does_not: list[str]
