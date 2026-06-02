#!/usr/bin/env python3
"""Build pre-matched Duvo cases (JSON array) for the fitshark-questions queue.

For each customer question, resolve the matching product from catalog.csv (using the
oracle `expected_sku` in the questions CSV) and attach up to 2 vehicle-compatible upsell
items, so the lightweight queue consumer can compose + send without searching feeds.

Output: cases.json (array, max 100) → seed with:
  duvo cases create --queue <id> --from-file duvo/cases.json
"""
import csv, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # fitshark/
CATALOG = os.path.join(ROOT, "duvo", "catalog.csv")
QUESTIONS = os.path.join(ROOT, "questions", "customer_questions.csv")
OUT = os.path.join(ROOT, "duvo", "cases.json")

cat, by_vehicle = {}, {}
with open(CATALOG, encoding="utf-8") as f:
    for r in csv.DictReader(f):
        cat[r["supplier_sku"]] = r
        by_vehicle.setdefault(r["vehicle_compatibility"], []).append(r)


def upsell_for(m):
    pool = [x for x in by_vehicle.get(m["vehicle_compatibility"], []) if x["supplier_sku"] != m["supplier_sku"]]
    seen, out = set(), []
    for x in sorted(pool, key=lambda x: (x["availability"] != "In stock", x["category"])):
        if x["category"] == m.get("category") or x["category"] in seen:
            continue
        seen.add(x["category"])
        out.append({"product_name": x["product_name"], "sku": x["supplier_sku"],
                    "price_incl_vat": x["price_incl_vat"], "currency": x["currency"]})
        if len(out) >= 2:
            break
    return out


cases, missing = [], 0
for r in csv.DictReader(open(QUESTIONS, encoding="utf-8")):
    m = cat.get(r.get("expected_sku", ""))
    if not m:
        missing += 1
        matched, ups = None, []
    else:
        matched = {k: m[v] for k, v in {
            "sku": "supplier_sku", "product_name": "product_name", "brand": "brand",
            "variant_value": "variant_value", "vehicle_compatibility": "vehicle_compatibility",
            "supplier": "supplier", "availability": "availability", "lead_time": "lead_time",
            "price_incl_vat": "price_incl_vat", "currency": "currency", "image_url": "image_url"}.items()}
        ups = upsell_for(m)
    data = {"question_id": r["question_id"], "customer_question": r["customer_question"],
            "customer_email": r["customer_email"], "matched": matched, "upsell": ups}
    cases.append({"title": f'{r["question_id"]}: {matched["product_name"] if matched else "??"}',
                  "data": json.dumps(data, ensure_ascii=False),
                  "labels": [{"key": "batch", "value": "prod100"}]})

json.dump(cases, open(OUT, "w", encoding="utf-8"), ensure_ascii=False)
print(f"{len(cases)} cases -> {OUT} (unmatched: {missing})")
