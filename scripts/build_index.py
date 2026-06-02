#!/usr/bin/env python3
"""Build the Master Catalog Index from the 11 supplier feeds.

Emits feeds/master_index.tsv — a slim, cross-catalog search surface (one row per SKU
across all sellers) used by the fitment-consumer to find the best market match.

Run: python3 scripts/build_index.py
"""
import csv
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEEDS_DIR = os.path.join(REPO, "feeds")
OUT = os.path.join(FEEDS_DIR, "master_index.tsv")

# prefix -> (seller_id, supplier display name)  [same mapping as upload_feeds.py]
SELLERS = {
    "aps": ("seller_001", "AutoParts Slovakia Ltd."),
    "mds": ("seller_002", "MotoParts SK Ltd."),
    "bpr": ("seller_003", "BrakePro Ltd."),
    "flc": ("seller_004", "FilterCentre Ltd."),
    "olx": ("seller_005", "OilExpert Ltd."),
    "pns": ("seller_006", "TyreService SK Ltd."),
    "ela": ("seller_007", "ElectroAuto Ltd."),
    "dex": ("seller_008", "PartsExpress Ltd."),
    "cst": ("seller_009", "CarStyle Ltd."),
    "eud": ("seller_010", "EuroParts Plc."),
    "mmk": ("seller_011", "MotoMarket Ltd."),
}

INDEX_COLS = [
    "seller_id", "supplier", "supplier_sku", "product_name", "brand", "category",
    "oe_numbers", "vehicle_make", "vehicle_model", "vehicle_generation",
    "vehicle_year_from", "vehicle_year_to", "vehicle_compatibility",
    "retail_price_incl_vat", "stock_qty", "availability", "lead_time_days", "product_link",
]


def slug(sku):
    s = re.sub(r"[^a-z0-9]+", "-", sku.lower()).strip("-")
    return s


def product_link(sku):
    return f"https://shop.fitshark.example/p/{slug(sku)}" if sku else ""


def main():
    n = 0
    with open(OUT, "w", newline="", encoding="utf-8") as out:
        w = csv.writer(out, delimiter="\t")
        w.writerow(INDEX_COLS)
        for prefix, (seller_id, supplier) in SELLERS.items():
            path = os.path.join(FEEDS_DIR, f"feed_{prefix}.tsv")
            for r in csv.DictReader(open(path, encoding="utf-8"), delimiter="\t"):
                sku = r["supplier_sku"]
                w.writerow([
                    seller_id, supplier, sku, r["product_name"], r["brand"], r["category"],
                    r["oe_numbers"], r["vehicle_make"], r["vehicle_model"],
                    r["vehicle_generation"], r["vehicle_year_from"], r["vehicle_year_to"],
                    r["vehicle_compatibility"], r["retail_price_incl_vat"], r["stock_qty"],
                    r["availability"], r["lead_time_days"], product_link(sku),
                ])
                n += 1
    print(f"Done: {n} rows -> {OUT} ({len(INDEX_COLS)} cols)")


if __name__ == "__main__":
    main()
