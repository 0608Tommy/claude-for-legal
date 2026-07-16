> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、corporate/M&A matter state向けに変更した派生ファイルです。

# Matter, binding, audit records

## Matter

```yaml
recordType: matter-profile
tenantId: "[tenant id]"
practiceId: "[practice id]"
pluginId: corporate-legal
matterId: "[server-generated immutable ID]"
slug: "project-sakura-2026"
title: "[Client/Company] — [short description]"
client: "[represented party]"
counterparties:
  - "[name]"
matterType: M&A buy-side | M&A sell-side | financing | board matter | entity reorg | integration project | public-company matter | other
transactionStructure: share sale | business transfer | merger | company split | share exchange | share transfer | share delivery | other | not-applicable
opened: "[ISO date]"
closed: "[ISO date or null]"
status: active | archived
confidentiality: standard | heightened | clean-team
jurisdictions:
  - ja-JP
authorizedViewers:
  - "[Microsoft Entra user/group ID]"
keyFacts: "[2–5 sentences]"
overrides:
  - "[matter-specific position]"
relatedMatterIds:
  - "[matterId]"
retentionPolicy: "[policy ID]"
dlpPolicy: "[policy ID]"
legalHold: false
crossMatterAllowed: false
```

## Binding

```yaml
recordType: session-matter-binding
tenantId: "[tenant id]"
practiceId: "[practice id]"
userObjectId: "[Microsoft Entra object ID]"
sessionId: "[Cowork session ID]"
matterId: "[matter ID]"
status: active | revoked
boundAt: "[ISO-8601]"
boundBy: "[Microsoft Entra object ID]"
expiresAt: "[ISO-8601]"
revokedAt: "[ISO-8601 or null]"
revokedBy: "[Microsoft Entra object ID or null]"
revocationReason: "[reason or null]"
```

unique key:
`tenantId + practiceId + userObjectId + sessionId`。

practice-level fresh sessionにはbindingが存在しない。active bindingのmatterIdは
non-null。`status != active`、`expiresAt <= now`、matter archivedを拒否する。

## Canonical audit envelope

```yaml
tenantId: "[tenant id]"
practiceId: "[practice id]"
matterId: "[matter ID or null]"
eventType: matter-created | matter-binding-changed | matter-closed
correlationId: "[16–128 character ID]"
idempotencyKey: "[key or null]"
actorObjectId: "[Microsoft Entra object ID]"
timestamp: "[ISO-8601]"
outcome: succeeded | failed | rejected | partial
itemIds:
  - "[SharePoint itemId]"
details:
  oldMatterId: "[ID or null]"
  newMatterId: "[ID or null]"
  oldSessionId: "[ID or null]"
  newSessionId: "[ID or null]"
  eTagBefore: "[eTag or null]"
  eTagAfter: "[eTag or null]"
  revocationReason: "[reason or null]"
```

auditはappend-only。update/deleteしない。
