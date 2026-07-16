> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Full privacy setup interview

## Part 0 — User / practice / integrations

- role
- attorney/supervisor route
- practice setting
- SharePoint / OneDrive / optional connector status
- Cowork DLP blocker acceptance

## Part 1 — Business and data

- what the organization sells / provides
- B2B / B2C / employer / public function
- whose data
- controller / processor / both by activity
- data locations and remote access
- privacy team / DPO / security partner

Do not force one company-wide role when activities differ.

## Part 2 — Regulatory footprint

- data-subject, customer, employee, operation jurisdictions
- GDPR / UK GDPR / US state
- GLBA、HIPAA、FERPA、COPPA等
- Japan APPI、My Number、finance、medical、telecom、employment、public sector
- regulator inquiry、order、contract commitment
- cross-border corridors

Specific law, threshold, deadline stated by user is verified before saving.

## Part 3 — DPA playbook

### We are processor

| Term | Standard | Fallback | Never |
|---|---|---|---|
| Audit | | | |
| Incident | | | |
| Subprocessor | | | |
| Location / transfer | | | |
| Deletion / backup | | | |
| Liability | | | |
| Independent use / training | | | |

### We are controller

| Term | Require | Acceptable | Never |
|---|---|---|---|

Capture the one automatic reject. Compare interview position to exact template.

## Part 4 — PIA

- house trigger
- binding-law trigger handling
- length / depth / section order
- risk scale
- sign-off
- children / biometric / employee / ad-tech / AI triggers
- policy diff surfaces

## Part 5 — DSAR / rights

- volume / handler
- systems list
- identity method
- internal SLA
- authorized agent
- exemption review
- secure delivery
- deletion/production authority
- Japan `保有個人データ` workflow vs GDPR/US

## Part 6 — Policy commitments

- data categories
- purposes
- recipients / processors
- sale/share representation
- retention
- rights
- countries
- AI training / improvement

Surfaces:

- website policy
- CMP / cookie
- App Store
- Google Data Safety
- in-product consent
- employee/applicant notice
- sector notice

## Part 7 — Escalation

- routine DSAR
- DPA fallback
- high-risk PIA
- regulator inquiry
- suspected incident
- child / guardian conflict
- My Number / biometric / employee
- outside counsel / qualified Japanese counsel

## Part 8 — Sources and outputs

Record exact itemId, version, read coverage, confidentiality.

- policy
- DPA
- PIA
- DSAR runbook
- notices

Configure:

- reviewed output library
- personal draft
- policy item IDs
- naming convention without person names
- policy sweep cursor scope
- matter workspace enabled / cross-matter false
- audit fields
