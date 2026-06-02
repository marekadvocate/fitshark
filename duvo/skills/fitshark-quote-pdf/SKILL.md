---
name: fitshark-quote-pdf
description: Generate a clean, branded PDF price quote for a matched auto part (and any add-ons) to attach to the customer reply. Use when a professional, attachable quote is wanted. Builds the PDF in the workspace with code; falls back to an HTML/text quote if PDF libraries are unavailable.
---

# Fitshark — PDF Quote Builder

Produces a one-page, branded **quote** the customer can keep, forward, or use to order. Attach it to
the reply email. Be robust: generate a real PDF if possible, otherwise fall back gracefully.

## Inputs
quote_ref (use the question_id, e.g. Q001), today_date, valid_until (today + 14 days),
customer_email, currency, and line items — each: description (product_name + variant), qty (default 1),
unit_price_incl_vat. Include any upsell items from fitshark-upsell-recommender as extra lines.
ORDER_LINK from fitshark-product-link. Follow fitshark-brand-voice for wording.

## What the quote contains
- Header: **FITSHARK** + "Price Quote" + quote_ref + date + valid-until.
- Bill-to: customer_email.
- Table: Description | Qty | Unit price (incl. VAT) | Line total. Then **Total (incl. VAT)**.
- A note: "Items available on order — estimated delivery stated per line / in the email."
- A prominent line: "Order online: <ORDER_LINK>".
- Footer: Fitshark Customer Care · prices incl. VAT · quote valid until <valid_until>.

## How to build it (in the sandbox)
1. Write the quote data, then generate `quote_<quote_ref>.pdf` in the workspace using Python.
   Try a PDF library in this order and use the first that imports:
   - `reportlab` (preferred), else `fpdf`/`fpdf2`, else `weasyprint` (HTML→PDF).
   - If none import, `pip install fpdf2` may be attempted; if that fails, FALL BACK (below).
2. Keep layout simple and clean (A4, generous margins, the table above). No logos required — a bold
   "FITSHARK" wordmark in the brand blue (#0b5fff) is enough.

## Attaching / fallback
- If the email send tool supports attachments: attach `quote_<quote_ref>.pdf` to the reply.
- If PDF generation OR attachment is not available: do NOT fail the reply. Instead include the same
  quote as a tidy text/HTML block inside the email body and keep the ORDER_LINK. Note in the run log
  that the PDF fell back to inline.

## Output
```
QUOTE_FILE: /workspace/quote_<quote_ref>.pdf   (or "inline" if fell back)
QUOTE_TOTAL: <total> <currency>
VALID_UNTIL: <valid_until>
```

## Don'ts
- Never block or fail the customer reply because of the PDF — always degrade to an inline quote.
- Prices on the quote must exactly match the matched Catalog prices (incl. VAT). Never invent totals —
  compute them from the line items.
- No internal data (SKU codes, supplier names, wholesale prices, margins) on the customer-facing quote.
