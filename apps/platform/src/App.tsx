import type { ReactElement } from "react";
import { Header } from "./components/Header";
import { Hero } from "./components/Hero";
import { Problem } from "./components/Problem";
import { Features } from "./components/Features";
import { Domains } from "./components/Domains";
import { TeamCta } from "./components/TeamCta";

export function App(): ReactElement {
  return (
    <>
      <Header />
      <main>
        <Hero />
        <Problem />
        <Features />
        <Domains />
        <TeamCta />
      </main>
    </>
  );
}
