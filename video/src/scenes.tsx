import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from "remotion";
import { BODY, C, HEAD } from "./theme";
import { Body, Clip, CountUp, FadeUp, fadeOut, Glow, H1, Logo, PopIn, Shot, Stage, Words } from "./ui";

type P = { len: number };
const MONO = "ui-monospace, SFMono-Regular, Menlo, monospace";

const Tag: React.FC<{ children: React.ReactNode; size?: number }> = ({ children, size = 21 }) => (
  <span style={{ fontFamily: MONO, fontSize: size, color: "#7a4a36", background: "#f3e3da", padding: "8px 14px", borderRadius: 9 }}>
    {children}
  </span>
);

/* Duvo-style skill lightbulb icon */
const Bulb: React.FC<{ size?: number }> = ({ size = 26 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={C.clay} strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
    <path d="M9 18h6" />
    <path d="M10 22h4" />
    <path d="M12 2a7 7 0 0 0-4 12.8c.5.4.9 1 1 1.7V17h6v-.5c.1-.7.5-1.3 1-1.7A7 7 0 0 0 12 2z" />
  </svg>
);

const SkillCard: React.FC<{ name: string; delay: number }> = ({ name, delay }) => (
  <PopIn delay={delay}>
    <div style={{ display: "flex", alignItems: "center", gap: 14, background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.14)", borderRadius: 14, padding: "15px 22px", width: 330 }}>
      <div style={{ width: 42, height: 42, borderRadius: 10, background: "rgba(217,119,87,0.18)", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
        <Bulb />
      </div>
      <span style={{ fontFamily: HEAD, fontWeight: 600, fontSize: 23, color: C.cream }}>{name}</span>
    </div>
  </PopIn>
);

/* Duvo Builder-Day aesthetic: drifting dot grid + shimmering ASCII field */
const DuvoGrid: React.FC = () => {
  const f = useCurrentFrame();
  const shift = (f * 0.15) % 120;
  return (
    <AbsoluteFill
      style={{
        backgroundImage: "radial-gradient(circle, rgba(255,255,255,0.10) 1.5px, transparent 1.5px)",
        backgroundSize: "120px 120px",
        backgroundPosition: `${shift}px ${shift}px`,
      }}
    />
  );
};

const RAMP = [" ", " ", " ", ".", ":", "+", "#", "%", "%"];
const Ascii: React.FC<{ rows?: number; cols?: number; opacity?: number; size?: number }> = ({ rows = 22, cols = 62, opacity = 0.42, size = 28 }) => {
  const f = useCurrentFrame();
  const lines: string[] = [];
  for (let r = 0; r < rows; r++) {
    let s = "";
    for (let c = 0; c < cols; c++) {
      const base = (Math.sin(c * 0.5 + f * 0.06) + Math.sin(r * 0.7 - f * 0.045) + Math.sin((r + c) * 0.33 + f * 0.05)) / 3;
      const tex = Math.sin(c * 12.9 + r * 4.1) * 0.28;
      let t = (base + tex + 1) / 2;
      t = Math.max(0, Math.min(0.999, t));
      s += RAMP[Math.floor(t * RAMP.length)];
    }
    lines.push(s);
  }
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
      <pre style={{ fontFamily: MONO, fontSize: size, lineHeight: 1, letterSpacing: 6, color: "#fff", opacity, margin: 0, whiteSpace: "pre" }}>
        {lines.join("\n")}
      </pre>
    </AbsoluteFill>
  );
};

const Vignette: React.FC<{ bg?: string }> = ({ bg = "rgba(10,10,11,0.86)" }) => (
  <AbsoluteFill style={{ background: `radial-gradient(circle at 50% 50%, transparent 28%, ${bg} 72%)` }} />
);

/** Dark Duvo "Builder-Day" stage: grid + ascii shimmer + vignette, content on top. */
const DarkStage: React.FC<{ children: React.ReactNode; asciiOpacity?: number }> = ({ children, asciiOpacity = 0.15 }) => (
  <AbsoluteFill style={{ background: "#0a0a0b", justifyContent: "center", alignItems: "center", padding: "0 150px", fontFamily: BODY }}>
    <DuvoGrid />
    <Ascii opacity={asciiOpacity} />
    <Vignette bg="rgba(10,10,11,0.82)" />
    <div style={{ position: "relative", zIndex: 2, width: "100%", display: "flex", justifyContent: "center" }}>{children}</div>
  </AbsoluteFill>
);

/* 1 — OPEN (word-by-word, two staggered lines) */
export const S1: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(f, len), maxWidth: 1640, textAlign: "center" }}>
        <Words text="Every motor-parts question is a sale" size={76} delay={2} step={3} />
        <Words text="waiting to happen." size={76} color={C.clay} delay={24} step={3} style={{ marginTop: 8 }} />
      </div>
    </Stage>
  );
};

/* 2 — THE QUESTION (word-by-word) */
export const S2: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(f, len), textAlign: "center" }}>
        <Words text={"“Will this fit my car?”"} size={118} delay={2} step={4} />
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
      <Glow strength={0.18} />
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
      <Glow strength={0.16} />
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
      <Glow strength={0.2} />
      <div style={{ opacity: fadeOut(f, len), textAlign: "center", maxWidth: 1500 }}>
        <FadeUp delay={2}><H1 size={88}>It gets what they mean.</H1></FadeUp>
        <FadeUp delay={11} style={{ marginTop: 18 }}><Body size={44} style={{ color: C.sub }}>Even what they don&apos;t say.</Body></FadeUp>
      </div>
    </Stage>
  );
};

/* 7 — FUNNY CUSTOMER QUESTIONS (animated cycle) */
export const SLang: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  const phrases: [string, string][] = [
    ["Dobre, mám turbo — skade beriem paru?", "SK"],
    ["Píská mi to vzadu, je to vážný?", "CZ"],
    ["Will this fit my old beast?", "EN"],
    ["Passt das an meinen alten Golf?", "DE"],
    ["Pasuje to do mojego malucha?", "PL"],
  ];
  const start = 16, per = 24;
  const idx = Math.min(Math.max(0, Math.floor((f - start) / per)), phrases.length - 1);
  const local = f - start - idx * per;
  const op = interpolate(local, [0, 6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const rise = interpolate(local, [0, 6], [16, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <Stage>
      <Glow strength={0.18} />
      <div style={{ opacity: fadeOut(f, len), textAlign: "center", width: "100%" }}>
        <FadeUp delay={2}><H1 size={68}>In their own words.</H1></FadeUp>
        <div style={{ marginTop: 34, opacity: op, transform: `translateY(${rise}px)` }}>
          <span style={{ fontFamily: HEAD, fontWeight: 700, fontSize: 64, color: C.clay }}>{phrases[idx][0]}</span>
          <span style={{ fontFamily: MONO, fontSize: 28, color: C.sub, marginLeft: 18 }}>{phrases[idx][1]}</span>
        </div>
        <FadeUp delay={10} style={{ marginTop: 30 }}>
          <Body size={30} style={{ color: C.sub }}>Slang, typos, half a sentence — it still understands.</Body>
        </FadeUp>
      </div>
    </Stage>
  );
};

/* 8 — THE MARKET (count-up) */
export const S6: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <Stage>
      <Glow strength={0.2} delay={4} />
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
    <AbsoluteFill style={{ background: "#0a0a0b", justifyContent: "center", alignItems: "center", padding: "0 150px" }}>
      <DuvoGrid />
      <Ascii opacity={0.22} />
      <Vignette />
      <Glow a={C.shark} b={C.clay} strength={0.3} />
      <div style={{ opacity: fadeOut(f, len), textAlign: "center", maxWidth: 1550, zIndex: 2 }}>
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

/* 9b — FEEDS GRAPH (animated bars, dark) */
export const SFeeds: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  const feeds: [string, number][] = [
    ["AutoParts SK", 14200],
    ["EuroParts", 13100],
    ["MotoParts SK", 12400],
    ["CarStyle", 11800],
    ["PartsExpress", 10300],
    ["MotoMarket", 9900],
    ["OilExpert", 9700],
    ["BrakePro", 8900],
    ["ElectroAuto", 7600],
    ["FilterCentre", 6200],
    ["TyreService SK", 5900],
  ];
  const max = Math.max(...feeds.map((x) => x[1]));
  return (
    <DarkStage asciiOpacity={0.1}>
      <div style={{ opacity: fadeOut(f, len), width: "100%", maxWidth: 1320 }}>
        <FadeUp delay={2}>
          <div style={{ fontFamily: HEAD, fontWeight: 700, fontSize: 62, color: C.cream, textAlign: "center", letterSpacing: -1 }}>
            11 live feeds. <span style={{ color: C.clay }}>One catalog.</span>
          </div>
        </FadeUp>
        <div style={{ marginTop: 36, display: "flex", flexDirection: "column", gap: 12 }}>
          {feeds.map(([name, val], i) => {
            const p = interpolate(f, [10 + i * 3, 36 + i * 3], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
            return (
              <div key={name} style={{ display: "flex", alignItems: "center", gap: 18 }}>
                <div style={{ width: 240, textAlign: "right", fontFamily: MONO, fontSize: 22, color: C.gray }}>{name}</div>
                <div style={{ flex: 1, height: 26, background: "rgba(255,255,255,0.05)", borderRadius: 6, overflow: "hidden" }}>
                  <div style={{ width: `${(val / max) * 100 * p}%`, height: "100%", background: C.clay, borderRadius: 6 }} />
                </div>
                <div style={{ width: 92, fontFamily: MONO, fontSize: 21, color: C.cream, textAlign: "right" }}>{Math.round(val * p).toLocaleString("en-US")}</div>
              </div>
            );
          })}
        </div>
        <FadeUp delay={50} style={{ marginTop: 28, textAlign: "center" }}>
          <div style={{ fontFamily: HEAD, fontWeight: 600, fontSize: 30, color: C.cream }}>
            <span style={{ color: C.clay }}><CountUp to={110000} delay={50} dur={26} /></span> motor parts · grep&apos;d in real time
          </div>
        </FadeUp>
      </div>
    </DarkStage>
  );
};

/* 10 — SKILLS (composable, with icons) */
export const SSkills: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  const skills = [
    "Fitment Decision",
    "Reply Writer",
    "Email Template",
    "Quote PDF",
    "Upsell Recommender",
    "Offer Personalizer",
    "Product Link",
    "Brand Voice",
  ];
  return (
    <DarkStage asciiOpacity={0.12}>
      <div style={{ opacity: fadeOut(f, len), textAlign: "center", width: "100%", maxWidth: 1460 }}>
        <FadeUp delay={2}><H1 size={72} style={{ color: C.cream }}>Built from <span style={{ color: C.clay }}>composable skills.</span></H1></FadeUp>
        <div style={{ marginTop: 38, display: "flex", gap: 18, justifyContent: "center", flexWrap: "wrap" }}>
          {skills.map((s, i) => (
            <SkillCard key={s} name={s} delay={12 + i * 4} />
          ))}
        </div>
        <FadeUp delay={50} style={{ marginTop: 30 }}>
          <Body size={30} style={{ color: C.gray }}>Reusable. Versioned. Shared across the team.</Body>
        </FadeUp>
      </div>
    </DarkStage>
  );
};

/* 10b — PER-SKILL DEEP DIVE (one screen each) */
type Skill = { name: string; what: React.ReactNode; detail: string };
const SKILLS: Skill[] = [
  { name: "Fitment Decision", what: <>Deterministic cross-catalog match — the <b>one</b> part that truly fits.</>, detail: "make · model · year · engine → 1 SKU" },
  { name: "Reply Writer", what: <>Turns a matched part into a polished, on-brand customer reply.</>, detail: "out-of-stock → ready-to-send" },
  { name: "Email Template", what: <>Wraps it in branded HTML — product card, price, prominent CTA.</>, detail: "inline CSS · product card · CTA" },
  { name: "Quote PDF", what: <>Generates a clean, branded PDF price quote for the part + add-ons.</>, detail: "quote_Q023.pdf" },
  { name: "Upsell Recommender", what: <>Suggests complementary cross-sell and trade-up items.</>, detail: "+ brake pads  + oil filter" },
  { name: "Offer Personalizer", what: <>Builds a seasonal offer for a known customer from their saved car.</>, detail: "saved vehicle → winter offer" },
  { name: "Product Link", what: <>Mints a unique per-customer <b>/buy/</b> link — one tap, fully tracked.</>, detail: "/buy/ · per-customer · tracked" },
  { name: "Brand Voice", what: <>The Fitshark voice + trust standards on every customer-facing word.</>, detail: "tone · trust · consistency" },
];

const SkillScene: React.FC<P & { skill: Skill; idx: number }> = ({ len, skill, idx }) => {
  const f = useCurrentFrame();
  return (
    <DarkStage asciiOpacity={0.14}>
      <div style={{ opacity: fadeOut(f, len), textAlign: "center", width: "100%", maxWidth: 1500 }}>
        <FadeUp delay={1}>
          <div style={{ fontFamily: MONO, fontSize: 22, letterSpacing: 3, color: C.gray }}>
            SKILL {String(idx + 1).padStart(2, "0")} / 08
          </div>
        </FadeUp>
        <PopIn delay={4} style={{ display: "flex", justifyContent: "center", marginTop: 18 }}>
          <div style={{ width: 96, height: 96, borderRadius: 24, background: "rgba(217,119,87,0.2)", border: "1px solid rgba(217,119,87,0.4)", display: "flex", alignItems: "center", justifyContent: "center" }}>
            <Bulb size={48} />
          </div>
        </PopIn>
        <div style={{ marginTop: 24 }}>
          <Words text={skill.name} size={80} color={C.clay} delay={9} step={3} />
        </div>
        <FadeUp delay={20} style={{ marginTop: 18 }}>
          <Body size={42} style={{ color: C.cream, maxWidth: 1200, marginLeft: "auto", marginRight: "auto" }}>{skill.what}</Body>
        </FadeUp>
        <FadeUp delay={30} style={{ marginTop: 26, display: "flex", justifyContent: "center" }}>
          <span style={{ fontFamily: MONO, fontSize: 28, color: "#e8c4b3", background: "rgba(217,119,87,0.14)", border: "1px solid rgba(217,119,87,0.32)", padding: "9px 16px", borderRadius: 9 }}>{skill.detail}</span>
        </FadeUp>
      </div>
    </DarkStage>
  );
};

const makeSkill = (i: number): React.FC<P> => {
  const C2: React.FC<P> = ({ len }) => <SkillScene len={len} skill={SKILLS[i]} idx={i} />;
  return C2;
};
export const Sk1 = makeSkill(0);
export const Sk2 = makeSkill(1);
export const Sk3 = makeSkill(2);
export const Sk4 = makeSkill(3);
export const Sk5 = makeSkill(4);
export const Sk6 = makeSkill(5);
export const Sk7 = makeSkill(6);
export const Sk8 = makeSkill(7);

/* 11 — PARALLEL (animated jobs) */
export const SPar: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <DarkStage asciiOpacity={0.12}>
      <div style={{ opacity: fadeOut(f, len), textAlign: "center", width: "100%" }}>
        <FadeUp delay={2}><H1 size={80} style={{ color: C.cream }}>10 inquiries. <span style={{ color: C.clay }}>At once.</span></H1></FadeUp>
        <FadeUp delay={11} style={{ marginTop: 12 }}>
          <Body size={28} style={{ color: C.gray, fontFamily: MONO }}>Case Queue · concurrency 10</Body>
        </FadeUp>
        <div style={{ marginTop: 36, display: "flex", gap: 12, justifyContent: "center", flexWrap: "wrap", maxWidth: 1300, marginLeft: "auto", marginRight: "auto" }}>
          {Array.from({ length: 10 }).map((_, i) => (
            <PopIn key={i} delay={20 + i * 4}>
              <div style={{ width: 110, height: 64, borderRadius: 12, background: "rgba(217,119,87,0.12)", border: `2px solid ${C.clay}`, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: MONO, fontSize: 17, color: "#e8c4b3" }}>
                job {i + 1}
              </div>
            </PopIn>
          ))}
        </div>
      </div>
    </DarkStage>
  );
};

/* 12 — THE REPLY (full product demo — plays through) */
export const S8: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(f, len), textAlign: "center", width: "100%" }}>
        <FadeUp delay={2}><H1 size={60}>A flawless reply. <span style={{ color: C.clay }}>In seconds.</span></H1></FadeUp>
        <FadeUp delay={10} style={{ marginTop: 8, marginBottom: 22 }}>
          <Body size={28} style={{ color: C.sub }}>Their language · price · delivery · branded PDF · one tap to buy.</Body>
        </FadeUp>
        <div style={{ display: "flex", justifyContent: "center" }}>
          <Clip src="showcase.mp4" w={1480} />
        </div>
      </div>
    </Stage>
  );
};

/* 13 — QUOTE + UPSELL */
export const SMore: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(f, len), textAlign: "center", width: "100%", maxWidth: 1500 }}>
        <FadeUp delay={2}><H1 size={78}>Not just an answer.</H1></FadeUp>
        <div style={{ marginTop: 34, display: "flex", gap: 22, justifyContent: "center", flexWrap: "wrap" }}>
          <FadeUp delay={12}><Tag size={28}>branded PDF quote</Tag></FadeUp>
          <FadeUp delay={22}><Tag size={28}>relevant upsell</Tag></FadeUp>
          <FadeUp delay={32}><Tag size={28}>1-tap order link</Tag></FadeUp>
        </div>
        <FadeUp delay={44} style={{ marginTop: 28 }}><Body size={34} style={{ color: C.sub }}>A bigger basket, every time.</Body></FadeUp>
      </div>
    </Stage>
  );
};

/* 14 — HUMAN APPROVAL (real Duvo HITL) */
export const SApprove: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <Stage>
      <Glow strength={0.18} delay={6} />
      <div style={{ opacity: fadeOut(f, len), textAlign: "center", width: "100%" }}>
        <FadeUp delay={2}><H1 size={70}>You approve. <span style={{ color: C.clay }}>It sends.</span></H1></FadeUp>
        <FadeUp delay={10} style={{ marginTop: 12, marginBottom: 24 }}>
          <Body size={28} style={{ color: C.sub }}>Every send is human-approved — right inside Duvo.</Body>
        </FadeUp>
        <div style={{ display: "flex", justifyContent: "center" }}>
          <Shot src="shot_hitl.png" w={1080} delay={12} />
        </div>
      </div>
    </Stage>
  );
};

/* 15 — FOLLOW-UP */
export const SFollow: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <Stage>
      <div style={{ opacity: fadeOut(f, len), textAlign: "center", maxWidth: 1500 }}>
        <FadeUp delay={2}><H1 size={84}>No reply? <span style={{ color: C.clay }}>It follows up.</span></H1></FadeUp>
        <FadeUp delay={12} style={{ marginTop: 18 }}><Body size={36} style={{ color: C.sub }}>Politely. On its own. Until the deal closes.</Body></FadeUp>
      </div>
    </Stage>
  );
};

/* 16 — REMEMBERS THE CAR (real CRM sheet) */
export const SRemember: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <Stage>
      <Glow a={C.shark} b={C.clay} strength={0.22} delay={6} />
      <div style={{ opacity: fadeOut(f, len), textAlign: "center", width: "100%" }}>
        <FadeUp delay={2}><H1 size={76}>It remembers every car.</H1></FadeUp>
        <FadeUp delay={11} style={{ marginTop: 14, marginBottom: 26 }}>
          <Body size={36} style={{ color: C.sub }}>You create <span style={{ color: C.clay }}>future upsell opportunities</span> — customized lifecycle parts for every car.</Body>
        </FadeUp>
        <div style={{ display: "flex", justifyContent: "center" }}>
          <Shot src="shot_crm.png" w={1180} delay={13} />
        </div>
      </div>
    </Stage>
  );
};

/* 17 — PAYOFF */
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

/* 18 — CLOSE (Duvo Builder-Day ASCII style) */
export const S11: React.FC<P> = ({ len }) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: "#0a0a0b", justifyContent: "center", alignItems: "center" }}>
      <DuvoGrid />
      <Ascii rows={22} cols={62} opacity={0.4} />
      <Vignette bg="rgba(10,10,11,0.9)" />
      <div style={{ opacity: fadeOut(f, len, 20), textAlign: "center", width: "100%", zIndex: 2 }}>
        <PopIn delay={1} style={{ display: "flex", justifyContent: "center" }}><Logo size={170} /></PopIn>
        <FadeUp delay={12} style={{ marginTop: 2 }}>
          <div style={{ fontFamily: HEAD, fontWeight: 700, fontSize: 100, color: C.shark, letterSpacing: -2 }}>Fitshark</div>
        </FadeUp>
        <FadeUp delay={22} style={{ marginTop: 8 }}>
          <div style={{ fontFamily: HEAD, fontWeight: 500, fontSize: 40, color: C.cream }}>From question to sale.</div>
        </FadeUp>
        <FadeUp delay={32} style={{ marginTop: 16 }}>
          <div style={{ fontFamily: MONO, fontSize: 24, color: C.gray, letterSpacing: 2 }}>built on Duvo · Prague Builder Day</div>
        </FadeUp>
      </div>
    </AbsoluteFill>
  );
};
