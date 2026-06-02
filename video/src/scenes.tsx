import React from "react";
import { useCurrentFrame } from "remotion";
import { BODY, C, HEAD } from "./theme";
import { Body, FadeUp, fadeOut, H1, Kicker, Stage } from "./ui";

type SceneProps = { len: number };

/* 1 — HOOK */
export const Hook: React.FC<SceneProps> = ({ len }) => {
  const frame = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(frame, len), maxWidth: 1400 }}>
        <FadeUp delay={4}>
          <Kicker>A pre-purchase question</Kicker>
        </FadeUp>
        <FadeUp delay={16} style={{ marginTop: 28 }}>
          <H1 size={96}>“Does this part fit my car?”</H1>
        </FadeUp>
        <FadeUp delay={64} style={{ marginTop: 40 }}>
          <Body size={42}>Today it&apos;s answered a day later. Or never.</Body>
        </FadeUp>
      </div>
    </Stage>
  );
};

/* 2 — PROBLEM */
export const Problem: React.FC<SceneProps> = ({ len }) => {
  const frame = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(frame, len), maxWidth: 1400 }}>
        <FadeUp delay={4}>
          <H1 size={82}>
            Every unanswered fitment question
            <br />
            is a <span style={{ color: C.clay }}>lost sale.</span>
          </H1>
        </FadeUp>
        <FadeUp delay={54} style={{ marginTop: 40 }}>
          <Body>The customer moves on. The shelf stays full.</Body>
        </FadeUp>
      </div>
    </Stage>
  );
};

/* 3 — INTRO */
export const Intro: React.FC<SceneProps> = ({ len }) => {
  const frame = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(frame, len), textAlign: "center", width: "100%" }}>
        <FadeUp delay={4}>
          <Kicker>Meet</Kicker>
        </FadeUp>
        <FadeUp delay={16} style={{ marginTop: 20 }}>
          <div style={{ fontFamily: HEAD, fontWeight: 700, fontSize: 170, color: C.clay, letterSpacing: -3 }}>
            Fitshark
          </div>
        </FadeUp>
        <FadeUp delay={60} style={{ marginTop: 16 }}>
          <Body size={44}>A fitment-to-sale agent. Built on Duvo.</Body>
        </FadeUp>
      </div>
    </Stage>
  );
};

/* 4 — HOW IT WORKS */
const Step: React.FC<{ n: number; title: string; sub: string; delay: number }> = ({
  n,
  title,
  sub,
  delay,
}) => (
  <FadeUp delay={delay} style={{ display: "flex", gap: 28, alignItems: "flex-start" }}>
    <div
      style={{
        fontFamily: HEAD,
        fontWeight: 600,
        fontSize: 26,
        color: C.cream,
        background: C.clay,
        width: 52,
        height: 52,
        borderRadius: 26,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        flexShrink: 0,
      }}
    >
      {n}
    </div>
    <div>
      <div style={{ fontFamily: HEAD, fontWeight: 600, fontSize: 40, color: C.dark }}>{title}</div>
      <div style={{ fontFamily: BODY, fontSize: 30, color: "#6b685f", marginTop: 4 }}>{sub}</div>
    </div>
  </FadeUp>
);

export const HowItWorks: React.FC<SceneProps> = ({ len }) => {
  const frame = useCurrentFrame();
  return (
    <Stage align="flex-start">
      <div style={{ opacity: fadeOut(frame, len), width: "100%" }}>
        <FadeUp delay={2}>
          <Kicker>How it works</Kicker>
        </FadeUp>
        <div style={{ display: "flex", flexDirection: "column", gap: 34, marginTop: 48 }}>
          <Step n={1} delay={20} title="A question arrives" sub="Any language — SK, CZ, EN, DE, PL." />
          <Step
            n={2}
            delay={70}
            title="It understands what you need"
            sub="Even from symptoms — “squeals when braking” → brake pads."
          />
          <Step
            n={3}
            delay={150}
            title="It searches the whole market"
            sub="Across every supplier catalog, instantly."
          />
          <Step
            n={4}
            delay={300}
            title="It finds the best offer"
            sub="Right part, in stock, best price and delivery."
          />
        </div>
        <FadeUp delay={210} style={{ marginTop: 64 }}>
          <div style={{ display: "flex", gap: 80 }}>
            {[
              ["110,000", "parts"],
              ["11", "suppliers"],
              ["1", "answer"],
            ].map(([big, small]) => (
              <div key={small}>
                <div style={{ fontFamily: HEAD, fontWeight: 700, fontSize: 76, color: C.clay, lineHeight: 1 }}>
                  {big}
                </div>
                <div style={{ fontFamily: BODY, fontSize: 28, color: "#6b685f", marginTop: 6 }}>{small}</div>
              </div>
            ))}
          </div>
        </FadeUp>
      </div>
    </Stage>
  );
};

/* 5 — THE REPLY (HITL + branded email) */
export const Reply: React.FC<SceneProps> = ({ len }) => {
  const frame = useCurrentFrame();
  return (
    <Stage>
      <div
        style={{
          opacity: fadeOut(frame, len),
          display: "flex",
          gap: 90,
          alignItems: "center",
          width: "100%",
        }}
      >
        <div style={{ flex: 1 }}>
          <FadeUp delay={4}>
            <Kicker>The reply</Kicker>
          </FadeUp>
          <FadeUp delay={16} style={{ marginTop: 24 }}>
            <H1 size={66}>A clear answer — in seconds.</H1>
          </FadeUp>
          <FadeUp delay={70} style={{ marginTop: 32 }}>
            <Body>
              Price, delivery, and a <span style={{ color: C.clay }}>unique buy link</span>, in the
              customer&apos;s language.
            </Body>
          </FadeUp>
          <FadeUp delay={150} style={{ marginTop: 28 }}>
            <Body size={32} style={{ color: C.green }}>
              A human approves. Only then does it send.
            </Body>
          </FadeUp>
        </div>

        {/* branded email card */}
        <FadeUp delay={40} style={{ flexShrink: 0 }}>
          <div
            style={{
              width: 620,
              background: "#fff",
              borderRadius: 20,
              border: `1px solid ${C.lightGray}`,
              overflow: "hidden",
              boxShadow: "0 30px 60px rgba(20,20,19,0.10)",
            }}
          >
            <div style={{ background: C.clay, padding: "18px 28px", fontFamily: HEAD, fontWeight: 700, fontSize: 26, color: "#fff" }}>
              Fitshark
            </div>
            <div style={{ padding: 32 }}>
              <div style={{ fontFamily: HEAD, fontWeight: 600, fontSize: 26, color: C.dark, lineHeight: 1.3 }}>
                Vaša H7 žiarovka Philips — skladom
              </div>
              <div style={{ fontFamily: BODY, fontSize: 24, color: "#3c3a36", marginTop: 18, lineHeight: 1.55 }}>
                Sedí na vaše Opel Astra J (2009–2015).
              </div>
              <div style={{ background: C.cream, borderRadius: 14, padding: "18px 22px", marginTop: 22, border: `1px solid ${C.lightGray}` }}>
                <div style={{ fontFamily: BODY, fontSize: 23, color: C.dark, margin: "2px 0" }}>
                  <b>Cena:</b> 3,81 € s DPH
                </div>
                <div style={{ fontFamily: BODY, fontSize: 23, color: C.dark, margin: "2px 0" }}>
                  <b>Dodanie:</b> skladom · 1 deň
                </div>
              </div>
              <div
                style={{
                  marginTop: 24,
                  background: C.clay,
                  color: "#fff",
                  fontFamily: HEAD,
                  fontWeight: 600,
                  fontSize: 24,
                  textAlign: "center",
                  padding: "16px 0",
                  borderRadius: 12,
                }}
              >
                Objednať →
              </div>
              <div style={{ fontFamily: BODY, fontSize: 18, color: C.gray, marginTop: 16, textAlign: "center" }}>
                shop.fitshark.example/buy/… · your link
              </div>
            </div>
          </div>
        </FadeUp>
      </div>
    </Stage>
  );
};

/* 6 — RESULTS */
export const Results: React.FC<SceneProps> = ({ len }) => {
  const frame = useCurrentFrame();
  const stats: [string, string][] = [
    ["11", "sellers"],
    ["110,000", "parts"],
    ["5", "languages"],
    ["100%", "grounded in real data"],
  ];
  return (
    <Stage>
      <div style={{ opacity: fadeOut(frame, len), width: "100%" }}>
        <FadeUp delay={4} style={{ marginBottom: 60 }}>
          <H1 size={64}>From question to sale.</H1>
        </FadeUp>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", rowGap: 56, columnGap: 80 }}>
          {stats.map(([big, small], i) => (
            <FadeUp key={small} delay={24 + i * 28}>
              <div style={{ fontFamily: HEAD, fontWeight: 700, fontSize: 92, color: C.clay, lineHeight: 1 }}>
                {big}
              </div>
              <div style={{ fontFamily: BODY, fontSize: 32, color: "#3c3a36", marginTop: 8 }}>{small}</div>
            </FadeUp>
          ))}
        </div>
      </div>
    </Stage>
  );
};

/* 7 — CLOSE */
export const Close: React.FC<SceneProps> = ({ len }) => {
  const frame = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(frame, len, 24), textAlign: "center", width: "100%" }}>
        <FadeUp delay={4}>
          <H1 size={72}>From question to sale — in minutes.</H1>
        </FadeUp>
        <FadeUp delay={50} style={{ marginTop: 44 }}>
          <div style={{ fontFamily: HEAD, fontWeight: 700, fontSize: 96, color: C.clay, letterSpacing: -2 }}>
            Fitshark
          </div>
        </FadeUp>
        <FadeUp delay={72} style={{ marginTop: 6 }}>
          <Body size={28} style={{ color: C.gray }}>built on Duvo</Body>
        </FadeUp>
      </div>
    </Stage>
  );
};
