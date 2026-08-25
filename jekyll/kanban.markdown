---
layout: doc
title: 칸반 보드
permalink: /kanban/
---

<style>
  .kb-legend{ display:flex; gap:1rem; flex-wrap:wrap; font-size:0.8rem; color:#6b7280; margin:0 0 2rem; }
  .kb-person{ margin:0 0 2.5rem; }
  .kb-person h2{ display:flex; align-items:center; gap:0.6rem; }
  .kb-person h2 .count{ font-size:0.75rem; font-weight:600; color:#6b7280; }
  .kanban{ display:grid; grid-template-columns:repeat(3,1fr); align-items:start; gap:0.9rem; margin:1rem 0 0; }
  .kanban .col{ background:#f6f7f9; border-radius:8px; padding:0.75rem; min-height:4rem; }
  .kanban .col h4{ margin:0 0 0.75rem; font-size:0.8rem; color:#6b7280; font-weight:700; }
  .kanban .card{ background:#fff; border:1px solid #e5e7eb; border-radius:6px; padding:0.6rem 0.7rem; margin-bottom:0.6rem; font-size:0.85rem; line-height:1.5; }
  .kanban .card a{ color:#111318; text-decoration:none; font-weight:600; }
  .kanban .card a:hover{ color:#2f6fed; text-decoration:underline; }
  .kanban .card .role{ display:inline-block; font-size:0.7rem; font-weight:700; padding:0.1rem 0.45rem; border-radius:999px; margin-bottom:0.35rem; white-space:nowrap; }
  .role-infra{ background:#e8f0fe; color:#1a56b8; }
  .role-ai{ background:#e9f7ef; color:#1b7a44; }
  .role-app{ background:#fdf0e6; color:#b45309; }
  .kanban .col.empty-hint{ color:#9ca3af; font-size:0.8rem; }
  @media (max-width:640px){ .kanban{ grid-template-columns:1fr; } }
</style>

담당자별 백로그입니다. **티켓 1건 = 파일 1개**(`jekyll/_backlogs/`)이므로 세 사람이 동시에 자기 티켓을 고쳐도 병합 충돌이 나지 않습니다.
주차별 목표는 [8주 마일스톤](/docs/08/), 일자별 기록은 [개발 로그](/progress/), 아직 정하지 못한 것은 [미결 항목](/open-items/)에 있습니다.

<div class="kb-legend">
  <span><span class="role role-infra">인프라</span> 정성윤</span>
  <span><span class="role role-ai">백엔드·AI</span> 류준</span>
  <span><span class="role role-app">앱·프론트</span> 장민석</span>
</div>

{% assign statuses = "todo,in-progress,done" | split: "," %}
{% assign people = site.backlogs | group_by: "assignee" | sort: "name" %}

{% for person in people %}
{% assign done_count = person.items | where: "status", "done" | size %}
<div class="kb-person">
  <h2>{{ person.name }} <span class="count">{{ done_count }} / {{ person.items | size }} 완료</span></h2>
  <div class="kanban">
    {% for st in statuses %}
    {% assign items = person.items | where: "status", st | sort: "priority" %}
    <div class="col">
      {% case st %}
        {% when "todo" %}<h4>할 일 ({{ items | size }})</h4>
        {% when "in-progress" %}<h4>진행 중 ({{ items | size }})</h4>
        {% when "done" %}<h4>완료 ({{ items | size }})</h4>
      {% endcase %}
      {% for item in items %}
      <div class="card">
        <span class="role role-{{ item.role }}">{% case item.role %}{% when "infra" %}인프라{% when "ai" %}백엔드·AI{% when "app" %}앱·프론트{% else %}{{ item.role }}{% endcase %}</span><br>
        <a href="{{ item.url | relative_url }}">{{ item.title }}</a>
      </div>
      {% endfor %}
      {% if items.size == 0 %}<div class="empty-hint">없음</div>{% endif %}
    </div>
    {% endfor %}
  </div>
</div>
{% endfor %}

## 티켓 추가하는 법

`jekyll/_backlogs/` 에 파일을 하나 만듭니다. **다른 사람 파일은 건드리지 않습니다.**

```yaml
---
title: "카카오 로그인 API 연동"
assignee: "류준"          # 정성윤 | 류준 | 장민석
role: "ai"                # infra | ai | app  (배지 색)
status: "in-progress"     # todo | in-progress | done
sprint: 1
priority: 5               # 같은 칸 안에서의 정렬 순서
date: 2026-08-25
---

무엇을 / 왜 / 완료 조건을 적습니다.
```

파일명은 `w{주차}-{영문-슬러그}.md` 로 짓습니다(예: `w1-eval-ci.md`). 한글 파일명은 URL이 깨집니다.
상태를 바꿀 때는 **자기 티켓의 `status` 한 줄만** 고칩니다.

---

[← 개발목차로 돌아가기](/toc/)
