> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 案件レコード

```yaml
recordType: matter-profile
tenantId: "[tenant id]"
practiceId: "[practice id]"
pluginId: ai-governance-legal
matterId: "[server-generated-id]"
slug: acme-ai-review-2026
title: "[Client] — [short description]"
client: "[name]"
counterparties:
  - "[name]"
matterType: vendor AI review
opened: "2026-07-16"
status: active
confidentiality: heightened
jurisdictions:
  - ja-JP
authorizedViewers:
  - "[group or user id]"
keyFacts: "[2–5 sentences]"
overrides:
  - "[matter-specific position]"
relatedMatters:
  - slug: "[slug]"
    reason: "[reason]"
retentionPolicy: "[policy id]"
dlpPolicy: "[policy id]"
legalHold: false
crossMatterAllowed: false
```

## History event

SharePoint `audit` に追記する。

```yaml
eventType: matter-opened
tenantId: "[tenant id]"
practiceId: "[practice id]"
matterId: "[matterId]"
slug: "[slug]"
timestamp: "[ISO-8601]"
performedBy: "[user id]"
sourceETag: "[eTag]"
idempotencyKey: "[idempotencyKey]"
notes: "[initial context]"
```

`close` は `matter-closed`、`switch` は `matter-binding-changed` とする。監査イベントを編集・削除しない。
