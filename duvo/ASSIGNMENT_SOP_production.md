GOAL: Fully automatically, every ~10 minutes, read new customer inquiries from the Google Drive questions CSV, find the matching product by searching the supplier feeds, draft a polished reply in the customer's language, get human approval for each send, email the customer, log every answer, save the customer's vehicle, and send one polite follow-up if they don't respond — never answering the same inquiry twice as the CSV grows. Run hands-free: never ask the operator to set anything up.

# CONNECTIONS USED
- Google Drive — read the questions CSV (grows over time) and the supplier feed files.
- Google Sheets — append to the Responses Log; upsert the Customer Vehicles table.
- Gmail — send replies, and check whether the customer already replied (for follow-ups).
- Human-in-the-Loop — built in; approval before every email send (initial replies AND follow-ups).

# SKILLS USED
- fitshark-brand-voice — voice, formatting, glossary and trust/fitment standards for EVERY message.
- fitshark-reply-writer — compose the polished, branded reply email (plain-text + HTML).
- fitshark-product-link — build the product link and the unique per-customer order link.
- fitshark-upsell-recommender — 1–3 genuinely relevant add-ons (+ optional premium upgrade).
- fitshark-quote-pdf — attach a clean branded PDF price quote (falls back to inline).

# PERSISTENT STATE (Assignment Memory) — reuse across every run
- `answered_ids` — question_ids already SENT (dedup ledger).
- `responses_log_url` — Responses Log Google Sheet.
- `vehicles_sheet_url` — Customer Vehicles Google Sheet.

# CONFIG
- FOLLOW_UP_DAYS = 3
- QUESTIONS_FOLDER = Google Drive folder 1QqOqPR_iX-obfEZ09yR1GgCfGFbUPw2Y ("MOTOR PARTS QUESTIONS"), file customer_questions.csv
- FEEDS_FOLDER = Google Drive folder 1f91aPPy8hEPXqzS_pSDg6yBSCKiLV8eg ("MOTOR PARTS"), 11 files feed_*.tsv

# STEP 0 — SELF-SETUP (no operator involvement, only when a value is missing from memory)
a. Responses Log — if `responses_log_url` missing: create Google Sheet "Fitshark — Responses Log",
   tab "Log", header row 1: timestamp | question_id | customer_email | status | matched_sku |
   matched_supplier | product_name | price_incl_vat | currency | lead_time | order_link | language |
   alternative_sku | follow_up_date | followed_up | notes | run_reference. Save URL to memory.
b. Customer Vehicles — if `vehicles_sheet_url` missing: create Google Sheet "Fitshark — Customer Vehicles",
   tab "Vehicles", header row 1: first_seen | last_seen | customer_email | vehicle_make | vehicle_model |
   vehicle_generation | vehicle_years | vehicle_compatibility | last_category | last_product | last_sku |
   inquiries_count | last_question_id | notes. Save URL to memory.
NEVER raise a human request for setup. Create what you need yourself.

# PHASE 1 — ANSWER NEW QUESTIONS (each run)

1. Download `customer_questions.csv` from QUESTIONS_FOLDER and read all rows (question_id,
   customer_question, customer_email). NEW = question_id not in `answered_ids`.
   If there are NO new questions: skip the feed download entirely, go to Phase 2.
   (Do NOT use any expected_* columns to find the product.)

2. If there ARE new questions, download the supplier feeds from FEEDS_FOLDER into the workspace once,
   then search them efficiently for each new question (process one at a time, in question_id order):
   a. Parse customer_question into: brand, product-type keywords, variant (size/capacity/quantity),
      vehicle (make+model+generation+years) if named.
   b. Use grep/file-search over the downloaded feed files (do NOT read whole 6 MB files into reasoning)
      to find candidate rows by brand + product keywords, then read only the matching rows. Feed key
      columns (header is row 1 of each TSV): supplier_sku, brand, product_name, variant_value,
      vehicle_compatibility, supplier, availability, lead_time, retail_price_incl_vat (= price incl VAT),
      currency, image_url.
   c. CONFIDENCE GATE: pick the best row only if brand + variant match and the vehicle matches the named
      vehicle (or is Universal), preferring availability "On order"/"Incoming". If ambiguous/weak, do NOT
      guess — log "Needs review" and skip (no email). Optionally raise a HITL question with the top
      candidates only when it would clearly help.
   d. ALTERNATIVE: if a clearly cheaper/better second row also fits, keep it as an optional alternative.
   e. Capture: supplier_sku, product_name, brand, variant_value, vehicle_compatibility, supplier,
      availability, lead_time, price_incl_vat (= retail_price_incl_vat), currency, image_url.

3. Compose the reply (follow fitshark-brand-voice throughout):
   a. Build product link + unique order link from supplier_sku, question_id, customer_email
      (fitshark-product-link).
   b. Detect the language of customer_question and write the reply in THAT language; use
      fitshark-reply-writer for structure/tone/HTML, keeping product name, price, currency and links unchanged.
   c. UPSELL: run fitshark-upsell-recommender; if it returns items, add a brief "You might also need:"
      block (1–3 add-ons + at most one upgrade). Skip if nothing relevant.
   d. FITMENT: when the question named a vehicle and the product matches, add the brand-voice fitment line.
      If an alternative was kept, add a short "Alternatively:" line.
   e. QUOTE PDF: build a branded quote with fitshark-quote-pdf (main item + upsell lines) and attach it;
      if PDF/attachment isn't available, fall back to an inline quote — never block the send.

4. HUMAN APPROVAL — one approval per question, BEFORE sending. Title:
   "Reply <question_id> -> <product_name> (<price_incl_vat> <currency>, <lead_time>)"; description = full
   draft (To, Subject, Body) + matched details + detected language + alternative.
   APPROVED → send via Gmail with the rendered HTML put into the `body` argument (the connector renders
   HTML in body; never send plain-text as the body), and attach the PDF quote if available.
   DENIED → log "Rejected" + reason; do not send.

5. RECORD after the outcome:
   - On successful SEND: append a Responses Log row (status "Sent", follow_up_date = today+FOLLOW_UP_DAYS,
     followed_up = "no"); add question_id to `answered_ids` ONLY after the send succeeds.
   - SAVE THE VEHICLE — upsert into Customer Vehicles keyed by customer_email (+ vehicle_compatibility):
     update an existing row (last_seen, last_category, last_product, last_sku, last_question_id,
     inquiries_count+1) or append a new one (first_seen=last_seen=today, inquiries_count=1). If no vehicle
     was named, store vehicle_compatibility "Universal"/blank but still record the customer + last product.
   - On Rejected / Needs review / Skipped: append the log row with that status; do not add to `answered_ids`.

# PHASE 2 — FOLLOW-UPS (each run, after Phase 1)

6. Read the Responses Log. For each row where status="Sent", followed_up="no", follow_up_date <= today:
   a. Check Gmail for a reply FROM that customer_email since the initial email. If they replied, set
      followed_up="replied" and do nothing else.
   b. Otherwise draft a short friendly follow-up in the customer's language (reference the same product,
      restate price + delivery, repeat the order link), subject prefixed "Following up:" — via
      fitshark-reply-writer + fitshark-brand-voice.
   c. HITL approval ("Follow-up <question_id> -> <product_name>"). APPROVED → send, set followed_up="sent";
      DENIED → set followed_up="skipped". Send at most ONE follow-up per inquiry; never if they already replied.

7. Post a short summary: New answered (Sent / Needs review / Rejected), Follow-ups (sent/replied/skipped),
   Vehicles saved/updated this run.

# RULES
- Run hands-free — NEVER ask the operator to set up sheets, the catalog, or anything else. Build/derive it yourself.
- Runs on a ~10-minute schedule; the CSV may grow. Dedup strictly by `answered_ids`; answer at most once.
- Only download the feeds when there is new work; if no new questions, do not download.
- Emails (initial AND follow-up) are sent ONLY after explicit human approval. Never auto-send.
- Mark "Sent" / add to `answered_ids` ONLY after the Gmail send actually succeeds.
- Use price incl. VAT, currency and lead time exactly as in the matched feed row — never invent them.
- Reply in the customer's own language. Never expose internal data (supplier names, SKU codes, wholesale
  prices, margins) in any email. When unsure about a match, escalate or skip — do not guess.
