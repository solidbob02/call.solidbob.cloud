---
title: "지식베이스 색인 — 고정 청킹 + 문서 ID 부여"
assignee: "류준·장민석"
role: "ai"
status: "todo"
sprint: 2
priority: 2
date: 2026-08-26
---

4개 도메인 지식베이스(`knowledge-base/{finance,dasan,shopping,health}/`)를 Elasticsearch 에 넣는다.
2주차는 **가장 단순한 형태**로 간다 — 고정 청킹, nori·dense_vector 없이 BM25 만.

## 할 것

- 고정 길이 청킹 (길이 기준은 여기서 정하고 기록한다)
- 청크마다 문서 ID 유지 — `FIN-3.2` 처럼 도메인 접두어 + 조항
- 인덱스를 도메인별로 나눌지 하나로 두고 필터할지 결정 → **[도메인 라우팅 결정](/backlog/w2-domain-routing/)에 달려 있다**
- 적재 후 chunk 목록 덤프 — 골든셋 라벨링이 이 목록을 본다

## 왜 단순하게 시작하나

4주차에 nori·dense_vector·RRF 를 넣고 **개선 폭을 수치로 보여주기 위해서**다.
처음부터 다 넣으면 무엇이 얼마나 기여했는지 말할 수 없다([평가 설계](/docs/06/)).

## 완료 조건

골든셋 라벨이 참조할 수 있는 chunk ID 목록이 나오고, 같은 명령으로 재적재가 재현된다.
