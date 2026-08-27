# Requirement: QUA-1, SEC-2
"""테스트 환경 격리.

**테스트는 주변 환경에 기대지 않는다.** 여러 테스트가 "PostgreSQL 이 설정되지 않았을 때
501 을 준다" 를 확인하는데, `.env` 를 export 한 셸에서 돌리면 그 전제가 깨져 **6건이
빨간불**이 된다. CI 는 `.env` 가 없어 통과하므로 **로컬에서만 나는 유령 실패**가 되고,
받은 사람은 자기 환경을 의심하며 시간을 쓴다(2026-08-27 실제로 겪었다).

그래서 설정 계열 환경변수를 테스트마다 걷어낸다. 실제 DB 가 필요한
`@pytest.mark.integration` 테스트는 **자기 안에서 `.env` 파일을 직접 읽어** 다시 채우므로
영향받지 않는다 — 필요한 쪽이 명시적으로 가져가는 구조다.
"""

from __future__ import annotations

import os

import pytest

# `core/config.py` 가 읽는 접두어들. 설정을 읽는 곳이 거기 하나뿐이라 목록이 짧게 유지된다.
_MANAGED_PREFIXES = ("POSTGRES_", "DATABASE_", "ELASTICSEARCH_", "GOOGLE_", "STT_", "AWS_")


@pytest.fixture(autouse=True)
def isolated_settings_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """설정 환경변수를 걷어낸 상태에서 각 테스트를 돌린다."""
    for key in list(os.environ):
        if key.startswith(_MANAGED_PREFIXES):
            monkeypatch.delenv(key, raising=False)
