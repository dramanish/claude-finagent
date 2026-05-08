# Statement Auditor — managed-agent template

## Overview

Audits pre-generated LP statements before distribution. Same source as the [`statement-auditor`](../../plugins/agent-plugins/statement-auditor) Cowork plugin — this directory is the Managed Agent cookbook for `POST /v1/agents`.

## Deploy

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export NAV_MCP_URL=...
../../scripts/deploy-managed-agent.sh statement-auditor
```

### Deploy via Apideck (unified accounting MCP, accounting-side tie-out)

For accounting-side tie-out data (balance sheet, ledger accounts, invoices, payments), [Apideck's unified accounting MCP](../../plugins/vertical-plugins/apideck-erp) provides one URL across 20+ ERPs. Pair it with your fund-admin NAV source — the orchestrator can fan out both.

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export APIDECK_API_KEY=apideck_...
export APIDECK_APP_ID=...
export APIDECK_CONSUMER_ID=...

cp managed-agent-cookbooks/statement-auditor/agent.apideck.yaml \
   managed-agent-cookbooks/statement-auditor/agent.yaml
./scripts/deploy-managed-agent.sh statement-auditor
```

See [`./agent.apideck.yaml`](./agent.apideck.yaml). Read-only — flagger output stays in `./out/` for IR sign-off.

## Steering events

See [`steering-examples.json`](./steering-examples.json).

## Security & handoffs

Generated statements are treated as untrusted (upstream system out of scope). Three-tier isolation:

| Tier | Touches untrusted docs? | Tools | Connectors |
|---|---|---|---|
| **`statement-reader`** | **Yes** | `Read`, `Grep` only | None |
| `reconciler` / Orchestrator | No | `Read`, `Grep`, `Glob`, `Agent` | nav (read-only) |
| **`flagger`** (Write-holder) | No | `Read`, `Write`, `Edit` | None |

`flagger` produces `./out/signoff-<batch>.xlsx`.

**Not guaranteed:** this agent recommends pass/hold; IR distributes after human sign-off.
