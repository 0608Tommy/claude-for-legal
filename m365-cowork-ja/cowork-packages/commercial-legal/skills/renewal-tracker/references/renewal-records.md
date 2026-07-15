> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Renewal state records

## Record

```yaml
recordType: renewal
tenantId: "[tenant id]"
practiceId: "[practice id]"
pluginId: commercial-legal
scopeType: practice | matter
scopeId: "[practiceId or matterId]"
recordId: "ren-001"
counterparty: "Acme SaaS Inc."
agreement: "Acme Platform Subscription Agreement"
sourceSystem: SharePoint | Ironclad | DocuSign | other
sourceItemId: "[exact source item ID]"
sourceVersion: "[version]"
signed_date: "2025-06-15"
initial_term_end: "2026-06-15"
current_term_end: "2026-06-15"
renewal_mechanism: "auto-renew annual"
notice_period_days: 60
notice_method: "email"
notice_clause_ref: "§12.3"
notice_address_or_portal: "[address/URL or restricted reference]"
receipt_rule: "sent | received | deemed received"
transit_buffer_days: 0
cancel_by_calendar: "2026-04-16"
cancel_by_effective: "2026-04-16"
send_by_effective: "2026-04-16"
deadline_time_zone: "Asia/Tokyo"
cancel_by_roll_note: ""
cancel_by_provenance: "[model calculation — verify against the notice clause]"
price_on_renewal: "then-current list (uncapped)"
annual_value: 48000
currency: USD
business_owner: "[user/object id]"
status: active | cancelled | renewed | lapsed
notes: "[notes]"
lastVerifiedAt: "[ISO datetime]"
lastVerifiedBy: "[object id]"
```

## Calculation

```text
cancel_by_calendar = current_term_end - notice_period_days
cancel_by_effective = contract/jurisdiction-aware last valid receipt date
send_by_effective = cancel_by_effective - required transit/processing buffer
daysUntilAction = send_by_effective - today
```

contractが「N日前までに発送」と定める場合、receipt前提を使わない。`business day`definitionがあればそれを優先する。

## Update event

```yaml
tenantId: "[tenant id]"
practiceId: "[practice id]"
eventType: renewal-updated
correlationId: "[correlation id]"
actorObjectId: "[object id]"
idempotencyKey: "[unique key]"
timestamp: "[ISO datetime]"
outcome: succeeded | failed | rejected | partial
itemIds:
  - "[renewal SharePoint itemId]"
details:
  recordId: "[renewal recordId]"
  changedFields:
    - "[field]"
  eTagBefore: "[eTag]"
  eTagAfter: "[eTag]"
  approvedBy: "[object id]"
```

## Scope cursor

```yaml
recordType: sync-cursor
tenantId: "[tenant id]"
practiceId: "[practice id]"
scopeType: practice | matter
scopeId: "[id]"
recordId: "renewal-sync:[sourceSystem]:[queryFingerprint]"
sourceSystem: "[connector]"
queryFingerprint: "[stable query hash]"
cursorValue: "[opaque value]"
lastSuccessfulItemId: "[source id or null]"
```

query/scope/sourceが変わればcursorを再利用しない。
