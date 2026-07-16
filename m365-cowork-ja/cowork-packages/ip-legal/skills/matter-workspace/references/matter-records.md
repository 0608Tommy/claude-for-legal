> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# IP matter record

## Matter

```yaml
tenantId: "[tenant id]"
practiceId: "[practice id]"
scopeType: matter
scopeId: "[matter ID]"
recordType: matter-profile
recordId: "matter:[matterId]"
payload:
  matterId: "[immutable matter ID]"
  slug: "[lowercase-hyphen slug]"
  pseudonymousCode: "[code]"
  representedParty: "[authorized value]"
  counterparty: "[authorized value or unknown]"
  matterType: trademark-clearance | trademark-enforcement | copyright-platform | patent-fto | patent-infringement | invention | design | trade-secret | ip-transaction | oss | portfolio | other
  confidentiality: standard | heightened | restricted | clean-team
  jurisdictions:
    - "[jurisdiction]"
  status: active | archived
  authorizedViewerObjectIds:
    - "[Entra object/group ID]"
  outsideCounsel: "[authorized record ID or null]"
  economicSecurityScreen: required | cleared | not-applicable | pending
  retentionClass: "[class]"
  legalHold: true | false
  openedAt: "[ISO-8601]"
  archivedAt: "[ISO-8601 or null]"
itemId: "[SharePoint item ID]"
eTag: "[eTag]"
version: 1
updatedAt: "[ISO-8601]"
```

record ID、slug、central indexへ発明title、trade-secret description、allegation、
claim strategyを入れません。restricted factsとdocumentsはitem-level ACL付きmatter
内に置きます。

## Create

`expectedAbsent: true`とunique `idempotencyKey`を使います。create後に自動binding
しません。

## Archive

matter profileをconditional updateし、対象matterを参照する全session bindingを
itemごとにrevokeします。partial failureは`outcome: partial`でauditし、accessを
blockします。
