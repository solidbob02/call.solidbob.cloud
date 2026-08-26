# Requirement: B-2, B-3
from __future__ import annotations

from fastapi import Depends

from hub.app.ports.input.search_use_case import SearchUseCase
from hub.app.ports.output.retrieval_port import RetrievalPort
from hub.app.use_cases.search_interactor import SearchInteractor
from hub.dependencies.retrieval_provider import get_retrieval_port


def get_search_use_case(retrieval: RetrievalPort = Depends(get_retrieval_port)) -> SearchUseCase:
    return SearchInteractor(retrieval=retrieval)
