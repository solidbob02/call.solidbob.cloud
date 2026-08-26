---
layout: doc
title: 칸반 보드
permalink: /kanban/
---

<style>
  main:has(.kb-layout){ max-width:1100px; }
  .kb-layout{ display:flex; gap:1.25rem; align-items:flex-start; margin:0 0 2rem; }
  .kb-sidebar{ flex:0 0 200px; display:flex; flex-direction:column; gap:0.4rem; }
  .kb-nav-item{ display:flex; flex-direction:column; align-items:flex-start; gap:0.3rem; width:100%; padding:0.7rem 0.75rem 0.7rem 0.85rem; border:1px solid rgba(223,228,238,.12); border-radius:6px; background:#080B12; color:#DFE4EE; text-align:left; cursor:pointer; }
  .kb-nav-item:hover{ border-color:rgba(245,166,35,.4); }
  .kb-nav-item.active{ background:#10151F; box-shadow:inset 3px 0 0 currentColor; }
  .kb-nav-item.active.role-infra{ color:#8FA8E8; }
  .kb-nav-item.active.role-ai{ color:#F5A623; }
  .kb-nav-item.active.role-app{ color:#FFE6A8; }
  .kb-nav-name{ font-weight:600; color:#DFE4EE; }
  .kb-nav-count{ font-family:'IBM Plex Mono',monospace; font-size:0.72rem; color:#79839B; }
  .kb-content{ flex:1; min-width:0; }
  .kb-panel{ display:none; }
  .kb-panel.active{ display:block; animation:kb-fade 140ms ease-out; }
  .kb-person{ margin:0; }
  .kb-person h2{ display:flex; align-items:center; gap:0.6rem; }
  .kb-person h2 .count{ font-family:'IBM Plex Mono',monospace; font-size:0.72rem; font-weight:500; color:#79839B; }
  .kanban{ display:grid; grid-template-columns:repeat(3,1fr); align-items:start; gap:0.9rem; margin:1rem 0 0; }
  .kanban .col{ background:#10151F; border:1px solid rgba(223,228,238,.12); border-radius:8px; padding:0.75rem; min-height:4rem; }
  .kanban .col h4{ margin:0 0 0.75rem; font-family:'IBM Plex Mono',monospace; font-size:0.72rem; letter-spacing:.05em; text-transform:uppercase; color:#79839B; font-weight:600; }
  .kanban .card{ background:#080B12; border:1px solid rgba(223,228,238,.12); border-radius:6px; padding:0.6rem 0.7rem; margin-bottom:0.6rem; font-size:0.85rem; line-height:1.5; }
  .kanban .card a{ color:#DFE4EE; text-decoration:none; font-weight:600; }
  .kanban .card a:hover{ color:#F5A623; text-decoration:underline; }
  .kanban .card .role{ display:inline-block; font-family:'IBM Plex Mono',monospace; font-size:0.65rem; letter-spacing:.04em; font-weight:600; padding:0.15rem 0.5rem; border-radius:999px; margin-bottom:0.35rem; white-space:nowrap; border:1px solid currentColor; }
  .role-infra{ background:rgba(110,143,214,.12); color:#8FA8E8; }
  .role-ai{ background:rgba(245,166,35,.12); color:#F5A623; }
  .role-app{ background:rgba(255,230,168,.10); color:#FFE6A8; }
  .kanban .col.empty-hint{ color:#4d5568; font-size:0.8rem; }
  .kb-nav-item .role{ display:inline-block; font-family:'IBM Plex Mono',monospace; font-size:0.65rem; letter-spacing:.04em; font-weight:600; padding:0.15rem 0.5rem; border-radius:999px; white-space:nowrap; border:1px solid currentColor; }
  @keyframes kb-fade{ from{ opacity:0; } to{ opacity:1; } }
  @media (max-width:640px){
    .kb-layout{ flex-direction:column; }
    .kb-sidebar{ flex:none; width:100%; flex-direction:row; flex-wrap:wrap; }
    .kb-nav-item{ flex:1 1 140px; }
    .kanban{ grid-template-columns:1fr; }
  }
  @media (prefers-reduced-motion: reduce){ .kb-panel.active{ animation:none; } }
</style>

담당자별 백로그입니다. **티켓 1건 = 파일 1개**(`jekyll/_backlogs/`)이므로 네 사람이 동시에 자기 티켓을 고쳐도 병합 충돌이 나지 않습니다.
주차별 목표는 [8주 마일스톤](/docs/08/), 일자별 기록은 [개발 로그](/progress/), 아직 정하지 못한 것은 [미결 항목](/open-items/)에 있습니다.

{% assign statuses = "todo,in-progress,done" | split: "," %}
{% assign team = "정성윤,류준,장민석,조서희" | split: "," %}
{% assign joint = site.backlogs | where: "assignee", "류준·장민석" %}

<div class="kb-layout">
  <nav class="kb-sidebar" aria-label="담당자">
    {% for name in team %}
    {% assign items = site.backlogs | where: "assignee", name %}
    {% if name == "류준" or name == "장민석" %}
      {% assign items = items | concat: joint %}
    {% endif %}
    {% assign done_count = items | where: "status", "done" | size %}
    {% assign person_role = items.first.role %}
    {% if person_role == nil %}
      {% case name %}
        {% when "정성윤" %}{% assign person_role = "infra" %}
        {% when "조서희" %}{% assign person_role = "app" %}
        {% else %}{% assign person_role = "ai" %}
      {% endcase %}
    {% endif %}
    {% case name %}
      {% when "정성윤" %}{% assign person_id = "seongyun" %}
      {% when "류준" %}{% assign person_id = "ryujun" %}
      {% when "장민석" %}{% assign person_id = "minseok" %}
      {% when "조서희" %}{% assign person_id = "seohee" %}
    {% endcase %}
    <button type="button" class="kb-nav-item role-{{ person_role }}{% if forloop.first %} active{% endif %}" data-person="{{ person_id }}">
      <span class="role role-{{ person_role }}">{% case person_role %}{% when "infra" %}인프라{% when "ai" %}백엔드·AI{% when "app" %}프론트엔드{% else %}{{ person_role }}{% endcase %}</span>
      <span class="kb-nav-name">{{ name }}</span>
      <span class="kb-nav-count">{{ done_count }}/{{ items.size }}</span>
    </button>
    {% endfor %}
  </nav>

  <div class="kb-content">
    {% for name in team %}
    {% assign items = site.backlogs | where: "assignee", name %}
    {% if name == "류준" or name == "장민석" %}
      {% assign items = items | concat: joint %}
    {% endif %}
    {% assign done_count = items | where: "status", "done" | size %}
    {% case name %}
      {% when "정성윤" %}{% assign person_id = "seongyun" %}
      {% when "류준" %}{% assign person_id = "ryujun" %}
      {% when "장민석" %}{% assign person_id = "minseok" %}
      {% when "조서희" %}{% assign person_id = "seohee" %}
    {% endcase %}
    <div class="kb-panel{% if forloop.first %} active{% endif %}" data-person="{{ person_id }}">
      <div class="kb-person">
        <h2>{{ name }} <span class="count">{{ done_count }} / {{ items.size }} 완료</span></h2>
        <div class="kanban">
          {% for st in statuses %}
          {% assign column = items | where: "status", st | sort: "priority" %}
          <div class="col">
            {% case st %}
              {% when "todo" %}<h4>할 일 ({{ column.size }})</h4>
              {% when "in-progress" %}<h4>진행 중 ({{ column.size }})</h4>
              {% when "done" %}<h4>완료 ({{ column.size }})</h4>
            {% endcase %}
            {% for item in column %}
            <div class="card">
              <span class="role role-{{ item.role }}">{% case item.role %}{% when "infra" %}인프라{% when "ai" %}백엔드·AI{% when "app" %}프론트엔드{% else %}{{ item.role }}{% endcase %}</span><br>
              <a href="{{ item.url | relative_url }}">{{ item.title }}</a>
            </div>
            {% endfor %}
            {% if column.size == 0 %}<div class="empty-hint">없음</div>{% endif %}
          </div>
          {% endfor %}
        </div>
      </div>
    </div>
    {% endfor %}
  </div>
</div>

<script>
document.querySelectorAll(".kb-nav-item").forEach(function (btn) {
  btn.addEventListener("click", function () {
    var target = btn.dataset.person;
    document.querySelectorAll(".kb-nav-item").forEach(function (other) {
      other.classList.toggle("active", other === btn);
    });
    document.querySelectorAll(".kb-panel").forEach(function (panel) {
      panel.classList.toggle("active", panel.dataset.person === target);
    });
  });
});
</script>

## 티켓 추가하는 법

`jekyll/_backlogs/` 에 파일을 하나 만듭니다. **다른 사람 파일은 건드리지 않습니다.**

```yaml
---
title: "카카오 로그인 API 연동"
assignee: "류준"          # 정성윤 | 류준 | 장민석 | 조서희
role: "ai"                # infra | ai | app  (배지 색 — ai: 류준·장민석, app: 조서희)
status: "in-progress"     # todo | in-progress | done | cancelled
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
