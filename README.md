# Fintegrity Plugins

Claude Cowork plugins that turn Claude into a CFOaaS specialist for Nordic SMEs — financial analysis, fund admin operations, advisory work, and the named agents we use most.

Forked from [`anthropics/financial-services`](https://github.com/anthropics/financial-services) and adapted for Swedish accounting conventions, our client systems (Fortnox, Kleer, Runn, Blikk), and our internal data platform on Microsoft Fabric.

## Why a fork

Upstream is built around US capital markets workflows — Daloopa, FactSet, S&P Capital IQ, SEC filings, US GAAP, sell-side IB, HNW wealth advisory. The skills are valuable but the framings don't fit our work. We:

- **Scoped to what we actually do** — kept three verticals (financial-analysis, fund-admin, private-equity) and five agents that map directly to live Fintegrity engagements. Dropped IB, equity-research, wealth-management, operations, and the partner-built plugins.
- **Swapped the data stack** — out goes the institutional US data layer, in comes the Fintegrity Fabric semantic model, Microsoft 365, and the client-facing systems we already operate (Fortnox, Kleer).
- **Adjusted accounting conventions** — K2/K3 over US GAAP, BAS-kontoplan over US chart-of-accounts, Swedish vacation/employer-cost rules over US payroll mechanics.
- **Adjusted output language** — client-facing deliverables default to Swedish; internal artifacts in English.

## What's in here

### Vertical plugins

| Plugin | Type | What it covers |
|---|---|---|
| **financial-analysis** | Core (install first) | Comps, DCF, LBO, 3-statement, Excel audit, deck QC. Holds the shared MCP connectors. |
| **fund-admin** | Operations | GL reconciliation, break tracing, accruals, roll-forwards, variance commentary, NAV tie-out. |
| **private-equity** | Advisory | DD checklists, IC memos, unit economics, returns analysis, portfolio monitoring. |

### Named agents

End-to-end workflow agents — install only the ones you'll use.

| Agent | What it does |
|---|---|
| **gl-reconciler** | Finds GL breaks, traces root cause, routes for sign-off. The Sourcian-style P&L reconstruction agent. |
| **month-end-closer** | Accruals, roll-forwards, variance commentary at month-end. |
| **statement-auditor** | Audits financial statements before they go out. Year-end and DD-context QC. |
| **meeting-prep-agent** | Builds a briefing pack before client meetings. |
| **valuation-reviewer** | Cross-checks valuation work against templates and peer data. DD valuation reviews and exit pricing. |

### Not included

Out of scope for Fintegrity and removed from this fork:
- Verticals: `investment-banking`, `equity-research`, `wealth-management`, `operations`
- Agents: `pitch-agent`, `market-researcher`, `earnings-reviewer`, `model-builder`, `kyc-screener`
- Partner-built plugins (LSEG, S&P Global)
- `claude-for-msft-365-install/` (we use the standard M365 add-in, not a custom routing path)

## Install

### In Claude Cowork (recommended for the team)

1. Owner / Primary Owner of the Fintegrity Cowork org goes to **Organization settings → Plugins**.
2. **Add plugin → GitHub** → install the Cowork GitHub App on the `fintegrity-ab` org and select `fintegrity-plugins`.
3. Set per-plugin defaults under group access:
   - **Required**: `financial-analysis` (everyone needs the core)
   - **Installed by default**: `fund-admin`, `gl-reconciler`, `month-end-closer`
   - **Available for install**: the rest

### In Claude Code (for local development)

```bash
claude plugin marketplace add fintegrity-ab/fintegrity-plugins

# Core (install first)
claude plugin install financial-analysis@fintegrity-plugins

# Operations verticals
claude plugin install fund-admin@fintegrity-plugins
claude plugin install private-equity@fintegrity-plugins

# Agents
claude plugin install gl-reconciler@fintegrity-plugins
claude plugin install month-end-closer@fintegrity-plugins
claude plugin install statement-auditor@fintegrity-plugins
claude plugin install meeting-prep-agent@fintegrity-plugins
claude plugin install valuation-reviewer@fintegrity-plugins
```

## Repository layout

```
fintegrity-plugins/
├── .claude-plugin/marketplace.json   # marketplace catalog (Fintegrity-customized)
├── plugins/
│   ├── vertical-plugins/             # skill + command bundles by vertical
│   │   ├── financial-analysis/       # core: modeling, Excel, deck QC, MCP connectors
│   │   ├── fund-admin/               # GL recon, accruals, roll-forwards, variance, NAV
│   │   └── private-equity/           # DD, IC memos, unit economics, portfolio
│   └── agent-plugins/                # named, self-contained agents
│       ├── gl-reconciler/
│       ├── month-end-closer/
│       ├── statement-auditor/
│       ├── meeting-prep-agent/
│       └── valuation-reviewer/
├── managed-agent-cookbooks/          # Claude Managed Agent cookbooks (one per kept agent)
├── scripts/                          # check.py, validate.py, sync-agent-skills.py — keep these
├── README.md
├── CLAUDE.md
└── MIGRATION.md
```

## Customizing further

Plugins are markdown and JSON — no build step. To customize:

- **Skills** live in `<plugin>/skills/` — drop in client-specific terminology, K2/K3 conventions, our deal templates, vacation-liability rules.
- **Commands** live in `<plugin>/commands/` — slash commands the team invokes explicitly.
- **Connectors** live in `plugins/vertical-plugins/financial-analysis/.mcp.json` — wire Claude to data sources.
- **Agents** live in `plugins/agent-plugins/<slug>/agents/<slug>.md` (canonical system prompt) plus `skills/` (synced bundled copies). Run `python3 scripts/sync-agent-skills.py` after editing a vertical skill that an agent bundles.
- **Lint** — `python3 scripts/check.py` validates manifests and cross-file references.

When upstream ships interesting changes, see [MIGRATION.md](./MIGRATION.md) for the merge process.

## Contributing internally

PRs welcome from anyone in Fintegrity. For new skills:

- Add the skill under `plugins/vertical-plugins/<vertical>/skills/<skill-name>/SKILL.md` with clear trigger conditions in frontmatter.
- Add a corresponding command in `commands/` if it's user-invokable.
- Run `python3 scripts/sync-agent-skills.py` if any kept agent bundles the skill.
- Run `python3 scripts/check.py` before pushing.

## License

Apache 2.0, inherited from upstream.

## Disclaimer

These plugins assist with financial workflows. They do not replace qualified judgement — every deliverable Claude produces is reviewed by a Fintegrity professional before it leaves the building.
