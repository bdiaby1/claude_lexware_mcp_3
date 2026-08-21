# Lexware Office MCP Server — Claude Instructions

## Benjamin's Brain (content / YouTube work)

This repo doubles as Benjamin's persistent Claude workspace. `brain/` is cross-session
memory for his content work (YouTube channel, video retention analysis, shorts, IG).

- Task about content, videos, scripts, shorts, Instagram, retention, Michael's cuts →
  read `brain/README.md` FIRST and follow its protocol (then STATE.md → the project).
- Task about Lexware/bookkeeping/MCP-server code → ignore `brain/`, use the sections below.
- Any session that changes content state must write back to `brain/STATE.md` +
  `brain/LOG.md` and commit + push before ending. Containers are ephemeral:
  unpushed = forgotten.

## API Documentation

Lexware Office REST API: https://developers.lexoffice.io/docs/

Fetch specific sections on demand with WebFetch. Key sections:
- Contacts: `/docs/#contacts-endpoint`
- Invoices: `/docs/#invoices-endpoint`
- Vouchers (voucherlist): `/docs/#voucherlist-endpoint`
- Down-Payment Invoices: `/docs/#down-payment-invoices-endpoint`
- Dunnings: `/docs/#dunnings-endpoint`

## Architecture (Code Mode)

- Single MCP server in `src/index.ts` exposing two tools: `search` and `execute`
- `src/lexware-spec.ts` — curated OpenAPI-lite catalog the `search` sandbox queries
- `src/executor.ts` — QuickJS sandbox that runs model-supplied JS
- `src/lexware-client.ts` — host-side HTTP client behind `lexware.request` (API key stays here, never in the sandbox)
- `src/truncate.ts` — response truncation for MCP payloads
- Writes (POST/PUT/PATCH/DELETE) blocked by default; `LEXWARE_OFFICE_ALLOW_WRITES=true` enables them, `LEXWARE_OFFICE_READ_ONLY=true` hard-blocks

## Conventions

- Catalog entries in `lexware-spec.ts` must match official Lexware docs (docsUrl per operation)
- Optional fields use `!== undefined` guards, not falsy checks
- Tests are `src/*.test.ts` (node:test); `pnpm test` builds then runs them; `pnpm run typecheck` for tsc only
- `docs/guide.md` is user-facing and checked in; `src/docs-contract.test.ts` asserts parts of it
