# Requirement: B-2
import pytest

from retrieval.domain.services.chunking import chunk_markdown, parse_doc_id

SAMPLE = """# 한별금융 상품 이용약관

머리말은 ID 마커가 없으므로 청크가 되지 않는다.

---

## 제1장 총칙

<!-- id: FIN-TERM-1.1 -->
### 1.1 목적

이 약관은 회사가 제공하는 상품의 이용조건을 규정한다.

<!-- id: FIN-TERM-1.2 -->
### 1.2 정의

"이용자"란 계약을 체결한 자를 말한다.
"""


def test_조항마다_청크가_하나씩_나온다():
    chunks = chunk_markdown(SAMPLE)
    assert [c.doc_id for c in chunks] == ["FIN-TERM-1.1", "FIN-TERM-1.2"]


def test_머리말은_청크가_되지_않는다():
    assert all("머리말" not in c.text for c in chunk_markdown(SAMPLE))


def test_제목과_본문을_분리한다():
    first = chunk_markdown(SAMPLE)[0]
    assert first.title == "1.1 목적"
    assert first.text.startswith("이 약관은")
    assert "###" not in first.text


def test_구분선은_본문에_남지_않는다():
    assert all(not c.text.strip().endswith("---") for c in chunk_markdown(SAMPLE))


def test_도메인과_문서종류를_ID에서_끌어온다():
    first = chunk_markdown(SAMPLE)[0]
    assert (first.domain, first.doc_type) == ("finance", "TERM")


def test_분할이_없으면_chunk_id는_doc_id와_같다():
    assert all(c.chunk_id == c.doc_id and c.part == 0 for c in chunk_markdown(SAMPLE))


def test_상한을_넘는_조항만_문단_경계에서_쪼갠다():
    body = "\n\n".join(["가" * 90] * 4)  # 문단 4개, 합계가 상한을 넘는다
    chunks = chunk_markdown(f"<!-- id: SHOP-MANUAL-9.9 -->\n### 9.9 긴 조항\n\n{body}", max_chars=200)
    assert len(chunks) > 1
    assert [c.chunk_id for c in chunks] == [f"SHOP-MANUAL-9.9#{i}" for i in range(len(chunks))]
    # 쪼개져도 골든셋이 대조하는 doc_id 는 조항 ID 그대로여야 한다
    assert {c.doc_id for c in chunks} == {"SHOP-MANUAL-9.9"}
    assert all(c.text for c in chunks)


def test_상한을_넘는_단일_문단은_문장_중간에서_끊지_않는다():
    long_para = "나" * 500
    chunks = chunk_markdown(f"<!-- id: HLT-POLICY-1 -->\n### 1 긴 문단\n\n{long_para}", max_chars=200)
    assert len(chunks) == 1
    assert len(chunks[0].text) == 500


@pytest.mark.parametrize(
    "doc_id,expected",
    [("FIN-TERM-3.2", ("finance", "TERM")), ("DASAN-MANUAL-1.4", ("dasan", "MANUAL")),
     ("SHOP-POLICY-RETURN-1", ("shopping", "POLICY")), ("HLT-TERM-2.1", ("health", "TERM"))],
)
def test_네_도메인_접두어를_모두_해석한다(doc_id, expected):
    assert parse_doc_id(doc_id) == expected


def test_모르는_접두어는_거부한다():
    with pytest.raises(ValueError):
        parse_doc_id("TELCO-TERM-1.1")  # 폐기된 통신 도메인
