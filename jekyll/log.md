---
layout: page
title: 개발 로그
permalink: /log/
---

작업이 있었던 모든 세션의 기록. 시간 순서로 쌓기만 하며 한 번 쓴 글은 고치지 않는다.
지금 무엇이 맞는지는 [목차]({{ '/toc/' | relative_url }})의 각 절이, 어디까지 왔는지는 [진행 상황]({{ '/progress/' | relative_url }})이 정본이다.

{% assign posts = site.posts %}
{% if posts.size == 0 %}
아직 기록이 없다.
{% else %}
<ul class="log-list">
  {% for post in posts %}
  <li class="log-list__item">
    <span class="log-list__meta">
      {{ post.date | date: "%Y-%m-%d" }}
      {% if post.week %}· {{ post.week }}주차{% endif %}
      {% if post.status %}· <code>{{ post.status }}</code>{% endif %}
      {% if post.track %}· {{ post.track | join: ", " }}{% endif %}
    </span>
    <a class="log-list__title" href="{{ post.url | relative_url }}">{{ post.title }}</a>
  </li>
  {% endfor %}
</ul>
{% endif %}

<p class="toc__back"><a href="{{ '/toc/' | relative_url }}">&larr; 목차</a></p>
