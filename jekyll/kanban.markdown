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
  .kanban .card .reqs{ display:flex; flex-wrap:wrap; gap:0.25rem; margin-top:0.4rem; }
  .req{ font-family:'IBM Plex Mono',monospace; font-size:0.6rem; letter-spacing:.03em; font-weight:600; padding:0.1rem 0.4rem; border-radius:3px; white-space:nowrap; border:1px solid currentColor; }
  .req-A{ background:rgba(126,214,199,.12); color:#7ED6C7; }
  .req-B{ background:rgba(245,166,35,.12); color:#F5A623; }
  .req-C{ background:rgba(233,127,127,.12); color:#E97F7F; }
  .req-D{ background:rgba(168,150,224,.12); color:#A896E0; }
  .req-E{ background:rgba(110,143,214,.12); color:#8FA8E8; }
  .req-F{ background:rgba(255,230,168,.12); color:#FFE6A8; }
  .req-G{ background:rgba(150,168,180,.12); color:#96A8B4; }
  .req-Q{ background:rgba(121,131,155,.14); color:#9AA3B8; }
  .req-S{ background:rgba(121,131,155,.14); color:#9AA3B8; }
  .kb-cover{ margin:0 0 2rem; }
  .kb-cover table{ width:100%; }
  .kb-cover td:first-child{ white-space:nowrap; width:1%; }
  .kb-cover .none{ color:#79839B; }
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

## 기능 ID 커버리지

기획서의 [기능 ID](/docs/02/)를 티켓에 그대로 단다 — 코드 파일 상단의 `# Requirement: <ID>` 주석과 **같은 ID**라
백로그에서 코드까지 한 줄로 이어진다. 티켓이 0건인 기능은 아직 아무도 손대지 않은 것이다.

{% assign req_ids = "A-1,A-2,B-0,B-1,B-2,B-3,B-4,B-5,B-6,C-1,C-2,C-3,C-4,C-5,D-1,D-2,D-3,D-4,E-1,E-2,E-4,F-2,G-2,SEC-1,SEC-2,QUA-1,QUA-2,COST-1" | split: "," %}

<div class="kb-cover" markdown="0">
<table>
<thead><tr><th>기능 ID</th><th>정의</th><th>티켓</th></tr></thead>
<tbody>
{% for rid in req_ids %}
  {% assign hits = "" | split: "" %}
  {% for t in site.backlogs %}
    {% if t.requirement contains rid %}{% assign hits = hits | push: t %}{% endif %}
  {% endfor %}
  {% assign fam = rid | slice: 0 %}
  <tr>
    <td><span class="req req-{{ fam }}">{{ rid }}</span></td>
    <td>{% case rid %}
      {% when "A-1" %}스트리밍 STT{% when "A-2" %}화자 분리
      {% when "B-0" %}도메인 라우팅{% when "B-1" %}트리거 판정{% when "B-2" %}하이브리드 검색{% when "B-3" %}리랭킹
      {% when "B-4" %}카드 요약 생성{% when "B-5" %}카드 표시{% when "B-6" %}출처 표시·근거 부족 처리
      {% when "C-1" %}확정적 보장 표현{% when "C-2" %}불필요한 민감정보 요구{% when "C-3" %}고지 누락{% when "C-4" %}대체 표현 제시
      {% when "C-5" %}개인정보 실시간 마스킹 <strong>(코어)</strong>
      {% when "D-1" %}상담 요약{% when "D-2" %}유형 분류{% when "D-3" %}후속조치 추출{% when "D-4" %}지식베이스 공백 리포트
      {% when "E-1" %}골든셋 채점{% when "E-2" %}지연 분포{% when "E-4" %}리포트
      {% when "F-2" %}종결 요건 검증 <em>(조건부)</em>{% when "G-2" %}지역 자원 연계 <em>(여유 시)</em>
      {% when "SEC-1" %}개인정보 원본 미보관{% when "SEC-2" %}자격증명 분리
      {% when "QUA-1" %}요구 ID별 자동화 테스트{% when "QUA-2" %}골든셋 회귀 자동화{% when "COST-1" %}STT 사용량 이중 캡
    {% endcase %}</td>
    <td>{% if hits.size == 0 %}<span class="none">— 티켓 없음</span>{% else %}{% for h in hits %}<a href="{{ h.url | relative_url }}">{{ h.title | truncate: 28 }}</a>{% unless forloop.last %} · {% endunless %}{% endfor %}{% endif %}</td>
  </tr>
{% endfor %}
</tbody>
</table>
</div>

---

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
              {% if item.requirement %}<div class="reqs">{% for r in item.requirement %}{% assign fam = r | slice: 0 %}<span class="req req-{{ fam }}" title="기능 ID {{ r }}">{{ r }}</span>{% endfor %}</div>{% endif %}
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
paths:                    # (선택) 이 티켓 소관 파일 — 붙여두면 상태 갱신을 잊었을 때 경고해 줍니다
  - "apps/dashboard/*"
depends_on:               # (선택) 앞 단계 티켓. 일부러 나눈 단계는 중복 경고에서 빠집니다
  - "w2-baseline"
requirement:              # (선택) 이 티켓이 만드는 기능 ID — 위 커버리지 표에 집계됩니다
  - "B-2"
---

무엇을 / 왜 / 완료 조건을 적습니다.
```

파일명은 `w{주차}-{영문-슬러그}.md` 로 짓습니다(예: `w1-eval-ci.md`). 한글 파일명은 URL이 깨집니다.
상태를 바꿀 때는 **자기 티켓의 `status` 한 줄만** 고칩니다.

`requirement` 는 기획서의 [기능 ID](/docs/02/)를 그대로 씁니다 — 새 접두어를 만들지 않습니다.
같은 ID를 코드 파일 상단에도 `# Requirement: B-2` 로 답니다. **두 곳이 같은 ID라 백로그에서 코드까지
추적이 이어집니다.** 배포·저장소 정리처럼 기능 ID 대상이 아닌 티켓은 비워 둡니다.

세션을 끝낼 때 `python3 scripts/check_session_end.py` 를 돌리면 상태가 실제와 어긋난 티켓과
중복 티켓을 알려줍니다. 진행 기록을 빠뜨리면 `Stop` 훅이 세션을 끝내지 못하게 막습니다.

---

[← 개발목차로 돌아가기](/toc/)
