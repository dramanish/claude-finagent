# CLAUDE.md — repo-level instructions

This file is read by Claude Code and Cowork when working inside this repository. It captures conventions that should apply across every plugin in the marketplace.

## What this repo is

A Fintegrity-internal Cowork plugin marketplace, forked from `anthropics/financial-services` and scoped to our practice. Three vertical plugins, five named agents, all sharing a common skills/commands/connectors model.

```
fintegrity-plugins/
├── .claude-plugin/marketplace.json   # marketplace catalog (the source of truth for what's exposed)
├── plugins/
│   ├── vertical-plugins/             # skill + command bundles by vertical
│   │   └── <vertical>/
│   │       ├── .claude-plugin/plugin.json
│   │       ├── .mcp.json             # MCP servers (financial-analysis holds the shared set)
│   │       ├── commands/             # explicit slash commands
│   │       └── skills/               # auto-fired domain knowledge (canonical source)
│   └── agent-plugins/                # named, self-contained agents
│       └── <slug>/
│           ├── .claude-plugin/plugin.json
│           ├── agents/<slug>.md      # canonical system prompt
│           └── skills/               # bundled copies, synced from vertical-plugins/
├── managed-agent-cookbooks/<slug>/   # cookbook for headless deployment via /v1/agents
├── scripts/                          # check.py, validate.py, sync-agent-skills.py, deploy-managed-agent.sh
└── ...
```

When editing a skill that an agent bundles, edit the **vertical-plugins** copy and run `python3 scripts/sync-agent-skills.py` — don't edit the bundled copies inside agent-plugins/ directly.

## Conventions

### Language
- **Client-facing output** (reports, memos, slides, emails to clients) — **Swedish** by default, unless the client explicitly works in English.
- **Internal output** (code, commit messages, this repo's docs, IC memos for Fintegrity-internal review) — English.
- Skills and commands themselves are written in English so they're maintainable, but should produce Swedish output when invoked in client-facing context.

### Accounting & finance conventions
- **Reporting framework**: K2 or K3 (BFNAR 2016:10 / BFNAR 2012:1). Not US GAAP. Full IFRS only when a client explicitly applies it.
- **Chart of accounts**: BAS-kontoplan (BAS 2024 unless stated). Account ranges follow Swedish convention — 1xxx assets, 2xxx liabilities/equity, 3xxx revenue, 4xxx COGS, 5–6xxx opex, 7xxx personnel, 8xxx financial.
- **Currency**: SEK by default. Mark all foreign-currency figures explicitly.
- **VAT**: Reverse-charge and EU-VAT logic apply. Don't assume sales tax mechanics from US examples.
- **Personnel costs**: Swedish employer's contribution (arbetsgivaravgifter, ~31.42% standard) and pension models (ITP1/ITP2 where relevant). Vacation liability follows Semesterlagen (1977:480), 25 days statutory minimum.

### Client systems
- **Fortnox** — primary bookkeeping system for most clients. SIE export is the lingua franca.
- **Kleer** (formerly PE Accounting) — used by some clients. Activity-to-cost-category mapping for employer cost allocation.
- **Runn**, **Blikk** — operational systems at specific clients.
- **Microsoft Fabric** — Fintegrity's internal data platform; medallion architecture (bronze/silver/gold), one workspace per client.
- **Microsoft 365 / SharePoint** — client document storage and collaboration.

When generating analysis, prefer pulling from the Fintegrity Fabric semantic model where it exists for the client; fall back to Fortnox SIE / Kleer exports otherwise.

### Output formats
- **Excel models** with live formulas — never paste static numbers a user can't audit. Use blue/black/green color coding (blue = input, black = formula, green = link from another tab).
- **PowerPoint decks** follow Fintegrity brand guidelines (see the `fintegrity-brand` skill).
- **Reports** default to Word or Notion-ready markdown depending on client preference.

## Plugin authoring rules

When adding or modifying a plugin:

1. **Skills must declare clear trigger conditions** in their `SKILL.md` frontmatter. If a skill could fire too broadly, it will — be specific.
2. **Commands should be Fintegrity-relevant**. Don't keep upstream commands that don't apply to our work.
3. **MCP connectors** in `.mcp.json` should reference servers we actually operate against. Don't keep dead URLs from upstream.
4. **Agents bundle skills as copies** — edit canonical sources in `plugins/vertical-plugins/<vertical>/skills/`, then run `python3 scripts/sync-agent-skills.py`. Never edit a bundled copy directly without syncing back.
5. **Run the lint** — `python3 scripts/check.py` before pushing. CI runs it too via `.github/workflows/`.
6. **Test locally** with `claude plugin install <plugin>@fintegrity-plugins` from a development checkout before pushing.

## Upstream sync

Upstream is `anthropics/financial-services`. We periodically pull interesting changes — see `MIGRATION.md` for the merge process and a record of which upstream changes have been integrated.

When upstream adds a new vertical or agent, evaluate it against Fintegrity's practice before pulling — most upstream additions will be US-market-flavored and need adaptation or rejection.
