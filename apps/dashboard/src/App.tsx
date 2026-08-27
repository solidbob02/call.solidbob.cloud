import type { ReactElement } from "react";
import { AppHeader } from "./components/AppHeader";
import { TermsPanel } from "./components/TermsPanel";
import { TranscriptPanel } from "./components/TranscriptPanel";
import { WrapUpPanel } from "./components/WrapUpPanel";
import { useGatewaySession } from "./hooks/useGatewaySession";
import { useCallStore } from "./store/callStore";

export function App(): ReactElement {
  const { replay, manualSearch, endCall, wrapUp } = useGatewaySession();
  const phase = useCallStore((state) => state.phase);
  const resumeCall = useCallStore((state) => state.resumeCall);

  return (
    <div className="app-viewport">
      <div className="app-shell">
        <AppHeader onReplay={replay} onEndCall={endCall} />
        {phase === "wrapup" ? (
          <WrapUpPanel
            onResume={resumeCall}
            onRestart={replay}
            onWrapUp={wrapUp}
          />
        ) : (
          <main className="panels">
            <TranscriptPanel />
            <TermsPanel onManualSearch={manualSearch} />
          </main>
        )}
      </div>
    </div>
  );
}
