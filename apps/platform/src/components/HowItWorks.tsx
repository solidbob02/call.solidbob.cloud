import type { ReactElement } from "react";

const STEPS = [
  {
    num: "01",
    title: "통화 시작",
    body: "실시간 음성 인식으로 텍스트로 바꿉니다.",
  },
  {
    num: "02",
    title: "맥락 분석",
    body: "RAG 엔진이 관련 규정·서류·사례를 찾습니다.",
  },
  {
    num: "03",
    title: "실시간 제안",
    body: "추천 문서, 권장 표현, 통역 결과를 화면에 띄웁니다.",
  },
  {
    num: "04",
    title: "통화 종료 정리",
    body: "요약·유형·후속조치를 만들고, 상담사 확인을 기다립니다.",
  },
] as const;

export function HowItWorks(): ReactElement {
  return (
    <section id="how" className="bg-brand-deep px-5 py-20 text-white">
      <div className="mx-auto max-w-[1120px]">
        <p className="mb-3 text-[13px] font-semibold text-brand-bright">작동 방식</p>
        <h2 className="m-0 max-w-[14em] text-[clamp(22px,3vw,32px)] font-semibold tracking-tight">
          네 단계. 상담사가 끊을 때까지 옆에서 돕습니다.
        </h2>
        <ol className="mt-12 grid list-none grid-cols-1 gap-0 p-0 mid:grid-cols-4">
          {STEPS.map((step, index) => (
            <li key={step.num} className="relative px-0 py-6 mid:px-4 mid:py-0">
              {index < STEPS.length - 1 ? (
                <span
                  className="pointer-events-none absolute top-[22px] left-[28px] hidden h-px bg-white/20 mid:block mid:right-[-8px] mid:left-[52px]"
                  aria-hidden="true"
                />
              ) : null}
              <span className="relative z-10 inline-flex h-11 w-11 items-center justify-center rounded-full border border-white/20 bg-brand-deep text-[13px] font-semibold text-brand-bright">
                {step.num}
              </span>
              <h3 className="mt-4 mb-2 text-[17px] font-semibold">{step.title}</h3>
              <p className="m-0 text-[14px] leading-relaxed text-white/70">
                {step.body}
              </p>
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}
