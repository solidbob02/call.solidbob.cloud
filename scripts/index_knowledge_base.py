#!/usr/bin/env python3
# Requirement: B-2
"""지식베이스 → 청크 목록 덤프 (w2-kb-index).

골든셋 라벨링이 이 목록을 보고 정답 문서 ID 를 고른다. 같은 입력이면 항상 같은 결과가
나오므로(정렬된 순회) diff 로 변경분을 확인할 수 있다.

    .venv/bin/python scripts/index_knowledge_base.py                 # 요약만
    .venv/bin/python scripts/index_knowledge_base.py --out data/processed/kb-chunks.json

ES 적재는 아직 붙이지 않았다 — 인덱스를 도메인별로 나눌지 하나로 두고 `domain` 필드로
필터할지가 미결이다(`docs/domain.md` §3). 그 결정 전에 인덱스를 만들면 다시 만들어야 한다.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "fastapi" / "apps"))

from retrieval.adapter.outbound.knowledge_base_loader import load_chunks  # noqa: E402
from retrieval.domain.services.chunking import MAX_CHARS  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="지식베이스를 조항 단위 청크로 자른다")
    ap.add_argument("--kb", type=Path, default=ROOT / "knowledge-base")
    ap.add_argument("--out", type=Path, help="청크 목록을 JSON 으로 저장할 경로")
    ap.add_argument("--max-chars", type=int, default=MAX_CHARS)
    args = ap.parse_args()

    chunks = load_chunks(args.kb, max_chars=args.max_chars)

    by_domain = Counter(c.domain for c in chunks)
    by_type = Counter(c.doc_type for c in chunks)
    split = [c for c in chunks if c.chunk_id != c.doc_id]
    lengths = sorted(len(c.text) for c in chunks)

    print(f"청크 {len(chunks)}개 (조항 {len({c.doc_id for c in chunks})}개, 상한 {args.max_chars}자)")
    print("  도메인별:", dict(by_domain))
    print("  문서종류별:", dict(by_type))
    print(f"  길이: 최소 {lengths[0]} / 중앙 {lengths[len(lengths) // 2]} / 최대 {lengths[-1]}자")
    print(f"  분할된 조항: {len(split)}개" + (f" — {[c.chunk_id for c in split]}" if split else ""))

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(
            json.dumps([c.__dict__ for c in chunks], ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"\n저장: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
