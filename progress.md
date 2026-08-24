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
    {% if t.status != "todo" %}<code>{{ t.status }}</code>{% endif %}
    {% if t.note %}<br><small>{{ t.note }}</small>{% endif %}
  </li>
{% endfor %}
</ul>
{% endfor %}

## 지표 — 목표 대비 실측

측정하지 않은 값은 **미측정**으로 둔다. 예시 수치를 채워 넣지 않는다.

| 지표 | 목표 | 실측 |
|---|---|---|
| Recall@5 (오류 0%) | ≥ {{ mx.targets.retrieval.recall_at_5_clean }} | {% if mx.measured.baseline.recall_at_5.value %}{{ mx.measured.baseline.recall_at_5.value }}{% else %}미측정{% endif %} |
| MRR | ≥ {{ mx.targets.retrieval.mrr }} | {% if mx.measured.baseline.mrr.value %}{{ mx.measured.baseline.mrr.value }}{% else %}미측정{% endif %} |
| 트리거 적절 발동률 | ≥ {{ mx.targets.trigger.fire_precision }} | {% if mx.measured.trigger.fire_precision.value %}{{ mx.measured.trigger.fire_precision.value }}{% else %}미측정{% endif %} |
| 트리거 불필요 발동률 | ≤ {{ mx.targets.trigger.false_fire_rate }} | {% if mx.measured.trigger.false_fire_rate.value %}{{ mx.measured.trigger.false_fire_rate.value }}{% else %}미측정{% endif %} |
| 컴플라이언스 재현율 | ≥ {{ mx.targets.compliance.recall }} | {% if mx.measured.compliance.recall.value %}{{ mx.measured.compliance.recall.value }}{% else %}미측정{% endif %} |
| 컴플라이언스 정밀도 | ≥ {{ mx.targets.compliance.precision }} | {% if mx.measured.compliance.precision.value %}{{ mx.measured.compliance.precision.value }}{% else %}미측정{% endif %} |
| p95 레이턴시 | ≤ {{ mx.targets.latency.p95_ms }}ms | {% if mx.measured.latency_ms.p95 %}{{ mx.measured.latency_ms.p95 }}ms{% else %}미측정{% endif %} |

### 대표 실험 — STT 오류율별 Recall@5

| 방식 | 0% | 5% | 10% | 15% | 20% |
|---|---|---|---|---|---|
{% for row in mx.measured.error_tolerance %}{% unless row[0] == "meta" %}| {{ row[0] }} | {% for c in row[1] %}{% if c[1] %}{{ c[1] }}{% else %}—{% endif %} | {% endfor %}
{% endunless %}{% endfor %}

{% unless mx.measured.error_tolerance.meta.measured_at %}아직 측정 전이다. 5주차 항목.{% endunless %}

측정 방법과 채점 원칙은 [평가 설계]({{ '/docs/evaluation/' | relative_url }}) 참조.
