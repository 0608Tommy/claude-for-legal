> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Matter records

## Matter

```yaml
recordType: matter-profile
tenantId: "[tenant id]"
practiceId: "[practice id]"
pluginId: privacy-legal
matterId: "[server-generated ID]"
slug: acme-dpa-2026
title: "[Client] — [short description]"
client: "[name]"
counterparties:
  - "[name]"
matterType: DPA review
opened: "2026-07-16"
status: active
confidentiality: heightened
jurisdictions:
  - ja-JP
authorizedViewers:
  - "[Entra user/group ID]"
keyFacts: "[2–5 sentences]"
overrides:
  - "[matter-specific position]"
relatedMatters:
  - matterId: "[ID]"
    reason: "[reason]"
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
userObjectId: "[Entra object ID]"
sessionId: "[Cowork session ID]"
matterId: "[matter ID]"
status: active | revoked
boundAt: "[ISO-8601]"
boundBy: "[Entra object ID]"
expiresAt: "[ISO-8601]"
revokedAt: "[ISO-8601 or null]"
revokedBy: "[Entra object ID or null]"
revocationReason: "[reason or null]"
```

`status != active`、`expiresAt <= now`、またはmatter archivedならbindingを
拒否する。

## Audit

```yaml
tenantId: "[tenant id]"
practiceId: "[practice id]"
eventType: matter-opened | matter-binding-changed | matter-closed
correlationId: "[correlation ID]"
actorObjectId: "[Entra object ID]"
idempotencyKey: "[idempotencyKey or null]"
timestamp: "[ISO-8601]"
outcome: succeeded | failed | rejected | partial
matterId: "[matter ID or null]"
itemIds:
  - "[SharePoint itemId]"
details:
  oldMatterId: "[matter ID or null]"
  newMatterId: "[matter ID or null]"
  oldSessionId: "[session ID or null]"
  newSessionId: "[session ID or null]"
  sourceETag: "[eTag or null]"
  notes: "[minimal context]"
```

audit eventを編集・削除しない。
