import React from "react";
import {
  AbsoluteFill,
  Img,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { BODY, C, HEAD } from "./theme";

export const Stage: React.FC<{
  children: React.ReactNode;
  bg?: string;
  align?: "center" | "flex-start";
}> = ({ children, bg = C.cream, align = "center" }) => (
  <AbsoluteFill
    style={{
      backgroundColor: bg,
      justifyContent: "center",
      alignItems: align,
      padding: "0 150px",
      fontFamily: BODY,
      color: C.dark,
    }}
  >
    {children}
  </AbsoluteFill>
);

/** Snappy fade + rise (settles in ~0.5s, no bounce). */
export const FadeUp: React.FC<{
  delay?: number;
  y?: number;
  children: React.ReactNode;
  style?: React.CSSProperties;
}> = ({ delay = 0, y = 22, children, style }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame: frame - delay, fps, durationInFrames: 16, config: { damping: 200 } });
  return (
    <div
      style={{
        opacity: interpolate(p, [0, 1], [0, 1]),
        transform: `translateY(${interpolate(p, [0, 1], [y, 0])}px)`,
        ...style,
      }}
    >
      {children}
    </div>
  );
};

/** Spring scale-in (for logo / hero pops). */
export const PopIn: React.FC<{
  delay?: number;
  children: React.ReactNode;
  style?: React.CSSProperties;
}> = ({ delay = 0, children, style }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame: frame - delay, fps, config: { damping: 14, mass: 0.7 } });
  return (
    <div style={{ opacity: interpolate(p, [0, 1], [0, 1]), transform: `scale(${interpolate(p, [0, 1], [0.7, 1])})`, ...style }}>
      {children}
    </div>
  );
};

export const fadeOut = (frame: number, total: number, dur = 14) =>
  interpolate(frame, [total - dur, total], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

export const Logo: React.FC<{ size?: number }> = ({ size = 220 }) => (
  <Img src={staticFile("logo.png")} style={{ width: size, height: size, objectFit: "contain" }} />
);

export const Kicker: React.FC<{ children: React.ReactNode; color?: string }> = ({
  children,
  color = C.blue,
}) => (
  <div
    style={{
      fontFamily: HEAD,
      fontWeight: 600,
      letterSpacing: 3,
      textTransform: "uppercase",
      fontSize: 22,
      color,
    }}
  >
    {children}
  </div>
);

export const H1: React.FC<{
  children: React.ReactNode;
  size?: number;
  style?: React.CSSProperties;
}> = ({ children, size = 84, style }) => (
  <div
    style={{ fontFamily: HEAD, fontWeight: 600, fontSize: size, lineHeight: 1.08, letterSpacing: -1.5, ...style }}
  >
    {children}
  </div>
);

export const Body: React.FC<{
  children: React.ReactNode;
  size?: number;
  style?: React.CSSProperties;
}> = ({ children, size = 38, style }) => (
  <div style={{ fontFamily: BODY, fontSize: size, lineHeight: 1.5, color: "#3c3a36", ...style }}>
    {children}
  </div>
);
