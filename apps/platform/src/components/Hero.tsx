import type { ReactElement } from "react";

export function Hero(): ReactElement {
  return (
    <section id="hero" className="relative overflow-hidden bg-linear-to-br from-brand-deep via-brand to-brand-bright text-white">
      <div className="mx-auto grid max-w-[1120px] grid-cols-1 items-center gap-12 px-5 pt-16 pb-8 mid:grid-cols-2 mid:pt-20 mid:pb-10">
        <div>
          <p className="mb-5 inline-flex items-center gap-2 rounded-full border border-white/20 bg-white/10 px-3 py-1.5 text-[12.5px] text-white/90">
            <span className="h-1.5 w-1.5 rounded-full bg-teal" aria-hidden="true" />
            다산콜센터 상담 시나리오 기반 · SOLIDBOB 8주 스프린트
          </p>
          <h1 className="m-0 text-[clamp(28px,4vw,42px)] font-semibold leading-[1.25] tracking-tight">
            상담사가 통화 중 놓치는 것을,
            <br />
            AI가 옆에서 같이 찾아드립니다
          </h1>
          <p className="mt-5 max-w-[36em] text-[16px] leading-relaxed text-white/80">
            CallGuard는 통화 내용을 실시간으로 이해하고 필요한 서류, 규정,
            번역을 그 자리에서 찾아주는 상담사 어시스트 RAG 시스템입니다.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <a
              href="#features"
              className="rounded-[10px] bg-white px-4 py-2.5 text-[14px] font-semibold text-brand-deep"
            >
              핵심 기능 보기
            </a>
            <a
              href="#how"
              className="rounded-[10px] border border-white/35 px-4 py-2.5 text-[14px] font-semibold text-white"
            >
              작동 방식 보기
            </a>
          </div>
          <dl className="mt-10 grid grid-cols-3 gap-4 text-[12.5px] text-white/75">
            <div>
              <dt className="font-semibold text-white">5개</dt>
              <dd className="m-0 mt-1 leading-snug">동시 통번역 언어</dd>
            </div>
            <div>
              <dt className="font-semibold text-white">4개</dt>
              <dd className="m-0 mt-1 leading-snug">핵심 어시스트 기능</dd>
            </div>
            <div>
              <dt className="font-semibold text-white">8주</dt>
              <dd className="m-0 mt-1 leading-snug">스프린트 개발</dd>
            </div>
          </dl>
        </div>
        <CallMock />
      </div>
      <svg
        className="block w-full text-bg"
        viewBox="0 0 1440 72"
        preserveAspectRatio="none"
        aria-hidden="true"
      >
        <path
          fill="currentColor"
          d="M0 40c180 28 360 28 540 8s360-40 540-28 360 40 360 40V72H0Z"
        />
      </svg>
    </section>
  );
}

function CallMock(): ReactElement {
  return (
    <article className="rounded-[16px] bg-card p-5 text-ink shadow-[0_8px_28px_rgba(22,27,46,0.12)]">
      <div className="mb-4 flex flex-wrap items-center justify-between gap-2 border-b border-line pb-3">
        <div className="flex items-center gap-2 text-[13px] font-semibold">
          <span className="anim-rec h-2 w-2 rounded-full bg-amber" aria-hidden="true" />
          <span className="text-amber">REC</span>
          <span className="font-medium text-ink-soft">상담 진행 중 · 02:47</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="rounded-[10px] bg-teal-bg px-2 py-0.5 text-[11px] font-semibold text-teal">
            KO
          </span>
          <span className="rounded-[10px] bg-teal-bg px-2 py-0.5 text-[11px] font-semibold text-teal">
            VI
          </span>
        </div>
      </div>
      <p className="mb-4 text-[12.5px] text-ink-soft">
        외국인 민원 · 등록증 재발급 문의
      </p>
      <div className="flex flex-col gap-3">
        <p className="max-w-[92%] rounded-[10px] bg-bg px-3.5 py-2.5 text-[13.5px] leading-relaxed">
          <span className="mb-1 block text-[11px] font-semibold text-ink-soft">
            발신자
          </span>
          등본… 다시 발급받으려면 뭐가 필요해요? 동생이 대신 가도 되나요?
        </p>
        <p className="ml-auto max-w-[92%] rounded-[10px] bg-teal-bg px-3.5 py-2.5 text-[13.5px] leading-relaxed">
          <span className="mb-1 block text-[11px] font-semibold text-teal">
            상담사
          </span>
          대리 신청이면 위임장과 대리인 신분증이 필요합니다.
        </p>
        <div className="anim-assist rounded-[10px] border border-line bg-bg px-3.5 py-3">
          <div className="flex items-center justify-between gap-2">
            <p className="m-0 text-[11px] font-semibold text-teal">AI 추천</p>
            <span className="text-[11px] font-semibold text-teal">유사도 92%</span>
          </div>
          <p className="mt-1 text-[13.5px] font-semibold">
            외국인등록증 재발급 절차 안내
          </p>
          <p className="mt-1 text-[12px] text-ink-soft">F-2 필요서류 · 목업</p>
        </div>
        <div className="anim-warn rounded-[10px] bg-amber-bg px-3.5 py-2.5 text-[13px] leading-relaxed text-ink">
          <span className="font-semibold text-amber">권장 표현</span>
          {" — “불법체류” 대신 “체류기간 경과”로 안내하세요."}
        </div>
      </div>
    </article>
  );
}
