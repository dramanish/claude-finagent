# Commerce Intelligence
 
## Purpose
This skill governs all transaction data analysis, pattern recognition, merchant and user intelligence generation, and cross-agent signal dispatch. Apply when generating insights dashboards, producing performance reports, identifying anomalies, or feeding intelligence to other agents.
 
## Data Sources
Transaction event stream (via Paperclip event bridge), user account data (via Base44 SSOT), merchant performance data, KVI metrics feed, SENTINEL risk scoring output, creator activity logs.
 
## Spending Pattern Analysis
Track at user level: average transaction frequency, average transaction value, preferred merchant categories, KLMback accumulation rate, redemption patterns. Segment users: high-frequency low-value (HF-LV), low-frequency high-value (LF-HV), new active, dormant (no transaction in 30 days). Personalised insights fed to User Personal Agent for individual user display.
 
## Merchant Pattern Analysis
Daily: transaction volume, average basket value, customer return rate, KLM redemption request frequency, discount utilisation rate. Weekly: merchant performance score (0-100), cohort analysis (new vs. returning customer ratio), category benchmark comparison. Flag: merchants below 50th percentile for three consecutive weeks (churn risk). Flag: merchants in top 20th percentile for tier promotion recommendation.
 
## Cross-Agent Signal Format
Signals dispatched via Paperclip event bridge. Standard signal structure: { signal_type: string, source_agent: string, target_agent: string, priority: 'critical' | 'high' | 'medium' | 'low', payload: object, requires_approval: boolean, timestamp: ISO8601 }. Research Scout signals to Creator Studio and Merchant Support must include: intelligence_category, urgency, recommended_action, raw_source_reference.
 
## Anomaly Detection Baselines
Establish rolling 30-day baseline per user and per merchant. Flag when: transaction value exceeds 3x baseline average, transaction frequency exceeds 5x baseline hourly rate, new merchant with zero history processes transaction above £500, or geographic pattern inconsistency detected. All anomalies above medium severity forwarded to Fraud and Scam Detection Agent.
 
## KVI Data Feed
Transaction Insights Agent calculates and pushes KVI dimension inputs to KVI Governance Agent via Paperclip at end of each assessment period. Inputs: total GTV (90 days), transaction count, unique active merchants, unique active creators, redemption volume, KPR inflow. Data is pre-validated for completeness before dispatch.
 
## Privacy Rules
All cross-user analytics are aggregated and anonymised for admin use. Individual user data is only surfaced to that user's own User Personal Agent instance. No merchant can see another merchant's transaction data. Creator performance data is private unless the creator opts into leaderboard features.
