import React from "react";
import { AbsoluteFill, Audio, interpolate, Series, staticFile, useCurrentFrame } from "remotion";
import { C } from "./theme";
import { S1, S2, S3, S4, STech, S5, SLang, S6, S7, SFeeds, SSkills, Sk1, Sk2, Sk3, Sk4, Sk5, Sk6, Sk7, Sk8, SPar, S8, SApprove, SFollow, SRemember, S10, S11 } from "./scenes";

// Beat-synced to the music (~128 BPM → 14 frames/beat). Cuts land on the beat.
const BEAT = 14;
const S = [
  { c: S1, beats: 9 },        // open (word-by-word)
  { c: S2, beats: 7 },        // the question
  { c: S3, beats: 6 },        // the gap
  { c: S4, beats: 8 },        // logo reveal
  { c: STech, beats: 10 },    // agentic pipeline on Duvo
  { c: S5, beats: 7 },        // understands
  { c: SLang, beats: 12 },    // funny customer questions
  { c: S6, beats: 8 },        // 110,000 motor parts (count-up)
  { c: S7, beats: 10 },       // WOW: out of stock -> ordered (dark)
  { c: SFeeds, beats: 9 },    // 11 feeds — animated bar graph (dark)
  { c: SSkills, beats: 8 },   // composable skills (overview grid)
  { c: Sk1, beats: 8 },       // Fitment Decision
  { c: Sk2, beats: 8 },       // Reply Writer
  { c: Sk3, beats: 8 },       // Email Template
  { c: Sk4, beats: 8 },       // Quote PDF
  { c: Sk5, beats: 8 },       // Upsell Recommender
  { c: Sk6, beats: 8 },       // Offer Personalizer
  { c: Sk7, beats: 8 },       // Product Link
  { c: Sk8, beats: 8 },       // Brand Voice
  { c: SPar, beats: 8 },      // parallel — concurrency 10
  { c: S8, beats: 42 },       // the reply — full product demo (plays through, ~19s)
  { c: SApprove, beats: 14 }, // you approve, it sends (real Duvo HITL)
  { c: SFollow, beats: 6 },   // follow-up
  { c: SRemember, beats: 13 },// remembers the car (real CRM)
  { c: S10, beats: 8 },       // browsers become buyers
  { c: S11, beats: 11 },      // close
].map((s) => ({ c: s.c, len: s.beats * BEAT }));

export const TOTAL = S.reduce((a, s) => a + s.len, 0); // 260 beats × 14 = 3640

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
