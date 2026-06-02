---
name: fitshark-upsell-recommender
description: Recommend complementary cross-sell and trade-up items for a matched auto part. Use when composing a customer reply or quote to suggest 1-3 relevant add-ons (and optionally a premium alternative) that fit the same vehicle, to raise order value without being pushy. Returns a short, ranked list of suggestions with price and order link.
---

# Fitshark — Upsell & Cross-sell Recommender

Given the product the customer asked about (and their vehicle), suggest a few genuinely useful
companion items and, where it makes sense, one premium trade-up. The goal is a higher order value
AND a more helpful reply — never spam. Keep it to **1–3 suggestions**.

## Inputs
matched product: product_name, brand, category, subcategory, variant_value, vehicle_compatibility,
price_incl_vat, currency. Access to the Catalog sheet (same columns A–O) to look up companions.

## Cross-sell map (by category — pick what fits, fitment must match the vehicle or be Universal)
- **Lighting** (H7/H4 bulbs) → the matching pair (2 pcs) if they asked for 1; the other position
  (low/high beam); wiper blades; bulb-grease.
- **Electrical / Battery** → battery terminals/clamps; smart charger/maintainer; terminal protector spray.
- **Brakes** (pads) → matching discs/rotors; brake fluid; sensor/wear indicator; caliper grease.
- **Filters** → the other filters due at the same service (oil/air/cabin/fuel); engine oil to match.
- **Tires** → the full set (4) or matching pair; valves/TPMS; wheel bolts; balancing note.
- **Fluids / Oil** → correct filter; funnel; the matching service kit.
- **Spare parts** (clutch/spark plugs) → related service items (e.g. clutch → release bearing/flywheel;
  plugs → ignition coils/leads).

## Rules for choosing
- Only suggest items that **fit the same vehicle** (vehicle_compatibility matches or Universal). Verify
  via the Catalog before suggesting — never invent a part or price.
- Rank by relevance, then by attach-rate logic above. Prefer in-catalog items with a real price.
- Optional **trade-up**: if a clearly premium equivalent exists (better brand/longer warranty), offer it
  as "Upgrade option" — at most one.
- Tone: helpful, not pushy. Frame as "customers with your <vehicle> often add…". Skip entirely if
  nothing genuinely relevant is found.

## Output
Return a compact block the reply-writer can drop in (each line has name, price, and an order link built
via the fitshark-product-link skill):
```
SUGGESTIONS:
- <product_name> — <price_incl_vat> <currency> — <order_link>
- <product_name> — <price_incl_vat> <currency> — <order_link>
UPGRADE (optional):
- <premium product_name> — <price_incl_vat> <currency> — <order_link>
```
If nothing relevant: return `SUGGESTIONS: (none)`.

## Don'ts
- Don't pad the email — 1–3 max, all genuinely relevant and vehicle-compatible.
- Don't expose internal data (SKU codes, supplier names, margins).
- Don't suggest items that are themselves out of stock unless you also give their lead time.
