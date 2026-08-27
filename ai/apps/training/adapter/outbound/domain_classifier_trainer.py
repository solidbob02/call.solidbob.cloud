# Requirement: B-0
"""KcELECTRA 파인튜닝 — 4클래스 도메인 분류기. torch 를 부르므로 adapter 계층.

`decisions/007` 설계 ①이다. 지금까지의 v1(검색 기반, 정확도 0.647)이 넘어야 할 대상이고,
학습 데이터는 **골든셋이 아니라** AI Hub 민원 데이터셋이다 — 골든셋은 평가 세트라 학습에
쓰면 그 라벨로 다시 잴 수 없다.

베이스 모델은 `models/kcelectra-base`(`beomi/KcELECTRA-base`). 댓글 코퍼스로 학습돼
**STT 오탈자에 강한 것**이 선정 이유다(`decisions/010`).

`torch`·`transformers` 는 **함수 안에서 import** 한다. CI 는 이 둘을 설치하지 않는데
(수 GB), 모듈을 import 하는 것만으로 실패하면 이 파일을 건드릴 때마다 CI 가 빨개진다.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from training.adapter.outbound.aihub_minwon_loader import Sample
from training.domain.services.domain_labels import LABEL_ORDER, label_to_index

# 상한이지 패딩 길이가 아니다 — 아래 `_collate` 가 **배치 안의 가장 긴 것**에 맞춰 패딩한다.
#
# 2026-08-27 실측: 단일 턴은 중앙 8 · p95 18, 초반 턴을 이어 붙인 증강까지 합치면
# 중앙 11 · p95 36 · 최대 110. 64 면 p95 를 넉넉히 덮는다.
#
# 처음에 128 **고정 패딩**으로 잡았다가 학습이 기어갔다 — 중앙값이 8인데 128 로 채우면
# **연산의 94%가 패딩**이다. 짧은 발화를 다루면서 관성으로 큰 값을 쓰면 조용히 16배를 태운다.
# 고정 패딩을 동적 패딩으로 바꾼 것이 그 교훈의 나머지 절반이다.
MAX_LENGTH = 64


def _log(*args, flush: bool = True, **kw) -> None:
    """기본 로거. **항상 flush 한다** — 파이프로 받으면 버퍼링돼 진행 상황이 안 보인다."""
    print(*args, flush=flush, **kw)


@dataclass(frozen=True)
class TrainConfig:
    base_model: str = "models/kcelectra-base"
    output_dir: str = "models/domain-classifier"
    epochs: int = 4
    batch_size: int = 64
    learning_rate: float = 2e-5
    warmup_ratio: float = 0.1
    max_length: int = MAX_LENGTH
    seed: int = 42


def pick_device() -> str:
    """M5 에는 CUDA 가 없다(V2 확인). MPS 가 있으면 쓰고, 없으면 CPU."""
    import torch

    if torch.backends.mps.is_available():
        return "mps"
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


class _Dataset:
    """토큰화만 해 두고 패딩은 배치를 만들 때 한다 — 짧은 발화가 대부분이라 이게 훨씬 싸다."""

    def __init__(self, tokenizer, samples: list[Sample], max_length: int):
        self._enc = tokenizer(
            [s.text for s in samples], truncation=True, max_length=max_length
        )["input_ids"]
        self._labels = [label_to_index(s.domain) for s in samples]

    def __len__(self) -> int:
        return len(self._labels)

    def __getitem__(self, i):
        return self._enc[i], self._labels[i]


def _collate(batch, pad_id: int):
    """배치 안에서 가장 긴 것에 맞춰 패딩한다. 고정 길이로 채우면 대부분이 패딩 연산이 된다."""
    import torch

    width = max(len(ids) for ids, _ in batch)
    input_ids = torch.full((len(batch), width), pad_id, dtype=torch.long)
    attention = torch.zeros((len(batch), width), dtype=torch.long)
    for row, (ids, _) in enumerate(batch):
        input_ids[row, : len(ids)] = torch.tensor(ids, dtype=torch.long)
        attention[row, : len(ids)] = 1
    return input_ids, attention, torch.tensor([label for _, label in batch], dtype=torch.long)


def evaluate(model, loader, device) -> dict:
    """검증 정확도 + 도메인별 정확도. 전체 정확도만 보면 큰 도메인에 가려진다."""
    import torch

    model.eval()
    correct = total = 0
    per_domain = {d: [0, 0] for d in LABEL_ORDER}
    with torch.no_grad():
        for ids, mask, labels in loader:
            ids, mask, labels = ids.to(device), mask.to(device), labels.to(device)
            pred = model(input_ids=ids, attention_mask=mask).logits.argmax(dim=-1)
            correct += (pred == labels).sum().item()
            total += labels.size(0)
            for p, l in zip(pred.tolist(), labels.tolist()):
                per_domain[LABEL_ORDER[l]][1] += 1
                if p == l:
                    per_domain[LABEL_ORDER[l]][0] += 1
    return {
        "accuracy": correct / total if total else float("nan"),
        "n": total,
        "per_domain": {d: (c / n if n else float("nan")) for d, (c, n) in per_domain.items()},
    }


def train(train_set: list[Sample], val_set: list[Sample], cfg: TrainConfig, *, log=_log) -> dict:
    """파인튜닝하고 `cfg.output_dir` 에 저장한다. 검증 지표를 돌려준다.

    **검증 세트는 AI Hub 안에서 나눈 것**이다. 골든셋 정확도는 이것과 별개로
    `scripts/run_eval.py` 가 잰다 — 데이터 출처가 다르니 값도 다르게 나오는 게 정상이다.
    """
    import torch
    from torch.optim import AdamW
    from torch.utils.data import DataLoader
    from transformers import AutoModelForSequenceClassification, AutoTokenizer, get_linear_schedule_with_warmup

    torch.manual_seed(cfg.seed)
    device = pick_device()
    log(f"장치: {device} · 베이스: {cfg.base_model}")

    tokenizer = AutoTokenizer.from_pretrained(cfg.base_model)
    model = AutoModelForSequenceClassification.from_pretrained(
        cfg.base_model,
        num_labels=len(LABEL_ORDER),
        id2label={i: d for i, d in enumerate(LABEL_ORDER)},
        label2id={d: i for i, d in enumerate(LABEL_ORDER)},
    ).to(device)

    pad_id = tokenizer.pad_token_id
    collate = lambda b: _collate(b, pad_id)  # noqa: E731
    train_loader = DataLoader(
        _Dataset(tokenizer, train_set, cfg.max_length),
        batch_size=cfg.batch_size, shuffle=True, collate_fn=collate,
    )
    val_loader = DataLoader(
        _Dataset(tokenizer, val_set, cfg.max_length), batch_size=cfg.batch_size, collate_fn=collate
    )

    steps = len(train_loader) * cfg.epochs
    optimizer = AdamW(model.parameters(), lr=cfg.learning_rate)
    scheduler = get_linear_schedule_with_warmup(optimizer, int(steps * cfg.warmup_ratio), steps)

    log(f"학습 {len(train_set)}건 · 검증 {len(val_set)}건 · {cfg.epochs} epoch · {steps} step")
    best: dict = {"accuracy": -1.0}
    for epoch in range(1, cfg.epochs + 1):
        model.train()
        running = 0.0
        for i, (ids, mask, labels) in enumerate(train_loader, start=1):
            ids, mask, labels = ids.to(device), mask.to(device), labels.to(device)
            loss = model(input_ids=ids, attention_mask=mask, labels=labels).loss
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            scheduler.step()
            optimizer.zero_grad()
            running += loss.item()
            if i % 50 == 0:
                log(f"  epoch {epoch} step {i}/{len(train_loader)} loss {running / i:.4f}", flush=True)

        metrics = evaluate(model, val_loader, device)
        log(f"  epoch {epoch} 검증 정확도 {metrics['accuracy']:.4f} · 도메인별 "
            + " ".join(f"{d} {v:.3f}" for d, v in metrics["per_domain"].items()))

        # 마지막 epoch 이 항상 최선은 아니다. 검증 정확도가 가장 높은 것만 남긴다.
        if metrics["accuracy"] > best["accuracy"]:
            best = metrics
            out = Path(cfg.output_dir)
            out.mkdir(parents=True, exist_ok=True)
            model.save_pretrained(out)
            tokenizer.save_pretrained(out)
            (out / "training_meta.json").write_text(
                json.dumps(
                    {"config": asdict(cfg), "epoch": epoch, "labels": list(LABEL_ORDER), **metrics},
                    ensure_ascii=False, indent=2,
                ) + "\n",
                encoding="utf-8",
            )
            log(f"  저장: {out} (epoch {epoch})")
    return best
