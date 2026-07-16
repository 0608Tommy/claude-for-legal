> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、日本のclosing state向けに変更した派生ファイルです。

# Closing checklist records

## State envelope

```yaml
tenantId: "[tenant id]"
practiceId: "[practice id]"
scopeType: matter
scopeId: "[matterId]"
recordType: closing-checklist-item
recordId: "[CP-001 or CD-001]"
itemId: "[SharePoint itemId]"
eTag: "[eTag]"
version: 1
updatedAt: "[ISO-8601]"
payload:
  dealCode: "[code]"
  transactionStructure: "[canonical value]"
  item: "[action]"
  category: "[category]"
  responsible: "[person/role]"
  due: "[ISO date or null]"
  status: not_started | in_progress | filed_pending | waiting_period | complete | blocked | waived | unknown
  blocking: true
  severity: "[🔴 | 🟠 | 🟡 | 🟢]"
  source: "[source item/version/location]"
  legal_basis: "[law/rule/guidance/contract]"
  source_version: "[version]"
  effective_date: "[date or null]"
  evidence_required: "[evidence]"
  evidence_item_ids:
    - "[itemId]"
  filing_system: "[system or null]"
  waiting_period_end: "[date or null]"
  waivable: false
  estimated_time_to_complete: "[duration or unknown]"
  depends_on:
    - "[recordId]"
  notes: "[minimal]"
```

## Create

new itemはcomplete canonical key、`expectedAbsent: true`、unique
`idempotencyKey`。existing `itemId`/`eTag`を要求しない。

## Update

exact `itemId`、latest`eTag`、unique`idempotencyKey`、single reviewed patch。
source/evidenceなしに`complete`または`waived`へしない。
