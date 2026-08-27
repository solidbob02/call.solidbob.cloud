#!/usr/bin/env python3
# Requirement: E-1, E-2, B-2
"""평가 하네스 실행 — 구현된 스포크를 포트에 꽂아 골든셋으로 채점한다 (w2-naive-rag).

    cd infra && docker compose up -d && cd ..
    export ELASTICSEARCH_URL=http://localhost:9200
    .venv/bin/python scripts/run_eval.py                                  # v1-10
    .venv/bin/python scripts/run_eval.py --golden-set golden-set/v1-50.json
    .venv/bin/python scripts/run_eval.py --runs 3                         # 최저치 확인용

**이 파일이 평가 쪽 합성 루트다.** `evaluation` 이 `retrieval` 을 직접 import 하면
`ai/.importlinter` 의 module-independence 계약이 깨진다 — 접점은 hub 포트(추상)뿐이어야 하고,
구체 구현을 꽂는 일은 두 모듈 **밖에서** 해야 한다. `server/main.py` 가 요청 경로에 대해
하는 일을 여기서 평가 경로에 대해 한다.

아직 구현되지 않은 스포크는 `None` 으로 남아 "측정 불가 — 모듈 미구현"으로 보고된다.
그 정직성을 우회하지 않는다(절대 원칙 2).

`--runs N` 은 같은 측정을 N 번 돌려 **최저치**를 함께 낸다(절대 원칙 4). 기준선을 고정할
때는 평균이 아니라 그 최저치를 쓴다. 다만 **기록은 이 스크립트가 하지 않는다** — 값 하나에
측정일·커밋·재현 명령·표본 수가 함께 남아야 하고(§5), 그건 `w2-baseline` 티켓의 몫이다.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / "ai" / "apps"), str(ROOT / "server" / "apps")]

from closure_gate.adapter.outbound.rule_closure_gate_adapter import (  # noqa: E402
    RuleClosureGateAdapter,
)
from evaluation.golden_set import load_golden_set  # noqa: E402
from evaluation.harness import Ports, run_eval  # noqa: E402
from evaluation.report import print_report  # noqa: E402
from masking.adapter.outbound.rule_masking_adapter import RuleMaskingAdapter  # noqa: E402
from retrieval.adapter.outbound.es_bm25_retriever import EsBm25Retriever  # noqa: E402
from retrieval.adapter.outbound.es_index import SINGLE_INDEX  # noqa: E402


def _es_client(url: str | None):
    """ES 클라이언트. 없으면 None 을 돌려주고 검색은 "미구현"으로 보고된다.

    설정을 읽는 곳을 스크립트 한 곳으로 모은다 — 어댑터가 환경변수를 직접 읽으면
    테스트에서 갈아끼울 수 없다. `scripts/index_knowledge_base.py` 와 같은 방식이다.
    """
    if not url:
        return None
    try:
        from elasticsearch import Elasticsearch
    except ModuleNotFoundError:
        raise SystemExit("elasticsearch 패키지가 없다:  pip install -r ai/requirements.txt") from None

    api_key = os.environ.get("ELASTICSEARCH_API_KEY") or None
    client = Elasticsearch(url, api_key=api_key) if api_key else Elasticsearch(url)
    if not client.ping():
        raise SystemExit(f"ES 에 붙지 못했다: {url}  (cd infra && docker compose up -d)")
    return client


def build_ports(client, *, index: str) -> Ports:
    """구현된 스포크만 꽂는다. 나머지는 None — 하네스가 "미구현"으로 보고한다.

    `masking`·`closure_gate` 는 `server/apps/` 에 산다. 규칙 기반 판정이라 요청 경로에서
    매번 실행되기 때문이다(`server/CLAUDE.md` §0). **여기서 꽂는 것이 계약 위반이 아닌 이유**:
    의존 방향은 `ai → server` 한쪽이고(`server/.importlinter` 계약 2), 이 파일은 두 모듈
    **밖의 합성 루트**라 어느 쪽 계약에도 걸리지 않는다.

    ⚠ **ES 가 없어도 마스킹·F-2 는 채점된다.** 둘 다 외부 의존이 없는 순수 규칙이라
    `ELASTICSEARCH_URL` 없이도 숫자가 나온다 — 검색만 "측정 불가"로 남는다.
    """
    return Ports(
        retrieval=EsBm25Retriever(client, index=index) if client is not None else None,
        masking=RuleMaskingAdapter(),          # C-5 (server/apps/masking)
        closure_gate=RuleClosureGateAdapter(),  # F-2 (server/apps/closure_gate)
        # 아직 없는 것: domain_routing(B-0) · trigger(3주차) · compliance(6주차)
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="골든셋으로 구현된 스포크를 채점한다")
    ap.add_argument("--golden-set", type=Path, default=None, help="기본: golden-set/v1-10.json")
    ap.add_argument("--index", default=SINGLE_INDEX)
    ap.add_argument("--runs", type=int, default=1, help="N 번 돌려 최저치를 함께 낸다 (절대 원칙 4)")
    args = ap.parse_args()

    golden_path = args.golden_set or (ROOT / "golden-set" / "v1-10.json")
    items = load_golden_set(golden_path)
    client = _es_client(os.environ.get("ELASTICSEARCH_URL"))
    if client is None:
        print("⚠ ELASTICSEARCH_URL 이 없다 — 검색은 '측정 불가'로 보고된다.\n")

    reports = [run_eval(items, build_ports(client, index=args.index)) for _ in range(args.runs)]
    print_report(reports[0], golden_set_path=golden_path)

    if args.runs > 1:
        _print_worst(reports)
    return 0


def _print_worst(reports: list[dict]) -> None:
    """여러 번 실행한 값 중 **최저치**. 기준선은 평균이 아니라 이 값으로 고정한다(절대 원칙 4)."""
    print("\n" + "=" * 60)
    print(f"{len(reports)}회 실행 중 최저치 (기준선은 이 값으로 고정한다 — 절대 원칙 4)")
    sections = [s for s, r in reports[0].items() if isinstance(r, dict)]
    for section in sections:
        values = [r[section] for r in reports if isinstance(r.get(section), dict)]
        if not values:
            continue
        numeric = [k for k, v in values[0].items() if isinstance(v, (int, float))]
        worst = {k: min(v[k] for v in values) for k in numeric}
        print(f"\n[{section}]")
        for k, v in worst.items():
            print(f"  {k}: {v}")


if __name__ == "__main__":
    raise SystemExit(main())
