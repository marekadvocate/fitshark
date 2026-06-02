#!/usr/bin/env python3
"""Distribute customer_questions.csv into each seller's Inbound_Questions tab.

Each question is routed by `expected_supplier` to the right seller spreadsheet.
The raw free-text question goes into `asked_part_text`; vehicle/SKU are left blank
on purpose so the fitment-producer assignment performs the extraction. The
`expected_*` columns are an answer key for validation and are NOT written.

Auth: active gcloud account with Drive scope (gcloud auth login --enable-gdrive-access).
Usage: python upload_questions.py
"""
import csv
import os
import subprocess
import sys

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(REPO, "questions", "customer_questions.csv")
SEED_DATE = "2026-06-02T09:00:00Z"

# supplier display name -> (seller_id, spreadsheet_id)
SUPPLIERS = {
    "AutoParts Slovakia Ltd.": ("seller_001", "19Nbq5rEumh2tDXc01QtM-1o1sqr6O5J75kU2tw1QA-k"),
    "MotoParts SK Ltd.":       ("seller_002", "1oIech2NwtIBcZxd4xNJbtBztK-DBt6FleZn0v7L52tM"),
    "BrakePro Ltd.":           ("seller_003", "1Cc12H6cUGB2xZa5v2aP5U4pFoa6Of24qnqgixeZUC9g"),
    "FilterCentre Ltd.":       ("seller_004", "1cgRkky0HZV4j5r7qMdo-_sQ8xWndtPQYLuulbV9BoCw"),
    "OilExpert Ltd.":          ("seller_005", "1qUTudtkUKh2I0q63cI9tgC8OfHbv6nzJAbxJtS-6Lt8"),
    "TyreService SK Ltd.":     ("seller_006", "1P20JP8u5Vizm_ptRYFR2nSulNMeR4zENgf3LWUiKPr4"),
    "ElectroAuto Ltd.":        ("seller_007", "1ImURaxdJLcOkJVp74x_UcpCRqoQdU0-8-6UD7tM_beA"),
    "PartsExpress Ltd.":       ("seller_008", "1fXuFHoi-pu6YDf76O5INts9xwdnMcxMJGadbYmYXQ-4"),
    "CarStyle Ltd.":           ("seller_009", "1IGIweETmdA5WsQBkHjGIerxqK7-99KfaQbtMn0llZu0"),
    "EuroParts Plc.":          ("seller_010", "1ek1nYHOOiyCC-AKBeoP4Rjsdqz8b1ycP-JrZ5rcs8yA"),
    "MotoMarket Ltd.":         ("seller_011", "1fqzgeBjwVc7Ctc_1v73S2daxU0VDtWpfOLjHhYPkeaE"),
}

# Inbound_Questions header order
HEADER = ["id", "received_at", "seller_id", "customer_name", "customer_email", "language",
          "vehicle_make", "vehicle_model", "vehicle_year", "vehicle_engine", "vin",
          "asked_part_text", "asked_sku", "status", "created_at"]


def main():
    tok = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode().strip()
    sheets = build("sheets", "v4", credentials=Credentials(token=tok))

    by_seller = {}  # spreadsheet_id -> list of rows
    unknown = []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        for q in csv.DictReader(f):
            sup = q["expected_supplier"].strip()
            if sup not in SUPPLIERS:
                unknown.append(sup)
                continue
            seller_id, sid = SUPPLIERS[sup]
            qid = q["question_id"].strip()
            row = [
                qid, SEED_DATE, seller_id,
                f"Test Customer {qid}", f"{qid.lower()}@example.test", "en",
                "", "", "", "", "",                    # vehicle/vin -> producer extracts
                q["customer_question"].strip(), "",     # asked_part_text, asked_sku
                "new", SEED_DATE,
            ]
            by_seller.setdefault(sid, []).append(row)

    total = 0
    for sid, rows in by_seller.items():
        sheets.spreadsheets().values().append(
            spreadsheetId=sid, range="Inbound_Questions!A1",
            valueInputOption="RAW", insertDataOption="INSERT_ROWS",
            body={"values": rows},
        ).execute()
        total += len(rows)
        print(f"# {sid}: +{len(rows)} questions")

    print(f"\nDONE: wrote {total} questions across {len(by_seller)} sellers")
    if unknown:
        print("!! unmapped suppliers:", sorted(set(unknown)), file=sys.stderr)


if __name__ == "__main__":
    main()
