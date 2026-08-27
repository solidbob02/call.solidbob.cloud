import type { ReactElement } from "react";

export function Problem(): ReactElement {
  return (
    <section className="quiet problem" id="problem">
      <p className="eyebrow">놓치는 순간</p>
      <h2>상담원이 약관을 찾는 동안, 통화는 이미 다음 질문으로 간다.</h2>
      <ul>
        <li>분실 신고와 해지 고지가 한 통화에 겹치면, 조항을 뒤적이는 손이 늦다.</li>
        <li>자막에 카드번호가 남으면, 그 화면을 저장하는 순간부터 개인정보다.</li>
        <li>종결 전에 해야 할 고지를 빼먹으면, 같은 고객이 다시 전화한다.</li>
      </ul>
    </section>
  );
}
