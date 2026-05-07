#!/usr/bin/env bash
#
# setup-fintegrity-fork.sh
#
# Apply Fintegrity customizations to a freshly cloned fork of
# anthropics/financial-services. Idempotent — safe to re-run.
#
# Run from the repo root, AFTER dropping these files into the root:
#   - marketplace.json
#   - financial-analysis-mcp.json
#   - README.md (replaces upstream)
#   - CLAUDE.md (replaces upstream)
#   - MIGRATION.md (new)
#
# What it does:
#   1. Removes upstream dirs out of scope for Fintegrity.
#   2. Moves marketplace.json -> .claude-plugin/marketplace.json
#   3. Moves financial-analysis-mcp.json -> plugins/vertical-plugins/financial-analysis/.mcp.json
#   4. Validates JSON and runs the upstream check.py if present.
#
# Does NOT commit or push. Review the diff first.

set -euo pipefail

# Sanity check
if [[ ! -f "README.md" || ! -d "plugins/vertical-plugins/financial-analysis" ]]; then
  echo "ERROR: This doesn't look like a clone of anthropics/financial-services."
  echo "       Run from the repo root after cloning."
  exit 1
fi

# ---------------------------------------------------------------------------
# 1. Remove out-of-scope verticals
# ---------------------------------------------------------------------------
echo "==> Removing out-of-scope verticals..."
for v in investment-banking equity-research wealth-management operations; do
  d="plugins/vertical-plugins/$v"
  if [[ -d "$d" ]]; then
    echo "    - $d/"
    rm -rf "$d"
  fi
done

# ---------------------------------------------------------------------------
# 2. Remove out-of-scope agents (and their managed-agent cookbooks)
# ---------------------------------------------------------------------------
echo "==> Removing out-of-scope agents..."
for a in pitch-agent market-researcher earnings-reviewer model-builder kyc-screener; do
  for d in "plugins/agent-plugins/$a" "managed-agent-cookbooks/$a"; do
    if [[ -d "$d" ]]; then
      echo "    - $d/"
      rm -rf "$d"
    fi
  done
done

# ---------------------------------------------------------------------------
# 3. Remove partner-built plugins (no relevant subscriptions)
# ---------------------------------------------------------------------------
echo "==> Removing partner-built plugins..."
if [[ -d "plugins/partner-built" ]]; then
  echo "    - plugins/partner-built/"
  rm -rf "plugins/partner-built"
fi

# ---------------------------------------------------------------------------
# 4. Remove the M365 install tooling — we use the standard add-in path
# ---------------------------------------------------------------------------
echo "==> Removing M365 install tooling (out of scope)..."
if [[ -d "claude-for-msft-365-install" ]]; then
  echo "    - claude-for-msft-365-install/"
  rm -rf "claude-for-msft-365-install"
fi

# ---------------------------------------------------------------------------
# 5. Install customized files
# ---------------------------------------------------------------------------
echo "==> Installing customized files..."

mkdir -p .claude-plugin
if [[ -f "marketplace.json" ]]; then
  mv marketplace.json .claude-plugin/marketplace.json
  echo "    - .claude-plugin/marketplace.json"
fi

if [[ -f "financial-analysis-mcp.json" ]]; then
  mv financial-analysis-mcp.json plugins/vertical-plugins/financial-analysis/.mcp.json
  echo "    - plugins/vertical-plugins/financial-analysis/.mcp.json"
fi

for f in README.md CLAUDE.md MIGRATION.md; do
  if [[ -f "$f" ]]; then
    echo "    - $f (in place)"
  else
    echo "    ! WARNING: $f missing — drop it into the repo root before committing."
  fi
done

# ---------------------------------------------------------------------------
# 6. Validate
# ---------------------------------------------------------------------------
echo ""
echo "==> Validating JSON..."
python3 -m json.tool .claude-plugin/marketplace.json > /dev/null && echo "    - marketplace.json OK"
python3 -m json.tool plugins/vertical-plugins/financial-analysis/.mcp.json > /dev/null && echo "    - financial-analysis/.mcp.json OK"

echo ""
echo "==> Running upstream lint (scripts/check.py) if available..."
if [[ -f "scripts/check.py" ]]; then
  if python3 scripts/check.py; then
    echo "    - check.py passed"
  else
    echo "    ! check.py reported issues. Review and fix before committing."
    echo "      The kept agents may reference skills bundled from the verticals we just deleted."
    echo "      Common fix: edit the agent's plugin.json or remove orphan bundled skills under"
    echo "      plugins/agent-plugins/<agent>/skills/ that came from a deleted vertical."
  fi
else
  echo "    (no scripts/check.py found, skipping)"
fi

# ---------------------------------------------------------------------------
# 7. Next steps
# ---------------------------------------------------------------------------
cat <<'EOF'

==> Done. Next steps:
    1. git status                    # review changes
    2. git diff --stat               # summary
    3. git checkout -b initial-fintegrity-fork
    4. git add -A
    5. git commit -m "Initial Fintegrity fork: scope to 3 verticals + 5 agents, swap MCP connectors"
    6. git push -u origin initial-fintegrity-fork
    7. Open a PR against main, merge, then connect to Cowork.

EOF
