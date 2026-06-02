#!/usr/bin/env python3
"""Prepare Google-Sheets-ready data for the Duvo fitshark agent.

Outputs (all in fitshark/duvo/):
  - ../questions/customer_questions.csv  : git oracle CSV, with customer_email added (in place)
  - questions_sheet.csv                  : agent INPUT for the Questions sheet (NO oracle cols)
  - catalog.csv                          : slim searchable product catalog (all 11 feeds)
"""
import csv, glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # fitshark/
DUVO = os.path.join(ROOT, "duvo")
FEEDS = sorted(glob.glob(os.path.join(ROOT, "feeds", "feed_*.tsv")))
TEST_EMAIL = "dominikfronc@gmail.com"
LINK_BASE = "https://shop.fitshark.example/p/"   # dynamic product link base (placeholder, configurable)

# ---------- 1) add customer_email to the git oracle CSV (in place) ----------
qpath = os.path.join(ROOT, "questions", "customer_questions.csv")
with open(qpath, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
oracle_fields = list(rows[0].keys())
if "customer_email" not in oracle_fields:
    # insert customer_email right after customer_question
    idx = oracle_fields.index("customer_question") + 1
    oracle_fields.insert(idx, "customer_email")
for r in rows:
    r["customer_email"] = TEST_EMAIL
with open(qpath, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=oracle_fields)
    w.writeheader(); w.writerows(rows)
print(f"[1] git oracle updated with customer_email -> {len(rows)} rows")

# ---------- 2) clean agent-input Questions sheet (no expected_* oracle) ----------
qsheet_fields = ["question_id", "customer_question", "customer_email", "status",
                 "matched_sku", "matched_supplier", "matched_product",
                 "price_incl_vat", "currency", "lead_time", "product_link",
                 "date_sent", "notes"]
with open(os.path.join(DUVO, "questions_sheet.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=qsheet_fields)
    w.writeheader()
    for r in rows:
        w.writerow({"question_id": r["question_id"],
                    "customer_question": r["customer_question"],
                    "customer_email": TEST_EMAIL,
                    "status": "Pending"})
print(f"[2] questions_sheet.csv written ({len(rows)} rows, status=Pending, oracle stripped)")

# ---------- 3) slim searchable catalog from all 11 feeds ----------
cat_fields = ["supplier_sku", "product_name", "brand", "category", "subcategory",
              "variant_value", "vehicle_compatibility", "supplier",
              "availability", "lead_time", "lead_time_days",
              "price_incl_vat", "currency", "image_url", "product_link"]
n = 0
with open(os.path.join(DUVO, "catalog.csv"), "w", newline="", encoding="utf-8") as out:
    w = csv.DictWriter(out, fieldnames=cat_fields)
    w.writeheader()
    for feed in FEEDS:
        with open(feed, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f, delimiter="\t"):
                sku = r["supplier_sku"]
                w.writerow({
                    "supplier_sku": sku,
                    "product_name": r["product_name"],
                    "brand": r["brand"],
                    "category": r["category"],
                    "subcategory": r["subcategory"],
                    "variant_value": r["variant_value"],
                    "vehicle_compatibility": r["vehicle_compatibility"],
                    "supplier": r["supplier"],
                    "availability": r["availability"],
                    "lead_time": r["lead_time"],
                    "lead_time_days": r["lead_time_days"],
                    "price_incl_vat": r["retail_price_incl_vat"],   # matches oracle
                    "currency": r["currency"],
                    "image_url": r["image_url"],
                    "product_link": LINK_BASE + sku.lower(),
                })
                n += 1
print(f"[3] catalog.csv written ({n} rows from {len(FEEDS)} feeds)")
