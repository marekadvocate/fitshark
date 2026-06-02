# Fitshark — Cross-Catalog Automotive Marketplace Agent

Fitshark turns pre-purchase automotive questions — *"does this part fit my car / how much / how
soon?"* — into **immediate, accurate, grounded answers**, delivered as a **branded HTML email** with
a **unique per-customer buy link**. A human approves every send (Human-in-the-Loop).

**v2 is a marketplace/aggregator:** Fitshark is the customer-facing brand; suppliers are backend.
A question is **not pre-routed** to one shop — the agent searches **across all 11 supplier catalogs**
and returns the best market match (price / stock / lead time). Supplier names, internal SKUs,
wholesale prices and margins are **never exposed** to the customer.

Built entirely on **[Duvo](https://www.duvo.ai)** (orchestrated via the Duvo MCP server) + Google
Sheets + Gmail. This repo holds the **synthetic test data** and the **loader/build scripts**; the
live logic lives in Duvo objects.

> ⚠️ Synthetic data only — fictional suppliers, random codes/EANs/prices. Test customer emails are the
> team's own inboxes. Manufacturer brands and vehicle models are real for feed realism.

---

## Architecture

```
        Fitshark Questions (1 central sheet)        Master Catalog Index (1 sheet, ~110k rows)
                     │  status=new                            ▲ one read + in-code filter
                     ▼                                        │ (search ALL 11 suppliers)
        ┌────────────────────────┐   case    ┌───────────────┴───────────────────────────┐
        │  fitment-producer       │ ───────▶ │  fitment-consumer                          │
        │  poll · infer intent/   │  queue   │  best-match → unique buy link → reply →     │
        │  vehicle/part (symptoms)│ fitment_ │  localize → HTML → HITL → Gmail send →      │
        └────────────────────────┘  intent  │  Fitshark Orders (full answer log)          │
                                             └─────────────────────────────────────────────┘
                                                   Human-in-the-Loop · Gmail (HTML)
```

- **Producer** polls the central **Questions** sheet, infers what the customer needs (even from
  symptoms — *"squeals when braking"* → brake pads), and enqueues a normalized case (no seller_id).
- **Consumer** searches the **Master Catalog Index** across all suppliers in one read + in-code
  filter, picks the best offer, builds a unique buy link, drafts a Fitshark-branded HTML reply,
  pauses at a **HITL gate**, sends via Gmail, and logs to **Orders**.

### Data files (Google Sheets)

| File | Role |
|---|---|
| 11 × **Catalog** | full supplier feed, **one `Catalog` tab only** (read-only product source) |
| **Master Catalog Index** | ~110k rows, slim columns + `seller_id` — the cross-catalog search surface |
| **Fitshark Questions** | central intake of customer questions (`new → queued → answered`) |
| **Fitshark Orders** | central, searchable **full answer log** (question, match, reply, status, …) |

### Skills (Duvo)

`fitment-decision` (cross-catalog best-match) · `fitshark-product-link` (plain `/p/` link + **unique
per-customer `/buy/` link**) · `fitshark-reply-writer` (Fitshark-branded reply, hides internals) ·
`seller-voice` (multilingual localization SK/CZ/EN/DE/PL) · `fitshark-email-template` (branded HTML
email + CTA buy button + plain-text fallback).

### Unique per-customer buy link

```
https://shop.fitshark.example/buy/<slug>?cid=<question_id>&t=<token8>
```
`<slug>` = lowercased SKU (non-alphanumeric → hyphen); `<token8>` = first 8 hex of
`sha256(customer_email + "|" + supplier_sku)`. Deterministic yet unique to (customer, product).

---

## Test data in this repo

### `feeds/` — 11 supplier feeds (11 × ~10,000 SKU, 70 columns, TSV)

Market SK · EUR · VAT 23%. Vehicle fitment is in structured columns
(`vehicle_make/model/generation/year_from/year_to/compatibility`, `Universal` for non-vehicle parts).
Each feed = one supplier → one seller (`feed_aps.tsv` → AutoParts Slovakia → `seller_001`, etc.).

### `feeds/master_index.tsv` — Master Catalog Index (110k rows, 18 columns)

Built from the 11 feeds: `seller_id, supplier, supplier_sku, product_name, brand, category,
oe_numbers, vehicle_*`, `retail_price_incl_vat, stock_qty, availability, lead_time_days,
product_link`.

### `questions/customer_questions.csv` — 100 customer questions

**Multilingual** (SK/CZ/EN/DE/PL, ~20 each), `customer_email` alternates between the two real test
inboxes, ~7 **symptom/implicit** questions (part not named → tests inference). `expected_*` columns
are the answer-key (not fed to the agent).

---

## Scripts (`scripts/`)

```bash
python3 -m venv .venv && .venv/bin/pip install google-api-python-client google-auth-httplib2
gcloud auth login --enable-gdrive-access     # Google account that owns the sheets

python3 scripts/make_questions.py            # regenerate multilingual questions
python3 scripts/build_index.py               # build feeds/master_index.tsv

.venv/bin/python scripts/sheets_admin.py strip             # remove extra tabs from the 11 catalogs
.venv/bin/python scripts/sheets_admin.py create-index      # → Master Catalog Index sheet
.venv/bin/python scripts/sheets_admin.py create-questions  # → Fitshark Questions sheet
.venv/bin/python scripts/sheets_admin.py create-orders     # → Fitshark Orders sheet
```

- `make_questions.py` — multilingual questions + real test emails + symptom/implicit cases.
- `build_index.py` — build the Master Catalog Index from the feeds.
- `sheets_admin.py` — strip catalog tabs; create the Index / Questions / Orders sheets.
- `upload_feeds.py` — upload each feed into its own Google Sheet (catalog).
- `generate_rich.py`, `generate_feed.py`, `generate_varied.py` — feed generators.

Object IDs (sheets, agents, skills, connections) are recorded in `config/fitshark.json`. Design and
plan live in `docs/superpowers/`.

## Running

1. Populate the sheets (scripts above); `config/fitshark.json` has every ID.
2. **Go live:** enable the `fitment-producer` schedule (every 5 min) or start a manual run.
3. Producer enqueues questions → consumer matches across catalogs → pauses at the Human-in-the-Loop
   gate → approve in the **Duvo dashboard** → branded HTML email is sent and the `Orders` row written.
