# Requirement: D-1, D-2, D-3
"""POST /hub/calls/{call_id}/close — 통화 종료 후 요약·유형 제안·후속조치.

응답은 언제나 초안이다. `confirmed` 를 서버가 true 로 만드는 경로는 없다 — 확정은 상담원 몫이다.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from hub.adapter.inbound.api.schemas.postcall_schema import (
    CallSummaryResponse,
    FollowUpActionSchema,
    PostcallRequest,
)
from hub.app.dtos.postcall_dto import PostcallCommand
from hub.app.dtos.transcript_dto import TranscriptEvent
from hub.app.ports.input.postcall_use_case import PostcallUseCase
from hub.dependencies.postcall_provider import get_postcall_use_case

postcall_router = APIRouter(prefix="/hub", tags=["hub"])


@postcall_router.post("/calls/{call_id}/close", response_model=CallSummaryResponse)
async def close_call(
    call_id: str,
    body: PostcallRequest,
    use_case: PostcallUseCase = Depends(get_postcall_use_case),
) -> CallSummaryResponse:
    if call_id != body.call_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="경로의 call_id 와 본문의 call_id 가 다릅니다",
        )

    try:
        draft = await use_case.close(
            PostcallCommand(
                call_id=call_id,
                segments=tuple(
                    TranscriptEvent(
                        call_id=call_id,
                        segment_id=s.segment_id,
                        speaker=s.speaker,
                        text=s.text,
                        is_final=s.is_final,
                        utterance_end_ms=s.utterance_end_ms,
                    )
                    for s in body.segments
                ),
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(exc)) from exc

    return CallSummaryResponse(
        call_id=draft.call_id,
        summary_text=draft.summary_text,
        inquiry_type=draft.inquiry_type,
        follow_up_actions=[FollowUpActionSchema(action_text=a.action_text) for a in draft.follow_up_actions],
        confirmed=draft.confirmed,
    )
