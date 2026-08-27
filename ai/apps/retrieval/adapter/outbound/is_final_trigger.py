# Requirement: B-1
"""`TriggerPort` 구현 v1 — `is_final` 도착 기반.

판정 규칙 자체는 `retrieval.domain.services.trigger` 에 있고 여기는 계약 DTO 로 옮기기만 한다
(`ai/CLAUDE.md` 4번 — 알고리즘은 domain, 배선은 adapter).

`RetrievalPort` 와 달리 **동기 함수**다. 규칙 계산뿐이라 외부 자원을 부르지 않는다
(`TriggerPort.decide` 가 `def` 인 이유).

## `at_ms` 를 무엇으로 채우는가 — 읽고 넘어갈 것

`TranscriptEvent` 에는 **이벤트가 언제 도착했는지가 없다.** `utterance_end_ms`(발화가 끝난
시각)만 있다. 그래서 발동 시각을 실제로 알 방법이 없고, 지금은 "발화 종료 + STT 최종 결과
지연(V4 실측 346ms)"으로 **모형화**한다.

그 결과 이 구현으로 낸 지연 분포는 **상수 하나로 수렴한다**(p50 = p95 = 346). 숫자가 나오지만
측정이 아니다 — 그래서 `scripts/run_eval.py` 는 트리거 포트를 **꽂지 않고** 하네스가
"측정 불가"로 보고하게 둔다(절대 원칙 10). 서버 경로에는 꽂는다 — 거기서는 발동 여부(fire)
자체가 파이프라인을 흐르게 하는 데 필요하고, 그건 진짜 판정이기 때문이다.

**고칠 방법**: 게이트웨이가 도착 시각을 실어 보내고 포트가 그걸 받게 한다. 계약 변경이라
`server/` 와 합의가 필요하다 — [미결 항목](/open-items/) 참고.
"""

from __future__ import annotations

from typing import Callable

from hub.app.dtos.transcript_dto import TranscriptEvent
from hub.app.dtos.trigger_decision_dto import TriggerDecision
from hub.app.ports.output.trigger_port import TriggerPort

from retrieval.domain.services.trigger import STT_FINAL_LAG_MS, fire_at_ms, should_fire


class IsFinalTrigger(TriggerPort):
    """고객의 `is_final` 전사가 도착하면 발동한다.

    `now_ms` 를 주면 그 값을 발동 시각으로 쓴다 — 실시간 경로가 붙었을 때의 통로다.
    주지 않으면 `utterance_end_ms + lag_ms` 로 모형화한다(위 주석).
    """

    def __init__(
        self,
        *,
        lag_ms: int = STT_FINAL_LAG_MS,
        now_ms: Callable[[], int] | None = None,  # 통화 기준 ms 를 돌려주는 시계
    ) -> None:
        if lag_ms < 0:
            raise ValueError(f"lag_ms 는 음수일 수 없다: {lag_ms}")
        self._lag_ms = lag_ms
        self._now_ms = now_ms

    def decide(self, event: TranscriptEvent) -> TriggerDecision:
        if not should_fire(is_final=event.is_final, speaker=event.speaker, text=event.text):
            return TriggerDecision(fire=False)

        at_ms = self._now_ms() if self._now_ms else fire_at_ms(
            event.utterance_end_ms, lag_ms=self._lag_ms
        )
        if at_ms is None:
            # 발동은 맞는데 시각을 모른다. 지어내지 않는다 — 하네스는 이걸 "발동 안 함"으로
            # 세지만, 그게 "0ms 에 발동했다"고 거짓말하는 것보다 낫다(절대 원칙 10).
            return TriggerDecision(fire=True, at_ms=None)
        return TriggerDecision(fire=True, at_ms=at_ms)
