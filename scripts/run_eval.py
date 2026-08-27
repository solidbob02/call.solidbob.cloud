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

from evaluation.golden_set import load_golden_set  # noqa: E402
from evaluation.harness import Ports, run_eval  # noqa: E402
from evaluation.report import print_report  # noqa: E402
from retrieval.adapter.outbound.es_bm25_retriever import EsBm25Retriever  # noqa: E402
from retrieval.adapter.outbound.es_index import SINGLE_INDEX  # noqa: E402
from retrieval.adapter.outbound.search_domain_router import SearchDomainRouter  # noqa: E402

DEFAULT_CLASSIFIER_DIR = ROOT / "models" / "domain-classifier"


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


def build_domain_router(kind: str, retriever, *, model_dir: Path):
    """B-0 라우터를 고른다. `decisions/007` 의 ①(분류기) / ②(검색 폴백)에 대응한다.

    `auto` 는 **검색 기반 v1** 을 쓴다. 분류기가 있어도 마찬가지다 —
    2026-08-27 실측에서 분류기(골든셋 0.786)가 v1(0.857)을 못 넘었기 때문이다.
    AI Hub 검증에서는 0.879 인데 골든셋에서는 안 오른다(분포가 다르다).

    분류기가 v1 을 넘는 것이 측정되면 이 기본값을 뒤집는다. 그때까지 분류기를 보려면
    `--domain-router model` 로 **명시적으로** 고른다 — 더 나쁜 쪽이 기본값으로 조용히
    끼어들면 안 된다. 어느 쪽으로 쟀는지는 실행할 때 출력에 찍힌다.
    """
    if kind == "none":
        return None
    if kind == "model" and model_dir.is_dir():
        from training.adapter.outbound.model_domain_router import ModelDomainRouter

        print(f"B-0: 분류기 사용 — {model_dir}")
        return ModelDomainRouter(model_dir)
    if kind == "model":
        raise SystemExit(
            f"분류기가 없다: {model_dir}\n"
            "  .venv/bin/python scripts/train_domain_classifier.py 로 먼저 학습한다"
        )
    if model_dir.is_dir():
        print("B-0: 검색 기반 v1 사용 (분류기가 있지만 v1 이 더 낫다 — --domain-router model 로 강제)")
    else:
        print("B-0: 검색 기반 v1 사용 (분류기 없음)")
    return SearchDomainRouter(retriever)


def build_ports(client, *, index: str, domain_router: str, model_dir: Path) -> Ports:
    """구현된 스포크만 꽂는다. 나머지는 None — 하네스가 "미구현"으로 보고한다."""
    if client is None:
        return Ports()

    retriever = EsBm25Retriever(client, index=index)
    return Ports(
        retrieval=retriever,
        domain_routing=build_domain_router(domain_router, retriever, model_dir=model_dir),
        # ⚠ trigger 는 **구현이 있는데도 일부러 꽂지 않는다**(IsFinalTrigger, B-1).
        #   TranscriptEvent 에 이벤트 도착 시각이 없어서 발동 시각을 "발화 종료 + STT 지연
        #   상수(346ms)"로 모형화하고 있다. 그대로 채점하면 지연 분포가 상수 하나로 수렴해
        #   p50 = p95 = 346, 적절 발동률 1.0 이 나온다 — **숫자는 나오지만 측정이 아니다.**
        #   측정할 수 없는 것을 측정한 것처럼 쓰지 않는다(절대 원칙 10). 게이트웨이가 도착
        #   시각을 실어 보내게 되면 그때 꽂는다. 서버 경로에는 꽂는다(발동 여부는 진짜 판정이다).
        #
        # 아직 구현이 없는 것: domain_routing(B-0) · compliance(6주차) · closure_gate(F-2)
        #   masking 은 server/apps/masking 에 있으나 하네스 배선은 별건이다.
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="골든셋으로 구현된 스포크를 채점한다")
    ap.add_argument("--golden-set", type=Path, default=None, help="기본: golden-set/v1-10.json")
    ap.add_argument("--index", default=SINGLE_INDEX)
    ap.add_argument("--runs", type=int, default=1, help="N 번 돌려 최저치를 함께 낸다 (절대 원칙 4)")
    ap.add_argument(
        "--domain-router",
        choices=("auto", "model", "search", "none"),
        default="auto",
        help="B-0 판정 방식. auto(기본): 검색 기반 v1 — 분류기가 아직 v1 을 못 넘었다",
    )
    ap.add_argument("--classifier", type=Path, default=DEFAULT_CLASSIFIER_DIR)
    args = ap.parse_args()

    golden_path = args.golden_set or (ROOT / "golden-set" / "v1-10.json")
    items = load_golden_set(golden_path)
    client = _es_client(os.environ.get("ELASTICSEARCH_URL"))
    if client is None:
        print("⚠ ELASTICSEARCH_URL 이 없다 — 검색은 '측정 불가'로 보고된다.\n")

    ports = build_ports(
        client, index=args.index, domain_router=args.domain_router, model_dir=args.classifier
    )
    reports = [run_eval(items, ports) for _ in range(args.runs)]
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
