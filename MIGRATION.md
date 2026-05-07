# MIGRATION.md

Tracking what changed from upstream (`anthropics/financial-services`) and how to merge future upstream updates without losing Fintegrity customizations.

## What we changed in the initial fork

### Removed verticals (`plugins/vertical-plugins/`)
- **`investment-banking/`** — out of scope; we don't do sell-side IB.
- **`equity-research/`** — public-co coverage isn't our work; sector reads are handled inside engagements.
- **`wealth-management/`** — HNW retail framing doesn't translate to SME owner-advisory.
- **`operations/`** — KYC/AML rules-grid; not core to CFOaaS.

### Removed agents (`plugins/agent-plugins/` and matching `managed-agent-cookbooks/<slug>/`)
- **`pitch-agent`** — sell-side pitch deck generation.
- **`market-researcher`** — sector/theme research with public-co focus.
- **`earnings-reviewer`** — public-co quarterly cycle.
- **`model-builder`** — useful but largely subsumed by the financial-analysis vertical.
- **`kyc-screener`** — adjacent to FR2000 risk work but not core.

### Removed other dirs
- **`plugins/partner-built/`** — LSEG and S&P Global plugins. We don't have these subscriptions.
- **`claude-for-msft-365-install/`** — admin tooling for routing Claude in M365 through a custom LLM gateway (Vertex/Bedrock). We use the standard M365 add-in path, so this is irrelevant.

### Replaced
- **`README.md`** — Fintegrity context, our scope, our install instructions.
- **`CLAUDE.md`** — repo-level instructions reflecting Swedish accounting conventions, our client systems, and Fintegrity output rules.
- **`.claude-plugin/marketplace.json`** — renamed to `fintegrity-plugins`, owner set to Fintegrity AB, only the eight kept plugins (3 verticals + 5 agents) listed.
- **`plugins/vertical-plugins/financial-analysis/.mcp.json`** — stripped of the 11 upstream US/UK data connectors. Replaced with M365 (Anthropic-hosted). Placeholder notes for Fabric / Fortnox / Kleer once those MCP servers exist.

### Kept (and to be customized incrementally)
- `plugins/vertical-plugins/financial-analysis/` — modeling skills mostly translate cleanly; assumptions/conventions need K2/K3 + SEK adaptation.
- `plugins/vertical-plugins/fund-admin/` — direct fit for CFOaaS month-end and forensic work; minor terminology adaptation.
- `plugins/vertical-plugins/private-equity/` — DD/IC-memo skills useful as-is; will diverge over time with our actual deal templates.
- `plugins/agent-plugins/` (5 kept agents) — the bundled skills inside each agent are copies that came from the verticals. Sync via `scripts/sync-agent-skills.py`.
- `scripts/` — lint and validation pipeline; useful guardrails.
- `managed-agent-cookbooks/` — kept for the 5 agents we use. Cookbooks for dropped agents removed.
- `.github/workflows/` — CI for the lint pipeline.

## Known follow-ups

- **Bundled-skill orphans**: when we deleted the verticals, any bundled skill copies inside the kept agents that originally came from a deleted vertical now have no canonical source. Run `python3 scripts/check.py` to identify these. Either delete the orphan, or re-home it into one of the kept verticals (most likely `fund-admin` or `financial-analysis`).
- **K2/K3 adaptation**: every skill that talks about US GAAP, SEC filings, or 10-K/10-Q references needs editing. Triage one skill per session, ideally driven by which skills actually fire during real client work.
- **MCP connectors**: `microsoft-365` is the only live entry. Add the Fintegrity Fabric semantic model MCP server when it ships. Add Fortnox and Kleer wrappers when those exist.
- **Brand alignment**: `/ppt-template` should be taught the Fintegrity brand templates so client-facing decks come out on-brand.

## Upstream sync workflow

Upstream evolves quickly. To pull in interesting changes without clobbering our work:

```bash
# One-time: add upstream as a remote
git remote add upstream https://github.com/anthropics/financial-services.git

# Each sync:
git fetch upstream
git checkout -b sync/upstream-YYYY-MM-DD upstream/main

# Cherry-pick or merge selectively. Avoid blanket `git merge upstream/main` —
# it will reintroduce dropped verticals, agents, partner plugins, and the US data connectors.
```

Recommended approach:

1. Review the upstream diff: `git log main..upstream/main --oneline`
2. For each commit that touches a plugin we keep, decide:
   - cherry-pick as-is: `git cherry-pick <sha>`
   - cherry-pick with adaptation: `git cherry-pick --no-commit <sha>` then edit
   - skip (e.g., changes to investment-banking, partner plugins, US data connectors)
3. Run `python3 scripts/check.py` before merging the sync branch.

## Sync log

| Date | Upstream commit range | Notes |
|---|---|---|
| YYYY-MM-DD | initial fork from `<sha>` | Initial scaffolding; see "What we changed" above. |

(Append rows as upstream syncs happen.)
