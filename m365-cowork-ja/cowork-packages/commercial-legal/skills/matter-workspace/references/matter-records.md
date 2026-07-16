> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Matter records

## Matter

```yaml
recordType: matter-profile
tenantId: "[tenant id]"
practiceId: "[practice id]"
matterId: "[immutable id]"
slug: "acme-msa-2026"
client: "[represented party]"
counterparties:
  - "[name]"
matterType: vendor MSA | customer agreement | NDA | SaaS subscription | amendment | renewal | other
status: active | archived
opened: "[ISO date]"
closed: "[ISO date or null]"
confidentiality: standard | heightened | clean-team
jurisdictions:
  - "[jurisdiction]"
keyFacts: "[2-5 sentences]"
playbookOverrides:
  - "[override]"
relatedMatterIds:
  - "[matterId]"
authorizedViewers:
  - "[Entra object/group id]"
retentionPolicy: "[policy id]"
legalHold: true | false
```

`matterId`、opened、audit historyは変更しない。slug変更が必要ならalias/historyを残す。

## Binding

```yaml
recordType: session-matter-binding
tenantId: "[tenant id]"
practiceId: "[practice id]"
userObjectId: "[Microsoft Entra object id]"
sessionId: "[Cowork session id]"
matterId: "[matter id]"
status: active | revoked
boundAt: "[ISO datetime]"
boundBy: "[object id]"
expiresAt: "[ISO datetime]"
revokedAt: "[ISO datetime or null]"
revokedBy: "[object id or null]"
revocationReason: "[matter closed / user selected none / access revoked / null]"
```

一意keyは`tenantId + practiceId + userObjectId + sessionId`。shared practice
profileにactive matterを書かない。matter close時は、その`matterId`を参照
する全bindingをrevokedにする。

## Audit event

```yaml
tenantId: "[tenant id]"
practiceId: "[practice id]"
eventType: matter-binding-changed | matter-created | matter-closed
correlationId: "[correlation id]"
actorObjectId: "[object id]"
idempotencyKey: "[unique key]"
timestamp: "[ISO datetime]"
outcome: succeeded | failed | rejected | partial
itemIds:
  - "[SharePoint itemId]"
details:
  oldMatterId: "[id or null]"
  newMatterId: "[id or null]"
  oldSessionId: "[session id or null]"
  newSessionId: "[session id or null]"
  eTagBefore: "[eTag or null]"
  eTagAfter: "[eTag or null]"
  revocationReason: "[reason or null]"
```
