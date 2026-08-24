---
layout: page
title: 인터페이스 계약
nav_order: 92
updated: 2026-08-24
owner: core
status: draft
---

> **status: draft** — 1주차 안에 팀 합의를 거쳐 `agreed` 로 올린다.
> 이 문서가 확정되어야 5개 트랙이 병렬로 움직일 수 있다.
> `agreed` 이후의 변경은 `_project/decisions/` 에 결정 기록을 남긴다.

## 전사 이벤트 (STT → 코어 / 게이트웨이 → 브라우저)

```json
{
  "call_id": "c_001",
  "speaker": "customer",
  "text": "6개월 할인 된다고 했는데",
  "is_final": true,
  "timestamp_ms": 3100
}
```

| 필드 | 타입 | 설명 |
|---|---|---|
| `call_id` | string | 통화 식별자 |
| `speaker` | `customer` \| `agent` | 화자 분리 결과 |
| `text` | string | 부분 또는 최종 전사 |
| `is_final` | bool | false = 중간 결과(갱신됨), true = 확정 |
| `timestamp_ms` | int | 통화 시작 기준 경과 시간 |

## 추천 카드 (코어 → 브라우저)

```json
{
  "call_id": "c_001",
  "trigger_at_ms": 3150,
  "cards": [
    {
      "title": "프로모션 할인 적용 시점 안내",
      "summary": "신규 가입 할인은 가입 다음 달 청구서부터 반영됩니다.",
      "source": {"doc": "요금제약관", "clause": "3.2"},
      "score": 0.87
    }
  ],
  "latency_ms": 780
}
```

- `cards` 가 빈 배열이면 화면에 **"관련 문서 없음"** 을 표시한다. 근거 없이 지어내지 않는다.
- `source` 는 필수. 출처 없는 카드는 표시하지 않는다 (출처 표시율 목표 100%).
- `latency_ms` 는 트리거 발동 → 응답 완료. 평가 하네스가 이 값을 수집한다.

## 컴플라이언스 경고 (코어 → 브라우저)

```json
{
  "call_id": "c_001",
  "at_ms": 872000,
  "type": "absolute_guarantee",
  "matched_text": "무조건 환불됩니다",
  "severity": "high",
  "suggestion": "확인 후 안내드리겠습니다"
}
```

`type`: `absolute_guarantee` | `excessive_pii_request` | `missing_disclosure`

## 미확정 항목

- 오디오 청크 포맷과 크기 (브라우저 → 게이트웨이)
- 재연결 시 세션 복구 방식
- 카드 갱신 정책 — 새 카드로 교체할지 누적할지
