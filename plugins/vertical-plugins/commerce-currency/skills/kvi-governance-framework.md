# KVI Governance Framework
 
## Purpose
The KAELUM Value Index (KVI) is the deterministic Ai-governed framework for assessing KAELUM ecosystem health and informing KLM floor price appreciation decisions. This skill governs all KVI assessment, scoring, reporting, and recommendation reasoning.
 
## KVI Assessment Dimensions (Four)
1. Transaction Volume: total GTV in the assessment period, velocity trend, average transaction value, peak-to-trough ratio.
2. Merchant Diversity: number of active merchants, category spread, geographic distribution, merchant churn rate, new merchant acquisition rate.
3. Creator Activity: active creator count, listings published, social paylink conversion rate, creator KLM spend rate.
4. Liquidity Metrics: KPR reserve balance as percentage of outstanding KLM, redemption rate (fiat off-ramp velocity), float efficiency, KLM circulation velocity.
 
## Scoring Methodology
Each dimension scores 0-100. The combined KVI Health Score is a weighted average: Transaction Volume 35%, Merchant Diversity 25%, Creator Activity 20%, Liquidity Metrics 20%. A KVI Health Score above 75 in three consecutive quarterly assessments triggers an appreciation recommendation. A score below 50 in any single dimension triggers a dimension-specific intervention recommendation.
 
## Assessment Cadence
Quarterly. Aligned with TPR distribution cycle. Assessment window: 90 days preceding the distribution date. Report due: 14 days before distribution.
 
## KVI Governance Report Contents
Executive summary (1 page), four dimension scorecards with trend analysis, KVI Health Score with prior-quarter comparison, appreciation recommendation (yes/no with justification), KPR reserve health analysis, KST sub-token performance section (one page per active KAELUM Sub Token), recommended ecosystem interventions with priority ranking, CEO action items.
 
All KVI Governance Reports are confidential internal documents for Greggar (CEO) review only. They are not disclosed to merchants, creators, investors, or the public.
 
## Appreciation Recommendation Protocol
When the KVI score crosses the appreciation threshold, the KVI Governance Agent produces a formal appreciation proposal: current floor price, proposed new floor price, justification scorecard, projected impact on merchant economics, projected impact on KPR reserve adequacy, risk considerations. All appreciation proposals require CEO approval before any price change is implemented. K.A.T.E. enforces the approved price change across all platform systems on Paperclip execution confirmation.
 
## Model Requirement
KVI Governance assessments use Claude Opus exclusively. The complexity of multi-dimensional ecosystem analysis, compounding KST mechanics, and appreciation risk reasoning requires Opus-level reasoning. Downgrading to Sonnet for KVI scoring is not permitted.
