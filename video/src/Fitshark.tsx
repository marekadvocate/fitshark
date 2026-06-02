import React from "react";
import { AbsoluteFill, Series } from "remotion";
import { C } from "./theme";
import { Hook, Problem, Intro, HowItWorks, Reply, Results, Close } from "./scenes";

const S = [
  { c: Hook, len: 360 },
  { c: Problem, len: 360 },
  { c: Intro, len: 420 },
  { c: HowItWorks, len: 1080 },
  { c: Reply, len: 660 },
  { c: Results, len: 420 },
  { c: Close, len: 300 },
];

export const Fitshark: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.cream }}>
    <Series>
      {S.map(({ c: Comp, len }, i) => (
        <Series.Sequence key={i} durationInFrames={len}>
          <Comp len={len} />
        </Series.Sequence>
      ))}
    </Series>
  </AbsoluteFill>
);
