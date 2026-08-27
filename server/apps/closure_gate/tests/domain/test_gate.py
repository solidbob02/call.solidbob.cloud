# Requirement: F-2, QUA-1
"""종결 게이트 판정. **필수 근거 미기재 시 100% 차단이 절대 규칙**이라, 통과가 하나라도
새면 여기서 먼저 깨진다.

규칙표의 출처는 도메인별 내부처리규정(`*-POLICY-*`)이다 — 이 테스트가 검증하는 것은
"코드가 그 문서와 같은가"이지 "규칙이 옳은가"가 아니다.
"""

import pytest

from closure_gate.domain.services.gate import UnknownClosureType, evaluate
from closure_gate.domain.value_objects.closure_rule import RULES

ALL_TRUE = {t: {f: True for f in r.required} for t, r in RULES.items()}


# ── 통과 ────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("closure_type", list(RULES))
def test_필수_근거가_전부_참일_때만_통과한다(closure_type):
    d = evaluate(closure_type, ALL_TRUE[closure_type])
    assert d.verdict == "approved" and d.missing == ()


# ── 차단 ────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("closure_type, drop", [
    (t, f) for t, r in RULES.items() for f in r.required
])
def test_하나라도_빠지면_차단한다(closure_type, drop):
    """건 단위다 — 3개 중 2개를 채워도 통과가 아니다(6.2절)."""
    evidence = {**ALL_TRUE[closure_type], drop: False}
    d = evaluate(closure_type, evidence)
    assert d.verdict == "blocked"
    assert drop in d.missing


@pytest.mark.parametrize("closure_type", list(RULES))
def test_키가_아예_없으면_미충족으로_본다(closure_type):
    """`false` 와 "키 없음"을 구분하지 않는다 — 둘 다 '고지했다는 근거가 없다'이다."""
    d = evaluate(closure_type, {"관계없는_필드": True})
    assert d.verdict == "blocked"
    assert d.missing == RULES[closure_type].required


@pytest.mark.parametrize("value", [1, "yes", "true", [1], {"a": 1}])
def test_True_가_아닌_참_같은_값은_참으로_세지_않는다(value):
    """`1`·`"yes"` 를 통과로 세면 클라이언트 버그가 종결을 승인시킨다. 애매하면 막는다."""
    d = evaluate("교환", {"교환가능_확인": value, "재고_확인": value})
    assert d.verdict == "blocked" and d.missing == ("교환가능_확인", "재고_확인")


def test_missing_은_규정_문서의_필드_순서를_지킨다():
    """상담원이 화면에서 보는 순서와 규정을 읽는 순서가 어긋나면 무엇을 빠뜨렸는지 찾기 어렵다."""
    d = evaluate("상품해지", {"고객확인_기록": True})
    assert d.missing == ("중도해지수수료_안내", "약정혜택소멸_안내")


# ── 판정할 수 없는 경우 ──────────────────────────────────────────────────────

@pytest.mark.parametrize("closure_type", ["민원접수", "문의", "", "해지"])
def test_규칙표에_없는_처리유형은_판정하지_않는다(closure_type):
    """`approved` 는 절대 규칙 위반이고 `blocked` 도 거짓말이다 — 근거가 빠진 게 아니라
    판정할 규칙이 없는 것이다. 요청 오류로 돌려보낸다(라우터가 422 로 옮긴다).

    `"해지"` 를 넣은 이유: 규칙표 값은 `"상품해지"` 다. 비슷한 이름을 눈감아 주면
    오타 하나로 게이트가 조용히 사라진다."""
    with pytest.raises(UnknownClosureType):
        evaluate(closure_type, {"아무거나": True})


# ── 규칙표가 규정 문서·DB 스키마와 어긋나지 않는지 ─────────────────────────────

def test_처리유형은_DB_스키마_CHECK_와_같다():
    """db/schema.sql: CHECK ("closure_type" IN ('상품해지','보상','반품','교환')).
    어긋나면 게이트는 통과시켰는데 저장에서 깨진다."""
    assert set(RULES) == {"상품해지", "보상", "반품", "교환"}


def test_필수_근거_필드는_전부_DB_컬럼으로_존재한다():
    from pathlib import Path
    schema = (Path(__file__).resolve().parents[4].parent / "db" / "schema.sql").read_text(encoding="utf-8")
    for rule in RULES.values():
        for field in rule.required:
            assert f'"{field}"' in schema, f"{rule.closure_type}: {field} 컬럼이 스키마에 없다"


def test_필수_근거가_없는_규칙은_만들_수_없다():
    from closure_gate.domain.value_objects.closure_rule import ClosureRule
    with pytest.raises(ValueError):
        ClosureRule(closure_type="빈규칙", required=(), source_doc_id="X", source_title="X")
