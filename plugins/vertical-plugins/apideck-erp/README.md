# Apideck ERP connector

A drop-in MCP connector that fills the `GL_MCP_URL` / `SUBLEDGER_MCP_URL` / `NAV_MCP_URL` slots used by the fund-admin agents in this repo (`gl-reconciler`, `month-end-closer`, `statement-auditor`) with a single unified accounting API spanning 20+ ERPs.

> Hosted by [Apideck](https://www.apideck.com). One MCP URL, one set of credentials, swap the connector per customer.

## What you get

- One MCP server URL — `https://mcp.apideck.dev/mcp` — that talks to QuickBooks Online, Xero, NetSuite, Sage Intacct, Microsoft Dynamics 365 Business Central, Zoho Books, MYOB, FreshBooks, Wave, and others through Apideck's [Unified Accounting API](https://www.apideck.com/apis/accounting).
- Read-only by default — pass scopes in the request to opt into write operations.
- Resource families exposed: chart of accounts, journal entries, bills, invoices, payments, suppliers, customers, purchase orders, credit notes, profit & loss, balance sheet, aged debtors / creditors, attachments.
- Auth via headers (`x-apideck-api-key`, `x-apideck-app-id`, `x-apideck-consumer-id`) plus the target connector via `xApideckServiceId` (e.g. `quickbooks`, `xero`, `netsuite`).

## Tool-discovery model

Apideck's MCP server exposes a small set of meta-tools — `list_tools`, `describe_tool_input`, `execute_tool` — and the agent progressively discovers concrete operations on demand. This keeps the LLM context small (typical discovery cost: ~1.3K tokens) while preserving access to the full surface area (200+ accounting operations).

```
list_tools({"search_terms": ["journal-entries"]})
  → ["accounting-journal-entries-list", "accounting-journal-entries-one", ...]

execute_tool({
  "tool_name": "accounting-journal-entries-list",
  "input": { "filter": {"posted_date_start": "2026-04-01"}, "xApideckServiceId": "quickbooks" }
})
```

The bundled skills in this plugin (`apideck-discovery`, `apideck-fetch`) document this pattern so agents discover tools in the right order and avoid loading the full 200-tool catalog upfront.

## Use it as the MCP source for fund-admin agents

In any of the managed-agent cookbooks that declare an ERP MCP slot, point the URL at Apideck and pass the headers via your secret store:

```yaml
# managed-agent-cookbooks/<agent>/agent.yaml
mcp_servers:
  - type: url
    name: internal-gl                # or `subledger`, `nav`
    url: https://mcp.apideck.dev/mcp
    headers:
      x-apideck-api-key:     ${APIDECK_API_KEY}
      x-apideck-app-id:      ${APIDECK_APP_ID}
      x-apideck-consumer-id: ${APIDECK_CONSUMER_ID}
```

Agents that benefit today:

| Agent | Slot it fills | Apideck resources used |
|---|---|---|
| [`gl-reconciler`](../../agent-plugins/gl-reconciler) | `internal-gl`, `subledger` | journal-entries, ledger-accounts, bills, invoices, payments |
| [`month-end-closer`](../../agent-plugins/month-end-closer) | `internal-gl` | bills, invoices, journal-entries, ledger-accounts, profit-and-loss, balance-sheet |
| [`statement-auditor`](../../agent-plugins/statement-auditor) | `nav` (subset — accounting side) | invoices, payments, ledger-accounts, balance-sheet |

The matching cookbook READMEs include a worked Apideck example next to the existing placeholder pattern.

## Setup

1. Create an Apideck account at <https://platform.apideck.com> and copy the API key + App ID.
2. Connect the customer's accounting system in Apideck Vault — this issues a consumer ID per customer.
3. Set the env vars consumed by the agent.yaml above.
4. Deploy the agent as usual (`scripts/deploy-managed-agent.sh <slug>`).

For local development, the same MCP URL works with the standard MCP HTTP transport — see Apideck's [MCP server docs](https://developers.apideck.com/guides/mcp).

## Read-only by default

Apideck's MCP server is read-only unless the request carries `write` or `destructive` scopes. The fund-admin agents in this repo are designed to be read-only against the system of record (they stage exception reports / close packages for human approval, never post). Leave the default scope set as `read` for those agents.

## What this plugin ships

- `.claude-plugin/plugin.json` — manifest
- `skills/apideck-discovery/` — how to call `list_tools` to find the right tool family
- `skills/apideck-fetch/` — how to call `execute_tool` with the right payload + service ID

Both skills are small, opinionated, and meant to be loaded by orchestrator agents that drive the Apideck MCP. No skill in this plugin writes to the ledger.

## Not guaranteed

Nothing here posts to the GL. Apideck's `write` scope is available, but the FSI agents in this repo deliberately do not enable it — every output stays in `./out/` for human sign-off, in line with the repository-wide "stage, don't post" guarantee.
