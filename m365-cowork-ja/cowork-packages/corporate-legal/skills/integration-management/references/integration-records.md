> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、日本のpost-close integration state向けに変更した派生ファイルです。

# Integration records

## Metadata

```yaml
recordType: integration-tracker
deal_code: "[code]"
target: "[company]"
transactionStructure: "[canonical value]"
close_date: "[ISO date]"
deal_lead: "[name]"
outside_counsel: "[firm/lead]"
last_updated: "[ISO-8601]"
last_status_report: "[ISO-8601 or null]"
trackerVersion: 1
status: active | superseded
```

## PA dates

```yaml
required_consents_deadline: "[date or null]"
rep_survival:
  - category: "[general/fundamental/tax/other]"
    expires: "[date]"
escrow_release: "[date or null]"
earnout_milestones:
  - description: "[milestone]"
    measurement_date: "[date]"
    payment_date: "[date]"
    owner: finance
```

## Workplan

```yaml
id: W-001
description: "[action]"
phase: day_1 | day_30 | day_90 | day_180
owner: legal-owns | legal-supports
workstream: legal | hr | it | finance | real-estate | other
priority: critical | high | medium | low
deadline: "[date or null]"
deadline_basis: pa-obligation | regulatory | best-practice
legal_basis: "[source]"
status: not_started | in_progress | complete | blocked | deferred
blocker: "[description or null]"
depends_on: "[ID or null]"
evidence_item_ids:
  - "[itemId]"
```

## Consent

```yaml
id: CON-001
counterparty: "[name]"
contract_type: customer | vendor | lease | IP-license | financial | other
required_consent: true
pa_deadline: "[date or null]"
status: not_started | outreach_sent | in_negotiation | obtained | waived | refused
assigned_to: "[name or null]"
outreach_date: "[date or null]"
obtained_date: "[date or null]"
conditions: "[conditions]"
source_item_id: "[itemId]"
source_version: "[version]"
```

## Contract

```yaml
id: C-001
name: "[contract]"
counterparty: "[name]"
contract_type: MSA | SaaS | lease | IP-license | employment | NDA | other
annual_value: "[amount or unknown]"
assignment_mechanism: auto-assign | consent-required | coc-provision | silent | not_reviewed
tier: 1
required_consent: false
pa_deadline: "[date or null]"
status: not_reviewed | no_action | consent_pending | outreach_sent | in_negotiation | consent_obtained | assignment_complete | waived | refused | coc_triggered
assigned_to: "[name or null]"
source_item_id: "[itemId]"
source_version: "[version]"
last_updated: "[ISO-8601]"
```

## State key/write

canonical key:
`tenantId + practiceId + scopeType + scopeId + recordType + recordId`。

new tracker/version/itemはconditional create、existing itemはexact `itemId`、
latest`eTag`、unique`idempotencyKey`でconditional update。old versionをdeleteしない。
