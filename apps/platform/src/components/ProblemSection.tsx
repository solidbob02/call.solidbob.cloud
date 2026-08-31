import type { ReactElement } from "react";

const CARDS = [
  {
    num: "01",
    title: "매뉴얼 찾는 시간",
    body: "규정과 서류가 여러 문서에 흩어져 있어, 찾는 동안 통화는 이미 다음 질문으로 갑니다.",
  },
  {
    num: "02",
    title: "표현 하나의 리스크",
    body: "한 마디가 민원인을 오해하게 만들 수 있습니다. 금지 표현을 그 자리에서 걸러야 합니다.",
  },
  {
    num: "03",
    title: "통화 후 반복 정리 업무",
    body: "요약·유형·후속조치를 매번 손으로 남기면, 상담이 끝난 뒤에도 일이 남습니다.",
  },
] as const;

export function ProblemSection(): ReactElement {
  return (
    <section id="problem" className="bg-bg px-5 py-20">
      <div className="mx-auto max-w-[1120px] text-center">
        <p className="mb-3 text-[13px] font-semibold text-brand">문제 상황</p>
        <h2 className="mx-auto m-0 max-w-[18em] text-[clamp(22px,3vw,32px)] font-semibold leading-snug tracking-tight">
          상담사 한 명이 규정, 서류, 언어까지 모두 기억하고 있을 순 없습니다
        </h2>
        <ul className="mt-12 grid list-none grid-cols-1 gap-4 p-0 text-left mid:grid-cols-3">
          {CARDS.map((card) => (
            <li
              key={card.num}
              className="rounded-[16px] border border-line bg-card p-6 shadow-[0_8px_28px_rgba(22,27,46,0.06)]"
            >
              <span className="text-[12px] font-semibold text-brand-bright">
                {card.num}
              </span>
              <h3 className="mt-3 mb-2 text-[17px] font-semibold">{card.title}</h3>
              <p className="m-0 text-[14px] leading-relaxed text-ink-soft">
                {card.body}
              </p>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
