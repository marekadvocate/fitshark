import React from "react";
import { useCurrentFrame } from "remotion";
import { BODY, C, HEAD } from "./theme";
import { Body, FadeUp, fadeOut, H1, Kicker, Logo, PopIn, Stage } from "./ui";

type SceneProps = { len: number };
const MONO = "ui-monospace, SFMono-Regular, Menlo, monospace";

const Mono: React.FC<{ children: React.ReactNode; size?: number; color?: string; bg?: string }> = ({
  children,
  size = 26,
  color = C.blueDeep,
  bg = "#eef2fb",
}) => (
  <span style={{ fontFamily: MONO, fontSize: size, color, background: bg, padding: "3px 10px", borderRadius: 7 }}>
    {children}
  </span>
);

const Node: React.FC<{ title: React.ReactNode; sub?: string; accent?: string; w?: number }> = ({
  title,
  sub,
  accent = C.blue,
  w,
}) => (
  <div
    style={{
      border: `2px solid ${accent}`,
      borderRadius: 12,
      padding: "12px 18px",
      background: "#fff",
      width: w,
      textAlign: "center",
    }}
  >
    <div style={{ fontFamily: HEAD, fontWeight: 600, fontSize: 24, color: C.dark }}>{title}</div>
    {sub && <div style={{ fontFamily: MONO, fontSize: 17, color: "#6b685f", marginTop: 3 }}>{sub}</div>}
  </div>
);

const Arrow: React.FC<{ label?: string; dir?: "down" | "right" }> = ({ label, dir = "down" }) => (
  <div style={{ display: "flex", flexDirection: "column", alignItems: "center", color: C.gray }}>
    <div style={{ fontFamily: HEAD, fontSize: 26, lineHeight: 1 }}>{dir === "down" ? "↓" : "→"}</div>
    {label && <div style={{ fontFamily: MONO, fontSize: 15, color: "#9a978d" }}>{label}</div>}
  </div>
);

/* 1 — TITLE */
export const Hook: React.FC<SceneProps> = ({ len }) => {
  const frame = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(frame, len), textAlign: "center", width: "100%" }}>
        <PopIn delay={1} style={{ display: "flex", justifyContent: "center" }}>
          <Logo size={150} />
        </PopIn>
        <FadeUp delay={12} style={{ marginTop: 6 }}>
          <div style={{ fontFamily: HEAD, fontWeight: 700, fontSize: 96, color: C.blue, letterSpacing: -2 }}>Fitshark</div>
        </FadeUp>
        <FadeUp delay={24} style={{ marginTop: 14 }}>
          <Mono size={28}>Backorder Reply System · on Duvo</Mono>
        </FadeUp>
        <FadeUp delay={40} style={{ marginTop: 24 }}>
          <Body size={36}>Out-of-stock auto-parts inquiries → matched, quoted, ordered.</Body>
        </FadeUp>
      </div>
    </Stage>
  );
};

/* 2 — PROBLEM */
export const Cost: React.FC<SceneProps> = ({ len }) => {
  const frame = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(frame, len), maxWidth: 1450 }}>
        <FadeUp delay={2}>
          <H1 size={80}>Out-of-stock inquiries pile up.</H1>
        </FadeUp>
        <FadeUp delay={26} style={{ marginTop: 30 }}>
          <Body>Answered slowly, one by one — or not at all. Each one is a <span style={{ color: C.blue }}>lost sale.</span></Body>
        </FadeUp>
      </div>
    </Stage>
  );
};

/* 3 — ARCHITECTURE */
export const Intro: React.FC<SceneProps> = ({ len }) => {
  const frame = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(frame, len), width: "100%" }}>
        <FadeUp delay={1}>
          <Kicker>Architecture</Kicker>
        </FadeUp>
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 8, marginTop: 22 }}>
          <FadeUp delay={8}><Node title="Google Drive" sub="customer_questions.csv · 11 feeds" /></FadeUp>
          <FadeUp delay={26}><Arrow /></FadeUp>
          <FadeUp delay={32}><Node title={'Case Queue "fitshark-questions"'} sub="1 case per inquiry" /></FadeUp>
          <FadeUp delay={50}><Arrow label="case trigger · concurrency 10" /></FadeUp>
          <FadeUp delay={58} style={{ display: "flex", gap: 12 }}>
            {[0, 1, 2, 3].map((i) => (
              <Node key={i} title={i < 3 ? "Job" : "…"} sub={i < 3 ? "case" : "×10"} accent={C.gold} w={120} />
            ))}
          </FadeUp>
          <FadeUp delay={92}><Arrow label="per job" /></FadeUp>
          <FadeUp delay={98}>
            <div style={{ display: "flex", gap: 10, alignItems: "center", flexWrap: "wrap", justifyContent: "center" }}>
              {["grep 11 feeds", "match", "skills", "HITL approve", "Gmail send"].map((s, i) => (
                <React.Fragment key={s}>
                  <Mono size={22}>{s}</Mono>
                  {i < 4 && <span style={{ color: C.gray, fontFamily: HEAD }}>→</span>}
                </React.Fragment>
              ))}
            </div>
          </FadeUp>
          <FadeUp delay={150}><Arrow /></FadeUp>
          <FadeUp delay={156}><Node title="Google Sheets" sub="Responses Log · Customer Vehicles (CRM)" accent={C.green} /></FadeUp>
        </div>
      </div>
    </Stage>
  );
};

/* 4 — PARALLEL */
export const HowItWorks: React.FC<SceneProps> = ({ len }) => {
  const frame = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(frame, len), maxWidth: 1500 }}>
        <FadeUp delay={1}>
          <Kicker>Parallel by design</Kicker>
        </FadeUp>
        <FadeUp delay={10} style={{ marginTop: 22 }}>
          <H1 size={72}>Concurrency <span style={{ color: C.gold }}>10</span>.</H1>
        </FadeUp>
        <FadeUp delay={34} style={{ marginTop: 26 }}>
          <Body size={36}>
            One HITL approval would block a run. So each inquiry is a <Mono size={24}>case</Mono> — the
            consumer runs up to 10 in parallel, each with its own approval in the Activity Inbox.
          </Body>
        </FadeUp>
        <div style={{ display: "flex", gap: 12, marginTop: 38, flexWrap: "wrap" }}>
          {Array.from({ length: 10 }).map((_, i) => (
            <FadeUp key={i} delay={70 + i * 6}>
              <div style={{ width: 96, height: 60, borderRadius: 10, background: "#fff", border: `2px solid ${C.blue}`, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: MONO, fontSize: 16, color: C.blueDeep }}>
                job {i + 1}
              </div>
            </FadeUp>
          ))}
        </div>
      </div>
    </Stage>
  );
};

/* 5 — GROUNDED MATCH */
export const KeyValue: React.FC<SceneProps> = ({ len }) => {
  const frame = useCurrentFrame();
  const rows: [string, string][] = [
    ["grep across 11 feeds", "110,000 SKUs searched directly in the sandbox"],
    ["confidence gate", "ambiguous → “Needs review”, never guessed"],
    ["auto-language", "reply written in the customer’s language: SK·CZ·EN·DE·PL"],
  ];
  return (
    <Stage align="flex-start">
      <div style={{ opacity: fadeOut(frame, len), width: "100%" }}>
        <FadeUp delay={1}>
          <Kicker>Grounded matching</Kicker>
        </FadeUp>
        <div style={{ display: "flex", flexDirection: "column", gap: 28, marginTop: 40 }}>
          {rows.map(([m, d], i) => (
            <FadeUp key={m} delay={14 + i * 26} style={{ display: "flex", gap: 22, alignItems: "center" }}>
              <Mono size={26}>{m}</Mono>
              <span style={{ color: C.gray, fontFamily: HEAD }}>→</span>
              <Body size={32}>{d}</Body>
            </FadeUp>
          ))}
        </div>
      </div>
    </Stage>
  );
};

/* 6 — THE CORE: out-of-stock → ordered (reply + PDF + upsell + link) */
export const Reply: React.FC<SceneProps> = ({ len }) => {
  const frame = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(frame, len), display: "flex", gap: 70, alignItems: "center", width: "100%" }}>
        <div style={{ flex: 1 }}>
          <FadeUp delay={2}>
            <Kicker color={C.gold}>The core</Kicker>
          </FadeUp>
          <FadeUp delay={10} style={{ marginTop: 20 }}>
            <H1 size={72}>Out of stock <span style={{ color: C.gold }}>→</span> ordered.</H1>
          </FadeUp>
          <FadeUp delay={40} style={{ marginTop: 26 }}>
            <Body size={34}>The backorder reply sources the part and places the order — with:</Body>
          </FadeUp>
          {[
            ["Branded HTML reply", "+ PDF price quote attached"],
            ["Unique per-customer order link", "/order/<qid>-<sku>"],
            ["Relevant upsell add-ons", "vehicle-compatible, raises order value"],
          ].map(([a, b], i) => (
            <FadeUp key={a} delay={72 + i * 22} style={{ marginTop: 14, display: "flex", gap: 12, alignItems: "baseline" }}>
              <span style={{ color: C.gold, fontFamily: HEAD, fontWeight: 700 }}>•</span>
              <div><span style={{ fontFamily: HEAD, fontWeight: 600, fontSize: 28, color: C.dark }}>{a}</span>{" "}
                <span style={{ fontFamily: MONO, fontSize: 20, color: "#6b685f" }}>{b}</span></div>
            </FadeUp>
          ))}
          <FadeUp delay={150} style={{ marginTop: 22 }}>
            <Body size={30} style={{ color: C.green }}>Every email is human-approved before it sends.</Body>
          </FadeUp>
        </div>

        <FadeUp delay={28} style={{ flexShrink: 0 }}>
          <div style={{ width: 540, background: "#fff", borderRadius: 18, border: `1px solid ${C.lightGray}`, overflow: "hidden", boxShadow: "0 28px 56px rgba(20,20,19,0.10)" }}>
            <div style={{ background: C.blue, padding: "14px 24px", fontFamily: HEAD, fontWeight: 700, fontSize: 24, color: "#fff", display: "flex", justifyContent: "space-between" }}>
              <span>Fitshark</span><span style={{ fontFamily: MONO, fontSize: 16, background: C.gold, color: "#3a2c06", padding: "2px 10px", borderRadius: 20 }}>ON ORDER</span>
            </div>
            <div style={{ padding: 28 }}>
              <div style={{ fontFamily: HEAD, fontWeight: 600, fontSize: 23, color: C.dark }}>Vaša H7 žiarovka Philips — objednáme pre vás</div>
              <div style={{ background: C.cream, borderRadius: 12, padding: "14px 18px", marginTop: 16, border: `1px solid ${C.lightGray}`, fontFamily: BODY, fontSize: 21, color: C.dark }}>
                <div><b>Cena:</b> 17,81 € s DPH</div>
                <div><b>Dodanie:</b> na objednávku · 7 dní</div>
              </div>
              <div style={{ marginTop: 18, background: C.blue, color: "#fff", fontFamily: HEAD, fontWeight: 600, fontSize: 22, textAlign: "center", padding: "13px 0", borderRadius: 11 }}>Objednať →</div>
              <div style={{ fontFamily: MONO, fontSize: 15, color: C.gray, marginTop: 12, textAlign: "center" }}>📎 quote.pdf · /order/Q001-… </div>
            </div>
          </div>
        </FadeUp>
      </div>
    </Stage>
  );
};

/* 7 — AFTER THE SEND */
export const Results: React.FC<SceneProps> = ({ len }) => {
  const frame = useCurrentFrame();
  const steps: [string, string][] = [
    ["Responses Log", "every answer: SKU · price · lead time · order link · status"],
    ["Customer Vehicles", "CRM — vehicle saved for later offers"],
    ["Auto follow-up", "+3 days if no reply (also human-approved)"],
    ["Campaign agent", "personalized seasonal offers → re-engagement"],
  ];
  return (
    <Stage align="flex-start">
      <div style={{ opacity: fadeOut(frame, len), width: "100%" }}>
        <FadeUp delay={1}>
          <Kicker color={C.green}>After approval</Kicker>
        </FadeUp>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", rowGap: 28, columnGap: 70, marginTop: 38 }}>
          {steps.map(([a, b], i) => (
            <FadeUp key={a} delay={12 + i * 20}>
              <div style={{ fontFamily: HEAD, fontWeight: 600, fontSize: 32, color: C.dark }}>{a}</div>
              <div style={{ fontFamily: MONO, fontSize: 20, color: "#6b685f", marginTop: 4 }}>{b}</div>
            </FadeUp>
          ))}
        </div>
      </div>
    </Stage>
  );
};

/* 8 — CLOSE / STACK */
export const Close: React.FC<SceneProps> = ({ len }) => {
  const frame = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(frame, len, 20), textAlign: "center", width: "100%" }}>
        <FadeUp delay={2}>
          <H1 size={64}>From inquiry to order — at scale.</H1>
        </FadeUp>
        <FadeUp delay={22} style={{ marginTop: 22 }}>
          <Mono size={24}>Duvo · Case Queue + HITL · Skills · Drive / Sheets / Gmail · @duvoai/cli + MCP</Mono>
        </FadeUp>
        <PopIn delay={40} style={{ display: "flex", justifyContent: "center", marginTop: 26 }}>
          <Logo size={140} />
        </PopIn>
        <FadeUp delay={54}>
          <div style={{ fontFamily: HEAD, fontWeight: 700, fontSize: 56, color: C.blue, letterSpacing: -1 }}>Fitshark</div>
        </FadeUp>
      </div>
    </Stage>
  );
};
