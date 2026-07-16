> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Product legal matter records

## Matter

```yaml
recordType: matter-profile
tenantId: "[tenant id]"
practiceId: "[practice id]"
pluginId: product-legal
matterId: "[server-generated ID]"
slug: "acme-japan-launch-2026"
title: "[pseudonymous title]"
representedOrganization: "[name]"
counterparties:
  - "[name]"
matterType: launch
opened: "2026-07-16"
status: active
confidentiality: restricted
jurisdictions:
  - ja-JP
authorizedViewers:
  - "[Microsoft Entra user/group ID]"
keyFacts: "[2–5 sentences]"
launchDate: "[date or null]"
listedOrReportingStatus: "[status]"
mnpi: false
overrides:
  - "[matter-specific framework/calibration position]"
relatedMatters:
  - matterId: "[ID]"
    reason: "[reason]"
retentionPolicy: "[policy ID]"
dlpPolicy: "[policy ID]"
legalHold: false
crossMatterAllowed: false
```

## Binding

次は`session-binding.schema.json`に適合する**domain payloadだけ**である。
gatewayの`scopeType: session`、`scopeId: [userObjectId]:[sessionId]`、
`recordType: session-matter-binding`、`recordId: active-matter`と
create/update/envelopeは
[保存契約](common/cowork-runtime-contract.md)を使う。

```yaml
tenantId: "[tenant id]"
practiceId: "[practice id]"
userObjectId: "[Microsoft Entra object ID]"
sessionId: "[Cowork session ID]"
matterId: "[non-null matter ID]"
status: active | revoked
boundAt: "[ISO-8601]"
boundBy: "[Microsoft Entra object ID]"
expiresAt: "[ISO-8601]"
revokedAt: "[ISO-8601 or null]"
revokedBy: "[Microsoft Entra object ID or null]"
revocationReason: "[reason or null]"
```

`status != active`、`expiresAt <= now`、matter archived、access deniedならbindingを
拒否する。practice modeはbinding recordを作らない。

## Audit event examples

canonical envelopeの`eventType`:

- `matter-opened`
- `matter-binding-revoked`
- `matter-binding-created`
- `matter-closed`
- `matter-binding-revocation-partial`

detailsにはold/new matter/session、source eTag、minimal reasonだけを入れ、PRD、
claim、personal data、MNPI全文を複製しない。
