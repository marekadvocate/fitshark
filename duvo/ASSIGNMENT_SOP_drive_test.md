GOAL: For a small test set of customer inquiries, read the questions and supplier feeds directly from Google Drive, find the matching product by searching the feeds, draft a professional reply with price and delivery time, get human approval for each one, and email the customer.

# TEST MODE
Process ONLY the first two questions: question_id Q001 and Q002. After those two, stop and post a
summary. This is a feasibility test of reading and searching the raw Drive feeds.

# CONNECTIONS USED
- Google Drive — read the questions CSV and the supplier feed TSV files.
- Gmail — send the approved reply from the connected Gmail account.
- Human-in-the-Loop — built in; require approval before every send.

# SKILLS USED
- fitshark-reply-writer — how to compose the customer reply email.
- fitshark-product-link — how to build the product-page link from the SKU.

# DATA IN GOOGLE DRIVE
- Questions: folder "MOTOR PARTS QUESTIONS"
  (https://drive.google.com/drive/folders/1QqOqPR_iX-obfEZ09yR1GgCfGFbUPw2Y) →
  file `customer_questions.csv`. Relevant columns: question_id, customer_question, customer_email.
  (The file may also contain expected_* columns — IGNORE them; do not use them to find the product.)
- Feeds: folder "MOTOR PARTS"
  (https://drive.google.com/drive/folders/1f91aPPy8hEPXqzS_pSDg6yBSCKiLV8eg) →
  11 tab-separated files feed_*.tsv (~6 MB, ~10,000 rows each). Each row is one product.
  Key columns: supplier_sku, brand, product_name, variant_value, vehicle_compatibility, supplier,
  availability, lead_time, retail_price_incl_vat, currency, image_url.

# STEPS

1. Download `customer_questions.csv` from the MOTOR PARTS QUESTIONS folder into your workspace and read
   the first two rows (Q001, Q002): question_id, customer_question, customer_email.

2. For each of the two questions, find the matching product by SEARCHING THE FEEDS (do not use any
   expected_* columns):
   a. Parse customer_question into search keys: brand, product-type keywords (e.g. "H7 bulb",
      "car battery", "tire size"), variant (e.g. "205/60 R16", "70 Ah", "Set"), and vehicle
      (make + model + generation + years) if named.
   b. Download the supplier feed files from the MOTOR PARTS folder into your workspace and search their
      rows for a product matching the keys. Search efficiently — do not try to read whole 6 MB files
      into your reasoning; use file search / filtering over the downloaded files to locate candidate
      rows (e.g. grep-style search for the brand + product keywords), then read only the matching rows.
   c. Choose the single best matching row: exact brand + variant match, and vehicle_compatibility
      matching the named vehicle (or "Universal"). Prefer rows whose availability is "On order" /
      "Incoming" (the customer said it was out of stock).
   d. Capture: supplier_sku, product_name, brand, variant_value, vehicle_compatibility, supplier,
      availability, retail_price_incl_vat (use this as price incl. VAT), currency, lead_time.
   e. If you cannot find a confident match, record "Skipped — no confident match" for that question
      and move on; do NOT email.

3. Compose the reply:
   a. Build the product link from supplier_sku using the fitshark-product-link skill.
   b. Draft the email with the fitshark-reply-writer skill. Recipient = the row's customer_email.
      State the product, that it is available on order, the price incl. VAT, the delivery (lead_time),
      and the product link. Use the price/currency/lead_time verbatim from the matched feed row.

4. HUMAN APPROVAL — one approval per question, BEFORE sending:
   - Raise a Human-in-the-Loop approval request.
   - Title: Reply <question_id> -> <product_name> (<price_incl_vat> <currency>, <lead_time>).
   - Description: the full draft (To, Subject, Body) plus matched details
     (supplier_sku, supplier, price incl. VAT, lead time, product link) so the reviewer can verify.
   - If APPROVED: send the email via Gmail to customer_email.
   - If DENIED: record "Rejected" with any reason, and do NOT send.

5. DEDUP / STATE: in Assignment Memory keep a list of question_ids whose email was ACTUALLY SENT.
   Add a question_id to that list ONLY after the email has been successfully sent (i.e. after human
   approval AND the Gmail send succeeded). Never record a question as sent if it was skipped, rejected,
   or not yet approved. Never email a question whose id is already in the sent list.

6. After Q001 and Q002, STOP and post a summary: for each, the matched product (sku, name, price,
   lead time), the action taken (Sent / Skipped / Rejected), and — importantly — a short note on HOW
   you searched the feeds and whether the feed search worked well, so we can judge the approach.

# RULES
- An email is sent ONLY after explicit human approval for that specific question. Never auto-send.
- Find the product by searching the feeds — do NOT shortcut using expected_* columns in the questions file.
- Use price incl. VAT, currency and lead time exactly as they appear in the matched feed row.
- Do not expose internal data (supplier company names, SKU codes, wholesale prices) in the email body.
