import { useState, type ReactElement } from "react";
import { AgentStandbyScreen } from "./components/AgentStandbyScreen";
import { AppHeader } from "./components/AppHeader";
import { CallSummaryHost } from "./components/CallSummaryPanel";
import { ForcePasswordSetup } from "./components/ForcePasswordSetup";
import { TermsPanel } from "./components/TermsPanel";
import { TranscriptPanel } from "./components/TranscriptPanel";
import { useGatewaySession } from "./hooks/useGatewaySession";
import {
  completeMockPasswordSetup,
  getMockAgentAccount,
} from "./mock/agentAuth";
import { useCallStore } from "./store/callStore";

export function App(): ReactElement {
  const { startCall, replay, leaveToStandby, manualSearch, endCall, wrapUp } =
    useGatewaySession();
  const [mustChangePassword, setMustChangePassword] = useState(
    () => getMockAgentAccount().mustChangePassword,
  );
  const phase = useCallStore((state) => state.phase);
  const shell = useCallStore((state) => state.shell);
  const viewMode = useCallStore((state) => state.viewMode);
  const summaryReturn = useCallStore((state) => state.summaryReturn);
  const resumeCall = useCallStore((state) => state.resumeCall);
  const resumeLive = useCallStore((state) => state.resumeLive);
  const enterStandby = useCallStore((state) => state.enterStandby);
  const showSummary = phase === "wrapup" || viewMode === "history";
  const agentName = getMockAgentAccount().name;

  function closeSummary(): void {
    if (viewMode === "history") {
      resumeLive();
      if (summaryReturn === "standby") {
        enterStandby();
      }
      return;
    }
    resumeCall();
  }

  if (mustChangePassword) {
    return (
      <div className="app-viewport">
        <div className="app-shell">
          <ForcePasswordSetup
            tempPasswordUsed
            onComplete={() => {
              completeMockPasswordSetup();
              setMustChangePassword(false);
            }}
          />
        </div>
      </div>
    );
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
              onLeaveToStandby={leaveToStandby}
            />
            <CallSummaryHost
              onClose={closeSummary}
              onStartNewCall={replay}
              onWrapUp={wrapUp}
            />
          </>
        ) : shell === "standby" ? (
          <AgentStandbyScreen
            agentName={agentName}
            onStartCall={startCall}
          />
        ) : (
          <main className="panels">
            <TranscriptPanel onManualSearch={manualSearch} />
            <TermsPanel
              onReplay={replay}
              onEndCall={endCall}
              onLeaveToStandby={leaveToStandby}
            />
          </main>
        )}
      </div>
    </div>
  );
}
