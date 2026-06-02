import React from "react";
import {
  AbsoluteFill,
  Easing,
  Img,
  interpolate,
  OffthreadVideo,
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
  const p = spring({ frame: frame - delay, fps, durationInFrames: 10, config: { damping: 200 } });
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

/** Count up to `to` over `dur` frames starting at `delay`, with comma formatting. */
export const CountUp: React.FC<{ to: number; delay?: number; dur?: number; style?: React.CSSProperties }> = ({
  to,
  delay = 0,
  dur = 28,
  style,
}) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame - delay, [0, dur], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  const v = Math.round(p * to);
  return <span style={style}>{v.toLocaleString("en-US")}</span>;
};

/** Siri-style soft animated aura behind AI-feature moments. */
export const Glow: React.FC<{
  a?: string;
  b?: string;
  strength?: number;
  delay?: number;
  size?: number;
}> = ({ a = C.clay, b = C.shark, strength = 0.4, delay = 0, size = 1150 }) => {
  const frame = useCurrentFrame();
  const pulse = 0.5 + 0.5 * Math.sin((frame - delay) / 20);
  const op =
    interpolate(frame, [delay, delay + 18], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) *
    strength *
    (0.7 + 0.5 * pulse);
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
      <div
        style={{
          position: "absolute",
          width: size,
          height: size,
          borderRadius: "50%",
          background: `radial-gradient(circle at 50% 48%, ${a}, ${b} 42%, transparent 68%)`,
          filter: "blur(85px)",
          opacity: op,
          transform: `scale(${0.88 + 0.14 * pulse})`,
        }}
      />
    </AbsoluteFill>
  );
};

/** Word-by-word reveal (each word rises in, staggered). */
export const Words: React.FC<{
  text: string;
  size: number;
  color?: string;
  weight?: number;
  delay?: number;
  step?: number;
  style?: React.CSSProperties;
}> = ({ text, size, color = C.dark, weight = 600, delay = 0, step = 3, style }) => (
  <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", rowGap: size * 0.12, ...style }}>
    {text.split(" ").map((w, i) => (
      <FadeUp key={i} delay={delay + i * step} y={16} style={{ marginRight: size * 0.26 }}>
        <span style={{ fontFamily: HEAD, fontWeight: weight, fontSize: size, letterSpacing: -1, color, lineHeight: 1.05 }}>{w}</span>
      </FadeUp>
    ))}
  </div>
);

/** A framed app screenshot that scales + rises in. */
export const Shot: React.FC<{ src: string; w?: number; delay?: number }> = ({ src, w = 1080, delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame: frame - delay, fps, config: { damping: 18, mass: 0.8 } });
  return (
    <div
      style={{
        transform: `scale(${interpolate(p, [0, 1], [0.86, 1])}) translateY(${interpolate(p, [0, 1], [24, 0])}px)`,
        opacity: interpolate(p, [0, 1], [0, 1]),
        borderRadius: 16,
        overflow: "hidden",
        border: `1px solid ${C.lightGray}`,
        boxShadow: "0 40px 90px rgba(20,20,19,0.20)",
      }}
    >
      <Img src={staticFile(src)} style={{ width: w, display: "block" }} />
    </div>
  );
};

/** A framed app screen-recording that scales in, then plays through. */
export const Clip: React.FC<{ src: string; w?: number; delay?: number }> = ({ src, w = 1500, delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame: frame - delay, fps, config: { damping: 18, mass: 0.8 } });
  return (
    <div
      style={{
        transform: `scale(${interpolate(p, [0, 1], [0.92, 1])})`,
        opacity: interpolate(p, [0, 1], [0, 1]),
        borderRadius: 16,
        overflow: "hidden",
        border: `1px solid ${C.lightGray}`,
        boxShadow: "0 44px 100px rgba(20,20,19,0.22)",
      }}
    >
      <OffthreadVideo src={staticFile(src)} muted style={{ width: w, display: "block" }} />
    </div>
  );
};

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
