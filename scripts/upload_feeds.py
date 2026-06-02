#!/usr/bin/env python3
"""Upload Fitshark supplier feed TSVs into Google Sheets (one spreadsheet per seller).

Streams each feed from disk into Drive (media upload -> convert to a Google Sheet),
so the data never passes through any model context. Renames the imported tab to
`Catalog` and adds the 4 standard header-only tabs.

Auth: Application Default Credentials with Drive + Sheets scope, e.g.
  gcloud auth application-default login \
    --scopes=openid,https://www.googleapis.com/auth/userinfo.email,\
https://www.googleapis.com/auth/drive,https://www.googleapis.com/auth/spreadsheets

Usage:  python upload_feeds.py aps            # one feed
        python upload_feeds.py aps mds bpr     # several
"""
import json
import os
import subprocess
import sys

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Duvo Google Sheets connection account — sheets must be accessible to it.
DUVO_ACCOUNT = "marekpodhorsky1993@gmail.com"

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEEDS_DIR = os.path.join(REPO_DIR, "feeds")

# prefix -> (seller_id, supplier display name)
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

HEADERS = {
    "Inbound_Questions": ["id", "received_at", "seller_id", "customer_name", "customer_email",
                           "language", "vehicle_make", "vehicle_model", "vehicle_year",
                           "vehicle_engine", "vin", "asked_part_text", "asked_sku", "status",
                           "created_at"],
    "Fitment": ["sku", "make", "model", "year_from", "year_to", "engine", "oem_numbers", "notes"],
    "Supplier_Catalog": ["supplier_sku", "product_name", "brand", "part_category", "fits_make",
                          "fits_model", "fits_year_from", "fits_year_to", "wholesale_price_eur",
                          "lead_time_days", "supplier_name", "supplier_portal_url"],
    "Orders": ["order_id", "question_id", "seller_id", "customer_email", "decision",
               "recommended_sku", "action_taken", "po_supplier_sku", "po_qty", "po_total_eur",
               "reply_sent_at", "approved_by", "status", "est_revenue_eur", "notes"],
}


def main(prefixes):
    token = subprocess.check_output(
        ["gcloud", "auth", "print-access-token"]).decode().strip()
    creds = Credentials(token=token)
    drive = build("drive", "v3", credentials=creds)
    sheets = build("sheets", "v4", credentials=creds)

    me = drive.about().get(fields="user(emailAddress)").execute()["user"]["emailAddress"]
    print(f"# authenticated as: {me}", file=sys.stderr)

    results = []
    for prefix in prefixes:
        if prefix not in SELLERS:
            print(f"!! unknown prefix {prefix}, skipping", file=sys.stderr)
            continue
        seller_id, supplier = SELLERS[prefix]
        path = os.path.join(FEEDS_DIR, f"feed_{prefix}.tsv")
        if not os.path.exists(path):
            print(f"!! missing {path}, skipping", file=sys.stderr)
            continue

        title = f"Fitshark - {supplier} ({seller_id})"
        print(f"# uploading {path} -> '{title}'", file=sys.stderr)

        # 1) Drive media upload + convert TSV -> Google Sheet
        media = MediaFileUpload(path, mimetype="text/tab-separated-values", resumable=True)
        created = drive.files().create(
            body={"name": title, "mimeType": "application/vnd.google-apps.spreadsheet"},
            media_body=media, fields="id,webViewLink",
        ).execute()
        sid = created["id"]
        url = created.get("webViewLink", f"https://docs.google.com/spreadsheets/d/{sid}/edit")

        # 2) Inspect imported sheet, rename first tab -> Catalog
        meta = sheets.spreadsheets().get(
            spreadsheetId=sid, fields="sheets.properties").execute()
        first = meta["sheets"][0]["properties"]
        rows = first.get("gridProperties", {}).get("rowCount")
        cols = first.get("gridProperties", {}).get("columnCount")

        requests = [{"updateSheetProperties": {
            "properties": {"sheetId": first["sheetId"], "title": "Catalog"},
            "fields": "title"}}]
        # 3) Add the 4 standard tabs
        for tab in HEADERS:
            requests.append({"addSheet": {"properties": {"title": tab}}})
        sheets.spreadsheets().batchUpdate(
            spreadsheetId=sid, body={"requests": requests}).execute()

        # 4) Write header rows into the 4 tabs
        data = [{"range": f"{tab}!A1", "values": [cols_]} for tab, cols_ in HEADERS.items()]
        sheets.spreadsheets().values().batchUpdate(
            spreadsheetId=sid,
            body={"valueInputOption": "RAW", "data": data}).execute()

        # 5) Share with the Duvo account if we are not it
        if me.lower() != DUVO_ACCOUNT.lower():
            try:
                drive.permissions().create(
                    fileId=sid, sendNotificationEmail=False,
                    body={"type": "user", "role": "writer", "emailAddress": DUVO_ACCOUNT},
                ).execute()
                shared = DUVO_ACCOUNT
            except Exception as e:  # noqa
                shared = f"FAILED: {e}"
        else:
            shared = "owner (no share needed)"

        results.append({
            "seller_id": seller_id, "supplier": supplier, "prefix": prefix,
            "spreadsheet_id": sid, "spreadsheet_url": url,
            "catalog_grid_rows": rows, "catalog_grid_cols": cols,
            "tabs": ["Catalog"] + list(HEADERS.keys()), "shared_with": shared,
        })
        print(f"# done: {sid} ({rows} rows x {cols} cols)", file=sys.stderr)

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    args = sys.argv[1:] or ["aps"]
    main(args)
