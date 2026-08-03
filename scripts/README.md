# scripts/

## clickup-import.mjs

Books the 16 ClickUp (Mango Technologies Inc) subscription receipts as
Lexware Office bookkeeping vouchers, categorized and with the PDF attached
to each voucher.

`clickup-manifest.json` maps each receipt filename to its bank statement
date/amount (matched by date, cross-checked against the invoice's USD
amount — see the commit that added this file for the reconciliation).

Run where `api.lexware.io` is reachable (this repo's dev sandbox has no
network access to it):

```bash
# 1. put the 16 ClickUp PDFs in ./clickup-receipts (gitignored, never commit them)
# 2. find your "Lizenzen und Konzessionen" posting category id
node --env-file=.env scripts/clickup-import.mjs --list-categories

# 3. preview (no writes)
node --env-file=.env scripts/clickup-import.mjs --category-id <uuid> --receipts ./clickup-receipts

# 4. actually create the vouchers + attach PDFs
node --env-file=.env scripts/clickup-import.mjs --category-id <uuid> --receipts ./clickup-receipts --yes
```

Requires `LEXWARE_OFFICE_API_KEY` (and `LEXWARE_OFFICE_ALLOW_WRITES=true` if
you're also running the MCP server with that env, though this script talks
to the API directly and isn't gated by it).

Note: ClickUp invoices these as 0% VAT, "reverse charged to customer"
(Art. 196 Directive 2006/112/EC). The script books the gross EUR amount at
0% as literally invoiced. If your chart of accounts has a dedicated
reverse-charge / §13b UStG posting category for foreign digital services,
use that category id instead — check with your Steuerberater.
