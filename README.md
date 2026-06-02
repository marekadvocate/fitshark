# Fitshark — Fitment-to-Sale Automotive Agent System

Fitshark turns unanswered pre-purchase automotive questions — *"does this part fit my car?"* —
into **immediate, accurate, grounded answers**, and when needed into **drafted purchase orders**
and **personalized sales replies**. Instead of a human replying a day later (or never), an agent
starts working the moment a question arrives.

The system is a **producer/consumer "Chain"** built entirely on the **[Duvo](https://www.duvo.ai)**
platform (orchestrated via the Duvo MCP server) plus **Google Sheets** as the per-seller data store.
It is **multi-seller**: up to 11 automotive parts e-shops, each with its own Google Sheet and the
same Standard Operating Procedures (adding a seller is pure config — no SOP changes).

This repository holds the **synthetic test data** (supplier feeds + customer questions) and the
**loader scripts** that push that data into the sellers' Google Sheets. The live logic lives in
Duvo objects, not in this repo.

> ⚠️ **Synthetic data only.** Fictional suppliers, random codes/EANs/prices; test customers use
> `@example.test` addresses. Manufacturer brands and vehicle models are real only for feed realism.

---

## Architecture

```
                         Google Sheet per seller (×11)
                ┌──────────────────────────────────────────────┐
                │ Catalog · Inbound_Questions · Fitment ·        │
                │ Supplier_Catalog · Orders                      │
                └──────────────────────────────────────────────┘
                      ▲ read questions           ▲ read catalog / write audit
                      │                           │
   ┌──────────────────┴───────┐        ┌──────────┴───────────────────────┐
   │  fitment-producer        │  case  │  fitment-consumer                 │
   │  (poll → normalize →      │ ─────▶ │  decision tree → HITL gates →     │
   │   enqueue case)          │ queue  │   reply / PO → write-back audit   │
   └──────────────────────────┘        └───────────────────────────────────┘
        every-5-min schedule        fitment_intent          Human-in-the-Loop
                                     (shared queue)          Gmail · Supplier sourcing
```

- **Case Queue `fitment_intent`** — shared across all sellers. Each case carries labels
  `seller_id`, `language`, `intent`, `priority`.
- **`fitment-producer`** (assignment) — polls every seller's `Inbound_Questions` (status `new`),
  extracts customer / vehicle / part, detects language + intent, and enqueues one normalized case.
  Never replies to the customer.
- **`fitment-consumer`** (assignment) — triggered per new case. Runs the decision tree, drafts the
  reply / purchase order, pauses at **Human-in-the-Loop** gates, then acts and writes the audit row.
- **Skills** — `fitment-decision` (deterministic fit/alternative/source logic + strict output
  contract) and `seller-voice` (per-seller tone + multilingual reply templates SK/CZ/EN/DE/PL).
- **`feed-ingestion`** (assignment) — one-off helper to import a supplier feed into a seller Sheet.
- **Per-seller registry** — `seller_registry.json` (a Duvo file) maps `seller_id →
  {spreadsheet_id, gmail_connection, supplier_access, …}`. Adding sellers 2–11 = a new block here.

### Consumer decision tree (summary)

1. **Identify** the asked part in `Catalog` (SKU / OEM / name).
2. **Fitment** against the vehicle (make / model / year-range / engine):
   - fits + in stock → confirm reply (price + link),
   - fits + out of stock → pre-order / ETA reply,
   - doesn't fit → recommend the correct in-stock alternative,
   - no match / no stock / no alternative → **supplier sourcing**.
3. **Supplier sourcing** → draft a PO → **HITL gate #1** (approve the order).
4. **Draft customer reply** (seller-voice) → **HITL gate #2** (approve the send) → send via Gmail.
5. **Close & audit** → append a row to `Orders`, set the `Inbound_Questions` status.
6. *Escalation:* a negative-sentiment complaint with a phone number proposes an **Outbound Call**
   (HITL-approved) instead of an email.

**Every side-effect — sending an email, committing a PO, placing a call — passes through a Human-in-the-Loop
approval gate first.** The agent drafts; a human approves; only then does it act.

---

## Duvo objects (team *Advocate*)

| Object | Type | ID |
|---|---|---|
| `fitment_intent` | Case Queue | `ca600d25-f6e2-451e-a02d-a9f6e3f83b13` |
| `fitment-producer` | Assignment | `0e1c81c3-3352-4be4-9c14-9721fd4d4801` |
| `fitment-consumer` | Assignment | `a85a14d0-3b91-43d5-90ce-58927a0c3c5c` |
| `feed-ingestion` | Assignment | `5a331849-0752-44ea-9fb1-848bcaa37e5c` |
| `fitment-decision` | Skill | `b7cf089a-893a-4615-9dd6-339789ff3930` |
| `seller-voice` | Skill | `17b629d7-ce99-44ee-82b3-7fbc63a2d2fa` |
| Producer poll | Schedule (every 5 min) | `a34839b4-…` *(disabled until go-live)* |
| Consumer case trigger | Case Trigger | `64c75e50-…` *(enabled)* |

**Connections:** Google Sheets + Gmail (OAuth, pinned to both assignments), Human-in-the-Loop,
Enterprise Browser, Web Scraper, Outbound Call. OAuth connections are authorized in the Duvo UI
(or via `startNativeOAuth`) — they cannot be minted head­lessly.

---

## Data model — one Google Sheet per seller

Each seller's spreadsheet has five tabs:

| Tab | Purpose |
|---|---|
| `Catalog` | the supplier's full product feed (70 columns, ~10k SKU). Vehicle fitment is embedded per row, so the consumer reads fitment directly from here. |
| `Inbound_Questions` | incoming customer questions (`status = new → queued → answered/…`). |
| `Fitment` | documented placeholder — fitment is embedded in `Catalog` for this dataset. |
| `Supplier_Catalog` | fallback wholesale source for supplier sourcing (Step D). |
| `Orders` | the audit log: decision, action, approver, timestamps, est. revenue. |

The 11 sellers map 1:1 to the feeds in `feeds/` (e.g. `feed_aps.tsv` → *AutoParts Slovakia Ltd.*
→ `seller_001`).

---

## Test data in this repo

### Supplier feeds — `feeds/` (11 × ~10,000 SKU, 70 columns, TSV)

Market SK · EUR · VAT 23% · 100% ASCII English. Vehicle fitment is split into structured columns
using the **same spelling and format in every feed** (`vehicle_make`, `vehicle_model`,
`vehicle_generation`, `vehicle_year_from`/`vehicle_year_to`, `vehicle_compatibility`), so it is
searchable across feeds. 13 makes, 24 model+generation combos; universal parts use
`vehicle_compatibility = Universal`.

| File | Supplier → seller | Focus |
|---|---|---|
| `feed_aps.tsv` | AutoParts Slovakia Ltd. → `seller_001` | full range |
| `feed_mds.tsv` | MotoParts SK Ltd. → `seller_002` | full range |
| `feed_bpr.tsv` | BrakePro Ltd. → `seller_003` | brakes |
| `feed_flc.tsv` | FilterCentre Ltd. → `seller_004` | filters |
| `feed_olx.tsv` | OilExpert Ltd. → `seller_005` | oils / fluids |
| `feed_pns.tsv` | TyreService SK Ltd. → `seller_006` | tires + wheels |
| `feed_ela.tsv` | ElectroAuto Ltd. → `seller_007` | batteries + lighting |
| `feed_dex.tsv` | PartsExpress Ltd. → `seller_008` | spare parts |
| `feed_cst.tsv` | CarStyle Ltd. → `seller_009` | accessories |
| `feed_eud.tsv` | EuroParts Plc. → `seller_010` | full range |
| `feed_mmk.tsv` | MotoMarket Ltd. → `seller_011` | full range |

Column groups: identity (sku, EAN, MPN, OE numbers, TecDoc) · brand/classification · text · variants ·
pricing (wholesale/retail excl. & incl. VAT, margin, discount, sale, unit, core deposit) ·
stock & logistics · dimensions/weight · structured vehicle fitment · automotive (standards, HS code,
origin, condition) · tire EU label · oil standards · media & meta.

### Customer questions — `questions/customer_questions.csv` (100)

Realistic English inquiries about **out-of-stock products**, evenly distributed across the 11 sellers
(~9–10 each). Every question maps to a real feed row (`availability = On order`, `stock_qty = 0`), so
a matching product + real price + delivery time always exists.

| Column | Purpose |
|---|---|
| `question_id` | Q001–Q100 |
| `customer_question` | the natural-language inquiry (agent input) |
| `expected_*` | ground-truth match (supplier, feed file, sku, product, brand, category, vehicle, variant) |
| `availability`, `expected_lead_time`, `expected_price_incl_vat`, `currency` | reference answer for validation |

The `expected_*` columns are the test oracle — they are **not** fed to the agent.

---

## Loading data into Google Sheets

The feeds are too large (~6 MB each) for an LLM or `IMPORTDATA` to ingest reliably, so a local script
streams them straight into Drive (media upload → convert to a Google Sheet — data never passes through
any model context). Sheets are created under the Google account that backs the Duvo Sheets connection,
so the assignments can read/write them.

```bash
python3 -m venv .venv && .venv/bin/pip install google-api-python-client google-auth-httplib2
gcloud auth login --enable-gdrive-access          # log in as the Duvo Sheets account

.venv/bin/python scripts/upload_feeds.py aps      # one seller (feed_aps → seller_001)
.venv/bin/python scripts/upload_feeds.py mds bpr flc olx pns ela dex cst eud mmk   # the rest
.venv/bin/python scripts/upload_questions.py      # distribute the 100 questions to each seller
```

Each upload creates the 5 tabs, imports the feed into `Catalog`, and prints the `spreadsheet_id`.

### Scripts (`scripts/`)

- `upload_feeds.py` — feed TSV → one Google Sheet per seller (5 tabs).
- `upload_questions.py` — `customer_questions.csv` → each seller's `Inbound_Questions`.
- `generate_rich.py` — current feed generator (deterministic, 70-col English TSV).
- `make_questions.py` — regenerate the customer questions from the feeds.
- `generate_feed.py`, `generate_varied.py` — earlier / heterogeneous-schema generators.

---

## Running the pipeline

1. Ensure the seller Sheets are populated (above) and `seller_registry.json` has each
   `spreadsheet_id`.
2. **Go live:** enable the `fitment-producer` schedule (every 5 min) — or start a manual run.
3. The producer enqueues `new` questions → the consumer fires per case → it pauses at the
   Human-in-the-Loop gates → approve in the **Duvo dashboard** → it sends the reply / commits the PO
   and writes the `Orders` audit row.

> Status: all Duvo objects and data are in place; the producer schedule is left **disabled** so the
> live pipeline only starts on an explicit go-live.
