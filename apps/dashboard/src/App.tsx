import type { ReactElement } from "react";
import { AppHeader } from "./components/AppHeader";
import { TermsPanel } from "./components/TermsPanel";
import { TranscriptPanel } from "./components/TranscriptPanel";
import { CallSummaryHost } from "./components/CallSummaryPanel";
import { useGatewaySession } from "./hooks/useGatewaySession";
import { useCallStore } from "./store/callStore";

export function App(): ReactElement {
  const { replay, manualSearch, endCall, wrapUp } = useGatewaySession();
  const phase = useCallStore((state) => state.phase);
  const viewMode = useCallStore((state) => state.viewMode);
  const resumeCall = useCallStore((state) => state.resumeCall);
  const resumeLive = useCallStore((state) => state.resumeLive);
  const showSummary = phase === "wrapup" || viewMode === "history";

  function closeSummary(): void {
    if (viewMode === "history") {
      resumeLive();
      return;
    }
    resumeCall();
  }

  return (
    <div className="app-viewport">
      <div className="app-shell">
        {showSummary ? (
          <>
            <AppHeader
              onReplay={replay}
              onEndCall={endCall}
              onStartNewCall={replay}
            />
            <CallSummaryHost
              onClose={closeSummary}
              onStartNewCall={replay}
              onWrapUp={wrapUp}
            />
          </>
        ) : (
          <main className="panels">
            <TranscriptPanel onManualSearch={manualSearch} />
            <TermsPanel onReplay={replay} onEndCall={endCall} />
          </main>
        )}
      </div>
    </div>
  );
}
