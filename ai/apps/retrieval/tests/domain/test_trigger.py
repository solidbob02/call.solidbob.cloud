# Requirement: B-1
"""트리거 판정 규칙 v1. 순수 계산이라 전부 ES 없이 돈다."""

from __future__ import annotations

import pytest

from retrieval.domain.services.trigger import (
    STT_FINAL_LAG_MS,
    fire_at_ms,
    should_fire,
)


def _fire(**kw) -> bool:
    args = {"is_final": True, "speaker": "customer", "text": "반품 배송비 누가 내나요"}
    args.update(kw)
    return should_fire(**args)


def test_고객의_최종_전사에_발동한다():
    assert _fire() is True


def test_interim_에는_발동하지_않는다():
    """20초 발화에 interim 이 199건 온다(V4 실측). 매번 발동하면 검색이 초당 수십 번 돈다."""
    assert _fire(is_final=False) is False


def test_상담원_발화에는_발동하지_않는다():
    """문서가 필요한 시점은 고객이 질문을 끝냈을 때다. 상담원이 말하는 중에 화면을 바꾸면 방해다."""
    assert _fire(speaker="agent") is False


@pytest.mark.parametrize("text", ["", "   ", "\n\t"])
def test_빈_발화에는_발동하지_않는다(text):
    """빈 문자열로 검색하면 아무 의미 없는 상위 문서가 뜬다."""
    assert _fire(text=text) is False


def test_발동_시각은_발화_종료에_STT_지연을_더한_값이다():
    assert fire_at_ms(3100) == 3100 + STT_FINAL_LAG_MS


def test_STT_지연은_V4_실측값_346ms_다():
    """모형이지 측정이 아니다 — 포트에 도착 시각이 없어서 상수로 놓았다(절대 원칙 10)."""
    assert STT_FINAL_LAG_MS == 346


def test_지연을_바꿔_끼울_수_있다():
    assert fire_at_ms(1000, lag_ms=0) == 1000
    assert fire_at_ms(1000, lag_ms=900) == 1900


def test_발화_종료_시각을_모르면_None_이다():
    """지어내지 않는다. 0 을 돌려주면 "0ms 에 발동했다"는 거짓말이 된다."""
    assert fire_at_ms(None) is None


def test_기본_지연은_허용_창_안에_들어간다():
    """허용 창은 0~1,500ms([4.1절], `decisions/001`). 346ms 는 '적절' 구간이다.

    창 값을 `evaluation.metrics.trigger` 에서 가져오지 않고 여기 적은 이유:
    `retrieval` 이 `evaluation` 을 import 하면 module-independence 계약이 깨진다.
    두 값이 어긋나면 하네스 쪽 테스트가 잡는다.
    """
    on_time_window_ms = (0, 1500)
    assert on_time_window_ms[0] <= STT_FINAL_LAG_MS <= on_time_window_ms[1]
