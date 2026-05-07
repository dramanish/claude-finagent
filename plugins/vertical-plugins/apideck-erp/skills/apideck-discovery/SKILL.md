---
name: apideck-discovery
description: Find the right Apideck MCP tool family for an accounting task without loading the full 200-tool catalog. Use whenever an agent needs to read ERP data through the Apideck unified accounting MCP.
---

# Apideck MCP — tool discovery

Apideck's MCP server exposes ~200 accounting operations behind three meta-tools. Discover what you need with `list_tools` before calling `execute_tool`. Loading the full schema upfront blows the context window; the meta-tool pattern keeps discovery to ~1.3K tokens.

## Step 1: Search by resource family

Call `list_tools` with one or two keywords aligned to the resource you need:

| You want to … | Search terms | Returns operations like |
|---|---|---|
| Read journal entries | `journal-entries` | `accounting-journal-entries-list`, `-one`, `-create`, `-update` |
| Read GL chart of accounts | `ledger-accounts` | `accounting-ledger-accounts-list`, `-one` |
| Read bills (AP) | `bills` | `accounting-bills-list`, `-one`, `-create` |
| Read invoices (AR) | `invoices` | `accounting-invoices-list`, `-one`, `-create` |
| Read payments | `payments` | `accounting-payments-list`, `accounting-bill-payments-list` |
| Read suppliers / vendors | `suppliers` | `accounting-suppliers-list`, `-one`, `-create` |
| Read customers | `customers` | `accounting-customers-list`, `-one`, `-create` |
| Read purchase orders | `purchase-orders` | `accounting-purchase-orders-list`, `-one` |
| Read credit notes | `credit-notes` | `accounting-credit-notes-list`, `-one` |
| Read P&L | `profit-and-loss` | `accounting-profit-and-loss-one` |
| Read balance sheet | `balance-sheet` | `accounting-balance-sheet-one` |
| Read aged debtors / creditors | `aged-debtors` / `aged-creditors` | `accounting-aged-debtors-one`, `accounting-aged-creditors-one` |
| Read attachments | `attachments` | `accounting-attachments-list`, `-download` |

Pass the `scope` filter so only tools within your granted scopes (`read`, `write`, `destructive`) come back. For all read-only agents in this repo, request `read` only.

## Step 2: Inspect the input shape

Before calling an operation you've never used in this session, call `describe_tool_input` with the tool name. It returns the JSON Schema for the operation's input — including every accepted filter, pagination key, and the required `xApideckServiceId` selector.

```
describe_tool_input({"tool_name": "accounting-journal-entries-list"})
```

## Step 3: Call the operation

Use `execute_tool` with the resolved tool name and a payload that always includes the target connector via `xApideckServiceId`:

```
execute_tool({
  "tool_name": "accounting-journal-entries-list",
  "input": {
    "xApideckServiceId": "quickbooks",
    "filter": { "posted_date_start": "2026-04-01" },
    "limit": 200
  }
})
```

Common `xApideckServiceId` values: `quickbooks`, `xero`, `netsuite`, `sage-intacct`, `microsoft-dynamics-365-business-central`, `zoho-books`, `myob`, `freshbooks`, `wave-accounting`. If the orchestrator already knows which connector the customer is on, pass it on every call. If not, list the configured connectors via `vault-connections-list` first.

## Errors are signal — read them

Apideck propagates downstream ERP errors verbatim with a 4xx status and a `detail` message. Common cases:

- `"inactive account"` — the GL account ID is disabled in the customer's chart of accounts. Re-list `ledger-accounts` with `active=true`.
- `"closed period"` — the posted date falls in a closed accounting period. Stop and report; do not retry.
- `"duplicate reference number"` — the bill / invoice reference already exists. Stop and report.
- `401 / 402` — connection issue (re-auth or billing). Stop and report.

Never retry the same call blindly. Read the error, adjust the input, then retry once.

## Read-only safety

The fund-admin agents in this repo are read-only against the system of record. Do not request `write` or `destructive` scopes for those agents. If a workflow needs to draft an entry, stage it in `./out/` for human sign-off — never call `*-create`, `*-update`, or `*-delete` operations.
