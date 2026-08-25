---
layout: page
title: 진행 상황
permalink: /progress/
---

{% assign m = site.data.milestones %}
{% assign mx = site.data.metrics %}

**{{ m.current_week }}주차 / 8주** · 착수 {{ m.start_date }} · 갱신 {{ m.updated }}

{% assign all_tasks = 0 %}{% assign done_tasks = 0 %}
{% for w in m.weeks %}{% for t in w.tasks %}{% assign all_tasks = all_tasks | plus: 1 %}{% if t.status == "done" %}{% assign done_tasks = done_tasks | plus: 1 %}{% endif %}{% endfor %}{% endfor %}

전체 {{ all_tasks }}개 항목 중 **{{ done_tasks }}개 완료**.

## 8주 체크리스트

{% for w in m.weeks %}
### {{ w.week }}주차 — {{ w.theme }}{% if w.week == m.current_week %} ← 현재{% endif %}

<ul>
{% for t in w.tasks %}
  <li>
    {% case t.status %}{% when "done" %}✅{% when "doing" %}🔵{% when "blocked" %}🔴{% when "dropped" %}⬜{% else %}⬜{% endcase %}
    {{ t.title }}
    {% if t.owner %}<em class="toc__status">{{ t.owner }}</em>{% endif %}
    {% if t.status != "todo" %}<code>{{ t.status }}</code>{% endif %}
    {% if t.note %}<br><small>{{ t.note }}</small>{% endif %}
  </li>
{% endfor %}
</ul>
{% endfor %}

## 지표 — 목표 대비 실측

측정하지 않은 값은 **미측정**으로 둔다. 예시 수치를 채워 넣지 않는다.
기준은 기획서 rev.4 6.1절 + 보완지시서. 베이스라인은 2주차 잠정(골든셋 50개) → 3주차 공식(150개) 두 단계다.

| 지표 | 목표 | 잠정 (2주차) | 공식 (3주차~) |
|---|---|---|---|
| Recall@5 (오류 0%) | ≥ {{ mx.targets.retrieval.recall_at_5_clean }} | {% if mx.measured.baseline_provisional.recall_at_5.value %}{{ mx.measured.baseline_provisional.recall_at_5.value }}{% else %}미측정{% endif %} | {% if mx.measured.baseline_official.recall_at_5.value %}{{ mx.measured.baseline_official.recall_at_5.value }}{% else %}미측정{% endif %} |
| MRR | ≥ {{ mx.targets.retrieval.mrr }} | {% if mx.measured.baseline_provisional.mrr.value %}{{ mx.measured.baseline_provisional.mrr.value }}{% else %}미측정{% endif %} | {% if mx.measured.baseline_official.mrr.value %}{{ mx.measured.baseline_official.mrr.value }}{% else %}미측정{% endif %} |

| 지표 | 목표 | 실측 |
|---|---|---|
| 트리거 적절 발동률 (0~{{ mx.targets.trigger.window_ms_max }}ms) | ≥ {{ mx.targets.trigger.fire_precision }} | {% if mx.measured.trigger.fire_precision.value %}{{ mx.measured.trigger.fire_precision.value }}{% else %}미측정{% endif %} |
| 트리거 발동 지연 p50 / p95 | 기록 | {% if mx.measured.trigger.delay_ms.p50 %}{{ mx.measured.trigger.delay_ms.p50 }}ms / {{ mx.measured.trigger.delay_ms.p95 }}ms{% else %}미측정{% endif %} |
| 컴플라이언스 재현율 | ≥ {{ mx.targets.compliance.recall }} | {% if mx.measured.compliance.recall.value %}{{ mx.measured.compliance.recall.value }}{% else %}미측정{% endif %} |
| 컴플라이언스 정밀도 | ≥ {{ mx.targets.compliance.precision }} | {% if mx.measured.compliance.precision.value %}{{ mx.measured.compliance.precision.value }}{% else %}미측정{% endif %} |
| **C-5 마스킹 누락 (P1~P7)** | **{{ mx.targets.masking.missed_count }}건 — 절대 규칙** | {% if mx.measured.masking.missed_count.value %}{{ mx.measured.masking.missed_count.value }}건{% else %}미측정{% endif %} |
| 내부 처리 p95 | ≤ {{ mx.targets.latency.internal_p95_ms }}ms | {% if mx.measured.latency_ms.internal.p95 %}{{ mx.measured.latency_ms.internal.p95 }}ms{% else %}미측정{% endif %} |
| E2E 체감 지연 p95 | 측정·기록 | {% if mx.measured.latency_ms.e2e.p95 %}{{ mx.measured.latency_ms.e2e.p95 }}ms{% else %}미측정{% endif %} |
| F-2 종결 요건 판정 정확도 *(조건부)* | 100% — 절대 규칙 | {% if mx.measured.f2.closure_verdict_accuracy.value %}{{ mx.measured.f2.closure_verdict_accuracy.value }}{% else %}미측정{% endif %} |

### 측정할 수 없는 것

{% for x in mx.not_measurable %}- {{ x }}
{% endfor %}

### 대표 실험 — STT 오류율별 성능 곡선

검색 3계열의 Recall@5 와 C-5 마스킹 재현율을 같은 축에 올린다.

| 계열 | 0% | 5% | 10% | 15% | 20% |
|---|---|---|---|---|---|
{% for row in mx.measured.error_tolerance %}{% unless row[0] == "meta" %}| {{ row[0] }} | {% for c in row[1] %}{% if c[1] %}{{ c[1] }}{% else %}—{% endif %} | {% endfor %}
{% endunless %}{% endfor %}

{% unless mx.measured.error_tolerance.meta.measured_at %}아직 측정 전이다. 5주차 항목.{% endunless %}

측정 방법과 채점 원칙은 [평가 설계]({{ '/docs/evaluation/' | relative_url }}) 참조.
