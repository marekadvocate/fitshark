# MCP prompt — create the Fitshark backorder-reply agent in Duvo

Paste the block below into a client connected to the **Duvo MCP server**
(`https://api.duvo.ai/v2/mcp`) — Claude Desktop, Claude Code, Cursor or ChatGPT.
It uses the Duvo MCP tools (`createSkill`, `createAgent`, `attachRevisionIntegrations`,
`pinRevisionIntegrationConnection`, `promoteRevision`) to build everything end-to-end.

> **Before you run it**, do the one-time setup in `SETUP.md` (create the two Google
> Sheets and paste their URLs into the two `<...>` placeholders below). Everything else
> — IDs, skills, SOP — is already filled in.

---

````text
You are connected to the Duvo MCP server. Create a complete assignment in the team
"Advocate" (team_id 78c96305-46bc-466c-83f7-d7761daea24a). Work in this order and
report the result of each step.

## Context / IDs (this team)
- team_id:                       78c96305-46bc-466c-83f7-d7761daea24a
- Google Sheets connection:      8bff539e-a206-4f12-a098-156f9806d2b9   (marekpodhorsky1993@gmail.com)
- Gmail connection:              bdff9e7d-aff0-4c90-a6e0-853e1fdc6222   (marekpodhorsky1993@gmail.com)
- Human-in-the-Loop:             built-in, no connection needed
- Questions sheet URL:           <QUESTIONS_SHEET_URL>
- Catalog sheet URL:             <CATALOG_SHEET_URL>

(Use the SAME Google identity for the sheets and for sending. The two sheets must be
owned by / shared with marekpodhorsky1993@gmail.com so the pinned Sheets connection can
read them. If you prefer to keep the sheets under dominikfroncik@gmail.com, pin Sheets
connection f42ca64c-12c6-42f0-8c2d-5a94d87384cc instead.)

## STEP 1 — Create skill "fitshark-product-link"
Call createSkill with:
  name: fitshark-product-link
  description: Generate the canonical Fitshark product-page link for a given supplier SKU. Use whenever an email, message, or sheet row needs a dynamic clickable link to the matched product. Returns one HTTPS URL built deterministically from the SKU.
  content: (the full Markdown body of skills/fitshark-product-link/SKILL.md from this repo)

## STEP 2 — Create skill "fitshark-reply-writer"
Call createSkill with:
  name: fitshark-reply-writer
  description: Write a professional, warm customer reply email for an out-of-stock auto-part inquiry. Use whenever an assignment has matched a customer question to a catalog product and needs to compose the reply that confirms availability-on-order, states the price (incl. VAT) and expected delivery time, and includes the product link. Produces a ready-to-send Subject and Body.
  content: (the full Markdown body of skills/fitshark-reply-writer/SKILL.md from this repo)

## STEP 3 — Create the assignment + first build
Call createAgent in team 78c96305-46bc-466c-83f7-d7761daea24a with:
  name: "Fitshark — Backorder Reply Agent"
  delivery / display name as above
  build config:
    - config.version: "v2"
    - model: a capable reasoning model (team default is fine)
    - input: the full SOP text below (between <<<SOP and SOP>>>)
    - skills: ["fitshark-product-link", "fitshark-reply-writer"]

<<<SOP
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
        =QUERY(Catalog!A2:O, "select * where lower(B) contains 'h7 bulb' and lower(C) contains 'philips' and lower(G) contains 'opel astra j' limit 5", 0)
        Build the WHERE clause from the keys you extracted: brand on column C, product-type/size
        tokens on column B (use lower() + contains), variant on column F, and
        vehicle on column G when the question names a vehicle. Keep limit 5.
      - Read back `Scratch!A1:O5` and choose the single best row: exact brand + variant match, and
        vehicle_compatibility (col G) matching the named vehicle (or `Universal`). Prefer rows whose
        availability (col I) is "On order" / "Incoming" since the customer said it was out of stock.
   c. If you cannot find a confident match (or the vehicle does not match and is not Universal):
      set `status` = "Skipped", write a short reason in `notes`, do NOT email, and move to the next row.
   d. From the chosen row capture: supplier_sku (A), product_name (B), supplier (H),
      price_incl_vat (L), currency (M), lead_time (J), vehicle_compatibility (G), variant_value (F).

3. Compose the reply:
   a. Build the product link from supplier_sku using the fitshark-product-link skill.
   b. Draft the email with the fitshark-reply-writer skill. Recipient = the row's `customer_email`.
      The body must state the product, that it is available on order, the price incl. VAT, the
      expected delivery (lead_time), and the product link. Use the price/currency/lead_time verbatim
      from the matched catalog row — never invent numbers.

4. HUMAN APPROVAL — one approval per question, BEFORE sending:
   - Raise a Human-in-the-Loop approval request.
   - Set the title to: Reply <question_id> -> <product_name> (<price_incl_vat> <currency>, <lead_time>).
   - In the description include the full draft so the reviewer can verify before it goes out:
     To: <customer_email>, Subject: <subject>, the full Body, and the matched details
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
SOP>>>

## STEP 4 — Attach connections to the build (revision)
On the new assignment's draft revision:
  - attachRevisionIntegrations: googlesheets and gmail.
  - pinRevisionIntegrationConnection: pin googlesheets -> 8bff539e-a206-4f12-a098-156f9806d2b9,
    and gmail -> bdff9e7d-aff0-4c90-a6e0-853e1fdc6222.
  - Human-in-the-Loop is built in; no attach needed.

## STEP 5 — Promote and report
  - promoteRevision so this build is live.
  - Return: the assignment id, its dashboard URL, the two skill ids, and the pinned connections.
  - Do NOT start a run yet — the human will open the assignment, click "Start Work", and approve
    each reply in the Activity Inbox.
````

---

## Notes
- Paste the **actual SKILL.md bodies** (from `skills/fitshark-product-link/SKILL.md` and
  `skills/fitshark-reply-writer/SKILL.md`) into the `content:` fields in steps 1–2. They're kept in
  the repo so they stay version-controlled; the MCP client can read them directly if it has file access.
- If your MCP client can't pass the SOP as one block, point it at `ASSIGNMENT_SOP.md` in this repo.
- HITL approvals land in the Duvo **Activity Inbox** (and Slack/Teams if you enable those in
  Settings → Notifications). You approve one reply per question.
