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
bindingGeneration: 1
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

`close`のatomic fenceはmatterを`close-pending`へtransitionし、generation方式を
使うgatewayでは同じconditional updateで`bindingGeneration`を増やす。zero active
確認後だけ`archived`へfinalizeする。

## 監査event

SharePoint `audit`にはshared audit envelopeで追記する。`pluginId`、`slug`、
operation、binding identity、eTag等のpackage固有fieldは`details`へ入れ、
top-levelへ追加しない。

### Matter create

<!-- audit-event-example -->
```yaml
tenantId: tenant-1
practiceId: ai-governance
matterId: matter-1
eventType: matter-opened
correlationId: corr-matter-open-0001
idempotencyKey: matter-create-0001
actorObjectId: user-1
timestamp: "2026-07-16T09:00:00+09:00"
outcome: succeeded
itemIds:
  - matter-item-1
details:
  pluginId: ai-governance-legal
  operation: matter-create
  slug: acme-ai-review-2026
  bindingGeneration: 1
  eTagBefore: null
  eTagAfter: '"1"'
  notes: initial-context-recorded
```

### Switch — current binding revoke

<!-- audit-event-example -->
```yaml
tenantId: tenant-1
practiceId: ai-governance
matterId: matter-1
eventType: session-binding-revoked
correlationId: corr-matter-switch-0001
idempotencyKey: binding-revoke-0001
actorObjectId: user-1
timestamp: "2026-07-16T10:00:00+09:00"
outcome: succeeded
itemIds:
  - binding-item-1
details:
  pluginId: ai-governance-legal
  operation: switch
  userObjectId: user-1
  sessionId: session-1
  oldMatterId: matter-1
  newMatterId: matter-2
  eTagBefore: '"7"'
  eTagAfter: '"8"'
  revocationReason: matter-switch
```

### Switch — fresh-session binding create

<!-- audit-event-example -->
```yaml
tenantId: tenant-1
practiceId: ai-governance
matterId: matter-2
eventType: session-binding-created
correlationId: corr-matter-switch-0001
idempotencyKey: binding-create-0002
actorObjectId: user-1
timestamp: "2026-07-16T10:02:00+09:00"
outcome: succeeded
itemIds:
  - binding-item-2
details:
  pluginId: ai-governance-legal
  operation: switch
  userObjectId: user-1
  sessionId: session-2
  previousSessionId: session-1
  oldMatterId: matter-1
  newMatterId: matter-2
  scopeType: session
  scopeId: user-1:session-2
  recordType: session-matter-binding
  recordId: active-matter
  expectedAbsent: true
  matterItemId: matter-item-2
  expectedMatterStatus: active
  matterETag: '"3"'
  bindingGeneration: 4
  atomicWithBindingExpectedAbsent: true
```

revokeとcreateは別eventで同じ`correlationId`を使う。createはfresh sessionで
binding不在を確認できた場合だけ記録する。`close`では`matter-closed`と
対象全bindingの`session-binding-revoked`を同じclose `correlationId`で関連付け、
各結果を追記する。監査eventを編集・削除しない。
