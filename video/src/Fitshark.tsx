import React from "react";
import { AbsoluteFill, Audio, interpolate, Series, staticFile, useCurrentFrame } from "remotion";
import { C } from "./theme";
import { Hook, Cost, Intro, HowItWorks, KeyValue, Reply, Results, Close } from "./scenes";

const S = [
  { c: Hook, len: 270 },
  { c: Cost, len: 270 },
  { c: Intro, len: 300 },
  { c: HowItWorks, len: 720 },
  { c: KeyValue, len: 420 },
  { c: Reply, len: 480 },
  { c: Results, len: 300 },
  { c: Close, len: 270 },
];

export const TOTAL = S.reduce((a, s) => a + s.len, 0); // 3030

const Music: React.FC = () => {
  const frame = useCurrentFrame();
  const v = interpolate(frame, [0, 40, TOTAL - 60, TOTAL], [0, 0.2, 0.2, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return <Audio src={staticFile("music.mp3")} volume={v} loop />;
};

export const Fitshark: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.cream }}>
    <Music />
    <Series>
      {S.map(({ c: Comp, len }, i) => (
        <Series.Sequence key={i} durationInFrames={len}>
          <Comp len={len} />
        </Series.Sequence>
      ))}
    </Series>
  </AbsoluteFill>
);
