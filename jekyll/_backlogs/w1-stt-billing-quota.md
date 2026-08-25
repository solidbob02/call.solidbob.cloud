---
title: "STT 결제 계정 · 키 발급 · 비용 방어선 설정"
assignee: "정성윤"
role: "infra"
status: "done"
sprint: 1
priority: 3
date: 2026-08-25
---

V3·V4 실측의 전제였다. 결제 계정이 열려야 STT 를 호출할 수 있다.

## 설정 내역

| 항목 | 값 |
|---|---|
| 프로젝트 | `callguard-506606` |
| 서비스 계정 | `callguard-stt@callguard-506606.iam.gserviceaccount.com` |
| 키 파일 | `~/.gcp/callguard-stt.json` (권한 600, 저장소 밖) |
| 환경변수 | `.env` 에 경로만 기입 (`.gitignore` 로 커밋 차단) |
| 크레딧 | ₩435,523 (100% 미사용), 유효기간 **~2026-11-24** |
| 연결 확인 | 서비스 계정 키로 토큰 발급 → `speech.googleapis.com/v1/operations` **200** |

## 비용 방어선

| 층 | 설정 | 실제 차단 |
|---|---|---|
| 1 | 할당량 `Audio seconds per day` 1,728,000 → **600** | ✅ |
| 2 | 할당량 `Concurrent StreamingRecognize sessions (global endpoint)` → **5** | ✅ |
| 3 | 예산 `callguard` — 월 ₩30,000, 임계값 50/90/100% | ⚠ 알림만 (반영 24시간 지연) |

하루 600초로 묶은 이유: STT 무료 한도가 월 3600초(60분)라, 하루 상한을 600초로 두면
**하루 실수로 한 달치를 소진하는 일이 구조적으로 불가능**하다.

## 설정하면서 확인한 함정

- **예산 생성 시 "절감(크레딧)" 체크박스는 해제해야 한다.** 켜두면 크레딧을 뺀 금액으로 산정되어
  크레딧으로 결제되는 동안 비용이 0원으로 잡히고 **알림이 오지 않는다**
- **지출 한도(spending limit) 기능은 STT 에 걸 수 없다.** Cloud Run·Cloud Run Functions·
  Gemini API·Vertex AI 네 서비스만 지원한다. 실제 차단은 할당량이 맡는다
- **지역 엔드포인트로 바꾸면 위 할당량이 적용되지 않는다.** 현재는 글로벌 엔드포인트
  (`speech.googleapis.com`) 기준. 지연을 줄이려 `asia-northeast3`(서울) 등으로 옮기면 다시 낮춰야 한다
- 유료 계정으로 업그레이드된 상태라 **크레딧 소진 시 자동 정지가 없다.** 카드로 청구된다

## 남은 것

**프로젝트 종료(10-27) 후 정리** — 크레딧 유효기간이 11-24 라, 종료 뒤 리소스를 켜둔 채 두면
만료 시점부터 카드로 청구된다. 프로젝트 삭제 또는 결제 연결 해제. → [미결 항목](/open-items/)
