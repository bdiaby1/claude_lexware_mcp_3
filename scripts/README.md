# scripts/

## import-vouchers.mjs

Generic Lexware Office voucher importer. Given a manifest JSON file, it
books one `purchaseinvoice` bookkeeping voucher per receipt — categorized,
vendor contact looked up/created, PDF attached, `voucherDate` set to the
bank statement date so Lexoffice's own Kontenabgleich can auto-suggest the
match. Idempotent: re-running skips any `voucherNumber` that's already
booked (retries HTTP 429s instead of racing the idempotency check).

Manifest shape:

```json
{
  "vendor": {
    "searchNames": ["Company Name", "Trading Name"],
    "company": { "name": "...", "street": "...", "city": "...", "zip": "...", "countryCode": "XX" }
  },
  "entries": [
    { "file": "receipt.pdf", "voucherNumber": "unique-id", "voucherDate": "2025-07-04",
      "bankAmountEur": 8.49, "taxRatePercent": 0, "taxAmount": 0, "plan": "..." }
  ]
}
```

`taxRatePercent`/`taxAmount` default to 0 (booked gross, no VAT) when
omitted. `voucherNumber` defaults to the filename without `.pdf`.

Run where `api.lexware.io` is reachable (this repo's dev sandbox has no
network access to it):

```bash
# find your "Lizenzen und Konzessionen" posting category id (auto-resolved if unambiguous)
node --env-file=.env scripts/import-vouchers.mjs --list-categories

# preview (no writes)
node --env-file=.env scripts/import-vouchers.mjs --manifest scripts/<vendor>-manifest.json --receipts ./<vendor>-receipts

# actually create the vouchers + attach PDFs
node --env-file=.env scripts/import-vouchers.mjs --manifest scripts/<vendor>-manifest.json --receipts ./<vendor>-receipts --yes
```

Requires `LEXWARE_OFFICE_API_KEY`.

### Existing manifests

- **clickup-manifest.json** — ClickUp (Mango Technologies Inc, US), 16
  receipts, booked 2026-08-03. US supplier, invoiced at 0% VAT
  ("reverse charged to customer", Art. 196 Directive 2006/112/EC) —
  booked as literally invoiced (0%). If your chart of accounts has a
  dedicated §13b UStG reverse-charge posting category for foreign digital
  services, that's a more correct treatment for the VAT return — check
  with your Steuerberater. (Lexoffice's own "Lizenzen und Konzessionen
  §13b Drittland" category rejects a 0% tax rate; it needs deliberate
  reverse-charge tax math this script doesn't attempt.)

- **tldv-manifest.json** — tl;dv (tldx Solutions GmbH, Aachen, Germany),
  15 receipts, booked 2026-08-03. Domestic German supplier: the 11 PRO-plan
  EUR invoices show real 19% German VAT (booked at 19%, deductible
  Vorsteuer); the 4 later Business-plan USD invoices show no VAT on the
  source invoice (booked at 0%, as literally invoiced). Two additional
  invoices for the free "Starter" plan have €0.00/$0.00 due and are
  excluded — nothing was paid, nothing to book.

Both manifests intentionally exclude duplicate/zero-amount entries found
while reconciling — see the commits that added each file for the full
date/amount matching against the bank statement.
