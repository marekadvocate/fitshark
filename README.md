# fitshark

Test automotive product feeds for developing and testing feed-ingestion agents.

## Overview

`feeds/` contains **11 synthetic supplier feeds**, each from a different (fictional) supplier.
They serve as input data for an agent that processes product feeds from Google Sheets.

> ⚠️ All data is **generated / synthetic** — fictional suppliers, random codes, EANs and prices.
> Manufacturer brands (Bosch, Brembo, Mann-Filter…) and vehicle models are real only for feed realism.

### Parameters

- **11 feeds × 10,000 SKU** (1 row = 1 SKU/variant)
- **67 columns** per product
- Market SK, currency EUR, VAT 23%
- **TSV (TAB-separated)** format — ready for direct paste into Google Sheets
- All headers and content in English

### Feed list

| File | Supplier | Focus |
|---|---|---|
| `feed_mds.tsv` | MotoDiely SK s.r.o. | full range |
| `feed_aps.tsv` | AutoParts Slovakia s.r.o. | full range |
| `feed_bpr.tsv` | BrzdyPro s.r.o. | brakes |
| `feed_flc.tsv` | FilterCentrum s.r.o. | filters |
| `feed_olx.tsv` | OlejExpert s.r.o. | oils / fluids |
| `feed_pns.tsv` | PneuServis SK s.r.o. | tires + wheels |
| `feed_ela.tsv` | ElektroAuto s.r.o. | batteries + lighting |
| `feed_dex.tsv` | DielyExpres s.r.o. | spare parts |
| `feed_cst.tsv` | CarStyle s.r.o. | accessories |
| `feed_eud.tsv` | EuroDiely a.s. | full range |
| `feed_mmk.tsv` | MotoMarket s.r.o. | full range |

### Parameter groups (67 columns)

Identity (sku, EAN, MPN, OE numbers, TecDoc) · brand/classification · text (name, short/long description) ·
variants (type, value, fitment position, side, color) · pricing (wholesale/retail excl. & incl. VAT, margin %,
discount, sale price, unit price, core deposit) · stock & logistics · physical dimensions and weight ·
automotive (vehicle compatibility, production years, standards, HS customs code, country of origin,
condition new/remanufactured) · tire EU label · oil standards · media and meta.

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
