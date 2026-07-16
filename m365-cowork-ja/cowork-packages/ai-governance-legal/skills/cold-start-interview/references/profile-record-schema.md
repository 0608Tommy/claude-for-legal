> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 実務プロファイル・レコード構造

以下はpayload構造であり、write requestのconcurrency fieldではない。first-time
createのouter requestはcanonical key、`recordId`、`expectedAbsent: true`、
unique `idempotencyKey`を使い、`itemId` / `eTag`を含めない。既存recordのupdate
だけがexact `itemId` / latest `eTag`を使う。

```yaml
recordType: practice-profile
tenantId: "[tenant id]"
practiceId: "[practice id]"
pluginId: ai-governance-legal
locale: ja-JP
setupStatus: complete
companyProfileItemId: "[SharePoint itemId]"

integrations:
  sharepoint: connected
  onedrive: connected
  Slack: configured-unverified
  Google Drive: not-connected

aiActivitySummary: "[summary]"
jurisdictions:
  - ja-JP
jurisdictionModules:
  - ja-JP
japanLawReviewStatus: pending
primarySourcesCheckedThrough: "2026-07-16"

useCaseRegistry:
  - useCase: "[name]"
    classification: Conditional
    conditions:
      - "[condition]"
    neverReason: null

redLines:
  - "[red line and reason]"

governanceTiers:
  Standard:
    approvalPath: "[role]"
  Elevated:
    approvalPath: "[role]"
  High:
    approvalPath: "[role]"

aiaHouseStyle:
  trigger: "[trigger]"
  format: "[source or baseline]"
  depth: "[depth]"
  signOff: "[role]"
  sections:
    - "[section]"

vendorGovernance:
  dataUse:
    standard: "[position]"
    fallback: "[position]"
    never: "[position]"

policyCommitments:
  sourceItemId: "[itemId]"
  prohibitedUses:
    - "[item]"
  requiredSafeguards:
    - "[item]"

governanceTeam:
  vendorOwner: "[role]"
  aiRiskOwner: "[role]"
  escalation:
    - issue: "[issue]"
      escalateTo: "[role]"
      trigger: "[trigger]"

seedDocuments:
  - type: "AI policy"
    itemId: "[itemId]"
    version: "[version]"
    reviewedOn: "[date]"
    readCoverage: "[all/pages]"

outputs:
  libraryId: "${M365_OUTPUTS_LIBRARY_ID}"
  policyItemId: "[itemId]"
  namingConvention: "[pattern]"
  policySweepCursorRecordType: policy-sweep-cursor

matterWorkspaces:
  enabled: false
  crossMatterAccess: false
```

利用者固有の役割と弁護士連絡先は共有practice profileへ保存しない。

```yaml
recordType: user-profile
tenantId: "[tenant id]"
practiceId: "[practice id]"
userObjectId: "[Microsoft Entra object id]"
role: "Lawyer / legal professional"
attorneyContact: "[name/team/N/A]"
```

現在案件は共有profileの単一値にせず、セッション単位で拘束する。

```yaml
scopeType: session
scopeId: "[userObjectId]:[sessionId]"
recordType: session-matter-binding
recordId: active-matter
tenantId: "[tenant id]"
practiceId: "[practice id]"
userObjectId: "[Microsoft Entra object id]"
sessionId: "[Cowork session id]"
matterId: "[matter id]"
status: active | revoked
boundAt: "[ISO-8601]"
boundBy: "[Microsoft Entra object id]"
expiresAt: "[ISO-8601]"
revokedAt: "[ISO-8601 or null]"
revokedBy: "[Microsoft Entra object id or null]"
revocationReason: "[reason or null]"
```

outer `tenantId` / `practiceId`とpayloadはexact一致し、`scopeId`は
`userObjectId:sessionId`と一致する。createはactive、`revokedAt` /
`revokedBy` / `revocationReason`がすべてnullのrecordだけを
`expectedAbsent: true`で作る。binding createはtarget matterのexact `itemId`、
`expectedStatus: active`、latest `eTag` / `version`またはbinding-generation
tokenをmatter preconditionに含め、gatewayがbinding absenceと同一transactionで
評価する。作成後はtenant、practice、user、session、matter、boundAt、boundBy、
expiresAtを変更せず、current activeから`revokedAt`、`revokedBy`、nonblank
reasonを揃えたrevokedへの一方向遷移だけを許可する。

実装時の列・JSON schemaはテナント設計に合わせるが、意味、複合キー、
正規enumを変えない。
