import React from "react";
import { AbsoluteFill, Audio, interpolate, Series, staticFile, useCurrentFrame } from "remotion";
import { C } from "./theme";
import { S1, S2, S3, S4, STech, S5, S6, S7, S8, S9, S10, S11 } from "./scenes";

// Beat-synced to the music (~128 BPM → 14 frames/beat). Cuts land on the beat.
const BEAT = 14;
const S = [
  { c: S1, beats: 9 },    // open
  { c: S2, beats: 9 },    // the question
  { c: S3, beats: 7 },    // the gap
  { c: S4, beats: 11 },   // logo reveal
  { c: STech, beats: 12 },// how it works (agentic pipeline on Duvo)
  { c: S5, beats: 9 },    // understands
  { c: S6, beats: 11 },   // 110,000 parts
  { c: S7, beats: 13 },   // WOW: out of stock -> ordered (dark)
  { c: S8, beats: 15 },   // the reply (hero)
  { c: S9, beats: 7 },    // you approve, it sends
  { c: S10, beats: 11 },  // browsers become buyers
  { c: S11, beats: 13 },  // close
].map((s) => ({ c: s.c, len: s.beats * BEAT }));

export const TOTAL = S.reduce((a, s) => a + s.len, 0); // 1610

const Music: React.FC = () => {
  const frame = useCurrentFrame();
  const v = interpolate(frame, [0, 36, TOTAL - 56, TOTAL], [0, 0.22, 0.22, 0], {
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
