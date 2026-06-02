# Fitshark v2 — Cross-Catalog Marketplace Redesign (Design Spec)

**Date:** 2026-06-02
**Status:** Approved — ready for implementation planning
**Platform:** Duvo (via Duvo MCP) + Google Sheets + Gmail

## 1. Goal & change summary

Fitshark answers pre-purchase automotive questions ("does this part fit my car / how much / how
soon?"). v1 was per-seller (one Google Sheet per seller, questions/answers as tabs inside it).

**v2 pivots to a marketplace/aggregator model:**
- Fitshark is the **customer-facing brand**. Suppliers are backend; supplier names, internal SKUs,
  wholesale prices and margins are **never exposed** to the customer.
- A customer question is **not pre-routed** to one seller — the agent searches **across all 11
  supplier catalogs** and returns the best market match (price / stock / lead time).
- Data is **split into separate files** (no more extra tabs inside catalogs).
- The agent must **understand intent even when implicit** (infer the part from symptoms/use-case,
  not just literal keywords).
- Customer emails are **branded HTML templates** with a **unique per-customer buy link**.

## 2. Data layout (Google Sheets)

| File | Type | Purpose |
|---|---|---|
| 11 × **Catalog** files | separate spreadsheets (existing) | Full 70-col supplier feed, **one sheet only** — the 4 extra tabs (Inbound_Questions, Fitment, Supplier_Catalog, Orders) are **removed**. Read-only product source. |
| **Master Catalog Index** | 1 new spreadsheet (~110k rows) | Cross-catalog search surface. Slim columns: `seller_id, supplier, supplier_sku, product_name, brand, category, oe_numbers, vehicle_make, vehicle_model, vehicle_generation, vehicle_year_from, vehicle_year_to, vehicle_compatibility, retail_price_incl_vat, stock_qty, availability, lead_time_days, product_link`. Built locally from the feeds. |
| **Fitshark Questions** | 1 new spreadsheet | Central intake of all customer questions. `status` flows `new → queued → answered`. |
| **Fitshark Orders** | 1 new spreadsheet | Central, searchable **full answer log** (see §6). |

**Approach A (chosen):** consolidated Master Index for cross-catalog search — one read + in-code
filter scans the whole market cheaply. (Rejected: B = loop over 11 catalogs per question, too slow;
C = BigQuery/Supabase SQL, best long-term but adds infra — revisit when scaling to production.)

### Questions schema
`id | received_at | customer_name | customer_email | language | raw_question | status | created_at`
(vehicle/part are intentionally NOT pre-filled — the producer infers them.)

## 3. Agents (recreated under Marek's API key — see §8)

**fitment-producer** — polls `Fitshark Questions` (status=new). For each: detect language
(SK/CZ/EN/DE/PL), **infer** customer intent + vehicle + part **including from symptoms/use-case**
(e.g. "squeals when braking on my Octavia" → brake pads, Skoda Octavia), classify intent + priority.
Enqueue ONE case into the `fitment_intent` queue (no seller_id — cross-catalog). Mark row `queued`.
Never replies to the customer.

**fitment-consumer** — triggered per case:
1. **Search** the Master Catalog Index in ONE read + in-code (python) filter → candidate products
   across all suppliers matching the (inferred) part + vehicle.
2. **Decide** via `fitment-decision`: best match by fit + stock + price + lead time; choose
   in-stock vs on-order/ETA vs alternative vs source-required. Note any inference assumptions.
3. **Build** the unique customer buy link via `fitshark-product-link` (customer mode, §5).
4. **Draft** the reply: `fitshark-reply-writer` produces the content (Fitshark-branded, hides
   suppliers/SKUs/margins); `seller-voice` localizes to the customer's language; wrap in the
   **HTML email template** (§7).
5. **HITL Gate** (approval to send) → on approve, send via Gmail as **HTML**.
6. **Audit:** append a full row to `Fitshark Orders`; set the Questions row `status=answered`;
   mark the case completed.

## 4. Skills (all wired into the consumer)

- `fitment-decision` (b7cf089a…) — match/branch logic + output contract (adapted for cross-catalog).
- `fitshark-product-link` (e2ef1fd7…) — **extended** with a unique per-customer link mode (§5).
- `fitshark-reply-writer` (3b3f3a5d…) — reply content, Fitshark brand, no internal data exposed.
- `seller-voice` (17b629d7…) — **role narrowed to multilingual localization** (SK/CZ/EN/DE/PL);
  per-seller tone is dropped (brand is Fitshark, not the seller).
- **new** `fitshark-email-template` — wraps the reply content in branded, inline-CSS HTML with a CTA
  button (the unique buy link). Returns HTML + plain-text fallback.

## 5. Unique per-customer buy link

`fitshark-product-link` gains a customer mode producing a link unique to the customer+product:
```
https://shop.fitshark.example/buy/<slug>?cid=<question_id>&t=<hash8(email + supplier_sku)>
```
- `<slug>` = supplier_sku lowercased, non-alphanumeric → single hyphen (existing rule).
- `<hash8>` = first 8 hex chars of a stable hash (e.g. sha256) of `customer_email + supplier_sku`.
- Deterministic yet unique per customer; verifiable; used in the **email** (with UTM tags).
- Plain (untagged, non-customer) link is stored alongside in `Fitshark Orders`.

## 6. Fitshark Orders schema (full answer log)

`order_id | question_id | received_at | customer_name | customer_email | language |
raw_question | understood_query | matched_seller_id | matched_supplier | matched_sku |
product_name | price_incl_vat | currency | stock_qty | availability | lead_time_days |
decision | alternatives | product_link | buy_link | reply_subject | reply_body_plain |
reply_body_html | reply_sent_at | approved_by | status | est_revenue_eur | notes | created_at`

Searchable record of every answered question and what was offered.

## 7. HTML email template

Branded Fitshark HTML email: header/wordmark, a product card (name, vehicle fit, price incl. VAT,
delivery/ETA), a prominent **CTA button → unique buy link**, "Fitshark Customer Care" footer. Inline
CSS, table layout, mobile-friendly. Sent as `text/html` via the Gmail connection; plain-text body
retained as fallback. (If the Gmail send action cannot take HTML, fall back to plain text — but Gmail
supports HTML natively.)

## 8. Ownership (route HITL approvals to Marek)

Runs are owned by the **agent's creator**, not the trigger creator. To make approvals land in
**Marek's** Activity Inbox, the producer + consumer assignments are **recreated under Marek's API
key** (the MCP is already repointed to Marek's key `dv_hhR…`). Connections (Gmail + Google Sheets,
both on `marekpodhorsky1993@gmail.com`) are already owned by Marek and will be pinned to the new
agents. The case trigger is created under Marek.

## 9. Synthetic test data

- **Questions:** regenerate 100 questions with a **shuffle of languages** (SK/CZ/EN/DE/PL) — the
  question text is written in-language so detection + inference are exercised. Include vague/implicit
  phrasings to test inference.
- **Emails:** `customer_email` alternates between the two **real** test inboxes
  `marekmicuda1@gmail.com` and `dominik@fronc.eu` (real delivery for the demo; replaces `@example.test`).
- All product/supplier data remains synthetic.

## 10. GitHub updates (repo `marekadvocate/fitshark`)

- `scripts/make_questions.py` — regenerate multilingual questions + real-email column.
- `questions/customer_questions.csv` — regenerated output.
- `scripts/build_index.py` (new) — build the Master Catalog Index from the 11 feeds.
- `scripts/upload_feeds.py` — adjust to create catalog-only spreadsheets (no extra tabs) + upload
  the index / questions / orders files.
- `README.md` — document the v2 marketplace architecture.
- Commit + push to master.

## 11. Reuse vs. rebuild

- **Reuse:** Case Queue `fitment_intent`; the 11 catalog spreadsheets (strip the 4 tabs); skills
  `fitment-decision`, `fitshark-product-link`, `fitshark-reply-writer`, `seller-voice`.
- **Rebuild:** Master Index + Questions + Orders files; producer + consumer SOPs (cross-catalog +
  inference + new skills + HTML) **under Marek's key**; new `fitshark-email-template` skill; new case
  trigger under Marek; multilingual question data.

## 12. Test plan (end-to-end on real inboxes)

Seed multilingual questions, then verify each path reaches the correct grounded outcome + HITL:
1. In-stock match across catalogs → confirm reply (price + buy link), HTML email, Orders row.
2. On-order match → ETA/pre-order reply.
3. Implicit/symptom-based question → correct inferred part + match (assumption noted).
4. Non-English question → localized reply.
Confirm: HITL approval appears in **Marek's** inbox; HTML email delivered to the real address;
unique buy link is per-customer; Orders log row written; Questions status updated.

## Open/Deferred
- Real checkout behind the buy link (needs a storefront backend) — out of scope; link is a demo URL.
- BigQuery/SQL search (Approach C) — deferred until production scale.
