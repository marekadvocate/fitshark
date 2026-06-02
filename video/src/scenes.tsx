import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { BODY, C, HEAD } from "./theme";
import { Body, FadeUp, fadeOut, H1, Kicker, Logo, PopIn, Stage } from "./ui";

type P = { len: number };
const NIGHT = "#0f2545";

/* 1 — OPEN */
export const S1: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(f, len), maxWidth: 1500, textAlign: "center" }}>
        <FadeUp delay={3}>
          <H1 size={92}>
            Every parts question is a sale
            <br />
            <span style={{ color: C.gray }}>waiting to happen.</span>
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
        <FadeUp delay={3}>
          <H1 size={120}>“Will this fit my car?”</H1>
        </FadeUp>
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
        <FadeUp delay={3}>
          <H1 size={86}>Answered in a day.</H1>
        </FadeUp>
        <FadeUp delay={16} style={{ marginTop: 10 }}>
          <H1 size={86} style={{ color: C.blue }}>Or never.</H1>
        </FadeUp>
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
        <PopIn delay={1} style={{ display: "flex", justifyContent: "center" }}>
          <Logo size={300} />
        </PopIn>
        <FadeUp delay={18} style={{ marginTop: 4 }}>
          <div style={{ fontFamily: HEAD, fontWeight: 700, fontSize: 130, color: C.blue, letterSpacing: -3 }}>Fitshark</div>
        </FadeUp>
      </div>
    </Stage>
  );
};

/* 5 — UNDERSTANDS */
export const S5: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(f, len), textAlign: "center", maxWidth: 1500 }}>
        <FadeUp delay={3}>
          <H1 size={88}>It gets what they mean.</H1>
        </FadeUp>
        <FadeUp delay={18} style={{ marginTop: 18 }}>
          <Body size={44} style={{ color: C.gray }}>Even what they don&apos;t say.</Body>
        </FadeUp>
      </div>
    </Stage>
  );
};

/* 6 — THE MARKET (big number) */
export const S6: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(f, len), textAlign: "center", width: "100%" }}>
        <PopIn delay={2}>
          <div style={{ fontFamily: HEAD, fontWeight: 700, fontSize: 200, color: C.blue, letterSpacing: -4, lineHeight: 1 }}>
            110,000
          </div>
        </PopIn>
        <FadeUp delay={18} style={{ marginTop: 8 }}>
          <H1 size={56}>parts. Every supplier. <span style={{ color: C.gray }}>One best answer.</span></H1>
        </FadeUp>
      </div>
    </Stage>
  );
};

/* 7 — THE WOW (dark, out-of-stock) */
export const S7: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: NIGHT, justifyContent: "center", alignItems: "center", padding: "0 150px" }}>
      <div style={{ opacity: fadeOut(f, len), textAlign: "center", maxWidth: 1550 }}>
        <FadeUp delay={3}>
          <div style={{ fontFamily: HEAD, fontWeight: 600, fontSize: 44, color: "#9fb6d8" }}>Out of stock?</div>
        </FadeUp>
        <FadeUp delay={16} style={{ marginTop: 18 }}>
          <div style={{ fontFamily: HEAD, fontWeight: 700, fontSize: 110, color: "#fff", letterSpacing: -2, lineHeight: 1.05 }}>
            It orders it <span style={{ color: C.gold }}>anyway.</span>
          </div>
        </FadeUp>
        <FadeUp delay={40} style={{ marginTop: 26 }}>
          <div style={{ fontFamily: BODY, fontSize: 38, color: "#c7d4e8" }}>
            Sources the part, places the order — turns a dead end into a sale.
          </div>
        </FadeUp>
      </div>
    </AbsoluteFill>
  );
};

/* 8 — THE REPLY (hero) */
export const S8: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(f, len), display: "flex", gap: 80, alignItems: "center", width: "100%" }}>
        <div style={{ flex: 1 }}>
          <FadeUp delay={3}>
            <H1 size={70}>A flawless reply.</H1>
          </FadeUp>
          <FadeUp delay={18} style={{ marginTop: 18 }}>
            <Body size={40} style={{ color: "#3c3a36" }}>
              Their language. A price, a date, and <span style={{ color: C.blue }}>one tap to buy.</span>
            </Body>
          </FadeUp>
          <FadeUp delay={40} style={{ marginTop: 22 }}>
            <Body size={30} style={{ color: C.green }}>In seconds.</Body>
          </FadeUp>
        </div>
        <PopIn delay={10} style={{ flexShrink: 0 }}>
          <div style={{ width: 560, background: "#fff", borderRadius: 20, border: `1px solid ${C.lightGray}`, overflow: "hidden", boxShadow: "0 34px 64px rgba(20,20,19,0.12)" }}>
            <div style={{ background: C.blue, padding: "16px 26px", fontFamily: HEAD, fontWeight: 700, fontSize: 26, color: "#fff", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <span>Fitshark</span><span style={{ fontFamily: HEAD, fontSize: 15, background: C.gold, color: "#3a2c06", padding: "3px 12px", borderRadius: 20 }}>ON ORDER</span>
            </div>
            <div style={{ padding: 30 }}>
              <div style={{ fontFamily: HEAD, fontWeight: 600, fontSize: 25, color: C.dark }}>Vaša H7 žiarovka Philips — objednáme pre vás</div>
              <div style={{ background: C.cream, borderRadius: 14, padding: "16px 20px", marginTop: 18, border: `1px solid ${C.lightGray}`, fontFamily: BODY, fontSize: 23, color: C.dark }}>
                <div><b>Cena:</b> 17,81 € s DPH</div>
                <div><b>Dodanie:</b> na objednávku · 7 dní</div>
              </div>
              <div style={{ marginTop: 20, background: C.blue, color: "#fff", fontFamily: HEAD, fontWeight: 600, fontSize: 23, textAlign: "center", padding: "15px 0", borderRadius: 12 }}>Objednať →</div>
            </div>
          </div>
        </PopIn>
      </div>
    </Stage>
  );
};

/* 9 — HUMAN */
export const S9: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(f, len), textAlign: "center" }}>
        <FadeUp delay={3}>
          <H1 size={96}>You approve. <span style={{ color: C.blue }}>It sends.</span></H1>
        </FadeUp>
      </div>
    </Stage>
  );
};

/* 10 — PAYOFF */
export const S10: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(f, len), textAlign: "center", maxWidth: 1500 }}>
        <FadeUp delay={3}>
          <H1 size={94}>Browsers become <span style={{ color: C.gold }}>buyers.</span></H1>
        </FadeUp>
        <FadeUp delay={18} style={{ marginTop: 18 }}>
          <Body size={42} style={{ color: C.gray }}>Automatically. Around the clock.</Body>
        </FadeUp>
      </div>
    </Stage>
  );
};

/* 11 — CLOSE */
export const S11: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(f, len, 22), textAlign: "center", width: "100%" }}>
        <PopIn delay={2} style={{ display: "flex", justifyContent: "center" }}>
          <Logo size={190} />
        </PopIn>
        <FadeUp delay={18} style={{ marginTop: 2 }}>
          <div style={{ fontFamily: HEAD, fontWeight: 700, fontSize: 92, color: C.blue, letterSpacing: -2 }}>Fitshark</div>
        </FadeUp>
        <FadeUp delay={30} style={{ marginTop: 8 }}>
          <Body size={38}>From question to sale.</Body>
        </FadeUp>
        <FadeUp delay={42} style={{ marginTop: 10 }}>
          <Body size={24} style={{ color: C.gray }}>built on Duvo</Body>
        </FadeUp>
      </div>
    </Stage>
  );
};
