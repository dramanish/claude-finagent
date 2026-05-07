---
name: apideck-fetch
description: Pull a complete, paginated, normalized dataset from the Apideck unified accounting MCP for a specific reconciliation or close period. Use when a fund-admin agent needs a deterministic extract (GL, AP, AR, payments, ledger accounts) over a date range.
---

# Apideck MCP — period fetch

Reconciliation and close workflows need a complete dataset over a defined period, not a sample. This skill standardizes how to pull that data through `execute_tool` with correct pagination, filtering, and normalization.

## Inputs you need from the orchestrator

- `service_id` — the target connector (e.g. `quickbooks`, `xero`, `netsuite`)
- `period` — `{ start: "YYYY-MM-DD", end: "YYYY-MM-DD" }`
- `scope` — which families to pull (e.g. `["journal-entries", "ledger-accounts", "bills", "invoices", "payments"]`)
- Optional: `entity_id` if the connector is multi-entity

## Pagination

Apideck list endpoints return a `meta.cursors.next` cursor when more pages exist. Loop until cursor is null. Default page size is 20; raise to 100–200 for fewer round-trips. Hard-cap total records per family at a number the orchestrator can hold (default 5,000) and stop with a clear note if you would exceed it.

```
cursor = null
while True:
  res = execute_tool({
    "tool_name": "accounting-journal-entries-list",
    "input": {
      "xApideckServiceId": service_id,
      "filter": { "posted_date_start": period.start, "posted_date_end": period.end },
      "limit": 200,
      "cursor": cursor
    }
  })
  yield res.data
  cursor = res.meta.cursors.next
  if cursor is None: break
```

## Per-family fetch recipes

| Family | Tool | Required filter | Notes |
|---|---|---|---|
| Journal entries | `accounting-journal-entries-list` | `posted_date_start` / `posted_date_end` | Each entry has `line_items[]` with `account.id`, `debit_amount`, `credit_amount` |
| Ledger accounts (CoA) | `accounting-ledger-accounts-list` | none | Use as the dimension for any GL aggregation |
| Bills (AP) | `accounting-bills-list` | `issued_date_start` / `issued_date_end` (or `updated_since` for delta loads) | Status filter: `status=open` for AP aging |
| Invoices (AR) | `accounting-invoices-list` | `issued_date_start` / `issued_date_end` | Same status pattern as bills |
| Payments | `accounting-payments-list`, `accounting-bill-payments-list` | `transaction_date_start` / `_end` | Two endpoints — pull both for full cash view |
| Aged debtors / creditors | `accounting-aged-debtors-one` / `accounting-aged-creditors-one` | report `as_of_date` | Single-shot — no pagination |
| P&L | `accounting-profit-and-loss-one` | `start_date` / `end_date` | Single-shot |
| Balance sheet | `accounting-balance-sheet-one` | `as_of_date` | Single-shot |

## Normalization (do this before passing to the recon skill)

1. **Identifier hygiene** — coerce `id` and `account.id` to strings; strip whitespace. Apideck IDs are stable per connector but not portable across connectors.
2. **Money** — every amount comes back with `value` (number) + `currency`. Fund-admin recon expects `local_amount`, `local_currency`, `base_amount`, `base_currency`. Convert FX using the rate already on the entry (`exchange_rate`); do not invent rates.
3. **Dates** — Apideck returns ISO 8601. Truncate to date for posting-date comparisons.
4. **Sign convention** — bills are positive (vendor owes you), credit notes are negative. Some connectors return signed amounts; others use a separate `type` field. Check the connector once per session and document the convention in the extract header.

## Determinism

For any reconciliation that must be reproducible, capture per fetch:

- The exact tool name
- The full input payload (including `xApideckServiceId`)
- The Apideck request ID returned in the response (`meta.request_id`) — surface this in the exception report so a human can audit the source pull

## Read-only invariant

Do not call `*-create`, `*-update`, or `*-delete` from this skill. Any required ledger change must be staged as a journal-entry draft in `./out/` for human approval — see the closer / reconciler agents' `Write`-tier handoff.
