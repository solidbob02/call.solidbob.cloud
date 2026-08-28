---
title: "자막 패널 스크롤백 · 자막 검색"
assignee: "조서희"
role: "app"
status: "done"
sprint: 2
priority: 5
date: 2026-08-27
depends_on: ["w2-transcript-autoscroll"]
paths:
  - "apps/dashboard/src/components/TranscriptPanel.tsx"
  - "apps/dashboard/src/components/MaskedText.tsx"
  - "apps/dashboard/src/lib/text/highlight.ts"
---

자동 스크롤([w2-transcript-autoscroll](/backlog/w2-transcript-autoscroll/))만으로는 과거 대화를
되짚어 볼 수 없다. 통화가 길어지면 상담원이 "아까 뭐라고 했더라"를 확인할 방법이 필요하다.

검색어는 마스킹이 **끝난** 텍스트에서 찾는다. 원문은 화면에 오지 않으므로(C-5) 검색으로
가려진 값을 되살릴 수 없다.

## 완료 조건

- 위로 올려 보는 동안 새 발화가 와도 끌려 내려가지 않는다
- 그 상태에서 새 발화가 오면 「최신 대화로 이동」 버튼이 뜨고, 누르면 맨 아래로 가며 자동 스크롤이 재개된다
- 검색어와 일치하는 부분이 하이라이트되고, 이전/다음으로 이동하며 「N / 총 M」이 보인다
- 검색어를 지우면 하이라이트가 사라진다
- 마스킹 표시·「⚠ 경고」 태그·화자 구분은 그대로다
