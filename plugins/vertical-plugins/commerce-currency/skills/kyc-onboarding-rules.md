# KYC and Onboarding Rules
 
## Purpose
This skill governs all user onboarding logic, KYC verification steps, Active Balance requirements, and account type-specific rules. Apply during onboarding flows, re-verification triggers, and any user account type change.
 
## Three Account Types
Customer, Creator, and Merchant. All three are first-class participants. Onboarding journey and requirements differ by type.
 
## Active Balance Minimums (Required Before First Transaction)
Customer: 400 KLM at £0.09 = £36 minimum. Creator: 1,800 KLM at £0.09 = £162 minimum. Merchant: 3,690 KLM at £0.09 = £332.10 minimum. Frame always as "starting balance," never as a fee. Explain it as the user's first position in the KAELUM commerce ecosystem.
 
## Onboarding Steps (Customer)
1. Account creation (email, phone, password). 2. Email and phone verification. 3. Identity verification (government photo ID upload + liveness check). 4. Address verification. 5. SENTINEL KYC clearance. 6. Active Balance purchase (minimum 400 KLM via TrueLayer Open Banking or Stripe). 7. First transaction enabled.
 
## Onboarding Steps (Creator)
Same as Customer steps 1 through 6, plus: social media or platform profile verification. Active Balance minimum: 1,800 KLM. Creator Studio and Social Paylinks unlocked on completion.
 
## Onboarding Steps (Merchant)
1. Account creation. 2. Contact verification. 3. Business registration document upload (Companies House number or equivalent). 4. Director identity verification. 5. Beneficial ownership declaration (all UBOs above 25% ownership). 6. Business bank account verification (via TrueLayer Open Banking). 7. SENTINEL merchant KYC clearance. 8. Active Balance purchase (minimum 3,690 KLM). 9. Merchant features unlocked. KST candidacy assessment available on request after 30 days of active trading.
 
## Re-Verification Triggers
SENTINEL risk score exceeds 70, identity document expiry within 30 days, address change submitted, device fingerprint anomaly, three or more failed authentication attempts in 24 hours, or manual trigger from Compliance and Regulatory Agent.
 
## Stall Re-engagement Protocol
User begins onboarding but does not complete within 48 hours: automated re-engagement message at 48 hours, 96 hours, and 7 days. Message content: warm, contextual, references the specific step they left incomplete. After 7 days without completion: flag to Onboarding Concierge Agent for personalised intervention. After 30 days of no activity on an incomplete onboarding: soft archive (account preserved, no further outreach unless user re-initiates).
 
## Approval Gates in Onboarding
KYC rejection (any reason): requires admin review before rejection is communicated to user. Merchant UBO declaration anomaly: escalate to Legal Counsel Agent and admin. SENTINEL hard hold during onboarding: admin release required. Merchant KST application: separate assessment process (KST Sub-Token Application Assessment function).
