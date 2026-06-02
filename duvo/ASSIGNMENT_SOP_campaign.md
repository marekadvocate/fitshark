GOAL: On a recurring schedule, turn the saved Customer Vehicles table into personalized, vehicle-specific parts offers — pick the most relevant parts for each customer's car from the supplier feeds, draft a polished campaign email in their language, get human approval, send it, and log it — without over-contacting anyone. Run hands-free; never ask the operator to set anything up.

# CONNECTIONS USED
- Google Sheets — read the Customer Vehicles table; write the Campaign Log.
- Google Drive — read the supplier feed files to find offerable parts.
- Gmail — send the approved offer from the connected account.
- Human-in-the-Loop — built in; approval before every send.

# SKILLS USED
- fitshark-brand-voice — voice, formatting, glossary and trust standards for every message.
- fitshark-offer-personalizer — pick the most relevant, fitting, seasonal parts for the customer's vehicle.
- fitshark-reply-writer — render the campaign email (plain-text + HTML), campaign tone.
- fitshark-product-link — product links + unique per-customer order links.
- fitshark-upsell-recommender — optionally enrich the offer with a companion item.

# DATA
- Customer Vehicles sheet: https://docs.google.com/spreadsheets/d/1AwQmFD4VtwChCwydWQUbonaDBurHBgtXre6vVTtC_A8/edit
  tab "Vehicles". Columns: first_seen, last_seen, customer_email, vehicle_make, vehicle_model,
  vehicle_generation, vehicle_years, vehicle_compatibility, last_category, last_product, last_sku,
  inquiries_count, last_question_id, notes.
- Feeds: Google Drive folder 1f91aPPy8hEPXqzS_pSDg6yBSCKiLV8eg ("MOTOR PARTS"), 11 files feed_*.tsv.
  Key columns: supplier_sku, brand, product_name, variant_value, vehicle_compatibility, supplier,
  availability, lead_time, retail_price_incl_vat (= price incl VAT), currency, image_url.
- Campaign Log sheet: `campaign_log_url` (from memory; created in Step 0).

# PERSISTENT STATE (Assignment Memory)
- `campaign_log_url` — Campaign Log Google Sheet.

# CONFIG
- MIN_DAYS_BETWEEN_OFFERS = 30
- MAX_OFFERS_PER_RUN = 10

# STEP 0 — SELF-SETUP (no operator involvement)
If `campaign_log_url` missing: create Google Sheet "Fitshark — Campaign Log", tab "Campaigns", header
row 1: sent_date | customer_email | vehicle_compatibility | theme | items | status | run_reference.
Save URL to memory. NEVER raise a human request for setup.

# STEPS (each run)

1. Read the Customer Vehicles sheet. Build the candidate list:
   - Exclude customers contacted within MIN_DAYS_BETWEEN_OFFERS (check the Campaign Log for the latest
     sent_date per customer_email).
   - Exclude anyone whose notes indicate opt-out / do-not-contact.
   - Keep at most MAX_OFFERS_PER_RUN candidates (oldest last_seen first). If none, post "No offers due." and stop.

2. For each candidate build the offer with fitshark-offer-personalizer (their vehicle + current season).
   To find offerable parts, download the supplier feeds from the MOTOR PARTS Drive folder once and
   grep them for parts that FIT the customer's vehicle (vehicle_compatibility matches or Universal) in
   seasonally/relevant categories. Verify each part exists with a real price. Optionally add one
   companion item via fitshark-upsell-recommender. Keep 2–4 items. If nothing genuinely fits, skip that
   customer (log "Skipped — no fit").

3. Compose the campaign email (follow fitshark-brand-voice; render with fitshark-reply-writer in a light
   campaign tone): a short friendly "something for your <vehicle>" message with the 2–4 items as a clean
   list (name, price incl. VAT, order link via fitshark-product-link). Detect and use the customer's
   language. One clear CTA per item. No pressure.

4. REQUEST APPROVAL — THEN STOP AND WAIT. Call request_approval with title
   "Offer -> <customer_email> (<vehicle_compatibility>)" and description = full draft + items + rationale.
   ⚠️ request_approval is ASYNCHRONOUS: after calling it you MUST STOP — end your turn, call NO further
   tools (especially NOT send_email), do not assume approval. The job pauses and re-invokes you when the
   human decides. ONLY after being RESUMED with the decision:
   - APPROVED → send via Gmail by calling send_email with: to=[customer_email], subject, body=the FULL
     HTML Body, **isHtml: true** (MANDATORY). Never put the plain-text version in `body`.
   - DENIED → log "Rejected" + reason.

5. RECORD after the outcome: append a Campaign Log row (sent_date=today, customer_email,
   vehicle_compatibility, theme, items, status, run_reference). Only "Sent" rows count toward the throttle.

6. Post a short summary: offers Sent / Skipped / Rejected, with the customer emails in each bucket.

# RULES
- Run hands-free — never ask the operator to set anything up.
- Offers are sent ONLY after explicit human approval. Never auto-send.
- Never offer parts that don't fit the customer's vehicle. Never invent prices — read them from the feeds.
- Respect MIN_DAYS_BETWEEN_OFFERS and opt-out — do not over-contact. At most one offer per customer per run.
- Reply in the customer's language. Never expose internal data (supplier names, SKU codes, wholesale
  prices, margins) in customer-facing text.
- Read the Vehicles sheet; do NOT write to it (the reply agent owns it). Write only to the Campaign Log.
