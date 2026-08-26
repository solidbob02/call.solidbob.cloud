---
title: "지식베이스 문서 초안 + 팀 리뷰"
assignee: "류준"
role: "ai"
status: "done"
sprint: 1
priority: 7
date: 2026-08-25
---

`knowledge-base/`에 이용약관(TERM)·응대매뉴얼(MANUAL)·내부처리규정(POLICY) 작성. 조항마다 ID 부여(`TERM-3.2` 등).

**2026-08-26 갱신**: 가상 통신사 "한별텔레콤" 단일 시나리오를 폐기하고, 실제 확보 데이터
(AI Hub 「민원(콜센터) 질의-응답」)가 다루는 4개 도메인 — 금융보험(한별금융)·다산콜센터
(한별시 통합민원콜센터)·쇼핑(한별샵)·질병관리본부(한별헬스콜) — 로 재구성 완료.
`knowledge-base/{finance,dasan,shopping,health}/`, 도메인 접두어 ID(`FIN-`/`DASAN-`/
`SHOP-`/`HLT-`). 근거: `_project/decisions/004-데모-도메인-4종-확정.md`.

**2026-08-26 완료**: 팀 회의로 리뷰 마무리 (정성윤·장민석·조서희). 골든셋도 도메인
기준으로 재작성 완료(`golden-set/v1-10.json`, 같은 날). 이 티켓은 종료 — 후속 논의는
`w1-domain-routing.md`(도메인 라우팅) 등 새 티켓에서 이어간다.
