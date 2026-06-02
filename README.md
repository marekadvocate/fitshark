# fitshark

Test automotive product feeds for developing and testing feed-ingestion agents.

## Overview

`feeds/` contains **11 synthetic supplier feeds**, each from a different (fictional) supplier.
They serve as input data for an agent that processes product feeds from Google Sheets.

> ⚠️ All data is **generated / synthetic** — fictional suppliers, random codes, EANs and prices.
> Manufacturer brands (Bosch, Brembo, Mann-Filter…) and vehicle models are real only for feed realism.

### Parameters

- **11 feeds × 10,000 SKU** (1 row = 1 SKU/variant)
- **70 columns** per product
- Market SK, currency EUR, VAT 23%
- **TSV (TAB-separated)** format — ready for direct paste into Google Sheets
- All content **100% ASCII English** — no diacritics, consistent formatting for easy cross-feed search

### Feed list

| File | Supplier | Focus |
|---|---|---|
| `feed_mds.tsv` | MotoParts SK Ltd. | full range |
| `feed_aps.tsv` | AutoParts Slovakia Ltd. | full range |
| `feed_bpr.tsv` | BrakePro Ltd. | brakes |
| `feed_flc.tsv` | FilterCentre Ltd. | filters |
| `feed_olx.tsv` | OilExpert Ltd. | oils / fluids |
| `feed_pns.tsv` | TyreService SK Ltd. | tires + wheels |
| `feed_ela.tsv` | ElectroAuto Ltd. | batteries + lighting |
| `feed_dex.tsv` | PartsExpress Ltd. | spare parts |
| `feed_cst.tsv` | CarStyle Ltd. | accessories |
| `feed_eud.tsv` | EuroParts Plc. | full range |
| `feed_mmk.tsv` | MotoMarket Ltd. | full range |

### Vehicle data (consistent, searchable across all feeds)

Vehicle fitment is split into structured columns using the **same spelling and format in every feed**, so
you can filter/search across all of them:

| Column | Example |
|---|---|
| `vehicle_make` | `BMW` |
| `vehicle_model` | `5 Series` |
| `vehicle_generation` | `F10` |
| `vehicle_year_from` / `vehicle_year_to` | `2010` / `2017` |
| `vehicle_compatibility` | `BMW 5 Series F10 2010-2017` (canonical combined string) |

13 makes, 24 model+generation combinations. Universal products have empty vehicle fields and
`vehicle_compatibility = Universal`.

### Parameter groups (70 columns)

Identity (sku, EAN, MPN, OE numbers, TecDoc) · brand/classification · text (name, short/long description) ·
variants (type, value, fitment position, side, color) · pricing (wholesale/retail excl. & incl. VAT, margin %,
discount, sale price, unit price, core deposit) · stock & logistics · physical dimensions and weight ·
structured vehicle fitment (make, model, generation, years) · automotive (standards, HS customs code,
country of origin, condition new/remanufactured) · tire EU label · oil standards · media and meta.

## Customer questions (`questions/customer_questions.csv`)

100 realistic English customer inquiries about **out-of-stock products**, evenly distributed across
all 11 feeds (~9-10 each). Each question is built from a real feed row where `availability` is
`On order` / `Incoming` and `stock_qty = 0`, so a matching product always exists and a real price +
delivery time is available.

Intended as input for an agent that searches the questions, recommends a matching product from the
feeds, and replies with **price + delivery time**.

| Column | Purpose |
|---|---|
| `question_id` | Q001–Q100 |
| `customer_question` | the natural-language inquiry (agent input) |
| `expected_*` | ground-truth match (supplier, feed file, sku, product name, brand, category, vehicle, variant) |
| `availability`, `expected_lead_time`, `expected_price_incl_vat`, `currency` | reference answer for validating the agent |

Every question maps to a real SKU (verified: 0 unmatched, 0 in-stock, 100% ASCII). The `expected_*`
columns are the test oracle — hide/remove them if you want a blank test set.

Regenerate with `python3 scripts/make_questions.py` (run from the feeds directory).

## Paste into Google Sheets

1. Open `feeds/feed_<prefix>.tsv` → **Cmd/Ctrl+A → Cmd/Ctrl+C**
2. In Google Sheets click cell **A1** → **Cmd/Ctrl+V**
3. The TAB separator auto-splits into 67 columns.

If numbers show as text: *File → Settings → Locale* (feeds use a dot decimal separator, ISO date).

## Generating

`scripts/` contains the generators (Python 3, no dependencies):

```bash
cd scripts
python3 generate_rich.py   # current: 11 feeds × 67 parameters (TSV)
```

- `generate_rich.py` — current generator (67-column English TSV)
- `generate_feed.py` — original category-generator core
- `generate_varied.py` — heterogeneous-schema variant (mixed languages/delimiters) for normalization testing

Generation is deterministic (fixed per-supplier seed) — re-running produces identical feeds.
