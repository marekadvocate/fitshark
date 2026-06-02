import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { BODY, C, HEAD } from "./theme";
import { Body, CountUp, FadeUp, fadeOut, H1, Logo, PopIn, Stage } from "./ui";

type P = { len: number };
const MONO = "ui-monospace, SFMono-Regular, Menlo, monospace";

const Tag: React.FC<{ children: React.ReactNode; size?: number }> = ({ children, size = 21 }) => (
  <span style={{ fontFamily: MONO, fontSize: size, color: "#7a4a36", background: "#f3e3da", padding: "8px 14px", borderRadius: 9 }}>
    {children}
  </span>
);

/* 1 — OPEN */
export const S1: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(f, len), maxWidth: 1550, textAlign: "center" }}>
        <FadeUp delay={2}>
          <H1 size={90}>
            Every motor-parts question is a sale
            <br />
            <span style={{ color: C.clay }}>waiting to happen.</span>
          </H1>
        </FadeUp>
      </div>
    </Stage>
  );
};

/* 2 — THE QUESTION */
export const S2: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(f, len), textAlign: "center" }}>
        <FadeUp delay={2}><H1 size={120}>“Will this fit my car?”</H1></FadeUp>
      </div>
    </Stage>
  );
};

/* 3 — THE GAP */
export const S3: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(f, len), textAlign: "center" }}>
        <FadeUp delay={2}><H1 size={86}>Answered in a day.</H1></FadeUp>
        <FadeUp delay={11} style={{ marginTop: 10 }}><H1 size={86} style={{ color: C.clay }}>Or never.</H1></FadeUp>
      </div>
    </Stage>
  );
};

/* 4 — LOGO REVEAL */
export const S4: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(f, len), textAlign: "center", width: "100%" }}>
        <PopIn delay={1} style={{ display: "flex", justifyContent: "center" }}><Logo size={300} /></PopIn>
        <FadeUp delay={12} style={{ marginTop: 8 }}>
          <div style={{ fontFamily: HEAD, fontWeight: 700, fontSize: 130, color: C.shark, letterSpacing: -3 }}>Fitshark</div>
        </FadeUp>
      </div>
    </Stage>
  );
};

/* 5 — TECH PIPELINE */
export const STech: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  const steps = ["customer question", "Case Queue", "parallel agents", "grep 11 feeds", "human-approved", "sent + ordered"];
  return (
    <Stage>
      <div style={{ opacity: fadeOut(f, len), textAlign: "center", width: "100%", maxWidth: 1640 }}>
        <FadeUp delay={2}>
          <Body size={30} style={{ color: C.sub, fontFamily: HEAD, letterSpacing: 2, textTransform: "uppercase" }}>An agentic pipeline on Duvo</Body>
        </FadeUp>
        <div style={{ marginTop: 28, display: "flex", gap: 10, alignItems: "center", justifyContent: "center", flexWrap: "wrap" }}>
          {steps.map((s, i) => (
            <FadeUp key={s} delay={8 + i * 7} style={{ display: "flex", gap: 10, alignItems: "center" }}>
              <Tag>{s}</Tag>
              {i < steps.length - 1 && <span style={{ color: C.clay, fontFamily: HEAD, fontSize: 26 }}>→</span>}
            </FadeUp>
          ))}
        </div>
        <FadeUp delay={56} style={{ marginTop: 28 }}>
          <Body size={32}>110,000 motor parts · 11 suppliers · grounded in real data.</Body>
        </FadeUp>
      </div>
    </Stage>
  );
};

/* 6 — UNDERSTANDS */
export const S5: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(f, len), textAlign: "center", maxWidth: 1500 }}>
        <FadeUp delay={2}><H1 size={88}>It gets what they mean.</H1></FadeUp>
        <FadeUp delay={11} style={{ marginTop: 18 }}><Body size={44} style={{ color: C.sub }}>Even what they don&apos;t say.</Body></FadeUp>
      </div>
    </Stage>
  );
};

/* 7 — MULTILINGUAL (animated cycle) */
export const SLang: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  const phrases: [string, string][] = [
    ["Sadne mi to?", "SK"],
    ["Padne mi to?", "CZ"],
    ["Will it fit?", "EN"],
    ["Passt das?", "DE"],
    ["Czy pasuje?", "PL"],
  ];
  const start = 14, per = 16;
  const idx = Math.min(Math.max(0, Math.floor((f - start) / per)), phrases.length - 1);
  const local = f - start - idx * per;
  const op = interpolate(local, [0, 5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <Stage>
      <div style={{ opacity: fadeOut(f, len), textAlign: "center", width: "100%" }}>
        <FadeUp delay={2}><H1 size={70}>In their language.</H1></FadeUp>
        <div style={{ marginTop: 30, opacity: op }}>
          <span style={{ fontFamily: HEAD, fontWeight: 700, fontSize: 84, color: C.clay }}>{phrases[idx][0]}</span>
          <span style={{ fontFamily: MONO, fontSize: 30, color: C.sub, marginLeft: 18 }}>{phrases[idx][1]}</span>
        </div>
      </div>
    </Stage>
  );
};

/* 8 — THE MARKET (count-up) */
export const S6: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(f, len), textAlign: "center", width: "100%" }}>
        <PopIn delay={2}>
          <div style={{ fontFamily: HEAD, fontWeight: 700, fontSize: 200, color: C.clay, letterSpacing: -4, lineHeight: 1 }}>
            <CountUp to={110000} delay={6} dur={34} />
          </div>
        </PopIn>
        <FadeUp delay={42} style={{ marginTop: 8 }}>
          <H1 size={56}>motor parts. Every supplier. <span style={{ color: C.sub }}>One best answer.</span></H1>
        </FadeUp>
      </div>
    </Stage>
  );
};

/* 9 — WOW (dark) */
export const S7: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: C.dark, justifyContent: "center", alignItems: "center", padding: "0 150px" }}>
      <div style={{ opacity: fadeOut(f, len), textAlign: "center", maxWidth: 1550 }}>
        <FadeUp delay={2}><div style={{ fontFamily: HEAD, fontWeight: 600, fontSize: 44, color: C.gray }}>Out of stock?</div></FadeUp>
        <FadeUp delay={11} style={{ marginTop: 18 }}>
          <div style={{ fontFamily: HEAD, fontWeight: 700, fontSize: 110, color: C.cream, letterSpacing: -2, lineHeight: 1.05 }}>
            It orders it <span style={{ color: C.clay }}>anyway.</span>
          </div>
        </FadeUp>
        <FadeUp delay={28} style={{ marginTop: 24 }}>
          <div style={{ fontFamily: BODY, fontSize: 38, color: "#cdcabf" }}>Sources the part, places the order — turns a dead end into a sale.</div>
        </FadeUp>
      </div>
    </AbsoluteFill>
  );
};

/* 10 — PARALLEL (animated jobs) */
export const SPar: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(f, len), textAlign: "center", width: "100%" }}>
        <FadeUp delay={2}><H1 size={80}>10 inquiries. <span style={{ color: C.clay }}>At once.</span></H1></FadeUp>
        <FadeUp delay={11} style={{ marginTop: 12 }}>
          <Body size={28} style={{ color: C.sub, fontFamily: MONO }}>Case Queue · concurrency 10</Body>
        </FadeUp>
        <div style={{ marginTop: 36, display: "flex", gap: 12, justifyContent: "center", flexWrap: "wrap", maxWidth: 1300, marginLeft: "auto", marginRight: "auto" }}>
          {Array.from({ length: 10 }).map((_, i) => (
            <PopIn key={i} delay={20 + i * 4}>
              <div style={{ width: 110, height: 64, borderRadius: 12, background: "#fff", border: `2px solid ${C.clay}`, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: MONO, fontSize: 17, color: "#7a4a36" }}>
                job {i + 1}
              </div>
            </PopIn>
          ))}
        </div>
      </div>
    </Stage>
  );
};

/* 11 — THE REPLY (hero) */
export const S8: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(f, len), display: "flex", gap: 80, alignItems: "center", width: "100%" }}>
        <div style={{ flex: 1 }}>
          <FadeUp delay={2}><H1 size={70}>A flawless reply.</H1></FadeUp>
          <FadeUp delay={11} style={{ marginTop: 18 }}>
            <Body size={40}>Their language. A price, a date, and <span style={{ color: C.clay }}>one tap to buy.</span></Body>
          </FadeUp>
          <FadeUp delay={26} style={{ marginTop: 22 }}><Body size={30} style={{ color: C.green }}>In seconds.</Body></FadeUp>
        </div>
        <PopIn delay={8} style={{ flexShrink: 0 }}>
          <div style={{ width: 560, background: "#fff", borderRadius: 20, border: `1px solid ${C.lightGray}`, overflow: "hidden", boxShadow: "0 34px 64px rgba(20,20,19,0.12)" }}>
            <div style={{ background: C.clay, padding: "16px 26px", fontFamily: HEAD, fontWeight: 700, fontSize: 26, color: "#fff", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <span>Fitshark</span><span style={{ fontFamily: HEAD, fontSize: 15, background: "#fff", color: C.clay, padding: "3px 12px", borderRadius: 20 }}>ON ORDER</span>
            </div>
            <div style={{ padding: 30 }}>
              <div style={{ fontFamily: HEAD, fontWeight: 600, fontSize: 25, color: C.dark }}>Vaša H7 žiarovka Philips — objednáme pre vás</div>
              <div style={{ background: C.cream, borderRadius: 14, padding: "16px 20px", marginTop: 18, border: `1px solid ${C.lightGray}`, fontFamily: BODY, fontSize: 23, color: C.dark }}>
                <div><b>Cena:</b> 17,81 € s DPH</div>
                <div><b>Dodanie:</b> na objednávku · 7 dní</div>
              </div>
              <div style={{ marginTop: 20, background: C.clay, color: "#fff", fontFamily: HEAD, fontWeight: 600, fontSize: 23, textAlign: "center", padding: "15px 0", borderRadius: 12 }}>Objednať →</div>
            </div>
          </div>
        </PopIn>
      </div>
    </Stage>
  );
};

/* 12 — QUOTE + UPSELL */
export const SMore: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(f, len), textAlign: "center", width: "100%", maxWidth: 1500 }}>
        <FadeUp delay={2}><H1 size={78}>Not just an answer.</H1></FadeUp>
        <div style={{ marginTop: 34, display: "flex", gap: 22, justifyContent: "center", flexWrap: "wrap" }}>
          <FadeUp delay={12}><Tag size={28}>📎 branded PDF quote</Tag></FadeUp>
          <FadeUp delay={22}><Tag size={28}>＋ relevant upsell</Tag></FadeUp>
          <FadeUp delay={32}><Tag size={28}>1-tap order link</Tag></FadeUp>
        </div>
        <FadeUp delay={44} style={{ marginTop: 28 }}><Body size={34} style={{ color: C.sub }}>A bigger basket, every time.</Body></FadeUp>
      </div>
    </Stage>
  );
};

/* 13 — FOLLOW-UP */
export const SFollow: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(f, len), textAlign: "center", maxWidth: 1500 }}>
        <FadeUp delay={2}><H1 size={84}>No reply? <span style={{ color: C.clay }}>It follows up.</span></H1></FadeUp>
        <FadeUp delay={12} style={{ marginTop: 18 }}><Body size={36} style={{ color: C.sub }}>And remembers the car — for the next sale.</Body></FadeUp>
      </div>
    </Stage>
  );
};

/* 14 — HUMAN */
export const S9: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(f, len), textAlign: "center" }}>
        <FadeUp delay={2}><H1 size={96}>You approve. <span style={{ color: C.clay }}>It sends.</span></H1></FadeUp>
      </div>
    </Stage>
  );
};

/* 15 — PAYOFF */
export const S10: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(f, len), textAlign: "center", maxWidth: 1500 }}>
        <FadeUp delay={2}><H1 size={94}>Browsers become <span style={{ color: C.clay }}>buyers.</span></H1></FadeUp>
        <FadeUp delay={12} style={{ marginTop: 18 }}><Body size={42} style={{ color: C.sub }}>Automatically. Around the clock.</Body></FadeUp>
      </div>
    </Stage>
  );
};

/* 16 — CLOSE */
export const S11: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(f, len, 20), textAlign: "center", width: "100%" }}>
        <PopIn delay={1} style={{ display: "flex", justifyContent: "center" }}><Logo size={190} /></PopIn>
        <FadeUp delay={12} style={{ marginTop: 2 }}>
          <div style={{ fontFamily: HEAD, fontWeight: 700, fontSize: 92, color: C.shark, letterSpacing: -2 }}>Fitshark</div>
        </FadeUp>
        <FadeUp delay={22} style={{ marginTop: 8 }}><Body size={38}>From question to sale.</Body></FadeUp>
        <FadeUp delay={32} style={{ marginTop: 10 }}><Body size={24} style={{ color: C.sub }}>built on Duvo</Body></FadeUp>
      </div>
    </Stage>
  );
};
