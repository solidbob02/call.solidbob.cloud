"""Google Cloud Speech-to-Text 연결 테스트 — 실제로 짧은 오디오 하나를 보내서
전사가 돌아오는지 확인한다. 키 파일 내용은 이 스크립트도, 실행한 사람도 읽지 않는다
(GOOGLE_APPLICATION_CREDENTIALS 경로만 라이브러리에 넘겨준다).

비용: 약 0.9초짜리 오디오 1건 = 사실상 무료 크레딧/최소 과금 단위 안에서 끝난다.

실행:
    .venv/bin/python scripts/test_stt.py
"""

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


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

    if not cred_path or not project:
        print("실패: .env에 GOOGLE_APPLICATION_CREDENTIALS 또는 GOOGLE_CLOUD_PROJECT가 비어있다.")
        return 1
    if not Path(cred_path).exists():
        print(f"실패: 키 파일을 못 찾음 — {cred_path}")
        return 1

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path
    os.environ["GOOGLE_CLOUD_PROJECT"] = project

    sample = REPO_ROOT / "data/raw/aihub-ktelspeech/validation/wav/D62/J93/S00007438/0016.wav"
    if not sample.exists():
        print(f"실패: 테스트용 오디오 샘플이 없음 — {sample}")
        return 1

    print(f"프로젝트: {project}")
    print(f"키 파일: {cred_path} (내용은 읽지 않음, 경로만 사용)")
    print(f"테스트 오디오: {sample.name} (약 0.9초, 8kHz mono)")
    print("Google STT에 요청 중...")

    try:
        from google.cloud import speech
    except ImportError:
        print("실패: google-cloud-speech가 설치되지 않음 (pip install google-cloud-speech)")
        return 1

    try:
        client = speech.SpeechClient()
        with open(sample, "rb") as f:
            audio_content = f.read()

        audio = speech.RecognitionAudio(content=audio_content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=8000,
            language_code="ko-KR",
        )
        response = client.recognize(config=config, audio=audio)
    except Exception as e:  # noqa: BLE001
        print(f"실패: STT 요청 중 오류 — {type(e).__name__}: {e}")
        return 1

    if not response.results:
        print("응답은 왔지만 인식된 텍스트가 없음 (오디오가 너무 짧거나 무음일 수 있음).")
        print("그래도 인증·연결 자체는 성공 — 키가 정상 동작한다는 뜻이다.")
        return 0

    print("\n성공! 인증·연결·STT 전부 정상 동작한다.")
    for result in response.results:
        alt = result.alternatives[0]
        print(f"  전사 결과: {alt.transcript!r} (신뢰도 {alt.confidence:.2f})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
