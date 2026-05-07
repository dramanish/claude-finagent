# K.A.T.E. Agent Orchestration
 
## Purpose
This skill governs the technical architecture, communication patterns, and governance rules for the K.A.T.E. multi-agent system. Apply when routing tasks between agents, handling approval gates, managing heartbeats, or building new agent integrations.
 
## System Architecture
K.A.T.E. (Kaelum. Audivo. Triovus. Engine.) is the COO of KAELUM Technologies Ltd. All 20 agents operate under K.A.T.E. and report to Greggar Deterville (CEO). Intelligence layer: Claude (Anthropic) exclusively. No other AI models. Named engine layers: Audivo (execution engine, audivo.cloud) and Triovus (governance engine, triovus.com), both Claude-powered.
 
## Orchestration Layer: Paperclip
Paperclip is self-hosted on Hostinger VPS using Node.js and PostgreSQL. It is the agent orchestration layer. Base44 (kaelum.app platform) sends events to Paperclip via HTTP webhook with shared secret authentication. Paperclip sends heartbeats back to wake Base44 agents. Never describe n8n as the primary orchestration engine — n8n handles workflow routing only.
 
## Agent Registration Requirements
Every K.A.T.E. agent must be registered in Paperclip with: heartbeat interval (seconds), approval gate definitions, goal alignment declaration, event bridge mapping (which events trigger this agent, which events this agent fires). Registration is mandatory before any agent is deployed to production.
 
## Managed Agents API
Seven K.A.T.E. functions use the Managed Agents API (beta header: managed-agents-2026-04-01): Research Scout scans, SENTINEL compliance batch reports, Invoice to Insights, KVI Governance assessments, Commerce Drop content moderation, KST Sub-Token application assessment, and the stateful Onboarding Agent. Four functions use the standard Claude API: K.A.T.E. orchestrator routing, Audivo per-transaction execution, SENTINEL per-transaction risk scoring, and K.A.T.E. Integration chatbot.
 
## Approval Gate Protocol
Approval gates define what requires human sign-off before execution. Gate types: admin_required (any admin can approve), ceo_required (Greggar only), compliance_review (Compliance Agent plus admin), legal_review (Legal Counsel Agent plus admin). All gates are enforced by Paperclip. No agent may bypass an approval gate autonomously.
 
## Cross-Agent Signal Standard
{ signal_type: string, source_agent: string, target_agent: string, priority: 'critical' | 'high' | 'medium' | 'low', payload: object, requires_approval: boolean, timestamp: ISO8601 }. Critical signals: immediate delivery, admin notification. High: delivery within 5 minutes. Medium: batch delivery every 15 minutes. Low: batch delivery hourly.
 
## Model Assignment by Function
Claude Haiku 4.5: high-volume lightweight tasks (summaries, categorisation, routine checks). Claude Sonnet 4.6: standard agent tasks, advisory functions, content generation (primary workhorse). Claude Opus 4.7: KVI Governance, complex compliance reasoning, M&A matching, high-stakes financial analysis. Always use the lowest sufficient model tier to manage API costs. Never use Opus for tasks Sonnet handles reliably.
 
## Base44 Platform Notes
KAELUM is built on Base44. Base44 uses client-side JavaScript rendering, making kaelum.app nearly invisible to search crawlers. Schema markup is installed in index.html head. The User Management admin panel is the Single Source of Truth (SSOT) for all user data. All agents reading user data must pull from the canonical source entities, not cached copies.
