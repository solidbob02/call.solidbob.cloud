---
title: "Python 의존성 고정 + 버전 자동 확인"
assignee: "류준"
role: "ai"
status: "done"
sprint: 1
priority: 16
date: 2026-08-25
---

모델 다운로드·실험용 Python 패키지를 `requirements.txt`로 고정하고, 버전이 뒤처지지 않도록 자동 확인
체계를 만들었다.

- `requirements.txt`: torch·transformers·huggingface_hub·sentencepiece·accelerate·pytest·google-cloud-speech
- `scripts/check_requirements_updates.py`: PyPI 최신 버전을 확인해 `requirements.txt`와 `.venv`를 갱신
- `~/Library/LaunchAgents/com.callguard.requirements-check.plist`: 매주 월요일 09:00 로컬 실행(맥북 로컬
  예약 작업 — 클라우드 RemoteTrigger는 로컬 `.venv`·파일에 접근할 수 없어 제외). 결과는
  `logs/requirements_check.log`
- `scripts/download_models.py`로 오픈소스 모델 4종(~8.9GB) 다운로드 완료 (V2 GPU 확인 결과에 따라
  소형 모델 위주로 선정 — [w1-v2-gpu 티켓](/kanban/) 참고)

기록: 세션 초반 작업이나 진행상황 로그 누락이 확인돼 [진행상황 (13)](/progress/)에 뒤늦게 기록.
