---
name: fitshark-product-link
description: Build the Fitshark product-page link AND a unique per-customer order link for a matched product. Use whenever a reply email, message, or sheet row needs (a) a link to the product page and (b) a unique link the customer can click to order this exact product. Both URLs are derived deterministically from the SKU and the inquiry.
---

# Fitshark — Product & Order Link Builder

Produces two links for a matched product. Both are deterministic — the same inputs always
yield the same URLs, so they can be regenerated anywhere without a lookup.

## Inputs
- `supplier_sku` (required) — e.g. `APS-LGT-007601`
- `question_id` (required for the order link) — the inquiry reference, e.g. `Q001`
- `customer_email` (optional) — pre-fills the order form

Helper — `slug(x)` = lowercase x, replace any run of non `[a-z0-9]` characters with a single
hyphen, strip leading/trailing hyphens. So `APS-LGT-007601` → `aps-lgt-007601`.

## 1. Product page link
```
https://shop.fitshark.example/p/<slug(supplier_sku)>
```
- `APS-LGT-007601` → `https://shop.fitshark.example/p/aps-lgt-007601`

Use this when the customer just wants to view the product.

## 2. Unique order link  (the "Order now" link)
A per-inquiry, per-product link the customer clicks to place the order. The path segment
`<question_id>-<slug(sku)>` is the unique **order reference** (one per customer inquiry):
```
https://shop.fitshark.example/order/<question_id_lower>-<slug(supplier_sku)>?email=<urlencoded customer_email>&utm_source=email&utm_medium=care&utm_campaign=backorder_reply
```
Example — question_id `Q001`, sku `APS-LGT-007601`, email `dominik@fronc.eu`:
```
https://shop.fitshark.example/order/q001-aps-lgt-007601?email=dominik%40fronc.eu&utm_source=email&utm_medium=care&utm_campaign=backorder_reply
```
- The order reference `q001-aps-lgt-007601` is unique to this customer + product, so clicking it
  opens a pre-filled order for exactly that part.
- URL-encode the email (`@` → `%40`). If `customer_email` is missing, drop the `email=` param.

## Output
Return both, clearly labelled, nothing else:
```
PRODUCT_LINK: <product page url>
ORDER_LINK: <unique order url>
```

## Notes & edge cases
- The base `https://shop.fitshark.example` is the demo storefront; if a real storefront base URL is
  configured for the team, swap the base and keep the same path rules.
- The **email body** should use the ORDER_LINK as the primary call-to-action and may use the
  PRODUCT_LINK as a secondary "see details" link. Logs/sheets should store the plain PRODUCT_LINK.
- If `supplier_sku` is missing/empty, return empty strings and signal that no link could be built
  (never fabricate a SKU). If `question_id` is missing, still return the PRODUCT_LINK and note the
  order link could not be made unique.
