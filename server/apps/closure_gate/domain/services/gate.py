# Requirement: F-2
"""판정 ③ — 종결 요건 검증. **규칙이 판정한다. 생성 모델은 여기 없다** (절대 원칙 9).

절대 규칙: **필수 근거가 하나라도 채워지지 않으면 종결 100% 차단.**
[6.2절](/docs/06/)대로 평균이 아니라 건 단위다 — 한 건이라도 통과시키면 실패다.

**주장 범위를 넘지 않는다.** 이 게이트는 *"근거 없는 종결의 비용을 올린다"* 는 목적이지
*"허위 기재를 막는다"* 는 목적이 아니다([2.7절](/docs/02/)·[부록 A-3](/docs/12/)).
상담원이 필드를 고의로 거짓 입력하면 막을 수 없고, 막을 수 있는 척하지도 않는다.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..value_objects.closure_rule import RULES, ClosureRule


class UnknownClosureType(ValueError):
    """규칙표에 없는 처리유형. **판정하지 않고 거절한다.**

    `approved` 는 절대 규칙 위반이고, `blocked` 도 거짓말이다 — "근거가 빠졌다"가 아니라
    "판정할 규칙이 없다"이기 때문이다. 둘 중 무엇을 돌려줘도 화면이 사실과 달라지므로
    요청 오류(422)로 돌려보낸다. F-2 미적용 도메인(다산·질병관리본부)은 애초에 이 경로를
    부르지 않는다.
    """


@dataclass(frozen=True)
class GateDecision:
    verdict: str  # "approved" | "blocked"
    missing: tuple[str, ...]
    rule: ClosureRule


def evaluate(closure_type: str, evidence: dict[str, bool]) -> GateDecision:
    """처리유형의 필수 근거가 전부 `True` 일 때만 `approved`.

    **값이 없으면 채워지지 않은 것으로 본다.** 키가 아예 빠진 경우와 `false` 인 경우를
    구분하지 않는다 — 둘 다 "고지했다는 근거가 없다"이고, 애매하면 막는다는 원칙에 맞는다.
    `True` 인지 **엄격하게** 본다(`1`·`"yes"` 같은 값을 참으로 세지 않는다).
    """
    rule = RULES.get(closure_type)
    if rule is None:
        raise UnknownClosureType(
            f"'{closure_type}' 은 종결 게이트가 판정할 수 있는 처리유형이 아닙니다 "
            f"(가능: {', '.join(RULES)})"
        )

    missing = tuple(field for field in rule.required if evidence.get(field) is not True)
    return GateDecision(
        verdict="blocked" if missing else "approved",
        missing=missing,
        rule=rule,
    )
