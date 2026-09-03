import type { ReactElement } from "react";
import { CTASection } from "./components/CTASection";
import { FeatureGrid } from "./components/FeatureGrid";
import { Footer } from "./components/Footer";
import { Hero } from "./components/Hero";
import { HowItWorks } from "./components/HowItWorks";
import { Nav } from "./components/Nav";
import { ProblemSection } from "./components/ProblemSection";
import { StatsStrip } from "./components/StatsStrip";

export function App(): ReactElement {
  return (
    <>
      <Nav />
      <main>
        <Hero />
        <ProblemSection />
        <FeatureGrid />
        <HowItWorks />
        <StatsStrip />
        <CTASection />
      </main>
      <Footer />
    </>
  );
}
