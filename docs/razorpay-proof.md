# Razorpay Test Mode proof

On 27 August 2026, the configured guarded path completed the following local flow:

1. Compiled and explicitly confirmed an outdoor basketball-shoe intent capped at ₹6,000.
2. Scanned the shared catalogue and flagged `sku_alpha_agent`.
3. Sanitized the flagged title and description before ranking.
4. Selected the eligible clean listing `sku_alpha_court`.
5. Produced a deterministic `ALLOW` decision after final validation.
6. Created one Razorpay Test Mode order through the server-side Orders API.

Recorded non-secret evidence:

| Field | Value |
|---|---|
| Decision | `ALLOW` |
| Selected SKU | `sku_alpha_court` |
| Flagged SKU | `sku_alpha_agent` |
| Order ID | `order_TUV7bq2owsl8PN` |
| Amount | `579900` paise (₹5,799.00) |
| Currency | `INR` |
| Receipt | `dec_26d29659ff7e` |

No API key or secret is stored in this repository. This is a simulated Test Mode order; no real money moved.
