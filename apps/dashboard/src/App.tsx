import type { ReactElement } from "react";
import { AppHeader } from "./components/AppHeader";
import { TermsPanel } from "./components/TermsPanel";
import { TranscriptPanel } from "./components/TranscriptPanel";
import { useGatewaySession } from "./hooks/useGatewaySession";

export function App(): ReactElement {
  const { replay } = useGatewaySession();

  return (
    <div className="app-viewport">
      <div className="app-shell">
        <AppHeader onReplay={replay} />
        <main className="panels">
          <TranscriptPanel />
          <TermsPanel />
        </main>
      </div>
    </div>
  );
}
