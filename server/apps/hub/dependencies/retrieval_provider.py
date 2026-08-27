# Requirement: B-2, B-3
"""RetrievalPort 프로바이더. retrieval 스포크(`ai/apps/retrieval/`)가 아직 이 포트를 구현하지 않았으므로
기본은 501 이다 — 빈 목록을 돌려주는 '임시 통과' 구현은 만들지 않는다.

빈 목록은 "관련 문서 없음"(B-6)과 구분되지 않아서, 검색이 죽은 것인지 정말 없는 것인지 알 수 없게 된다.
측정할 수 없는 상태를 만들지 않는다(절대 원칙 10).

스포크가 생기면 main.py 에서 `app.dependency_overrides[get_retrieval_port] = ...` 로 꽂는다.
"""

from __future__ import annotations

from fastapi import HTTPException, status

from hub.app.ports.output.retrieval_port import RetrievalPort


def get_retrieval_port() -> RetrievalPort:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="retrieval 스포크가 등록되지 않았습니다 (B-2)",
    )
