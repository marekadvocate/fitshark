import React from "react";
import { AbsoluteFill, Audio, interpolate, Series, staticFile, useCurrentFrame } from "remotion";
import { C } from "./theme";
import { Hook, Cost, Intro, HowItWorks, KeyValue, Reply, Results, Close } from "./scenes";

// Beat-synced to the music (~128 BPM → 14 frames/beat). Each scene length is a
// whole number of beats, so slide changes land on the beat. (beats shown in comments)
const BEAT = 14;
const S = [
  { c: Hook, beats: 12 },        // title
  { c: Cost, beats: 10 },        // problem
  { c: Intro, beats: 28 },       // architecture
  { c: HowItWorks, beats: 18 },  // parallel / concurrency 10
  { c: KeyValue, beats: 18 },    // grounded matching
  { c: Reply, beats: 26 },       // core: out-of-stock -> ordered
  { c: Results, beats: 18 },     // after the send
  { c: Close, beats: 16 },       // close / stack
].map((s) => ({ c: s.c, len: s.beats * BEAT }));

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
