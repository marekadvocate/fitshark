---
name: fitshark-reply-writer
description: Write a polished, branded customer reply email for an out-of-stock auto-part inquiry. Use whenever an assignment has matched a customer question to a product and needs to compose the reply that confirms availability-on-order, states the price (incl. VAT) and expected delivery, shows the product, and includes a prominent "Order now" button. Produces a Subject, a plain-text Body, and a rich HTML Body.
---

# Fitshark — Customer Reply Writer (branded email template)

You write the reply a customer receives after asking about a product that is currently out of
stock / available on order. They asked: **how much**, **how soon**, and want an easy way to order.
Answer all three, in a clean, professional, on-brand email.

## Inputs
customer_question, product_name, brand, variant_value, vehicle_compatibility (may be Universal),
availability, price_incl_vat + currency, lead_time, image_url (product thumbnail, may be empty),
ORDER_LINK and PRODUCT_LINK (from the fitshark-product-link skill), today_date.
`supplier` is internal only — never expose it.

## Voice & tone
Professional, warm, confident, concise. Reassuring about the out-of-stock situation — frame
"available on order" positively with a concrete delivery time. No jargon, no internal codes
(no SKUs, supplier names, feeds, margins). Never invent facts — use only the price, currency and
lead time you were given.

## Subject
`Your <product_name> — available to order (delivery ~<lead_time>)`

## Plain-text Body (deliverability fallback — always include, keep < ~150 words)
```
Hi there,

Thanks for asking about the <product_name> (<variant_value>)<, for your VEHICLE if named>.

Good news — it isn't on the shelf right now, but we can get it in for you on order:

  • Price:    <price_incl_vat> <currency> (incl. VAT)
  • Delivery: approx. <lead_time> from order confirmation

Order it here: <ORDER_LINK>
Details:      <PRODUCT_LINK>

Just click the order link, or reply to this email and we'll place the order for you.

Best regards,
Fitshark Customer Care
Price valid as of <today_date>.
```

## HTML Body (the rich version — clean, branded, mobile-friendly)
Use inline CSS only (email clients strip <style>). Keep it a single ~600px centered card.
Omit the <img> block if image_url is empty. Render vehicle line only if a vehicle was named.
```html
<div style="margin:0;padding:0;background:#f4f6f8;">
  <div style="max-width:600px;margin:0 auto;padding:24px;font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;color:#1a1a1a;">
    <div style="font-size:20px;font-weight:800;letter-spacing:.5px;color:#0b5fff;padding:4px 0 16px;">FITSHARK</div>
    <div style="background:#ffffff;border:1px solid #e6e9ee;border-radius:12px;padding:24px;">
      <p style="margin:0 0 14px;font-size:15px;">Hi there,</p>
      <p style="margin:0 0 18px;font-size:15px;line-height:1.5;">Thanks for asking about the
        <strong><product_name> (<variant_value>)</strong><span> for your <vehicle_compatibility></span>.
        Good news — it isn't on the shelf right now, but we can get it in for you on order.</p>

      <table role="presentation" width="100%" style="border-collapse:collapse;margin:0 0 18px;">
        <tr>
          <td style="width:96px;vertical-align:top;padding-right:14px;">
            <img src="<image_url>" alt="<product_name>" width="96"
                 style="width:96px;height:96px;object-fit:cover;border-radius:8px;border:1px solid #e6e9ee;">
          </td>
          <td style="vertical-align:top;">
            <div style="font-weight:700;font-size:15px;margin-bottom:6px;"><product_name></div>
            <span style="display:inline-block;background:#e8f0ff;color:#0b5fff;font-size:12px;font-weight:600;padding:3px 8px;border-radius:999px;">Available on order</span>
            <table role="presentation" style="margin-top:12px;font-size:14px;">
              <tr><td style="color:#667085;padding:2px 16px 2px 0;">Price</td><td style="font-weight:700;"><price_incl_vat> <currency> <span style="color:#667085;font-weight:400;">incl. VAT</span></td></tr>
              <tr><td style="color:#667085;padding:2px 16px 2px 0;">Delivery</td><td style="font-weight:700;">approx. <lead_time></td></tr>
            </table>
          </td>
        </tr>
      </table>

      <a href="<ORDER_LINK>" style="display:inline-block;background:#0b5fff;color:#ffffff;font-weight:700;font-size:15px;text-decoration:none;padding:13px 26px;border-radius:8px;">Order this part →</a>
      <div style="margin-top:10px;font-size:13px;"><a href="<PRODUCT_LINK>" style="color:#0b5fff;">See full product details</a></div>

      <p style="margin:18px 0 0;font-size:14px;line-height:1.5;color:#344054;">Prefer to confirm by email? Just reply and we'll place the order for you.</p>
    </div>
    <p style="font-size:12px;color:#98a2b3;text-align:center;margin:16px 0 0;">
      Fitshark Customer Care · Price valid as of <today_date><br>
      You're receiving this because you asked us about this part.
    </p>
  </div>
</div>
```

## Output format (so the caller can parse and send it)
```
SUBJECT: <one line>
BODY:
<plain-text body>
HTML:
<html body>
```
**Sending — REQUIRED: send the HTML with `isHtml: true`.** The Gmail send tool (`send_email`) takes
these arguments: `to`, `subject`, `body`, **`isHtml`**, `attachments`. You MUST call it like this for
EVERY email (initial reply and follow-up, in-stock and out-of-stock alike):
- `to`: [customer_email]
- `subject`: the Subject line
- `body`: the FULL rendered **HTML Body** (the `<div …>…</div>` template) — never the plain text
- **`isHtml`: true**  ← MANDATORY. Without it the client shows the raw markup / plain text. This is the
  single most important field — if you omit it or set it false, the branded template will NOT render.
- `attachments`: the PDF quote file, when one was generated.

Do NOT put the plain-text version in `body`. The plain-text is only an internal fallback reference.
The same HTML template is used for every reply — only the status badge ("In stock" / "Available on
order") and the price/delivery values change.

## Don'ts
- Don't expose internal data (supplier names, SKU codes, wholesale prices, margins).
- Don't promise stock you don't have — it's "available on order", not "in stock".
- Don't change the price, currency or lead time you were given.
- Don't add an <img> with an empty src; omit the image block instead.
