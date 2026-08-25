"""V3 — Google STT 한국어 숫자 출력 형태 테스트.

AI Hub 라벨은 (표기)/(발음) 이중 표기를 쓴다. 예: "(8673)/(팔 육 칠 삼)"은
실제 발화가 "팔육칠삼"(자릿수 낭독)이고 표준 표기가 "8673"이라는 뜻이다.
Google STT가 이런 발화를 아라비아 숫자로 정규화해서 돌려주는지, 한글 발음
그대로 돌려주는지를 실제 오디오로 확인한다.

- 자릿수 낭독형(인증코드류): "코드 팔육칠삼" → STT가 "8673"으로 정규화하는지
- 단위 낭독형(금액류): "마이너스 천" → STT가 "1000" / "마이너스 1000"으로
  정규화하는지, 아니면 "천"을 그대로 남기는지

키 파일 내용은 읽지 않는다 (GOOGLE_APPLICATION_CREDENTIALS 경로만 사용).

실행:
    .venv/bin/python scripts/test_stt_v3.py
"""

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

CASES = [
    {
        "name": "자릿수 낭독형 (인증/에러 코드)",
        "wav": "data/raw/aihub-lowquality-phone/validation/wav/D04/J16/S006963/0002.wav",
        "label": "o/ 서버 오류가 발생했습니다. 잠시 후 재시도해 주세요. 코드 (8673)/(팔 육 칠 삼) 계속 뜨는데요.",
        "ground_truth_digits": "8673",
    },
    {
        "name": "단위 낭독형 (금액, 마이너스 포함)",
        "wav": "data/raw/aihub-lowquality-phone/validation/wav/D04/J16/S006999/0004.wav",
        "label": "마이너스 (1000)/(천)이라고 뜨거든요. 일시적인 오류가 발생하였습니다. 이렇게요.",
        "ground_truth_digits": "1000 (또는 -1000)",
    },
    {
        "name": "단위 낭독형 (금액, 원 단위)",
        "wav": "data/raw/aihub-ktelspeech/validation/wav/D62/J93/S00009996/0004.wav",
        "label": "하루 만에 금액이 (5000원)/(오천 원) 빠져나갔다고 하셨잖아요.",
        "ground_truth_digits": "5000원",
    },
]


def load_env(path: Path) -> dict:
    env = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        env[key.strip()] = value.strip()
    return env


def main() -> int:
    env = load_env(REPO_ROOT / ".env")
    cred_path = env.get("GOOGLE_APPLICATION_CREDENTIALS", "")
    project = env.get("GOOGLE_CLOUD_PROJECT", "")

    if not cred_path or not project or not Path(cred_path).exists():
        print("실패: .env의 GOOGLE_APPLICATION_CREDENTIALS/GOOGLE_CLOUD_PROJECT 확인 필요")
        return 1

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path
    os.environ["GOOGLE_CLOUD_PROJECT"] = project

    try:
        from google.cloud import speech
    except ImportError:
        print("실패: google-cloud-speech 미설치")
        return 1

    client = speech.SpeechClient()

    print("=" * 70)
    print("V3 — Google STT 한국어 숫자 출력 형태 테스트")
    print("=" * 70)

    for case in CASES:
        wav_path = REPO_ROOT / case["wav"]
        print(f"\n[{case['name']}]")
        print(f"  라벨(정답, AI Hub): {case['label']}")
        print(f"  숫자 정답: {case['ground_truth_digits']}")

        if not wav_path.exists():
            print(f"  실패: 오디오 없음 — {wav_path}")
            continue

        with open(wav_path, "rb") as f:
            audio_content = f.read()

        audio = speech.RecognitionAudio(content=audio_content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=8000,
            language_code="ko-KR",
        )
        try:
            response = client.recognize(config=config, audio=audio)
        except Exception as e:  # noqa: BLE001
            print(f"  실패: STT 요청 오류 — {type(e).__name__}: {e}")
            continue

        if not response.results:
            print("  결과 없음 (무음/인식 실패)")
            continue

        for result in response.results:
            alt = result.alternatives[0]
            print(f"  STT 출력: {alt.transcript!r} (신뢰도 {alt.confidence:.2f})")

    print("\n" + "=" * 70)
    print("완료 — 위 STT 출력에서 숫자가 아라비아 숫자로 나오는지, 한글 그대로 나오는지 눈으로 비교할 것.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
