# Requirement: E-4
"""리포트 출력. [평가 설계 6.2절 원칙 3·4]: 기준선 미달은 CI 실패로 처리하고, 절대
규칙(C-5, F-2) 위반은 평균값 뒤에 숨기지 않고 항상 따로 강조한다."""

from __future__ import annotations

from pathlib import Path


def print_report(report: dict, golden_set_path: Path) -> None:
    print(f"골든셋: {golden_set_path}")
    print("=" * 60)
    for section, result in report.items():
        print(f"\n[{section}]")
        if isinstance(result, str):
            print(f"  {result}")
            continue
        for key, value in result.items():
            print(f"  {key}: {value}")
        if result.get("absolute_rule_passed") is False:
            print("  ⛔ 절대 규칙 위반 — 평균으로 통과시키지 않는다 (6.2절 원칙 4)")
