# GL Reconciler — managed-agent template

## Overview

Finds breaks between general ledger and subledger for a trade date and set of asset classes, traces root cause, and produces an exception report for controller sign-off.

Same source as the [`gl-reconciler`](../../plugins/agent-plugins/gl-reconciler) Cowork plugin — this directory is the Managed Agent cookbook for `POST /v1/agents`.

## Deploy

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export GL_MCP_URL=...           # read-only GL MCP
export SUBLEDGER_MCP_URL=...    # read-only subledger MCP
../../scripts/deploy-managed-agent.sh gl-reconciler
```

### Deploy via Apideck (unified accounting MCP)

If your firm sources GL + subledger data through one or more cloud accounting systems (QuickBooks, Xero, NetSuite, Sage Intacct, Microsoft Dynamics, Zoho Books, MYOB, …), you can drop in [Apideck's unified accounting MCP](../../plugins/vertical-plugins/apideck-erp) — one URL, one set of credentials, swap the connector per customer.

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export APIDECK_API_KEY=apideck_...
export APIDECK_APP_ID=...
export APIDECK_CONSUMER_ID=...   # the customer's Vault consumer ID

# Swap in the Apideck variant manifest, then deploy as usual
cp managed-agent-cookbooks/gl-reconciler/agent.apideck.yaml \
   managed-agent-cookbooks/gl-reconciler/agent.yaml
./scripts/deploy-managed-agent.sh gl-reconciler
```

See [`./agent.apideck.yaml`](./agent.apideck.yaml) for the worked manifest. Apideck is read-only by default (the reconciler doesn't need write).

## Steering events

See [`steering-examples.json`](./steering-examples.json). Kick a session with a trade date and asset-class list; follow-up events can re-trace a single break.

## Security & handoffs

This agent reads counterparty/custodian statements — documents authored by outsiders that may carry adversarial instructions. The template is structured so a payload in one of those documents cannot reach a shell, a write tool, or a firm system:

| Tier | Touches untrusted docs? | Tools | Connectors |
|---|---|---|---|
| **`reader`** | **Yes** | `Read`, `Grep` only | None |
| **Orchestrator** | No | `Read`, `Grep`, `Glob`, `Agent` | Read-only GL + subledger MCPs |
| **`resolver`** (Write-holder) | No | `Read`, `Write`, `Edit` | None |

The `reader` returns length-capped, schema-validated JSON only (validated by `scripts/validate.py`). The `critic` independently re-verifies each break against trusted sources before the orchestrator hands the set to `resolver`. The `resolver` writes the exception report to `./out/`; it never opens an outsider file.

**Handoff:** to feed verified breaks into Month-End Closer, the orchestrator emits a `handoff_request` for `month-end-closer` in its final output; `scripts/orchestrate.py` (or your Temporal/Airflow worker) routes it as a new steering event. See the script for the allowlist + payload-validation pattern.

**Not guaranteed:** none of this writes to a system of record. Ledger adjustments require human approval outside the agent.
