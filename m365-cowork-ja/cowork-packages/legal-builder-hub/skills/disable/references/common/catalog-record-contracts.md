> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Catalog record contracts

テナント管理型スキル カタログのrecordは、external textではなくschema-valid fieldで
構成する。Coworkはread、draft、restricted quarantine requestを行えるが、
catalog-writer権限を持たない。

## 共通envelope

```yaml
tenantId: "[tenant ID]"
practiceId: "[practice ID]"
recordType: "[builder-* canonical type]"
recordId: "[opaque ID]"
itemId: "[SharePoint/Dataverse row ID]"
eTag: "[current eTag or row version]"
version: 1
status: "[record-specific canonical status]"
createdAt: "[ISO-8601]"
createdBy: "[Entra object ID]"
updatedAt: "[ISO-8601]"
payload: {}
```

createでは`itemId`/`eTag`をclientが創作しない。gateway responseを保存する。
updateはexact ID/versionを要求する。raw sourceをpayloadへ無制限に埋め込まず、
SharePoint quarantine item IDとhashを参照する。

`status`は共通envelopeの唯一のlifecycle fieldである。payload内に
`policyStatus`、`trustStatus`、`requestState`、`findingStatus`、
`packageStatus`を重複させない。record typeごとのcanonical enumだけを使う。

## `builder-registry`

主なfield:

- `registryId`
- `canonicalUri`
- `registryType`
- `publisherId`
- `enabled`
- `allowedPathPrefixes`
- `sourceAuthType`
- `lastValidatedAt`
- `validationEvidenceId`
- `cursor`

envelope `status`: `proposed | approved | paused | denied`。

`sourceAuthType`は
`public | oauth-delegated | oauth-app-only | managed-identity |
tenant-managed | custom | unknown`。`cursor`はnon-empty string（最大2,048文字）または
`null`で、field自体は必須。`status: approved`では`sourceAuthType: unknown`を拒否する。

registry追加、resume、pause、削除はpolicy change requestであり、browser skillが直接
変更しない。redirect先、ownership transfer、repository renameは再審査する。

## `builder-publisher`

- `publisherId`
- `normalizedName`
- `verifiedIdentity`
- `approvedRegistryIds`
- `vendorStatus`
- `securityContact`
- `lastReviewedAt`

envelope `status`: `unverified | review-required | approved | denied`。

`approvedRegistryIds`と`securityContact`は常にfieldを持つ。前者は最大100件のunique
registry IDs、後者はexact Entra object IDまたは`null`。`status: approved`では
approved registryが1件以上、security contactがnon-nullでなければならない。

publisher自身のREADME、badge、verified claimをidentity evidenceにしない。GitHub
owner、vendor entity、signing identity、contracting entityが一致するか別々に確認する。

## `builder-license-policy`

- `policyId`
- `deploymentContext: personal | firm-internal | product-embedding | tenant-wide`
- `spdxId`
- `disposition: allow | review | deny`
- `conditions`
- `approvedBy`
- `effectiveFrom`
- `expiresAt`

envelope `status`: `draft | active | expired | superseded | denied`。

`approvedBy`はexact Entra object IDまたは`null`、`effectiveFrom`はISO-8601
date-timeまたは`null`で、両fieldを必須にする。`status: active`では双方non-null。

license textはstrict SPDX token extractionのdataであり、directiveとして解釈しない。
metadata、LICENSE file、package noticeが不一致なら`review`または`deny`。license
policyはsource trustと別gateである。

## `builder-connector-policy`

- `connectorPolicyId`
- `connectorId`
- `canonicalHost`
- `transport`
- `disposition`
- `allowedToolNames`
- `deniedToolNames`
- `authModel`
- `dataClasses`
- `destinationPolicy`
- `lastLiveValidatedAt`

envelope `status`: `draft | active | expired | superseded | denied`。

`authModel`:
`none | oauth-delegated | oauth-app-only | api-key | managed-identity |
custom | unknown`。`dataClasses`は1～20件のunique canonical values:
`public | internal | confidential | privileged | personal-data | client-data |
source-code | credentials`。

`destinationPolicy`:

```yaml
allowedDestinationIds:
  - "[destination ID]"
externalSharingAllowed: false
retentionPolicyId: "[policy ID]"
dlpPolicyId: "[policy ID]"
```

各fieldとnon-empty destinationを必須にする。`status: active`では
`authModel: unknown`を拒否する。

`connected`はlive probe成功時だけ。write/destructive tool、OAuth scope、operator、
retention、DLP、service-principal supportを個別審査する。

## `builder-candidate`

```yaml
candidateId: "[opaque ID]"
requestedSkillId: "[ASCII kebab-case]"
registryId: "[approved registry ID]"
publisherId: "[publisher ID]"
sourceUriCanonical: "https://..."
requestedRevision: "[commit SHA or immutable revision]"
requesterObjectId: "[Entra object ID]"
correlationId: "[correlation ID]"
```

envelope `status`:
`draft | submitted | source-policy-check | rejected-source-policy |
quarantine-authorized | fetching | quarantined | deterministic-scan |
refused-malicious | raw-review-pending | raw-review-attested | qa-pending |
qa-complete | eligible | remediation-required | refused | expired | superseded`。

`rejected-source-policy`ではnetwork fetchしない。`quarantine-authorized`はrestricted
quarantine createだけを許可し、catalog/package/assignment mutationを許可しない。

## `builder-snapshot`

```yaml
snapshotId: "[opaque ID]"
candidateId: "[candidate ID]"
sourceRevision: "[commit SHA or immutable revision]"
capturedAt: "[ISO-8601]"
fileCount: 0
byteLength: 0
snapshotSha256: "[64 lowercase hex]"
fileInventoryItemId: "[exact item ID]"
malwareScanStatus: not-run | pending | passed | failed | unavailable
contentScanStatus: not-run | pending | passed | failed | unavailable
signatureStatus: not-present | unverified | verified | invalid
signatureEvidenceId: "[ID or null]"
rawReviewStatus: pending | attested | rejected
qaStatus: pending | complete | refused
licenseSpdx: "[SPDX or none or unknown]"
licenseMatch: match | mismatch | absent | unknown
```

envelope `status`:
`capturing | quarantined | scan-pending | review-pending | qa-pending |
eligible | remediation-required | refused | expired | superseded`。

file inventoryはrelative path、media type、byte length、file SHA-256を全件保持する。
symlink、path traversal、device file、executable、encrypted archive、oversized file、
hidden Unicodeを拒否または隔離する。`signatureStatus: verified`はapproved verifierの
evidenceがある場合だけ。

## `builder-scan-finding`

- `findingId`
- `snapshotId`
- `category`
- `severity: blocking | high | medium | low`
- `relativePath`
- `lineStart`, `lineEnd`
- `excerptHash`
- `boundedExcerpt`（最大500文字、secret除外）
- `detectorId`, `detectorVersion`

envelope `status`: `open | confirmed | false-positive | remediated`。

raw source全文をDataverse、flow log、notificationへ複製しない。

## `builder-qa-review`

- `qaReviewId`
- `snapshotId`
- `frameworkVersion`
- `verdict: READY | SOME CONCERN | MATERIAL CONCERNS | REFUSE`
- `coverage`
- `dependencyMap`:
  `upstream`, `downstream`, `automaticTriggers`, `breakageRisks`,
  `coverageComplete`, `missingArtifacts`
- `legalFailureModes`:
  `legalAdviceVsSupport`, `privilegeConfidentiality`, `accountabilityGap`
- `reviewerObjectId`
- `reportItemId`
- `completedAt`

envelope `status`: `draft | complete | superseded`。
failure mode statusは
`addressed | partially-addressed | not-addressed | not-applicable`。

`REFUSE`から`eligible`へ遷移しない。QAは法的正確性、security audit、tenant approval、
deployment clearanceではない。

## `builder-package`

```yaml
packageId: "[opaque ID]"
appId: "[Unified App app ID]"
skillIds:
  - "[ASCII skill ID]"
catalogVersion: "[immutable managed version]"
sourceSnapshotId: "[snapshot ID]"
packageSha256: "[64 lowercase hex]"
manifestVersion: "1.28"
licenseSpdx: "Apache-2.0"
signatureStatus: not-present | unverified | verified | invalid
approvalId: "[approval ID]"
protectionClass: community | first-party-protected | vendor-blocked
supersedesPackageId: "[package ID or null]"
```

envelope `status`:
`proposed | approved | active | disabled | superseded | retired | blocked`。

prior approved contentへのrollbackは既存packageを巻き戻すのではなく、prior snapshotを
sourceに新しいmanaged versionとfresh approvalを作る。

## `builder-protected-asset`

- `assetType: app | package | plugin | skill | publisher`
- `assetId`
- `sourcePlugin`
- `protectionClass: first-party-protected | vendor-blocked`
- `solutionManaged`
- `editableByRequestFlow: false`
- `reason`

envelope `status`: `active | retired`。

12 first-party source pluginsとhub自身はdisable、uninstall、unauthorized updateの対象外。
CoCounsel / Thomson Reutersはvendor approval確認まで`vendor-blocked`であり、
generic fallbackを同一IDへ登録しない。

## Catalog writer gate

catalog writeは次が揃った別operationだけ。

1. exact eligible snapshot/package
2. raw review attestation
3. QA resultと全open finding
4. source/publisher/license/connector policy
5. signature/security/privacy/tool-scope evidence
6. fresh approval binding
7. first-party/vendor blocker check
8. deployment/rollback plan
9. writer identityとappend-only audit

Cowork skill、requester、reviewer、approverはcatalog writerではない。
