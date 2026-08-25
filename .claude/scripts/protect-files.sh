#!/usr/bin/env bash
# PreToolUse 훅 — 자격증명 파일 편집 차단
# CLAUDE.md 2절(절대 원칙)·7절(공개/비공개 경계): 키는 .env 로 관리하고 저장소에 커밋하지 않는다.
# 종료 코드 2 = 작업 차단 + stderr 메시지를 Claude 에게 전달.

INPUT=$(cat)

# jq 대신 python3 사용 (이 환경에 jq 미설치)
FILE_PATH=$(printf '%s' "$INPUT" | python3 -c '
import sys, json
try:
    d = json.load(sys.stdin).get("tool_input", {}) or {}
except Exception:
    d = {}
print(d.get("file_path") or d.get("path") or "")
' 2>/dev/null)

[ -z "$FILE_PATH" ] && exit 0

case "$(basename "$FILE_PATH")" in
  .env|.env.*|*.key|*.pem|*.p12|*.pfx|secrets.*|*credential*.json|*service-account*.json|id_rsa|id_ed25519)
    echo "보안 정책: '$FILE_PATH' 는 자격증명 파일이라 수정할 수 없습니다." >&2
    echo "키는 .env(gitignore)로 관리하고 저장소에 커밋하지 않는다 — CLAUDE.md 7절." >&2
    exit 2
    ;;
esac

exit 0
