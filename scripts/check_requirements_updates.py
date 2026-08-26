"""requirements.txt에 고정된 패키지의 PyPI 최신 버전을 확인하고, 새 버전이 있으면
requirements.txt를 갱신한 뒤 이 저장소 전용 .venv에 pip install로 실제 반영한다.

launchd(매주 실행)로 무인 실행되므로, 실행 결과는 표준출력 대신 로그 파일에 남긴다.
수동으로도 실행 가능: .venv/bin/python scripts/check_requirements_updates.py
"""

import json
import re
import subprocess
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REQUIREMENTS = REPO_ROOT / "fastapi" / "requirements.txt"
VENV_PIP = REPO_ROOT / ".venv" / "bin" / "pip"
LOG_DIR = REPO_ROOT / "logs"
LOG_FILE = LOG_DIR / "requirements_check.log"

PIN_RE = re.compile(r"^([A-Za-z0-9_.\-]+)==([A-Za-z0-9_.\-]+)\s*$")


def log(msg: str) -> None:
    LOG_DIR.mkdir(exist_ok=True)
    line = f"[{datetime.now().isoformat(timespec='seconds')}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def latest_version(pkg: str) -> str | None:
    url = f"https://pypi.org/pypi/{pkg}/json"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.load(resp)
        return data["info"]["version"]
    except Exception as e:
        log(f"  {pkg}: PyPI 조회 실패 ({e}) — 건너뜀")
        return None


def main() -> None:
    if not REQUIREMENTS.exists():
        log("requirements.txt가 없습니다. 종료.")
        sys.exit(1)

    lines = REQUIREMENTS.read_text(encoding="utf-8").splitlines()
    updated_lines = []
    changes = []

    for line in lines:
        m = PIN_RE.match(line.strip())
        if not m:
            updated_lines.append(line)
            continue
        pkg, cur = m.group(1), m.group(2)
        latest = latest_version(pkg)
        if latest and latest != cur:
            log(f"  {pkg}: {cur} -> {latest} (업데이트 발견)")
            changes.append((pkg, cur, latest))
            updated_lines.append(f"{pkg}=={latest}")
        else:
            updated_lines.append(line)

    if not changes:
        log("모든 패키지가 최신 버전입니다. 변경 없음.")
        return

    REQUIREMENTS.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")
    log(f"requirements.txt 갱신 완료 — {len(changes)}건")

    if not VENV_PIP.exists():
        log(f".venv를 찾을 수 없습니다({VENV_PIP}) — 로컬 반영은 건너뜀. 직접 pip install -r requirements.txt 실행 필요.")
        return

    log(".venv에 반영 중 (pip install -r requirements.txt)...")
    result = subprocess.run(
        [str(VENV_PIP), "install", "-r", str(REQUIREMENTS)],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        log(".venv 반영 완료.")
    else:
        log(f".venv 반영 실패 (exit {result.returncode}):\n{result.stderr[-2000:]}")

    log("변경 요약: " + ", ".join(f"{p} {c}->{n}" for p, c, n in changes))


if __name__ == "__main__":
    main()
