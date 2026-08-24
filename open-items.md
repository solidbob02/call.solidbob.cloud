---
layout: page
title: 미결 항목
permalink: /open-items/
---

아직 정하지 못했거나 답을 기다리는 것들. 결정되면 `resolved` 로 닫고 결정 기록을 남긴다.
비워두면 다음 세션이 같은 질문을 다시 하게 되므로, 판단이 갈린 지점은 반드시 여기에 남긴다.

{% assign items = site.data.open_items %}
{% assign open = items | where: "status", "open" %}
{% assign resolved = items | where: "status", "resolved" %}

## 미결 ({{ open.size }})

{% if open.size == 0 %}
없음.
{% else %}
<div class="oi">
{% for it in open %}
  <div class="oi__item">
    <h3 class="oi__title"><span class="oi__id">{{ it.id }}</span> {{ it.title }}</h3>
    <p class="oi__why">{{ it.why }}</p>
    <p class="oi__meta">
      담당 {{ it.owner }} · 제기 {{ it.opened }}
      {% if it.blocks %}· 막고 있는 것: {% for b in it.blocks %}<code>{{ b }}</code>{% unless forloop.last %}, {% endunless %}{% endfor %}{% endif %}
    </p>
  </div>
{% endfor %}
</div>
{% endif %}

## 해소됨 ({{ resolved.size }})

{% if resolved.size == 0 %}
아직 없음.
{% else %}
<ul>
{% for it in resolved %}
  <li><strong>{{ it.id }}</strong> {{ it.title }} — {{ it.resolution }} <em>({{ it.resolved }})</em></li>
{% endfor %}
</ul>
{% endif %}

<p class="toc__back"><a href="{{ '/toc/' | relative_url }}">&larr; 목차</a></p>
