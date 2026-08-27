# Requirement: C-5, QUA-1
"""P1~P5 탐지. **누락 0건이 절대 규칙**이라, 못 잡는 케이스가 생기면 여기서 먼저 깨진다.

지표 우선순위(2.4절): 누락 0건 > 과잉 마스킹 억제. 애매하면 가린다.
"""

import pytest

from masking.domain.services.masker import mask_text


def _patterns(text):
    return [s.pattern for s in mask_text(text)[1]]


def _masked(text):
    return mask_text(text)[0]


# ── 주 실패 모드: 구분자 부재·띄어쓰기 붕괴 (2.4절 ①) ──────────────────────────

@pytest.mark.parametrize("text", [
    "제 번호는 010-1234-5678 입니다",       # 하이픈
    "제 번호는 010 1234 5678 입니다",       # 공백
    "제 번호는 01012345678 입니다",         # 붙임 — 주 실패 모드
    "제 번호는 010.1234.5678 입니다",       # 점
    "제 번호는 (010)1234-5678 입니다",      # 괄호 혼합
])
def test_P4_휴대전화는_구분자와_무관하게_잡힌다(text):
    assert "1234" not in _masked(text)
    assert "P4" in _patterns(text)


@pytest.mark.parametrize("text,pattern", [
    ("주민번호 900101-1234567 입니다", "P1"),
    ("주민번호 9001011234567 입니다", "P1"),
    ("카드번호 1234-5678-9012-3456", "P2"),
    ("카드번호 1234567890123456", "P2"),
    ("계좌 110-123-456789 로 보내주세요", "P3"),
    ("계좌 110123456789 로 보내주세요", "P3"),
])
def test_P1_P2_P3_도_구분자와_무관하다(text, pattern):
    assert pattern in _patterns(text)


# ── 한글 수사 낭독형 (2.4절 ②, 보조) ────────────────────────────────────────

def test_낭독형_숫자를_잡는다():
    """'공일공일이삼사오육칠팔' — STT 가 정규화하지 못한 경우."""
    text = "번호는 공일공일이삼사오육칠팔 입니다"
    assert "P4" in _patterns(text)


def test_일상어에_섞인_한_글자는_숫자로_보지_않는다():
    """'이사'·'사과' 를 숫자로 바꾸면 엉뚱한 곳이 가려진다. 연속 3자 이상만 낭독형으로 본다."""
    assert _masked("이사 가는데 사과 두 개 주세요") == "이사 가는데 사과 두 개 주세요"


def test_번호_뒤에_붙은_조사가_번호에_먹히지_않는다():
    """'01012345678이고' 의 '이' 를 2 로 바꾸면 구간이 뒤로 번진다 (2026-08-27 실제 발생)."""
    masked = _masked("제 번호는 01012345678이고 문자로 남겨주세요")
    assert masked.endswith("이고 문자로 남겨주세요")
    assert "01012345678" not in masked


# ── P5 인증번호 — 문맥 조건 ────────────────────────────────────────────────

@pytest.mark.parametrize("text", [
    "인증번호 4821 입니다", "승인번호는 123456", "확인번호 9012 알려주세요", "OTP 5566",
])
def test_P5_는_문맥이_있을_때_잡는다(text):
    assert "P5" in _patterns(text)


@pytest.mark.parametrize("text", [
    "3천원이고 2개 주세요", "2026년 8월입니다", "1234 번지로 가주세요",
])
def test_문맥이_없으면_짧은_숫자를_가리지_않는다(text):
    """4자리를 전부 가리면 금액·개수·연도까지 지워져 자막 자체가 못 쓰게 된다.
    누락 0건 우선과 충돌하지 않는다 — P5 는 문맥 조건이 명세에 있다(2.4절)."""
    assert "P5" not in _patterns(text)


# ── 겹칠 때: 넓은 쪽을 남긴다 (누락 0건 우선) ────────────────────────────────

def test_자릿수가_겹치면_넓은_쪽을_남긴다():
    """카드(14~16)와 계좌(10~14)가 겹친다. 좁은 쪽을 고르면 뒷자리가 노출된다."""
    masked, spans = mask_text("번호 12345678901234 입니다")
    assert len(spans) == 1
    assert "1234" not in masked


def test_한_발화에_여러_건이_있으면_전부_잡는다():
    text = "번호는 01012345678 이고 카드는 1234567890123456 입니다"
    assert set(_patterns(text)) >= {"P4", "P2"}
    assert "01012345678" not in _masked(text)
    assert "1234567890123456" not in _masked(text)


# ── 마스킹 결과 형태 ──────────────────────────────────────────────────────

def test_자리수를_보존한다():
    """길이가 바뀌면 7.3절 span 오프셋이 화면 텍스트와 어긋난다."""
    text = "제 번호는 01012345678 입니다"
    assert len(_masked(text)) == len(text)


def test_구간은_문자_오프셋이다():
    """한글은 UTF-8 에서 3바이트 — byte 로 재면 프론트와 어긋난다 (7.3절)."""
    text = "제 번호는 01012345678 입니다"
    span = mask_text(text)[1][0]
    assert text[span.start:span.end] == "01012345678"


def test_개인정보가_없으면_원문_그대로다():
    text = "반품 배송비는 누가 내나요"
    assert mask_text(text) == (text, ())
