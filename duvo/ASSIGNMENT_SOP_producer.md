GOAL: Every hour, enqueue any NEW customer inquiries from the Drive questions CSV as cases in the "fitshark-questions" queue — with the matching product PRE-RESOLVED in the case data — so the parallel consumer can answer them quickly. Never enqueue the same inquiry twice. This agent only matches and enqueues; it never emails.

# CONNECTIONS USED
- Google Drive — read the questions CSV and the supplier feeds.
- Case Queue (Producer) — linked to the "fitshark-questions" queue; create cases here.

# CONFIG
- QUESTIONS_FOLDER = Google Drive folder 1QqOqPR_iX-obfEZ09yR1GgCfGFbUPw2Y ("MOTOR PARTS QUESTIONS"), file customer_questions.csv
- FEEDS_FOLDER = Google Drive folder 1f91aPPy8hEPXqzS_pSDg6yBSCKiLV8eg ("MOTOR PARTS"), 11 files feed_*.tsv
- MAX_NEW_PER_RUN = 30

# STEPS (each hourly run)

1. Download `customer_questions.csv` from QUESTIONS_FOLDER; read all rows
   (question_id, customer_question, customer_email).

2. Dedup: list the existing cases in the queue and collect the `question_id`s already present (from each
   case's data/title). NEW = question_ids with NO existing case. If there are none, post "No new
   inquiries." and stop. Otherwise take up to MAX_NEW_PER_RUN new ones (lowest question_id first).

3. Download the supplier feeds from FEEDS_FOLDER into the workspace ONCE (not per inquiry). For each NEW
   inquiry:
   a. Parse brand, product-type keywords, variant, vehicle (make+model+generation+years) from
      `customer_question`. Do NOT use any expected_* columns.
   b. grep the downloaded feeds for the best matching row (confidence gate: brand + variant match and
      vehicle matches or Universal; prefer availability "On order"/"Incoming"). Capture: supplier_sku,
      product_name, brand, variant_value, vehicle_compatibility, supplier, availability, lead_time,
      retail_price_incl_vat (→ price_incl_vat), currency, image_url. If no confident match, set
      matched=null and add a note.
   c. Find up to 2 companion items for upsell: rows fitting the SAME vehicle (or Universal) in a
      DIFFERENT category; capture product_name, supplier_sku, retail_price_incl_vat, currency.
   d. Create ONE case in the queue with:
      - title: "<question_id>: <product_name or '??'>"
      - data (JSON):
        {"question_id","customer_question","customer_email",
         "matched":{"sku","product_name","brand","variant_value","vehicle_compatibility","supplier",
                    "availability","lead_time","price_incl_vat","currency","image_url"},
         "upsell":[{"product_name","sku","price_incl_vat","currency"}]}
      - label: batch=auto

4. Post a summary: number of new cases enqueued, and any inquiries with no confident match.

# RULES
- Never enqueue a question_id that already has a case (strict dedup against existing cases).
- Match from the question text; ignore expected_* columns. Use retail_price_incl_vat as price_incl_vat.
- This agent NEVER sends email and never resolves cases — it only creates them. The consumer answers them.
- Download the feeds once per run (efficient), not once per inquiry.
