import React from "react";
import { AbsoluteFill, Audio, interpolate, Series, staticFile, useCurrentFrame } from "remotion";
import { C } from "./theme";
import { S1, S2, S3, S4, STech, S5, SLang, S6, S7, SPar, S8, SMore, SFollow, S9, S10, S11 } from "./scenes";

// Beat-synced to the music (~128 BPM → 14 frames/beat). Cuts land on the beat.
const BEAT = 14;
const S = [
  { c: S1, beats: 8 },     // open
  { c: S2, beats: 7 },     // the question
  { c: S3, beats: 6 },     // the gap
  { c: S4, beats: 8 },     // logo reveal
  { c: STech, beats: 9 },  // agentic pipeline on Duvo
  { c: S5, beats: 7 },     // understands
  { c: SLang, beats: 8 },  // multilingual cycle
  { c: S6, beats: 8 },     // 110,000 motor parts (count-up)
  { c: S7, beats: 10 },    // WOW: out of stock -> ordered (dark)
  { c: SPar, beats: 8 },   // parallel — concurrency 10
  { c: S8, beats: 12 },    // the reply (hero)
  { c: SMore, beats: 7 },  // quote + upsell
  { c: SFollow, beats: 7 },// follow-up + CRM
  { c: S9, beats: 6 },     // you approve, it sends
  { c: S10, beats: 8 },    // browsers become buyers
  { c: S11, beats: 10 },   // close
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
