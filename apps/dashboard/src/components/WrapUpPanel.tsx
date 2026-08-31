import { useEffect, useMemo, useState, type ReactElement } from "react";
import type { CallWrapUp, SentimentSummary } from "../types/contract";
import { cardId, useCallStore } from "../store/callStore";

interface WrapUpPanelProps {
  onResume: () => void;
  onRestart: () => void;
  onWrapUp: () => Promise<CallWrapUp>;
}

/**
 * §2.5 D 통화 후 처리. D-1 요약 · D-2 유형 · D-3 후속조치는 게이트웨이가 주고,
 * D-4 지식베이스 공백은 이 통화에서 화면이 직접 본 것(수동 검색 실패)만 센다.
 * 상담 분위기는 감정분석 모델이 없어 정성 라벨·C-6 건수만 보여 준다.
 */
export function WrapUpPanel({
  onResume,
  onRestart,
  onWrapUp,
}: WrapUpPanelProps): ReactElement {
  const mode = useCallStore((state) => state.mode);
  const utterances = useCallStore((state) => state.utterances);
  const manualSearches = useCallStore((state) => state.manualSearches);
  const cards = useCallStore((state) => state.cards);
  const adoptions = useCallStore((state) => state.adoptions);

  const adopted = useMemo(
    () =>
      cards.filter(
        (item) => adoptions[cardId(item.card)]?.adopted === true,
      ),
    [cards, adoptions],
  );

  const [wrapUp, setWrapUp] = useState<CallWrapUp | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [done, setDone] = useState<ReadonlySet<number>>(new Set());

  useEffect(() => {
    let alive = true;
    setWrapUp(null);
    setError(null);
    onWrapUp()
      .then((result) => {
        if (alive) {
          setWrapUp(result);
        }
      })
      .catch((cause: unknown) => {
        if (alive) {
          setError(
            cause instanceof Error
              ? cause.message
              : "통화 후 처리를 불러오지 못했습니다.",
          );
        }
      });
    return () => {
      alive = false;
    };
  }, [onWrapUp]);

  function toggle(index: number): void {
    setDone((current) => {
      const next = new Set(current);
      if (next.has(index)) {
        next.delete(index);
      } else {
        next.add(index);
      }
      return next;
    });
  }

  const failed = manualSearches.filter((entry) => !entry.found);

  return (
    <main className="wrapup">
      {/* 돌아갈 길은 스크롤과 무관하게 늘 보여야 해서 스크롤 영역 밖에 둔다. */}
      <div className="wrapup-topbar">
        <header className="wrapup-inner wrapup-head">
          <div>
            <p className="wrapup-eyebrow">통화 종료</p>
            <h2>통화 후 처리</h2>
          </div>
          <div className="wrapup-actions">
            <button type="button" className="btn-outline" onClick={onResume}>
              통화로 돌아가기
            </button>
            <button type="button" className="btn-replay" onClick={onRestart}>
              새 통화 시작
            </button>
          </div>
        </header>
      </div>
      <div className="wrapup-scroll">
        <div className="wrapup-inner">
        {error !== null ? (
          <section className="wrapup-card">
            <p className="wrapup-error">{error}</p>
          </section>
        ) : wrapUp === null ? (
          <section className="wrapup-card">
            <p className="wrapup-loading">
              <span className="spinner" aria-hidden="true" />
              정리하는 중...
            </p>
          </section>
        ) : (
          <>
            <section className="wrapup-card">
              <div className="wrapup-card-head">
                <h3>상담 요약</h3>
                <span className="wrapup-badge">{wrapUp.category}</span>
              </div>
              <ul className="wrapup-summary">
                {wrapUp.summary.map((line) => (
                  <li key={line}>{line}</li>
                ))}
              </ul>
              {mode === "mock" ? (
                <p className="wrapup-note">
                  요약·유형·후속조치는 생성 모델이 아직 없어 mock 시나리오에 미리
                  적어둔 문장입니다. 발화 {utterances.length}건에서 뽑아낸 것이
                  아닙니다.
                </p>
              ) : null}
            </section>

            <section className="wrapup-card">
              <div className="wrapup-card-head">
                <h3>후속 조치</h3>
                <span className="wrapup-count">
                  {done.size}/{wrapUp.follow_ups.length}
                </span>
              </div>
              <ul className="followup-list">
                {wrapUp.follow_ups.map((item, index) => (
                  <li key={item}>
                    <button
                      type="button"
                      className={`followup-item${done.has(index) ? " done" : ""}`}
                      aria-pressed={done.has(index)}
                      onClick={() => {
                        toggle(index);
                      }}
                    >
                      <span className="followup-box" aria-hidden="true">
                        <CheckIcon />
                      </span>
                      <span className="followup-text">{item}</span>
                    </button>
                  </li>
                ))}
              </ul>
            </section>

            {cards.length > 0 ? (
              <section className="wrapup-card">
                <div className="wrapup-card-head">
                  <h3>카드 사용 현황</h3>
                </div>
                <div className="adopt-stats">
                  <div className="adopt-stat">
                    <span className="adopt-stat-num">{cards.length}</span>
                    <span className="adopt-stat-label">총 카드</span>
                  </div>
                  <div className="adopt-stat">
                    <span className="adopt-stat-num">{adopted.length}</span>
                    <span className="adopt-stat-label">채택</span>
                  </div>
                  <div className="adopt-stat">
                    <span className="adopt-stat-num">
                      {cards.length - adopted.length}
                    </span>
                    <span className="adopt-stat-label">무시</span>
                  </div>
                </div>
                {adopted.length > 0 ? (
                  <ul className="adopt-titles">
                    {adopted.map((item) => (
                      <li key={cardId(item.card)}>{item.card.title}</li>
                    ))}
                  </ul>
                ) : null}
                <p className="wrapup-note">
                  어떤 문서가 실제로 쓰였는지 지식베이스에 돌려주는 기록입니다.
                  상담 품질을 재는 값이 아닙니다.
                </p>
              </section>
            ) : null}

            {manualSearches.length > 0 ? (
              <section className="wrapup-card">
                <div className="wrapup-card-head">
                  <h3>지식베이스 공백</h3>
                </div>
                {failed.length > 0 ? (
                  <>
                    <p className="gap-headline">
                      이번 통화에서 검색 실패 {failed.length}건 발생
                    </p>
                    <ul className="gap-list">
                      {failed.map((entry, index) => (
                        <li key={`${entry.query}-${index}`}>{entry.query}</li>
                      ))}
                    </ul>
                    <p className="wrapup-note">
                      상담원이 직접 찾았는데 문서가 없던 질문입니다. 지식베이스
                      보강 후보로 남깁니다.
                    </p>
                  </>
                ) : (
                  <p className="gap-headline muted">
                    직접 검색 {manualSearches.length}건, 모두 문서를 찾았습니다.
                  </p>
                )}
              </section>
            ) : null}

            {wrapUp.sentiment !== undefined ? (
              <MoodSection sentiment={wrapUp.sentiment} isMock={mode === "mock"} />
            ) : null}
          </>
        )}
        </div>
      </div>
    </main>
  );
}

function moodTone(label: string): "calm" | "lift" | "peak" {
  if (label === "격앙") {
    return "peak";
  }
  if (label.includes("격앙")) {
    return "lift";
  }
  return "calm";
}

function MoodSection({
  sentiment,
  isMock,
}: {
  sentiment: SentimentSummary;
  isMock: boolean;
}): ReactElement {
  return (
    <section className="wrapup-card">
      <div className="wrapup-card-head">
        <h3>상담 분위기</h3>
        <span
          className={`mood-overall${sentiment.overall === "주의 필요" ? " is-watch" : ""}`}
        >
          {sentiment.overall}
        </span>
      </div>
      <ol className="mood-track" aria-label="통화 흐름">
        {sentiment.trajectory.map((label, index) => (
          <li key={`${label}-${index}`} className="mood-step">
            <span
              className={`mood-dot is-${moodTone(label)}`}
              aria-hidden="true"
            />
            <span className="mood-label">{label}</span>
          </li>
        ))}
      </ol>
      <p className="mood-guard">
        콜가드 경고 {sentiment.guard_flag_count}건
        {sentiment.guard_flag_count > 0
          ? " — 이번 통화에서 뜬 C-6 태그와 같은 수입니다."
          : " — 이 통화에는 콜가드 태그가 없습니다."}
      </p>
      {isMock ? (
        <p className="wrapup-note">
          감정분석 모델 연동 전 — mock 라벨입니다. 점수는 없습니다.
        </p>
      ) : null}
    </section>
  );
}

function CheckIcon(): ReactElement {
  return (
    <svg
      width="11"
      height="11"
      viewBox="0 0 16 16"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d="M3.4 8.2 6.5 11.1 12.6 4.8" />
    </svg>
  );
}
