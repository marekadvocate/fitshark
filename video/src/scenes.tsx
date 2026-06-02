import React from "react";
import { useCurrentFrame } from "remotion";
import { BODY, C, HEAD } from "./theme";
import { Body, FadeUp, fadeOut, H1, Kicker, Logo, PopIn, Stage } from "./ui";

type SceneProps = { len: number };

/* 1 — HOOK */
export const Hook: React.FC<SceneProps> = ({ len }) => {
  const frame = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(frame, len), maxWidth: 1450 }}>
        <FadeUp delay={3}>
          <Kicker>A pre-purchase question</Kicker>
        </FadeUp>
        <FadeUp delay={12} style={{ marginTop: 26 }}>
          <H1 size={94}>“Does this part fit my car?”</H1>
        </FadeUp>
        <FadeUp delay={40} style={{ marginTop: 34 }}>
          <Body size={42}>Today it&apos;s answered a day later. Or never.</Body>
        </FadeUp>
      </div>
    </Stage>
  );
};

/* 2 — COST */
export const Cost: React.FC<SceneProps> = ({ len }) => {
  const frame = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(frame, len), maxWidth: 1450 }}>
        <FadeUp delay={3}>
          <H1 size={86}>
            Every unanswered question
            <br />
            is a <span style={{ color: C.blue }}>lost sale.</span>
          </H1>
        </FadeUp>
        <FadeUp delay={34} style={{ marginTop: 36 }}>
          <Body>The customer moves on. The shelf stays full.</Body>
        </FadeUp>
      </div>
    </Stage>
  );
};

/* 3 — INTRO (logo) */
export const Intro: React.FC<SceneProps> = ({ len }) => {
  const frame = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(frame, len), textAlign: "center", width: "100%" }}>
        <PopIn delay={2} style={{ display: "flex", justifyContent: "center" }}>
          <Logo size={260} />
        </PopIn>
        <FadeUp delay={20} style={{ marginTop: 8 }}>
          <div style={{ fontFamily: HEAD, fontWeight: 700, fontSize: 110, color: C.blue, letterSpacing: -2 }}>
            Fitshark
          </div>
        </FadeUp>
        <FadeUp delay={34} style={{ marginTop: 10 }}>
          <Body size={42}>
            Turns parts questions into <span style={{ color: C.gold, fontWeight: 600 }}>sales</span>. On Duvo.
          </Body>
        </FadeUp>
      </div>
    </Stage>
  );
};

/* 4 — HOW IT WORKS */
const Step: React.FC<{ n: number; title: string; sub: string; delay: number }> = ({ n, title, sub, delay }) => (
  <FadeUp delay={delay} style={{ display: "flex", gap: 26, alignItems: "flex-start" }}>
    <div
      style={{
        fontFamily: HEAD,
        fontWeight: 600,
        fontSize: 26,
        color: "#fff",
        background: C.blue,
        width: 50,
        height: 50,
        borderRadius: 25,
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
      <div style={{ fontFamily: BODY, fontSize: 29, color: "#6b685f", marginTop: 3 }}>{sub}</div>
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
        <div style={{ display: "flex", flexDirection: "column", gap: 30, marginTop: 44 }}>
          <Step n={1} delay={16} title="A customer asks — in any language" sub="SK · CZ · EN · DE · PL." />
          <Step n={2} delay={56} title="It understands what they need" sub="Even from symptoms — “squeals when braking” → brake pads." />
          <Step n={3} delay={150} title="It searches the whole market" sub="110,000 parts across 11 suppliers — in one query." />
          <Step n={4} delay={300} title="It returns the best offer" sub="Right part, best price and delivery — grounded in real data." />
        </div>
      </div>
    </Stage>
  );
};

/* 5 — KEY VALUE: orders even out-of-stock parts */
export const KeyValue: React.FC<SceneProps> = ({ len }) => {
  const frame = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(frame, len), maxWidth: 1500 }}>
        <FadeUp delay={2}>
          <Kicker color={C.gold}>The difference</Kicker>
        </FadeUp>
        <FadeUp delay={12} style={{ marginTop: 24 }}>
          <H1 size={92}>
            Out of stock isn&apos;t <span style={{ color: C.gold }}>out of luck.</span>
          </H1>
        </FadeUp>
        <FadeUp delay={46} style={{ marginTop: 34 }}>
          <Body size={40}>
            When no one has the part on the shelf, Fitshark <b>sources it and places the order</b> —
            turning a dead-end question into a sale.
          </Body>
        </FadeUp>
        <FadeUp delay={92} style={{ marginTop: 40, display: "flex", gap: 22, alignItems: "center" }}>
          <Pill label="Not in stock" muted />
          <span style={{ fontFamily: HEAD, fontSize: 40, color: C.gold }}>→</span>
          <Pill label="Ordered for you · ETA 7 days" gold />
        </FadeUp>
      </div>
    </Stage>
  );
};

const Pill: React.FC<{ label: string; muted?: boolean; gold?: boolean }> = ({ label, muted, gold }) => (
  <div
    style={{
      fontFamily: HEAD,
      fontWeight: 600,
      fontSize: 28,
      padding: "14px 26px",
      borderRadius: 999,
      color: muted ? "#9a978d" : gold ? "#5a4410" : C.dark,
      background: gold ? "#f6e3b0" : "transparent",
      border: muted ? `2px dashed ${C.lightGray}` : "none",
      textDecoration: muted ? "line-through" : "none",
    }}
  >
    {label}
  </div>
);

/* 6 — THE REPLY (HITL + branded email) */
export const Reply: React.FC<SceneProps> = ({ len }) => {
  const frame = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(frame, len), display: "flex", gap: 80, alignItems: "center", width: "100%" }}>
        <div style={{ flex: 1 }}>
          <FadeUp delay={3}>
            <Kicker>The reply</Kicker>
          </FadeUp>
          <FadeUp delay={12} style={{ marginTop: 22 }}>
            <H1 size={64}>A clear answer — in seconds.</H1>
          </FadeUp>
          <FadeUp delay={44} style={{ marginTop: 30 }}>
            <Body>
              Price, delivery and a <span style={{ color: C.blue }}>unique buy link</span>, in the
              customer&apos;s language.
            </Body>
          </FadeUp>
          <FadeUp delay={110} style={{ marginTop: 26 }}>
            <Body size={32} style={{ color: C.green }}>A human approves. Only then does it send.</Body>
          </FadeUp>
        </div>

        <FadeUp delay={30} style={{ flexShrink: 0 }}>
          <div style={{ width: 600, background: "#fff", borderRadius: 20, border: `1px solid ${C.lightGray}`, overflow: "hidden", boxShadow: "0 30px 60px rgba(20,20,19,0.10)" }}>
            <div style={{ background: C.blue, padding: "16px 26px", fontFamily: HEAD, fontWeight: 700, fontSize: 26, color: "#fff" }}>
              Fitshark
            </div>
            <div style={{ padding: 30 }}>
              <div style={{ fontFamily: HEAD, fontWeight: 600, fontSize: 25, color: C.dark, lineHeight: 1.3 }}>
                Vaša H7 žiarovka Philips — objednáme pre vás
              </div>
              <div style={{ fontFamily: BODY, fontSize: 23, color: "#3c3a36", marginTop: 16, lineHeight: 1.5 }}>
                Sedí na vaše Opel Astra J (2009–2015).
              </div>
              <div style={{ background: C.cream, borderRadius: 14, padding: "16px 20px", marginTop: 20, border: `1px solid ${C.lightGray}` }}>
                <div style={{ fontFamily: BODY, fontSize: 22, color: C.dark, margin: "2px 0" }}><b>Cena:</b> 17,81 € s DPH</div>
                <div style={{ fontFamily: BODY, fontSize: 22, color: C.dark, margin: "2px 0" }}><b>Dodanie:</b> na objednávku · 7 dní</div>
              </div>
              <div style={{ marginTop: 22, background: C.blue, color: "#fff", fontFamily: HEAD, fontWeight: 600, fontSize: 23, textAlign: "center", padding: "15px 0", borderRadius: 12 }}>
                Objednať →
              </div>
              <div style={{ fontFamily: BODY, fontSize: 17, color: C.gray, marginTop: 14, textAlign: "center" }}>
                shop.fitshark.example/buy/… · your link
              </div>
            </div>
          </div>
        </FadeUp>
      </div>
    </Stage>
  );
};

/* 7 — RESULTS */
export const Results: React.FC<SceneProps> = ({ len }) => {
  const frame = useCurrentFrame();
  const stats: [string, string][] = [
    ["11", "suppliers"],
    ["110,000", "parts"],
    ["5", "languages"],
    ["100%", "grounded in real data"],
  ];
  return (
    <Stage>
      <div style={{ opacity: fadeOut(frame, len), width: "100%" }}>
        <FadeUp delay={3} style={{ marginBottom: 54 }}>
          <H1 size={62}>One agent. The whole market.</H1>
        </FadeUp>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", rowGap: 50, columnGap: 80 }}>
          {stats.map(([big, small], i) => (
            <FadeUp key={small} delay={20 + i * 18}>
              <div style={{ fontFamily: HEAD, fontWeight: 700, fontSize: 88, color: C.blue, lineHeight: 1 }}>{big}</div>
              <div style={{ fontFamily: BODY, fontSize: 31, color: "#3c3a36", marginTop: 8 }}>{small}</div>
            </FadeUp>
          ))}
        </div>
      </div>
    </Stage>
  );
};

/* 8 — CLOSE */
export const Close: React.FC<SceneProps> = ({ len }) => {
  const frame = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(frame, len, 22), textAlign: "center", width: "100%" }}>
        <FadeUp delay={3}>
          <H1 size={70}>From question to sale — in minutes.</H1>
        </FadeUp>
        <PopIn delay={26} style={{ display: "flex", justifyContent: "center", marginTop: 30 }}>
          <Logo size={180} />
        </PopIn>
        <FadeUp delay={44} style={{ marginTop: 4 }}>
          <div style={{ fontFamily: HEAD, fontWeight: 700, fontSize: 64, color: C.blue, letterSpacing: -1 }}>Fitshark</div>
        </FadeUp>
        <FadeUp delay={56} style={{ marginTop: 2 }}>
          <Body size={26} style={{ color: C.gray }}>built on Duvo</Body>
        </FadeUp>
      </div>
    </Stage>
  );
};
