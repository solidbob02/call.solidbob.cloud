# Requirement: B-2
"""`knowledge-base/` 디렉토리 → 청크 목록. 파일시스템 I/O 라서 adapter 계층에 둔다.

도메인 폴더(`finance`·`dasan`·`shopping`·`health`) 아래 `terms`/`manual`/`policy` 의
마크다운을 읽어 조항 단위로 자른다. 실제 자르는 규칙은 domain 계층
(`retrieval.domain.services.chunking`)이 갖고 있고 여기서는 읽어 넘기기만 한다.
"""

from __future__ import annotations

from pathlib import Path

from retrieval.domain.services.chunking import MAX_CHARS, chunk_markdown
from retrieval.domain.value_objects.chunk import DOMAINS, Chunk


def load_chunks(kb_root: Path, *, max_chars: int = MAX_CHARS) -> list[Chunk]:
    """도메인 폴더를 순서대로 훑어 청크를 모은다. 같은 입력이면 항상 같은 순서로 나온다."""
    if not kb_root.is_dir():
        raise FileNotFoundError(f"지식베이스 경로가 없다: {kb_root}")

    chunks: list[Chunk] = []
    for domain in DOMAINS:
        domain_dir = kb_root / domain
        if not domain_dir.is_dir():
            raise FileNotFoundError(f"도메인 폴더가 없다: {domain_dir}")
        for md in sorted(domain_dir.rglob("*.md")):
            if md.name == "README.md":
                continue
            found = chunk_markdown(md.read_text(encoding="utf-8"), max_chars=max_chars)
            mismatched = [c.doc_id for c in found if c.domain != domain]
            if mismatched:
                raise ValueError(f"{md}: 폴더({domain})와 다른 도메인 접두어 — {mismatched}")
            chunks.extend(found)
    return chunks
