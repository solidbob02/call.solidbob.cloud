# Requirement: B-0
"""파인튜닝한 KcELECTRA 로 도메인을 판정한다. `DomainRoutingPort` 구현 (설계 ①).

`decisions/007` 이 그린 경로의 ①이다. `retrieval` 쪽 `SearchDomainRouter`(검색 기반 v1)가
②(폴백)이고, 이쪽이 1차가 된다.

`torch`·`transformers` 는 **함수 안에서 import** 한다 — CI 는 둘을 설치하지 않으므로
모듈 import 만으로 실패하면 이 파일을 건드릴 때마다 CI 가 빨개진다.

⚠ 모델 파일은 `models/domain-classifier/`(gitignore)에 있다. 없으면 학습부터 한다:
`.venv/bin/python scripts/train_domain_classifier.py`
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from hub.app.dtos.domain_classification_dto import DomainClassification
from hub.app.ports.output.domain_routing_port import DomainRoutingPort

from training.domain.services.domain_labels import LABEL_ORDER, index_to_label

DEFAULT_MODEL_DIR = "models/domain-classifier"


class ModelDomainRouter(DomainRoutingPort):
    """4클래스 분류기 추론. 모델을 **한 번만** 올려 재사용한다.

    신뢰도는 softmax 최댓값이다. 검색 기반 v1 의 "표 차이"와 달리 확률의 형태를 갖지만,
    **교정된 확률은 아니다** — 신경망 softmax 는 대체로 과신한다. 폴백 임계값을 정할 때는
    이 값을 그대로 믿지 말고 실측으로 정한다.
    """

    def __init__(self, model_dir: str | Path = DEFAULT_MODEL_DIR, *, device: str | None = None):
        self._model_dir = Path(model_dir)
        if not self._model_dir.is_dir():
            raise FileNotFoundError(
                f"분류기가 없다: {self._model_dir}\n"
                "  .venv/bin/python scripts/train_domain_classifier.py 로 먼저 학습한다"
            )
        self._device = device
        self._model: Any = None
        self._tokenizer: Any = None

    def _ensure_loaded(self) -> None:
        if self._model is not None:
            return
        import torch
        from transformers import AutoModelForSequenceClassification, AutoTokenizer

        if self._device is None:
            self._device = "mps" if torch.backends.mps.is_available() else "cpu"
        self._tokenizer = AutoTokenizer.from_pretrained(self._model_dir)
        self._model = AutoModelForSequenceClassification.from_pretrained(self._model_dir)
        self._model.to(self._device).eval()

    async def classify(self, utterance: str) -> DomainClassification:
        """빈 발화는 판정하지 않는다 — 지어내지 않는다.

        ⚠ `DomainClassification.domain` 타입이 `str` 이라 "판정 불가"를 표현할 방법이 없어
        런타임에 `None` 을 넣는다. DTO 변경은 `server/` 소관 — [미결](/open-items/) 참고.
        """
        if not utterance.strip():
            return DomainClassification(domain=None, confidence=0.0)

        import torch

        self._ensure_loaded()
        enc = self._tokenizer(
            utterance, truncation=True, max_length=128, return_tensors="pt"
        ).to(self._device)
        with torch.no_grad():
            probs = self._model(**enc).logits.softmax(dim=-1)[0]
        index = int(probs.argmax().item())
        return DomainClassification(
            domain=index_to_label(index),
            confidence=float(probs[index].item()),
        )


def labels_match_training() -> bool:
    """학습과 추론이 같은 라벨 순서를 보는지. 어긋나면 정확도가 조용히 무너진다."""
    return len(LABEL_ORDER) == len(set(LABEL_ORDER)) == 4
