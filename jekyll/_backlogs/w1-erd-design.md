---
title: "MySQL 스키마·ERD 설계 (17테이블)"
assignee: "류준"
role: "ai"
status: "done"
sprint: 1
priority: 21
date: 2026-08-25
requirement:
  - "SEC-1"
---

기획서에는 테이블 5종의 이름만 있었다. 실제 기능 명세와 대조해 **17개**로 설계했다.
가입자·요금제·문서·후속조치·공백리포트 등이 추가로 필요했다.

산출물: `db/schema.sql`(DDL) · `db/docs/ERD.md` · `db/docs/erd.dot` · `db/generate_schema_docs.py`
사이트: [16. ERD](/docs/16/)

## 정규화

1:N 관계는 분리해 1NF 준수, 2NF/3NF 검토. `closure`·`call` 은 컬럼이 좁아지는 하위 테이블 대신
**의도적으로 역정규화**했고 근거를 `ERD.md` 에 적었다.

관계선에 **실선(식별)/점선(비식별)** 표기를 넣었다. 서로게이트 PK 만 쓰는 스키마라
물리적 식별관계는 없고 개념적 표시임을 문서에 명시했다.

## 팀 교차검증

다른 팀원이 독립적으로 그린 ERD 와 대조해 서로의 누락을 찾았다.

- 상대 설계에서 흡수: `eval_run.error_rate`(4.2절 오류율 실험에 필수) · `compliance_rule`(C-4 권장 대체 표현) · `agent`
- 상대에게 전달한 피드백: `subscriber`/`plan`(F-3·TERM-5.3), `follow_up_action`·`knowledge_gap`(D-3·D-4) 누락

FK 생성 순서 버그(`document` 가 `recommendation_card` 보다 뒤에 있어 실행 시 에러)도 이때 발견해 고쳤다.

**미결**: F-2 `evidence` 를 넓은 표로 둘지 EAV + 추적 테이블로 둘지 — F-2 구현 시 재검토.
스키마 자체의 팀 최종 승인은 [별도 티켓](/backlog/w1-db-schema/).
