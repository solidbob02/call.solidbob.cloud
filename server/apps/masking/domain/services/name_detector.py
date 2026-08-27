# Requirement: C-5
"""탐지 파이프라인 ③ 확장 — P6 인명.

⚠ **이것은 NER 이 아니다.** [2.4절](/docs/02/)은 P6 를 NER 로 정했고 그 판단은 유효하다 —
모델 없이 임의의 한국어 이름을 찾을 수는 없다. 다만 `server/.importlinter` 계약 2 가
`server/` 안에서 `transformers` import 를 금지하므로 **모델은 `ai/` 몫**이다.

그때까지 **문맥이 있을 때만** 잡는다. `"제 이름은 김민준이고"` 처럼 이름을 밝히는
말버릇은 콜센터 발화에서 반복되고, 이 경로가 실제로 개인정보가 흐르는 지점이다.
**문맥 없는 이름(`"그 김민준 씨가"`)은 못 잡는다** — 그 사실을 숨기지 않는다.

문맥을 요구하는 이유는 P5(인증번호)와 같다. 2~4자 한글을 문맥 없이 전부 가리면
자막에서 일반 명사가 통째로 사라져 **자막 자체가 못 쓰게 된다.**
"""

from __future__ import annotations

import re

from ..value_objects.pii_pattern import PiiSpan

# 이름을 밝히는 문맥. 이 뒤에 오는 한글 덩어리만 후보로 본다.
# **목적격(을·를)은 뺀다.** `"이름을 바꾸고"` 는 이름이 무엇인지 밝히는 말이 아니라
# 이름을 대상으로 하는 말이다. 넣어두면 `"바꾸고"` 를 이름으로 잡는다(실제로 걸렸다).
_CONTEXT = r"(?:이름|성함|명의자?|본인\s*이름)\s*(?:은|는|이|가)?\s*"
_CANDIDATE = re.compile(_CONTEXT + r"(?P<name>[가-힣]{2,8})")

# 이름 뒤에 붙는 조사·서술어. 긴 것부터 벗겨야 `"이고"` 가 `"이"` 로 잘리지 않는다.
# 홑글자 `"고"` 는 넣지 않는다 — `"바꾸고"` 가 `"바꾸"` 로 남아 이름이 되어버린다.
_PARTICLES = (
    "이라고", "이라는", "이에요", "예요", "입니다", "이고", "이며", "이지만",
    "인데", "이란", "님", "씨", "은", "는", "이", "가", "을", "를",
)


def _strip_particles(name: str) -> str:
    """뒤에 붙은 조사를 벗긴다. 한 번만 벗긴다 — 두 번 벗기면 이름 글자를 먹는다."""
    for p in _PARTICLES:
        if len(name) - len(p) >= 2 and name.endswith(p):
            return name[: -len(p)]
    return name


def detect_names(text: str) -> list[PiiSpan]:
    """P6 구간 목록. **문맥이 있을 때만** 잡는다 — 일반 NER 을 대체하지 않는다."""
    found: list[PiiSpan] = []
    for m in _CANDIDATE.finditer(text):
        raw = m.group("name")
        name = _strip_particles(raw)
        if not 2 <= len(name) <= 4:          # 한국어 이름의 현실적 길이
            continue
        start = m.start("name")
        found.append(PiiSpan(pattern="P6", start=start, end=start + len(name)))
    return found
