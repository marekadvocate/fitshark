#!/usr/bin/env python3
"""Fitshark v2 Google Sheets admin (gcloud Drive/Sheets token).

Subcommands:
  strip            Remove the 4 extra tabs from each of the 11 catalog spreadsheets.
  create-index     Upload feeds/master_index.tsv -> 'Fitshark - Master Catalog Index'.
  create-questions Create 'Fitshark - Questions' from questions/customer_questions.csv.
  create-orders    Create 'Fitshark - Orders' (header only).

Auth: active gcloud account `marekpodhorsky1993` with Drive scope.
Usage: .venv/bin/python scripts/sheets_admin.py <subcommand>
"""
import csv
import os
import subprocess
import sys

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CATALOGS = {
    "seller_001": "19Nbq5rEumh2tDXc01QtM-1o1sqr6O5J75kU2tw1QA-k",
    "seller_002": "1oIech2NwtIBcZxd4xNJbtBztK-DBt6FleZn0v7L52tM",
    "seller_003": "1Cc12H6cUGB2xZa5v2aP5U4pFoa6Of24qnqgixeZUC9g",
    "seller_004": "1cgRkky0HZV4j5r7qMdo-_sQ8xWndtPQYLuulbV9BoCw",
    "seller_005": "1qUTudtkUKh2I0q63cI9tgC8OfHbv6nzJAbxJtS-6Lt8",
    "seller_006": "1P20JP8u5Vizm_ptRYFR2nSulNMeR4zENgf3LWUiKPr4",
    "seller_007": "1ImURaxdJLcOkJVp74x_UcpCRqoQdU0-8-6UD7tM_beA",
    "seller_008": "1fXuFHoi-pu6YDf76O5INts9xwdnMcxMJGadbYmYXQ-4",
    "seller_009": "1IGIweETmdA5WsQBkHjGIerxqK7-99KfaQbtMn0llZu0",
    "seller_010": "1ek1nYHOOiyCC-AKBeoP4Rjsdqz8b1ycP-JrZ5rcs8yA",
    "seller_011": "1fqzgeBjwVc7Ctc_1v73S2daxU0VDtWpfOLjHhYPkeaE",
}
EXTRA_TABS = {"Inbound_Questions", "Fitment", "Supplier_Catalog", "Orders"}

QUESTIONS_HEADER = ["id", "received_at", "customer_name", "customer_email", "language",
                    "raw_question", "status", "created_at"]
ORDERS_HEADER = ["order_id", "question_id", "received_at", "customer_name", "customer_email",
                 "language", "raw_question", "understood_query", "matched_seller_id",
                 "matched_supplier", "matched_sku", "product_name", "price_incl_vat", "currency",
                 "stock_qty", "availability", "lead_time_days", "decision", "alternatives",
                 "product_link", "buy_link", "reply_subject", "reply_body_plain",
                 "reply_body_html", "reply_sent_at", "approved_by", "status", "est_revenue_eur",
                 "notes", "created_at"]
SEED_TS = "2026-06-02T09:00:00Z"


def services():
    tok = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode().strip()
    creds = Credentials(token=tok)
    return build("drive", "v3", credentials=creds), build("sheets", "v4", credentials=creds)


def strip(drive, sheets):
    for seller_id, sid in CATALOGS.items():
        meta = sheets.spreadsheets().get(spreadsheetId=sid, fields="sheets.properties").execute()
        reqs = [{"deleteSheet": {"sheetId": s["properties"]["sheetId"]}}
                for s in meta["sheets"] if s["properties"]["title"] in EXTRA_TABS]
        if reqs:
            sheets.spreadsheets().batchUpdate(spreadsheetId=sid, body={"requests": reqs}).execute()
        meta2 = sheets.spreadsheets().get(spreadsheetId=sid, fields="sheets.properties").execute()
        tabs = [s["properties"]["title"] for s in meta2["sheets"]]
        print(f"{seller_id}: tabs={tabs}")


def create_index(drive, sheets):
    path = os.path.join(REPO, "feeds", "master_index.tsv")
    media = MediaFileUpload(path, mimetype="text/tab-separated-values", resumable=True)
    f = drive.files().create(
        body={"name": "Fitshark - Master Catalog Index",
              "mimeType": "application/vnd.google-apps.spreadsheet"},
        media_body=media, fields="id").execute()
    sid = f["id"]
    meta = sheets.spreadsheets().get(spreadsheetId=sid, fields="sheets.properties").execute()
    p = meta["sheets"][0]["properties"]
    # name the imported tab 'Index'
    sheets.spreadsheets().batchUpdate(spreadsheetId=sid, body={"requests": [
        {"updateSheetProperties": {"properties": {"sheetId": p["sheetId"], "title": "Index"},
                                    "fields": "title"}}]}).execute()
    g = p.get("gridProperties", {})
    print(f"INDEX spreadsheet_id={sid}  rows={g.get('rowCount')} cols={g.get('columnCount')}")
    print(f"url=https://docs.google.com/spreadsheets/d/{sid}/edit")


def create_questions(drive, sheets):
    rows = [QUESTIONS_HEADER]
    for q in csv.DictReader(open(os.path.join(REPO, "questions", "customer_questions.csv"),
                                 encoding="utf-8")):
        qid = q["question_id"]
        rows.append([qid, SEED_TS, f"Customer {qid}", q["customer_email"], q["language"],
                     q["customer_question"], "new", SEED_TS])
    f = sheets.spreadsheets().create(body={
        "properties": {"title": "Fitshark - Questions"},
        "sheets": [{"properties": {"title": "Questions"}}]}).execute()
    sid = f["spreadsheetId"]
    sheets.spreadsheets().values().update(
        spreadsheetId=sid, range="Questions!A1", valueInputOption="RAW",
        body={"values": rows}).execute()
    print(f"QUESTIONS spreadsheet_id={sid}  rows_written={len(rows) - 1}")
    print(f"url=https://docs.google.com/spreadsheets/d/{sid}/edit")


def create_orders(drive, sheets):
    f = sheets.spreadsheets().create(body={
        "properties": {"title": "Fitshark - Orders"},
        "sheets": [{"properties": {"title": "Orders"}}]}).execute()
    sid = f["spreadsheetId"]
    sheets.spreadsheets().values().update(
        spreadsheetId=sid, range="Orders!A1", valueInputOption="RAW",
        body={"values": [ORDERS_HEADER]}).execute()
    print(f"ORDERS spreadsheet_id={sid}  cols={len(ORDERS_HEADER)}")
    print(f"url=https://docs.google.com/spreadsheets/d/{sid}/edit")


CMDS = {"strip": strip, "create-index": create_index,
        "create-questions": create_questions, "create-orders": create_orders}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
        print("usage: sheets_admin.py {strip|create-index|create-questions|create-orders}")
        sys.exit(1)
    drive, sheets = services()
    CMDS[sys.argv[1]](drive, sheets)
