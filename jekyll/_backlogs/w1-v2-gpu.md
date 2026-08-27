---
title: "V2 — GPU 가용 여부 확인"
assignee: "류준"
role: "ai"
status: "done"
sprint: 1
priority: 3
date: 2026-08-25
requirement:
  - "B-4"
---

**결과: Apple M5 MacBook Air 24GB 통합메모리, CUDA 없음(MPS 가속).**

소형 모델(`polyglot-ko-1.3b` 등)로 대응하며 오픈소스 모델 4종 다운로드 완료.
첫 토큰 500ms를 못 맞추면 생성 없이 검색 스니펫만 표시하는 폴백 모드로 전환한다.
