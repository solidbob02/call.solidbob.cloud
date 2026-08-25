---
layout: page
title: 목차
permalink: /toc/
---

<div class="toc">

<section class="toc__section">
  <h2><a href="{{ '/docs/1-business/' | relative_url }}">1. 사업 개요</a></h2>
  <ol class="toc__items">
    <li><span>1)</span> <a href="{{ '/docs/1-business/' | relative_url }}#1-사업-목적">사업 목적</a></li>
    <li><span>2)</span> <a href="{{ '/docs/1-business/' | relative_url }}#2-주요-사업-내용">주요 사업 내용</a></li>
    <li><span>3)</span> <a href="{{ '/docs/1-business/' | relative_url }}#3-기대-효과">기대 효과</a></li>
    <li><span>4)</span> <a href="{{ '/docs/1-business/' | relative_url }}#4-성공-조건">성공 조건</a></li>
  </ol>
</section>

<section class="toc__section">
  <h2><a href="{{ '/docs/2-requirements/' | relative_url }}">2. 개발 요구 사항</a></h2>
  <ol class="toc__items">
    <li><span>1)</span> <a href="{{ '/docs/2-requirements/' | relative_url }}#1-목적">목적</a></li>
    <li><span>2)</span> <a href="{{ '/docs/2-requirements/' | relative_url }}#2-개발-범위">개발 범위</a></li>
    <li><span>3)</span> <a href="{{ '/docs/2-requirements/' | relative_url }}#3-음성-데이터-수집-및-연계">음성 데이터 수집 및 연계</a></li>
    <li><span>4)</span> <a href="{{ '/docs/2-requirements/' | relative_url }}#4-실시간-문서-추천-처리--rag-핵심">실시간 문서 추천 처리 (RAG 핵심)</a></li>
    <li><span>5)</span> <a href="{{ '/docs/2-requirements/' | relative_url }}#5-개인정보-마스킹-c-5--코어">개인정보 마스킹 (C-5) — 코어</a></li>
    <li><span>6)</span> <a href="{{ '/docs/2-requirements/' | relative_url }}#6-상담원-지원-화면-기능">상담원 지원 화면 기능</a></li>
    <li><span>7)</span> <a href="{{ '/docs/2-requirements/' | relative_url }}#7-시스템-아키텍처">시스템 아키텍처</a></li>
    <li><span>8)</span> <a href="{{ '/docs/2-requirements/' | relative_url }}#8-보안-및-개인정보-보호">보안 및 개인정보 보호</a></li>
  </ol>
</section>

<section class="toc__section">
  <h2><a href="{{ '/docs/3-guidelines/' | relative_url }}">3. 주요 개발 수행 지침</a></h2>
  <ol class="toc__items">
    <li><span>1)</span> <a href="{{ '/docs/3-guidelines/' | relative_url }}#1-일반-사항">일반 사항</a></li>
    <li><span>2)</span> <a href="{{ '/docs/3-guidelines/' | relative_url }}#2-개발-표준-및-산출물">개발 표준 및 산출물</a></li>
    <li><span>3)</span> <a href="{{ '/docs/3-guidelines/' | relative_url }}#3-품질-관리-및-테스트">품질 관리 및 테스트</a></li>
  </ol>
</section>

<section class="toc__section">
  <h2><a href="{{ '/docs/4-schedule/' | relative_url }}">4. 개발 일정 및 추진 체계</a></h2>
  <ol class="toc__items">
    <li><span>1)</span> <a href="{{ '/docs/4-schedule/' | relative_url }}#1-단계별-개발-일정">단계별 개발 일정</a></li>
    <li><span>2)</span> <a href="{{ '/docs/4-schedule/' | relative_url }}#2-조직-구성-및-역할-분담">조직 구성 및 역할 분담</a></li>
    <li><span>3)</span> <a href="{{ '/docs/4-schedule/' | relative_url }}#3-위험-관리-방안">위험 관리 방안</a></li>
  </ol>
</section>

<section class="toc__section">
  <h2><a href="{{ '/docs/5-appendix/' | relative_url }}">5. 부록</a></h2>
  <ol class="toc__items">
    <li><span>1)</span> <a href="{{ '/docs/5-appendix/' | relative_url }}#1-용어-정의">용어 정의</a></li>
    <li><span>2)</span> <a href="{{ '/docs/5-appendix/' | relative_url }}#2-관련-서식">관련 서식</a></li>
    <li><span>3)</span> <a href="{{ '/docs/5-appendix/' | relative_url }}#3-민감-기능-공통-설계-원칙">민감 기능 공통 설계 원칙</a></li>
    <li><span>4)</span> <a href="{{ '/docs/5-appendix/' | relative_url }}#4-개정-이력">개정 이력</a></li>
    <li><span>5)</span> <a href="{{ '/docs/5-appendix/' | relative_url }}#5-참고-자료">참고 자료</a></li>
  </ol>
</section>

<section class="toc__section toc__section--sub">
  <h2>세부 문서 · 진행 기록</h2>
  <ol class="toc__items">
    {% assign details = site.docs | where_exp: "d", "d.nav_order > 5" | sort: "nav_order" %}
    {% for d in details %}
    <li><span>·</span> <a href="{{ d.url | relative_url }}">{{ d.title }}</a>
      <em class="toc__status">{{ d.status }} · {{ d.owner }} · 갱신 {{ d.updated }}</em></li>
    {% endfor %}
    <li><span>·</span> <a href="{{ '/progress/' | relative_url }}">진행 상황</a> <em class="toc__status">체크리스트와 실측 지표</em></li>
    <li><span>·</span> <a href="{{ '/log/' | relative_url }}">개발 로그</a> <em class="toc__status">세션별 작업 기록</em></li>
    <li><span>·</span> <a href="{{ '/open-items/' | relative_url }}">미결 항목</a> <em class="toc__status">아직 정하지 못한 것</em></li>
  </ol>
</section>

<p class="toc__back"><a href="{{ '/' | relative_url }}">&larr; 표지</a></p>

</div>
