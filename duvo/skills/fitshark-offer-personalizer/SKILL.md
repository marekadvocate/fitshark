---
name: fitshark-offer-personalizer
description: Build a personalized, seasonally-relevant parts offer for a known customer using their saved vehicle. Use when running later marketing/re-engagement campaigns off the Customer Vehicles table — given a customer's vehicle and history, propose the most relevant parts to offer next. Returns a ranked, vehicle-specific offer.
---

# Fitshark — Personalized Offer Engine

Turns a saved customer + vehicle (from the "Fitshark — Customer Vehicles" sheet) into a relevant,
well-timed parts offer. Powers later "we have something for your car" campaigns — not the initial reply.

## Inputs
From the Vehicles table: customer_email, vehicle_make/model/generation/years, vehicle_compatibility,
last_category, last_product, last_sku, last_seen, inquiries_count. Also: current_date / season, and
access to the Catalog sheet (columns A–O) to find offerable parts that fit the vehicle.

## How to pick the offer
1. **Fitment first** — only parts whose vehicle_compatibility matches the customer's vehicle (or Universal).
2. **Seasonality** (use current_date):
   - Autumn/Winter → battery, winter tires, wiper blades, antifreeze/AdBlue, bulbs.
   - Spring/Summer → summer tires, A/C cabin filter, brakes check, fluids.
3. **Service logic** — items complementary to what they bought (e.g., bought pads earlier → discs now;
   bought oil → filters), and consumables likely due given vehicle age (years).
4. **Don't repeat** — avoid re-offering the exact last_sku they already enquired about unless it's a
   genuine refill/replacement cycle.
5. Rank by fitment confidence → seasonality → margin-neutral relevance. Keep to **2–4 items**.

## Output
```
OFFER_FOR: <customer_email> (<vehicle_compatibility>)
THEME: <e.g. "Winter readiness for your VW Golf VII">
ITEMS:
- <product_name> — <price_incl_vat> <currency> — <order_link>
- <product_name> — <price_incl_vat> <currency> — <order_link>
RATIONALE: <one short line on why these, for the approver>
```
Compose the actual email with fitshark-reply-writer (campaign tone) + fitshark-brand-voice, and build
links with fitshark-product-link. Always send personalized offers behind human approval.

## Don'ts
- Never offer parts that don't fit the customer's vehicle.
- Respect opt-out / do-not-contact if such a flag exists in the Vehicles table.
- No internal data in customer-facing text. Don't invent prices — read them from the Catalog.
