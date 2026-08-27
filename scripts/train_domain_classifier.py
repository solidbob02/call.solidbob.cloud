#!/usr/bin/env python3
# Requirement: B-0
"""B-0 도메인 분류기 파인튜닝 (w1-domain-routing).

    .venv/bin/python scripts/train_domain_classifier.py                 # 기본 2 epoch
    .venv/bin/python scripts/train_domain_classifier.py --epochs 1 --limit 4000   # 빠른 확인

학습 데이터는 **AI Hub 민원(콜센터) 질의응답**(`data/raw/aihub-minwon-qa/`)이다.
**골든셋은 쓰지 않는다** — 평가 세트라 학습에 쓰면 그 라벨로 다시 잴 수 없다.

산출물은 `models/domain-classifier/`(gitignore 대상). 각자 이 명령으로 다시 만든다.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "ai" / "apps"))

from training.adapter.outbound.aihub_minwon_loader import (  # noqa: E402
    load_samples,
    stratified_split,
)
from training.adapter.outbound.domain_classifier_trainer import TrainConfig, train  # noqa: E402


def main() -> int:
    cfg = TrainConfig()
    ap = argparse.ArgumentParser(description="AI Hub 민원 데이터로 B-0 분류기를 학습한다")
    ap.add_argument("--data", type=Path, default=ROOT / "data" / "raw" / "aihub-minwon-qa")
    ap.add_argument("--base-model", default=str(ROOT / cfg.base_model))
    ap.add_argument("--out", default=str(ROOT / cfg.output_dir))
    ap.add_argument("--epochs", type=int, default=cfg.epochs)
    ap.add_argument("--batch-size", type=int, default=cfg.batch_size)
    ap.add_argument("--limit", type=int, help="도메인별 상한 — 빠르게 확인할 때만 쓴다")
    args = ap.parse_args()

    samples, dropped = load_samples(args.data)
    print(f"표본 {len(samples)}건 · 걸러낸 것 {dropped}")

    if args.limit:
        by: dict[str, list] = {}
        for s in samples:
            by.setdefault(s.domain, []).append(s)
        samples = [s for d in sorted(by) for s in by[d][: args.limit]]
        print(f"⚠ --limit {args.limit} 적용 → {len(samples)}건. 이 결과는 기준선으로 쓰지 않는다")

    train_set, val_set = stratified_split(samples)
    metrics = train(
        train_set,
        val_set,
        TrainConfig(
            base_model=args.base_model,
            output_dir=args.out,
            epochs=args.epochs,
            batch_size=args.batch_size,
        ),
    )
    print(f"\n검증 정확도(AI Hub 분할): {metrics['accuracy']:.4f} (n={metrics['n']})")
    print("도메인별:", {d: round(v, 4) for d, v in metrics["per_domain"].items()})
    print("\n골든셋 기준 B-0 정확도는 따로 잰다:")
    print("  .venv/bin/python scripts/run_eval.py --golden-set golden-set/v1-50.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
