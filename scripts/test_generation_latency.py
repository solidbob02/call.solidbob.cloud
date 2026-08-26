"""V5 — 카드 요약 생성(B-4) 레이턴시 실측: polyglot-ko-1.3b, Apple M5 MPS.

[4.3절 레이턴시 예산]의 "생성 첫 토큰 500ms" 목표를 실제 다운로드한 모델
(models/polyglot-ko-1.3b, scripts/download_models.py)로 검증한다. GPU가 없는
환경([V2] 확인 완료, MPS 백엔드)에서 이 소형 모델이 그 예산 안에 들어오는지가
관건이다.

측정 대상:
  - 모델 로드 시간 (1회성, 예산에는 안 들어가지만 참고용)
  - 첫 토큰까지 걸린 시간 (TTFT) — 예산 500ms
  - 전체 생성 시간 / 토큰당 평균 시간 (tok/s)

입력은 지식베이스 실제 조항(FIN-TERM-2.2, 부정사용 보상 기준)을 요약하는
B-4 시나리오를 그대로 흉내낸 프롬프트다 — 임의 문장이 아니라 실제 카드 생성에
쓰일 형태의 입력.

실행:
    .venv/bin/python scripts/test_generation_latency.py
"""

from __future__ import annotations

import time

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_DIR = "models/polyglot-ko-1.3b"

# FIN-TERM-2.2 (부정사용 보상 기준) 원문 그대로 — knowledge-base/finance/terms/TERM.md
SOURCE_TEXT = (
    "1. 신고 접수 이전 부정사용액은 이용자의 고의·중과실이 없는 한 회사가 보상한다. "
    "2. 비밀번호를 타인에게 알려준 경우 등 이용자 귀책이 확인되면 보상이 제한될 수 있다. "
    "3. 보상 여부는 사고 경위 조사 후 확정되며, 조사 전 보상을 확정적으로 안내하지 않는다."
)
PROMPT = f"다음 약관 조항을 상담원이 고객에게 읽어줄 수 있도록 2~3문장으로 요약해줘.\n\n조항: {SOURCE_TEXT}\n\n요약:"

MAX_NEW_TOKENS = 250


def main() -> None:
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"device: {device}")
    print(f"torch: {torch.__version__}")

    t0 = time.perf_counter()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForCausalLM.from_pretrained(MODEL_DIR, torch_dtype=torch.float16)
    model.to(device)
    model.eval()
    load_s = time.perf_counter() - t0
    print(f"모델 로드: {load_s:.2f}s (dtype=float16)")

    inputs = tokenizer(PROMPT, return_tensors="pt").to(device)
    prompt_tokens = inputs["input_ids"].shape[1]
    print(f"프롬프트 토큰 수: {prompt_tokens}")

    # 첫 토큰까지 걸린 시간(TTFT) 측정 — max_new_tokens=1로 별도 실행
    t0 = time.perf_counter()
    with torch.no_grad():
        _ = model.generate(
            **inputs, max_new_tokens=1, do_sample=False, pad_token_id=tokenizer.eos_token_id
        )
    if device == "mps":
        torch.mps.synchronize()
    ttft_s = time.perf_counter() - t0
    print(f"\n첫 토큰까지(TTFT): {ttft_s * 1000:.0f}ms  (목표: 500ms — 4.3절)")

    # 전체 생성 시간 측정 — MAX_NEW_TOKENS개
    t0 = time.perf_counter()
    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )
    if device == "mps":
        torch.mps.synchronize()
    total_s = time.perf_counter() - t0

    generated_tokens = output.shape[1] - prompt_tokens
    tok_per_s = generated_tokens / total_s if total_s > 0 else float("nan")

    generated_text = tokenizer.decode(output[0][prompt_tokens:], skip_special_tokens=True)

    print(f"전체 생성 시간: {total_s:.2f}s ({generated_tokens} 토큰, {tok_per_s:.1f} tok/s)")
    print(f"\n--- 생성 결과 ---\n{generated_text}\n-----------------")


if __name__ == "__main__":
    main()
