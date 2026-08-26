import type { ReactElement } from "react";
import { AppHeader } from "./components/AppHeader";
import { BookmarkDock } from "./components/BookmarkDock";
import { ClosureModal } from "./components/ClosureModal";
import { MaskingLogPanel } from "./components/MaskingLogPanel";
import { TranscriptPanel } from "./components/TranscriptPanel";
import { useGatewaySession } from "./hooks/useGatewaySession";

export function App(): ReactElement {
  const { replay } = useGatewaySession();

  return (
    <div className="app-shell">
      <AppHeader onReplay={replay} />
      <main className="panels">
        <TranscriptPanel />
        <MaskingLogPanel />
      </main>
      <BookmarkDock />
      <ClosureModal />
    </div>
  );
}
