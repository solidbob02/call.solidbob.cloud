"""V5-b — Ollama 서빙 후보 모델 레이턴시 실측 (같은 프롬프트, 같은 250토큰 기준).

scripts/test_generation_latency.py(HF Transformers, polyglot-ko-1.3b)가 250토큰에
7.6~7.7초로 목표(3~5초)를 못 맞춰서, Ollama(llama.cpp/GGUF) 서빙으로 후보를
바꿔 같은 방식으로 재측정한다. 같은 프롬프트를 써야 비교가 성립한다.

실행:
    python3 scripts/test_ollama_latency.py <model> [<model2> ...]
    (인자 없으면 로컬에 이미 받아둔 후보 전부 테스트)
"""

from __future__ import annotations

import json
import sys
import time

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

SOURCE_TEXT = (
    "1. 신고 접수 이전 부정사용액은 이용자의 고의·중과실이 없는 한 회사가 보상한다. "
    "2. 비밀번호를 타인에게 알려준 경우 등 이용자 귀책이 확인되면 보상이 제한될 수 있다. "
    "3. 보상 여부는 사고 경위 조사 후 확정되며, 조사 전 보상을 확정적으로 안내하지 않는다."
)
PROMPT = f"다음 약관 조항을 상담원이 고객에게 읽어줄 수 있도록 2~3문장으로 요약해줘.\n\n조항: {SOURCE_TEXT}\n\n요약:"

NUM_PREDICT = 250


def run_once(model: str) -> dict:
    t0 = time.perf_counter()
    resp = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "prompt": PROMPT,
            "stream": True,
            "options": {"num_predict": NUM_PREDICT, "temperature": 0},
        },
        stream=True,
        timeout=120,
    )
    first_token_s = None
    tokens = 0
    text_parts = []
    final = None
    for line in resp.iter_lines():
        if not line:
            continue
        chunk = json.loads(line)
        if chunk.get("response"):
            if first_token_s is None:
                first_token_s = time.perf_counter() - t0
            tokens += 1
            text_parts.append(chunk["response"])
        if chunk.get("done"):
            final = chunk
            break
    total_s = time.perf_counter() - t0
    return {
        "model": model,
        "ttft_ms": (first_token_s or 0) * 1000,
        "total_s": total_s,
        "tokens": final.get("eval_count", tokens) if final else tokens,
        "eval_duration_s": (final.get("eval_duration", 0) / 1e9) if final else None,
        "text": "".join(text_parts),
    }


def main() -> None:
    models = sys.argv[1:] or ["qwen2.5:1.5b-instruct", "qwen3:4b", "qwen3:8b"]
    for model in models:
        print(f"\n=== {model} ===")
        try:
            r = run_once(model)
        except Exception as e:  # noqa: BLE001
            print(f"  실패: {e}")
            continue
        tok_s = r["tokens"] / r["eval_duration_s"] if r["eval_duration_s"] else float("nan")
        print(f"  TTFT: {r['ttft_ms']:.0f}ms")
        print(f"  전체: {r['total_s']:.2f}s ({r['tokens']} 토큰, eval_duration={r['eval_duration_s']:.2f}s, {tok_s:.1f} tok/s)")
        print(f"  결과: {r['text'][:200]}")


if __name__ == "__main__":
    main()
