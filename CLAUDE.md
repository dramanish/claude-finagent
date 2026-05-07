# KAELUM K.A.T.E. Architecture
 
This repository contains the complete K.A.T.E. (Kaelum Audivo Triovus Engine)
agent architecture for KAELUM Technologies Ltd, forked from and aligned with
anthropics/financial-services.
 
## What KAELUM Is
The world's first Ai-powered, non-crypto, Closed-Loop Digital Commerce Currency.
Governed exclusively by Claude (Anthropic). Live at kaelum.app.
Company: KAELUM Technologies Ltd, England & Wales No. 16681154.
 
## Architecture Overview
- 20 K.A.T.E. agents across three categories (Internal, External, Cross-System)
- 1 vertical plugin: commerce-currency (11 skills)
- 11 functional prompts (7 Managed Agents API, 4 Standard API)
- Orchestration: Paperclip (self-hosted Node.js + PostgreSQL, Hostinger VPS)
- Platform: Base44 (kaelum.app) via HTTP webhook (shared secret) to Paperclip
- Managed Agents API: beta header managed-agents-2026-04-01
 
## Intelligence Layer
Claude (Anthropic) exclusively. No other AI models. Named engine layers:
Audivo (execution engine, audivo.cloud) and Triovus (governance engine,
triovus.com), both Claude-powered.
 
## Model Tiers
- claude-haiku-4-5: high-volume lightweight tasks
- claude-sonnet-4-6: standard agent tasks (primary workhorse)
- claude-opus-4-7: KVI Governance, complex compliance, M&A matching (Opus-only)
 
## Managed Agents (7)
Research Scout scans, SENTINEL compliance batch, Invoice to Insights,
KVI Governance, Commerce Drop content moderation, KST assessment,
Onboarding Concierge (stateful).
 
## Standard API (4)
K.A.T.E. orchestrator routing, Audivo per-transaction execution,
SENTINEL per-transaction risk scoring, K.A.T.E. Integration Chatbot.
 
## Mandatory Terminology
- Always: Ai (capital A, lowercase i) — never AI in branded contexts
- Always: Commerce Currency / Account — never token, crypto, blockchain, wallet
- Always: issued / allocated / credited — never minted / mined
- Always: multi-instance Claude — never multi-LLM
- Never reference competing AI systems
 
## Regulatory Context
Closed-loop exemption: UK EMR 2011, EU E-Money Directive 2009/110/EC.
KLM classified as Multi-Purpose Voucher (MPV) for UK VAT.
CARF non-applicable. Standard UK trading company tax position.
 
## Contact
Greggar Deterville, Founder and CEO
info@kaelumtechnologies.com | https://kaelum.app
