# Fitshark — Backorder Reply System (Duvo)

An end-to-end AI automation built on **[Duvo](https://duvo.ai)** that answers customer inquiries
about **out-of-stock auto parts**. It reads customer questions, finds the matching product across 11
supplier feeds, writes a polished reply (price + delivery + a unique one-click order link), attaches a
branded PDF quote, **gets human approval for every email**, sends it, logs the answer, saves the
customer's vehicle for later offers, and follows up if the customer doesn't respond.

It runs on a **parallel Case Queue** so many inquiries are processed at the same time — each becomes its
own approval in the Activity Inbox instead of being handled strictly one-by-one.

---

## 1. The data (this repo)

| Path | What it is |
|------|-----------|
| `feeds/feed_*.tsv` | 11 synthetic supplier feeds, ~10,000 SKUs each, 70 columns (the product catalog source). |
| `questions/customer_questions.csv` | 100 customer inquiries about out-of-stock parts (test set). `customer_email` is set to `dominik@fronc.eu` so test replies arrive there. Also holds `expected_*` oracle columns for validation (the agents are told to ignore them). |
| `duvo/` | The Duvo build: agent SOPs, skills, helper scripts, configs (this folder). |
| `duvo/catalog.csv` | A slim, consolidated catalog (110k rows) generated from the feeds — *gitignored* (regenerate with `prepare_duvo_data.py`). |

In Duvo, the feeds and questions live in Google Drive (account `dominikfroncik@gmail.com`):
- **MOTOR PARTS** — the 11 `feed_*.tsv` files.
- **MOTOR PARTS QUESTIONS** — `customer_questions.csv`.

---

## 2. How it works (architecture)

```
                    Google Drive: MOTOR PARTS QUESTIONS / customer_questions.csv  (grows over time)
                                                │
                                                ▼
                         ┌──────────────────────────────────────────┐
                         │  Case Queue "fitshark-questions"           │   one CASE per inquiry
                         └──────────────────────────────────────────┘
                                                │  case trigger (CONCURRENCY = 10)
                          ┌──────────────┬──────┴───────┬──────────────┐   ← PARALLEL: up to 10 at once
                          ▼              ▼              ▼              ▼
                       Job (case)     Job (case)    Job (case)    Job (case)        each is an independent
                          │              │              │              │            job with its OWN approval
   per job:  grep the 11 supplier feeds (Drive) → match product → compose reply
             (skills) → attach PDF quote → ▶ HUMAN APPROVAL (Activity Inbox) ──→ send (Gmail)
                          │
                          ▼
        Google Sheets:  Responses Log  +  Customer Vehicles        (audit + CRM for later offers)
                          │
                          ▼
        Auto follow-up after 3 days (if the customer hasn't replied/ordered) — also human-approved.

        Later / separately:  Campaign agent reads Customer Vehicles → personalized seasonal offers.
```

**Why a Case Queue?** A single agent run can only hold one Human-in-the-Loop approval at a time (it
pauses until you answer), which forces sequential approving. By turning each inquiry into a **case** and
running a **consumer with concurrency 10**, up to 10 inquiries are processed simultaneously — so ~10
approvals appear in the Activity Inbox at once and you approve them independently, in any order.

---

## 3. Skills (reusable knowledge packs, attached to the agents)

| Skill | Purpose |
|-------|---------|
| **fitshark-brand-voice** | The Fitshark voice, formatting, glossary, and trust/**fitment-guarantee** standards applied to every customer message. |
| **fitshark-reply-writer** | Composes the polished reply (Subject + plain-text + HTML), price/delivery box, CTA, sign-off. |
| **fitshark-product-link** | Builds the product-page link **and a unique per-customer order link** (`…/order/<question_id>-<sku>?email=…`). |
| **fitshark-upsell-recommender** | Suggests 1–3 genuinely relevant, vehicle-compatible add-ons (+ optional premium upgrade) — raises order value. |
| **fitshark-quote-pdf** | Generates a branded **PDF price quote** (line items, totals, validity) and attaches it; falls back to inline if PDF isn't available. |
| **fitshark-offer-personalizer** | (Campaign) Turns a saved vehicle into a seasonal, vehicle-specific offer for later re-engagement. |

Skills are attached to a build **by skill ID** (attaching by name silently fails with "Unknown skill").

---

## 4. Agents (Duvo team "Advocate")

| Agent | Role | Notes |
|-------|------|-------|
| **Fitshark — Reply Consumer (Queue)** | **Primary.** Case-queue **consumer**, trigger **concurrency 10**. Processes one case → match → compose → approve → send → log → save vehicle → resolve case. | The parallel production path. |
| **Fitshark — Personalized Offers (Campaign)** | Reads Customer Vehicles → builds personalized offers (offer-personalizer) → human-approved sends → Campaign Log. Weekly schedule (disabled until vehicle data exists). | Later re-engagement / upsell. |
| **Fitshark — Backorder Reply (Production)** | Earlier **sequential** version (single run loops the CSV, one approval at a time). 10-min schedule (disabled). Superseded by the queue consumer for parallel approval. | Kept as reference. |
| _Fitshark — Drive TEST v2 / Drive CSV Editor / Sheets agent_ | Experimental/one-off agents used while building. | Safe to delete. |

All production agents use the `dominikfroncik@gmail.com` Google connections (Drive + Sheets + Gmail) and
Human-in-the-Loop.

---

## 5. Connections & storage

- **Google Drive** — read the questions CSV and the supplier feeds. *(Read-only via Duvo — the connector cannot write back to Drive.)*
- **Google Sheets** — the agent creates and maintains:
  - **Fitshark — Responses Log** — one row per answered inquiry (status, matched SKU, price, lead time, order link, language, follow-up date, …).
  - **Fitshark — Customer Vehicles** — one row per customer+vehicle (CRM for the campaign agent).
  - **Fitshark — Campaign Log** — personalized offers sent (campaign agent).
- **Gmail** — sends the reply (from `dominikfroncik@gmail.com`); recipient is the `customer_email` on each row (test data = `dominik@fronc.eu`).
- **Human-in-the-Loop** — every email (reply and follow-up) is approved in the Activity Inbox before sending.

---

## 6. Key behaviours

- **Hands-free**: agents create the sheets they need and never ask the operator to set anything up; the catalog is searched directly in the Drive feeds via `grep` in the sandbox.
- **Dedup / growing CSV**: each inquiry becomes a case exactly once; new questions added to the CSV become new cases.
- **Confidence gate**: ambiguous matches are not guessed — they're flagged "Needs review" / failed rather than sent.
- **Auto-language**: the reply is written in the customer's language.
- **Upsell + fitment + PDF quote**: every reply can include relevant add-ons, a fitment-guarantee line, and an attached branded quote.
- **Auto follow-up**: 3 days after sending, if the customer hasn't replied, a single approved reminder is sent.

---

## 7. Known limitations

- **Email rendering:** the reply is sent as the branded **HTML template** (FITSHARK card, status badge,
  "Order this part" button, upsell, footer) by placing the HTML in the Gmail send `body`, which the
  connector renders. A branded **PDF quote** is also attached. (Plain text is kept only as an internal
  fallback.) The same HTML template is used for both in-stock and out-of-stock replies — only the badge
  and the price/delivery values change.
- **Order links** point at the demo storefront `shop.fitshark.example` — swap the base URL for a real shop to make them live.
- The Google **Drive connector is read-only** (download + list; no upload) — files are edited locally and re-uploaded manually.

---

## 8. Operate it

- **Seed the queue** from the questions (one case per inquiry): `duvo cases create --queue <id> --from-file cases.json`.
- The consumer's case trigger then dispatches up to 10 jobs in parallel; approve each reply in the
  **Activity Inbox** (or Slack/Teams if enabled).
- Regenerate the slim catalog: `python3 duvo/prepare_duvo_data.py`.
- The Duvo build is driven entirely through the `@duvoai/cli` (a thin wrapper over the Duvo API), which
  mirrors the Duvo MCP server — anything here can also be done from a Duvo-MCP-connected client.

---

*All data in this repo is synthetic. Brands and vehicle models are real only for feed realism.*
