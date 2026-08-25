---
layout: page
title: 인터페이스 계약
nav_order: 92
updated: 2026-08-25
owner: 류준
status: draft
---

> **status: draft** — 1주차 안에 3인 합의를 거쳐 `agreed`로 올린다.
> 이 문서가 확정되어야 세 담당이 병렬로 움직일 수 있다.
> `agreed` 이후의 변경은 `_project/decisions/`에 결정 기록을 남긴다.

## 1. 전사 이벤트 (STT → 코어 / 게이트웨이 → 브라우저)

**마스킹 적용 후**의 형태만 전달·저장한다. 원본은 보관하지 않는다.

```json
{
  "call_id": "c_001",
  "speaker": "customer",
  "text": "카드번호는 **** 입니다",
  "masked": [{"type": "P2", "span": [7, 11]}],
  "is_final": true,
  "utterance_end_ms": 3100
}
```

| 필드 | 타입 | 설명 |
|---|---|---|
| `call_id` | string | 통화 식별자 |
| `speaker` | `customer` \| `agent` | 화자 분리 결과 |
| `text` | string | **마스킹된** 부분/최종 전사 |
| `masked` | array | 마스킹 구간 — `type`은 P1~P7, `span`은 문자 오프셋 |
| `is_final` | bool | false = 중간 결과(갱신됨), true = 확정 |
| `utterance_end_ms` | int | **발화 종료 시각.** 트리거 채점의 기준점 |

`utterance_end_ms`가 없으면 트리거 적절 발동률을 채점할 수 없다. 골든셋 스펙에도 같은 필드가 들어간다.

## 2. 추천 카드 (코어 → 브라우저)

```json
{
  "call_id": "c_001",
  "trigger_at_ms": 3150,
  "mode": "generated",
  "cards": [
    {
      "title": "프로모션 할인 적용 시점 안내",
      "summary": "신규 가입 할인은 가입 다음 달 청구서부터 반영됩니다.",
      "source": {"doc": "요금제약관", "clause": "3.2"},
      "score": 0.87
    }
  ],
  "internal_latency_ms": 780,
  "e2e_latency_ms": 1240
}
```

- `mode`: `generated`(생성 모드) \| `snippet`(폴백 모드 — 검색 원문 스니펫). 폴백에서도 `source`는 필수다.
- `cards`가 빈 배열이면 화면에 **"관련 문서 없음"**을 표시한다. 근거 없이 지어내지 않는다.
- `source` 없는 카드는 표시하지 않는다 (출처 표시율 목표 100%).
- **레이턴시는 두 값을 모두 싣는다.** `internal_latency_ms`는 트리거 발동 → 응답 완료(목표 p95 ≤ 1,000ms), `e2e_latency_ms`는 발화 종료 → 표시(목표 미설정, 기록만).

## 3. 종결 판정 (F-2, 조건부)

```json
{
  "call_id": "c_001",
  "closure_type": "해지",
  "reason": "고지 완료",
  "evidence": {"위약금_안내": true, "잔여할부_안내": false, "고객확인_기록": false},
  "verdict": "blocked",
  "missing": ["잔여할부_안내", "고객확인_기록"],
  "source": {"doc": "응대매뉴얼", "clause": "7장"}
}
```

- `verdict`: `passed` \| `blocked`. **판정은 규칙이 한다.** LLM은 판정 사유를 사람이 읽을 문장으로 옮기는 역할만 맡는다.
- `source`는 판정 근거가 된 규정의 출처다. 게이트가 무엇을 보고 막았는지 상담원이 확인할 수 있어야 한다.

## 4. 컴플라이언스 경고 (코어 → 브라우저)

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
- 폴백 모드 전환을 서버가 판단할지 설정으로 고정할지 (V2 결과에 따라)
