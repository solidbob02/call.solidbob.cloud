"""V4 — Google STT 스트리밍 부분 결과(interim result) 지연 테스트.

실시간 상담 화면처럼 오디오를 청크 단위로 "실시간 속도"에 맞춰 전송하면서,
각 interim/최종 결과가 스트림 시작 시점 대비 몇 ms 후에 도착하는지 측정한다.
단발성 recognize()가 아니라 streaming_recognize()를 써야 부분 결과 지연을
관찰할 수 있다.

키 파일 내용은 읽지 않는다 (GOOGLE_APPLICATION_CREDENTIALS 경로만 사용).

실행:
    .venv/bin/python scripts/test_stt_v4_streaming.py
"""

import os
import sys
import time
import wave
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# 약 20초짜리 실제 발화 — 부분 결과가 여러 번 나올 만큼 길다.
SAMPLE_WAV = "data/raw/aihub-ktelspeech/validation/wav/D62/J93/S00008764/0013.wav"

CHUNK_MS = 100  # 100ms 단위로 전송 (실시간 마이크 스트림과 유사한 페이싱)


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


def audio_chunks(wav_path: Path, chunk_ms: int):
    with wave.open(str(wav_path), "rb") as w:
        rate = w.getframerate()
        width = w.getsampwidth()
        channels = w.getnchannels()
        frames_per_chunk = int(rate * chunk_ms / 1000)
        while True:
            data = w.readframes(frames_per_chunk)
            if not data:
                break
            yield data
        return rate, width, channels


def get_wav_info(wav_path: Path):
    with wave.open(str(wav_path), "rb") as w:
        return w.getframerate(), w.getsampwidth(), w.getnchannels(), w.getnframes() / w.getframerate()


def main() -> int:
    env = load_env(REPO_ROOT / ".env")
    cred_path = env.get("GOOGLE_APPLICATION_CREDENTIALS", "")
    project = env.get("GOOGLE_CLOUD_PROJECT", "")

    if not cred_path or not project or not Path(cred_path).exists():
        print("실패: .env의 GOOGLE_APPLICATION_CREDENTIALS/GOOGLE_CLOUD_PROJECT 확인 필요")
        return 1

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path
    os.environ["GOOGLE_CLOUD_PROJECT"] = project

    wav_path = REPO_ROOT / SAMPLE_WAV
    if not wav_path.exists():
        print(f"실패: 오디오 없음 — {wav_path}")
        return 1

    rate, width, channels, dur = get_wav_info(wav_path)
    print("=" * 70)
    print("V4 — Google STT 스트리밍 부분 결과 지연 테스트")
    print("=" * 70)
    print(f"오디오: {wav_path.name} ({dur:.2f}s, {rate}Hz, {channels}ch, {width*8}bit)")
    print(f"청크 크기: {CHUNK_MS}ms (실시간 페이싱으로 전송)")

    try:
        from google.cloud import speech
    except ImportError:
        print("실패: google-cloud-speech 미설치")
        return 1

    client = speech.SpeechClient()

    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=rate,
        language_code="ko-KR",
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=True,
    )

    # 전체 오디오를 미리 청크로 쪼개둔다 (전송 자체는 실시간 페이싱으로).
    chunks = []
    with wave.open(str(wav_path), "rb") as w:
        frames_per_chunk = int(rate * CHUNK_MS / 1000)
        while True:
            data = w.readframes(frames_per_chunk)
            if not data:
                break
            chunks.append(data)

    stream_start = time.monotonic()
    sent_ms_marks = []  # 각 청크 전송 완료 시각 (스트림 시작 대비 ms)

    def request_generator():
        for i, chunk in enumerate(chunks):
            yield speech.StreamingRecognizeRequest(audio_content=chunk)
            sent_ms_marks.append((time.monotonic() - stream_start) * 1000)
            time.sleep(CHUNK_MS / 1000)

    print("\n스트리밍 전송 시작...\n")

    try:
        responses = client.streaming_recognize(
            config=streaming_config, requests=request_generator()
        )

        interim_count = 0
        first_interim_ms = None
        last_result_ms = None
        results_log = []

        for response in responses:
            now_ms = (time.monotonic() - stream_start) * 1000
            if not response.results:
                continue
            for result in response.results:
                transcript = result.alternatives[0].transcript if result.alternatives else ""
                is_final = result.is_final
                if not is_final:
                    interim_count += 1
                    if first_interim_ms is None:
                        first_interim_ms = now_ms
                results_log.append((now_ms, is_final, transcript))
                last_result_ms = now_ms
                tag = "FINAL" if is_final else "interim"
                print(f"  [{now_ms:7.0f}ms] ({tag:7s}) {transcript!r}")

    except Exception as e:  # noqa: BLE001
        print(f"실패: 스트리밍 요청 오류 — {type(e).__name__}: {e}")
        return 1

    total_sent_ms = sent_ms_marks[-1] if sent_ms_marks else 0

    print("\n" + "=" * 70)
    print("결과 요약")
    print("=" * 70)
    print(f"오디오 전송 완료 시각: {total_sent_ms:.0f}ms (오디오 길이 {dur*1000:.0f}ms)")
    print(f"첫 interim 결과 도착: {first_interim_ms:.0f}ms 후" if first_interim_ms else "첫 interim 결과: 없음")
    print(f"부분 결과 총 개수: {interim_count}건")
    if last_result_ms is not None:
        print(f"마지막 결과 도착: {last_result_ms:.0f}ms (전송 종료 대비 +{last_result_ms - total_sent_ms:.0f}ms)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
