#!/usr/bin/env python3
"""
Generates 100 realistic English customer questions about OUT-OF-STOCK products,
each matchable to a real product across all 11 feeds, evenly distributed.

Goal: input for an agent that searches these questions, recommends a matching
product from the feeds, and replies with price + delivery time.

Each question is built from a real feed row where availability is
'On order' / 'Incoming' and stock_qty = 0 — so a matching product always exists,
and a real price + lead time is available as ground truth.

Output: customer_questions.csv (RFC4180, comma-separated, UTF-8, ASCII content).

Run:  python3 make_questions.py
"""

import csv
import glob
import os
import random

random.seed(2024)

TOTAL = 100
FEEDS = sorted(glob.glob("feed_*.tsv"))  # 11 feeds
OUT = "customer_questions.csv"


# ── Question templates ──────────────────────────────────────────────────────
# {desc} = product descriptor, {veh} = vehicle (only for vehicle-specific parts)
TEMPLATES_VEHICLE = [
    "Hi, do you stock {desc} for a {veh}? It shows as out of stock on your site "
    "- could you tell me the price and expected delivery time?",
    "I need {desc} for my {veh}. It's currently unavailable - what would it cost "
    "and how soon could you deliver?",
    "Looking to order {desc} to fit a {veh}. Out of stock at the moment - please "
    "advise the price and lead time.",
    "Can you source {desc} for a {veh}? I saw it's on backorder. What's the price "
    "and when can I expect it?",
    "Hello, I'm after {desc} for a {veh}. Not in stock right now - could you quote "
    "the price and delivery time?",
]
TEMPLATES_UNIVERSAL = [
    "Hi, I'm after {desc}. It's showing as out of stock - could you give me the "
    "price and delivery time?",
    "Do you have {desc} available? It seems to be on backorder. How much is it and "
    "how long for delivery?",
    "I'd like to order {desc}. Currently not in stock - please quote the price and "
    "expected lead time.",
    "Need {desc}. Out of stock right now - what's the cost and delivery time?",
    "Hello, can you get {desc} in? It's listed as unavailable - price and lead "
    "time please.",
]


def descriptor(row):
    """Builds a natural product descriptor from a feed row (matchable to feeds)."""
    cat = row["category"]
    brand = row["brand"]
    name = row["product_name"]
    sub = row["subcategory"]

    # Items whose product_name is already fully descriptive (size/spec inside)
    if cat in ("Tires", "Wheels", "Electrical", "Fluids"):
        return name
    # Brakes / filters / spare parts / lighting / accessories:
    # use type + brand, optionally with variant for specificity
    variant = row.get("variant_value", "").strip()
    if variant and cat in ("Filters", "Accessories", "Lighting & visibility"):
        return f"{sub} ({brand}, {variant})"
    return f"{sub} by {brand}"


def make_question(row, idx):
    desc = descriptor(row)
    veh = row["vehicle_compatibility"]
    if veh and veh != "Universal":
        tpl = TEMPLATES_VEHICLE[idx % len(TEMPLATES_VEHICLE)]
        return tpl.format(desc=desc, veh=veh)
    tpl = TEMPLATES_UNIVERSAL[idx % len(TEMPLATES_UNIVERSAL)]
    return tpl.format(desc=desc)


def main():
    # Even distribution: 100 across 11 feeds -> one feed gets the +1 remainder
    base, extra = divmod(TOTAL, len(FEEDS))
    counts = [base + (1 if i < extra else 0) for i in range(len(FEEDS))]

    # Sample per feed from the not-in-stock pool
    sampled = []  # list of lists, one per feed
    for fn, n in zip(FEEDS, counts):
        rows = list(csv.DictReader(open(fn, encoding="utf-8"), delimiter="\t"))
        pool = [r for r in rows
                if r["availability"] in ("On order", "Incoming") and r["stock_qty"] == "0"]
        picks = random.sample(pool, n)
        for r in picks:
            r["_feed"] = os.path.basename(fn)
        sampled.append(picks)

    # Round-robin interleave for an even spread across feeds in the sheet
    ordered = []
    i = 0
    while len(ordered) < TOTAL:
        for feed_picks in sampled:
            if i < len(feed_picks):
                ordered.append(feed_picks[i])
                if len(ordered) == TOTAL:
                    break
        i += 1

    cols = [
        "question_id", "customer_question",
        "expected_supplier", "expected_feed_file", "expected_sku",
        "expected_product_name", "expected_brand", "expected_category",
        "expected_vehicle", "expected_variant",
        "availability", "expected_lead_time",
        "expected_price_incl_vat", "currency",
    ]
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for idx, r in enumerate(ordered, 1):
            w.writerow([
                f"Q{idx:03d}",
                make_question(r, idx),
                r["supplier"], r["_feed"], r["supplier_sku"],
                r["product_name"], r["brand"], r["category"],
                r["vehicle_compatibility"], r.get("variant_value", ""),
                r["availability"], r["lead_time"],
                r["retail_price_incl_vat"], r["currency"],
            ])
    print(f"Done: {TOTAL} questions -> {OUT}")
    print(f"Per-feed counts: {dict(zip([os.path.basename(x) for x in FEEDS], counts))}")


if __name__ == "__main__":
    main()
