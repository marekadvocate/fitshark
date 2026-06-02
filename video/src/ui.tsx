import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { BODY, C, HEAD } from "./theme";

/** Cream full-screen stage with generous padding. */
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
      padding: "0 160px",
      fontFamily: BODY,
      color: C.dark,
    }}
  >
    {children}
  </AbsoluteFill>
);

/** Fade + rise in, with a spring, after `delay` frames. */
export const FadeUp: React.FC<{
  delay?: number;
  y?: number;
  children: React.ReactNode;
  style?: React.CSSProperties;
}> = ({ delay = 0, y = 28, children, style }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame: frame - delay, fps, config: { damping: 200 } });
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

/** Fade OUT over the last `dur` frames of a sequence of length `total`. */
export const fadeOut = (frame: number, total: number, dur = 18) =>
  interpolate(frame, [total - dur, total], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

export const Kicker: React.FC<{ children: React.ReactNode; color?: string }> = ({
  children,
  color = C.clay,
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
    style={{
      fontFamily: HEAD,
      fontWeight: 600,
      fontSize: size,
      lineHeight: 1.08,
      letterSpacing: -1.5,
      ...style,
    }}
  >
    {children}
  </div>
);

export const Body: React.FC<{
  children: React.ReactNode;
  size?: number;
  style?: React.CSSProperties;
}> = ({ children, size = 38, style }) => (
  <div
    style={{ fontFamily: BODY, fontSize: size, lineHeight: 1.5, color: "#3c3a36", ...style }}
  >
    {children}
  </div>
);
