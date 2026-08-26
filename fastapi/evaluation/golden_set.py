# Requirement: E-1
"""골든셋(JSON)을 로드해서 항목별 타입으로 돌려준다.

골든셋 자체는 이 저장소의 golden-set/v1-10.json이며, 스펙은 golden-set/README.md
(= 데이터 확보 계획 5.3절)와 동일하다. 이 모듈은 그 JSON을 채점 코드가 쓰기 편한
형태로만 파싱한다 — 정답을 스스로 만들어내지 않는다.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_GOLDEN_SET_PATH = (
    Path(__file__).resolve().parents[2] / "golden-set" / "v1-10.json"
)


@dataclass(frozen=True)
class ComplianceViolation:
    type: str
    phrase: str
    expected_alternative_source: str | None = None


@dataclass(frozen=True)
class PiiPattern:
    pattern: str  # P1~P7
    raw_span: str
    masked_expected: bool


@dataclass(frozen=True)
class F2Case:
    closure_type: str
    evidence: dict[str, bool]
    expected_verdict: str  # "approved" | "blocked"
    expected_missing: list[str]
    source: str | None = None


@dataclass(frozen=True)
class GoldenItem:
    id: str
    module: str
    customer_utterance: str | None = None
    agent_utterance: str | None = None
    utterance_end_ms: int | None = None
    trigger_examples: list[dict] = field(default_factory=list)
    expected_doc_ids: list[str] = field(default_factory=list)
    distractor_doc_ids: list[str] = field(default_factory=list)
    compliance_violation: ComplianceViolation | None = None
    pii_patterns: list[PiiPattern] = field(default_factory=list)
    f2_case: F2Case | None = None
    notes: str | None = None


def load_golden_set(path: Path | str = DEFAULT_GOLDEN_SET_PATH) -> list[GoldenItem]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    items: list[GoldenItem] = []
    for entry in raw["items"]:
        cv = entry.get("compliance_violation")
        f2 = entry.get("f2_case")
        items.append(
            GoldenItem(
                id=entry["id"],
                module=entry["module"],
                customer_utterance=entry.get("customer_utterance"),
                agent_utterance=entry.get("agent_utterance"),
                utterance_end_ms=entry.get("utterance_end_ms"),
                trigger_examples=entry.get("trigger_examples", []),
                expected_doc_ids=entry.get("expected_doc_ids", []),
                distractor_doc_ids=entry.get("distractor_doc_ids", []),
                compliance_violation=(
                    ComplianceViolation(**cv) if cv else None
                ),
                pii_patterns=[
                    PiiPattern(**p) for p in entry.get("pii_patterns", [])
                ],
                f2_case=(F2Case(**f2) if f2 else None),
                notes=entry.get("notes"),
            )
        )
    return items
