GOAL: For every pending customer inquiry in the Questions sheet, find the matching product in the Catalog, draft a professional reply with price and delivery time, get human approval, and email the customer one question at a time.

# CONNECTIONS USED
- Google Sheets — read the Questions and Catalog sheets, write results back to the Questions sheet.
- Gmail — send the approved reply from the connected Gmail account.
- Human-in-the-Loop — built in; require approval before every send.

# SKILLS USED
- fitshark-reply-writer — how to compose the customer reply email.
- fitshark-product-link — how to build the product-page link from the SKU.

# DATA
- Questions sheet: <QUESTIONS_SHEET_URL>, tab "Questions".
  Columns: question_id, customer_question, customer_email, status, matched_sku, matched_supplier,
  matched_product, price_incl_vat, currency, lead_time, product_link, date_sent, notes.
- Catalog sheet: <CATALOG_SHEET_URL>, tab "Catalog", header in row 1, data from row 2.
  Columns A–O: A supplier_sku, B product_name, C brand, D category, E subcategory, F variant_value,
  G vehicle_compatibility, H supplier, I availability, J lead_time, K lead_time_days,
  L price_incl_vat, M currency, N image_url, O product_link.
- Use a tab named "Scratch" in the Catalog sheet for QUERY lookups (create it if missing).

# STEPS

1. Open the Questions sheet. Read every row where `status` = "Pending". Process them ONE AT A TIME,
   in question_id order. Target: all pending rows.

2. For each Pending question, identify the product:
   a. Parse `customer_question` into search keys: brand, product-type keywords (e.g. "H7 bulb",
      "car battery", "air filter", "tire size"), variant (size / capacity / quantity, e.g.
      "205/60 R16", "70 Ah", "Set"), and vehicle (make + model + generation + years) if named.
   b. Find the best match in the Catalog with a server-side lookup:
      - Write a formula into cell `Scratch!A1` of the Catalog sheet, for example:
        `=QUERY(Catalog!A2:O, "select * where lower(B) contains 'h7 bulb' and lower(C) contains 'philips' and lower(G) contains 'opel astra j' limit 5", 0)`
        Build the WHERE clause from the keys you extracted: brand on column C, product-type/size
        tokens on column B (use `lower()` + `contains`), variant on column F, and
        vehicle on column G when the question names a vehicle. Keep `limit 5`.
      - Read back `Scratch!A1:O5` and choose the single best row: exact brand + variant match, and
        vehicle_compatibility (col G) matching the named vehicle (or `Universal`). Prefer rows whose
        availability (col I) is "On order" / "Incoming" since the customer said it was out of stock.
   c. If you cannot find a confident match (or the vehicle does not match and is not Universal):
      set `status` = "Skipped", write a short reason in `notes`, do NOT email, and move to the next row.
   d. From the chosen row capture: supplier_sku (A), product_name (B), supplier (H),
      price_incl_vat (L), currency (M), lead_time (J), vehicle_compatibility (G), variant_value (F).

3. Compose the reply:
   a. Build the product link from supplier_sku using the **fitshark-product-link** skill.
   b. Draft the email with the **fitshark-reply-writer** skill. Recipient = the row's `customer_email`.
      The body must state the product, that it is available on order, the price incl. VAT, the
      expected delivery (lead_time), and the product link. Use the price/currency/lead_time verbatim
      from the matched catalog row — never invent numbers.

4. HUMAN APPROVAL — one approval per question, BEFORE sending:
   - Raise a Human-in-the-Loop **approval** request.
   - Set the title to: `Reply <question_id> -> <product_name> (<price_incl_vat> <currency>, <lead_time>)`.
   - In the description include the full draft so the reviewer can verify before it goes out:
     `To: <customer_email>`, `Subject: <subject>`, the full `Body`, and the matched details
     (SKU, supplier, price incl. VAT, lead time, product link).
   - If APPROVED: send the email via Gmail to `customer_email`. Then update that question's row:
     `status` = "Sent", and fill `matched_sku`, `matched_supplier`, `matched_product`,
     `price_incl_vat`, `currency`, `lead_time`, `product_link`, `date_sent` = today's date.
   - If DENIED: set `status` = "Rejected", record any reason given in `notes`, and do NOT send.

5. After handling each row, write its new status to the sheet immediately, so the Job can resume
   safely if interrupted. Only ever act on rows whose status is "Pending".

6. When all pending rows are processed, post a final summary message with the counts:
   Sent / Skipped / Rejected, and list any Skipped/Rejected question_ids.

# RULES
- An email is sent ONLY after explicit human approval for that specific question. Never auto-send,
  never batch approvals — each question is approved separately.
- Send from the connected Gmail account; the visible recipient is the `customer_email` on the row
  (all test rows are dominikfronc@gmail.com).
- Use price incl. VAT, currency and lead time exactly as they appear in the matched catalog row.
- If the question names a vehicle, the matched product's vehicle_compatibility must match it (or be
  Universal). If it cannot be matched confidently, Skip the row rather than guess.
- Do not expose internal data (supplier company names, SKU codes, wholesale prices) in the email body.
