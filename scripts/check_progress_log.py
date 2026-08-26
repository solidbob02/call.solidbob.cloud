#!/usr/bin/env python3
# Requirement: QUA-2 (기록 추적성)
"""커밋이 있는 날짜에 진행 기록 항목이 있는지 확인한다.

왜 필요한가
    CLAUDE.md 의 규칙 중 지켜진 것들은 전부 "어기면 즉시 드러나는" 것이었다.
    자격증명을 커밋하면 사고가 나고, 한글 파일명을 쓰면 링크가 깨져 CI 가 잡는다.
    진행 기록만 어겨도 아무 일이 일어나지 않아서, 08-25~08-26 이틀간 PM 세션 기록이
    한 건도 남지 않았다(같은 기간 다른 팀원은 5건 남겼다). 사람 의지에 기대는 대신
    확인 장치를 붙인다.

왜 실패시키지 않는가
    로그 누락은 코드 결함이 아니다. 이걸로 CI 를 빨갛게 만들면 코드 머지까지 막히고,
    급할 때 "일단 아무 줄이나 적고 통과시키는" 회피가 생긴다. 그러면 기록의 질이
    오히려 나빠진다. 그래서 exit code 는 항상 0 이고, 눈에 띄는 경고만 낸다.

사용법
    python3 scripts/check_progress_log.py            # 최근 7일
    python3 scripts/check_progress_log.py --days 14
    python3 scripts/check_progress_log.py --strict   # 누락 시 exit 1 (로컬 확인용)
"""

import argparse
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

PROGRESS = Path(__file__).resolve().parent.parent / "jekyll" / "progress.markdown"
DATE_HEADING = re.compile(r"^###\s+(\d{4}-\d{2}-\d{2})")

# 기록할 내용이 없는 커밋 — 이것만 있는 날은 경고하지 않는다
IGNORED_SUBJECT = re.compile(r"^(Merge |merge:|Revert )")


def logged_dates() -> set[str]:
    if not PROGRESS.exists():
        return set()
    text = PROGRESS.read_text(encoding="utf-8")
    return {m.group(1) for line in text.splitlines() if (m := DATE_HEADING.match(line))}


def commit_dates(days: int) -> dict[str, list[tuple[str, str]]]:
    """날짜 -> [(작성자, 제목)]. 병합 커밋만 있는 날은 제외한다."""
    out = subprocess.run(
        ["git", "log", f"--since={days} days ago", "--date=short",
         "--pretty=format:%ad\t%an\t%s"],
        capture_output=True, text=True, check=True,
    ).stdout

    by_date: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for line in out.splitlines():
        if not line.strip():
            continue
        date, author, subject = line.split("\t", 2)
        if IGNORED_SUBJECT.match(subject):
            continue
        by_date[date].append((author, subject))
    return by_date


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--strict", action="store_true",
                    help="누락이 있으면 exit 1 (기본은 경고만)")
    args = ap.parse_args()

    logged = logged_dates()
    commits = commit_dates(args.days)
    missing = {d: c for d, c in commits.items() if d not in logged}

    print(f"검사 범위: 최근 {args.days}일 · 커밋이 있는 날 {len(commits)}일 "
          f"· 로그 항목이 있는 날 {len(commits) - len(missing)}일")

    if not missing:
        print("진행 기록 누락: 없음")
        return 0

    print(f"\n⚠ 진행 기록이 없는 날 {len(missing)}일 — jekyll/progress.markdown 에 항목을 남겨 주세요")
    for date in sorted(missing, reverse=True):
        entries = missing[date]
        authors = ", ".join(sorted({a for a, _ in entries}))
        print(f"\n  {date}  커밋 {len(entries)}건 ({authors})")
        for _, subject in entries[:4]:
            print(f"    - {subject[:88]}")
        if len(entries) > 4:
            print(f"    … 외 {len(entries) - 4}건")

    print("\n형식:  ### YYYY-MM-DD  아래에 '무엇을 했는지' 와 '남은 것' 을 적습니다 (최신이 맨 위)")
    return 1 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
