# Requirement: [Task 1] FastAPI 앱 골격, SEC-2
"""CallGuard FastAPI 코어 — 엔트리포인트 = 합성 루트.

실행 (server/ 에서):
    uvicorn main:app --reload --env-file ../.env

이 파일은 앱을 조립만 한다. 라우터는 각 앱의 adapter/inbound/api/v1/ 에, 파이프라인 배선은 hub 에 둔다
(docs/architecture.md). 스포크 구현체는 여기서 `app.dependency_overrides[<hub 프로바이더>] = <스포크 프로바이더>`
로 꽂는다 — 허브는 스포크를 import 하지 않고(계약 5), 이 파일만 양쪽을 안다. 스포크는 아직 0개다.
"""

from __future__ import annotations

import sys
from contextlib import asynccontextmanager
from pathlib import Path

# apps/ 를 경로에 올려 각 앱(hub·evaluation·<스포크>)을 최상위 패키지로 인식시킨다.
# pytest.ini(pythonpath)·.importlinter(PYTHONPATH=apps) 와 같은 맥락 — 세 곳이 항상 같아야 한다.
sys.path.insert(0, str(Path(__file__).resolve().parent / "apps"))

from fastapi import FastAPI, Request  # noqa: E402

from core.config import Settings, load_settings  # noqa: E402
from hub.adapter.inbound.api.v1.closure_router import closure_router  # noqa: E402
from hub.adapter.inbound.api.v1.compliance_router import compliance_router  # noqa: E402
from hub.adapter.inbound.api.v1.myself_router import myself_router  # noqa: E402
from hub.adapter.inbound.api.v1.postcall_router import postcall_router  # noqa: E402
from hub.adapter.inbound.api.v1.recommendation_router import recommendation_router  # noqa: E402
from hub.adapter.inbound.api.v1.search_router import search_router  # noqa: E402
from hub.adapter.inbound.api.v1.transcript_ingest_router import transcript_ingest_router  # noqa: E402

SPOKES: list[str] = []  # 스포크를 꽂을 때 이름을 추가한다 — /health 가 그대로 보고한다


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.settings = load_settings()
    yield


app = FastAPI(
    title="CallGuard Core",
    summary="실시간 상담원 어시스트 RAG — FastAPI 코어",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(closure_router)
app.include_router(compliance_router)
app.include_router(myself_router)
app.include_router(postcall_router)
app.include_router(recommendation_router)
app.include_router(search_router)
app.include_router(transcript_ingest_router)


@app.get("/health")
def health(request: Request) -> dict:
    """기동 여부 + 외부 자원 설정 여부 + 등록된 스포크. 설정 '값'은 절대 싣지 않는다 (SEC-2)."""
    settings: Settings = request.app.state.settings
    return {
        "status": "ok",
        "mysql_configured": settings.mysql_configured,
        "elasticsearch_configured": settings.elasticsearch_configured,
        "spokes": list(SPOKES),
    }
