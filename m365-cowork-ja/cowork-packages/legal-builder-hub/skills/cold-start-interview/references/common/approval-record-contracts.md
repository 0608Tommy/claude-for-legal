> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Approval record contracts

承認は一般的な「よさそう」ではない。exact operation、artifact、audience、target、
hash、diff、destination、expiryへ束縛されたimmutable decision setである。

## Canonical operations

`install | update | disable | enable | remove | registry-add |
registry-pause | policy-change | package-approve`

user-facing `uninstall`はbackend `remove`へ変換する。user-facing rollbackは
`operation: update`, `updateMode: rollback`で表す。

## Approval request

```yaml
approvalRequestId: "[opaque ID]"
tenantId: "[exact Entra tenant ID]"
practiceId: "[practice ID]"
requestId: "[queue/policy request ID]"
operation: "[canonical operation]"
requesterObjectId: "[exact Entra object ID]"
reviewerObjectIds:
  - "[exact Entra object ID]"
approverObjectIds:
  - "[exact Entra object ID]"
deploymentOperatorObjectId: "[exact Entra object ID]"
submittedAt: "[ISO-8601]"
expiresAt: "[ISO-8601]"
binding:
  artifact: {}
  audience:
    tenantId: "[exact Entra tenant ID]"
    targetGroupIds:
      - "[exact Entra group ID]"
    destinationIds:
      - "[catalog/admin destination ID]"
  target: {}
  dependencySnapshotSha256: "[hash]"
  bindingSha256: "[canonical artifact+audience+target hash]"
evidence:
  provenanceReviewId: "[ID]"
  rawReviewAttestationId: "[ID]"
  qaReviewId: "[ID]"
  licenseReviewId: "[ID]"
  signatureEvidenceId: "[ID or null]"
  securityReviewId: "[ID]"
  privacyReviewId: "[ID]"
  toolScopeReviewId: "[ID]"
  rollbackPlanId: "[ID]"
requiredReviewerRoles:
  - catalog-reviewer
  - security-reviewer
  - privacy-reviewer
  - legal-reviewer
  - policy-approver
decisions: []
immutableDecisionLog: true
state: draft | submitted | awaiting-review | awaiting-approval | approved | rejected | expired | cancelled | superseded
```

empty artifact/audience/targetは承認対象にならない。binding、evidence、actor setの
どれかが変われば新しいapproval requestを作る。

## Operation-specific binding

### `install`

- artifact:
  app/package/skill/candidate/snapshot/source revision、snapshot/package hash、
  target version
- audience:
  non-empty exact target group IDsとdestination IDs
- target:
  exact tenant catalog ID、`intendedStatus: active`

### `update`

- artifact:
  current/target package hash、full diff hash、current/target version、
  snapshot/source、`updateMode: forward | rollback`
- audience:
  non-empty exact target group IDsとdestination IDs
- target:
  exact tenant catalog ID、`intendedStatus: active`

`updateMode: rollback`ではrollback source package ID/hash/versionを必須にする。
rollbackもprior approved contentからnew managed versionを作るupdateである。

### `disable`, `enable`, `remove`

- artifact:
  exact current app/package/skills/hash/version
- audience:
  non-empty affected group IDsとadmin destination IDs
- target:
  exact catalog IDとそれぞれ
  `disabled | active | removed`

### `registry-add`

- artifact:
  registry ID、canonical registry URI、publisher ID、
  `currentPolicySha256: null`、target policy hash、policy diff hash
- audience:
  exact tenantとnon-empty destination IDs
- target:
 同じregistry ID/URI/publisher、`intendedStatus: approved`

### `registry-pause`

- artifact:
  registry ID、canonical URI、publisher ID、current/target policy hash、diff hash
- audience:
  exact tenantとnon-empty destination IDs
- target:
 同じregistry ID/URI/publisher、`intendedStatus: paused`

### `policy-change`

- artifact:
  policy ID/type、current/target policy hash、policy diff hash
- audience:
  non-empty affected group IDsとdestination IDs
- target:
  exact policy ID、`intendedStatus: active`

### `package-approve`

exact package/snapshot/hash/version、planned group IDs、catalog destinationへ束縛する。

## Exact actor identities

`approved`前に次が必須。

- requester、reviewer、approver、deployment operatorはexact Entra object ID
- reviewer/approver arraysはnon-empty、各array内unique
- requester、reviewer、approver、deployment operatorの全IDはcross-setでもdistinct
- current group membershipとrole assignmentのevidence
- `actorSeparation.allActorIdsDistinct: true`
- `distinctActorIds`、全`decisionActorIds`、verification evidence、verified time
- `allDecisionActorsIncluded: true`
- `selfApprovalAbsent: true`
- `roleMembershipValidated: true`

JSON Schemaはcross-field equalityを完全には比較できないため、gatewayはschema
validation後に全actor setと全decision actorを比較し、重複、self-approval、
role membership不一致が1件でもあれば`approved`を拒否する。

## Required role decisions

`approved`には5 roleすべてのimmutable `approve` decisionが必要。

```yaml
approvalRequestId: "[same approval request ID]"
decisionId: "[immutable ID]"
actorObjectId: "[exact Entra object ID]"
reviewerRole: catalog-reviewer | security-reviewer | privacy-reviewer | legal-reviewer | policy-approver
decision: approve | reject | request-changes | abstain
decidedAt: "[ISO-8601]"
bindingSha256: "[same current binding hash]"
reasonCode: "[canonical code]"
boundedReason: "[secretを含まない]"
evidenceIds:
  - "[review evidence ID]"
actorMembership:
  actorSet: reviewerObjectIds | approverObjectIds
  membershipEvidenceId: "[membership evidence ID]"
  membershipVerified: true
  selfApprovalChecked: true
  roleValidationChecked: true
immutable: true
decisionSha256: "[event hash]"
previousDecisionSha256: "[prior event hash or null]"
```

gatewayは各decisionの`approvalRequestId`と`bindingSha256`がparent recordに一致するか
確認する。`catalog-reviewer`, `security-reviewer`, `privacy-reviewer`,
`legal-reviewer`の`actorObjectId`はparent `reviewerObjectIds`に含まれ、
`policy-approver`はparent `approverObjectIds`に含まれなければならない。
全decision actorを`actorSeparation.decisionActorIds`とdistinct/self-approval checkへ
含める。approved stateにはreject/request-changesを含めない。

decisionはupdate/deleteしない。訂正はnew immutable superseding event。

## Mandatory remediation / refusal

confirmed prompt overrideまたはruntimeでsecret/credentialを要求するbehaviorは
`SOME CONCERN`のrisk acceptance対象外。

- intent/影響が限定され、除去可能: `MATERIAL CONCERNS`、mandatory remediation
- guardrail override、secret取得/use/store/transmit、credential theft/exfiltration:
  `REFUSE`

修正後はnew snapshot/hash/QA/approvalを要求する。exception approvalで元snapshotを
通さない。

## Freshness and invalidation

次が変われば承認失効:

- source、snapshot、package、signature、license
- security/privacy/tool scope、hook、connector、network/write path
- current/target version、full diff
- target group、destination、tenant、operation
- dependency set、rollback scope
- actor IDs、role membership、evidence
- expiry

承認直前と管理者実行直前にbinding/hashを再計算する。

## Approval output

- approval request ID
- operation-specific artifact/audience/target
- binding hash
- required/received role decisions
- actor separation result
- expiry、open remediation
- next state。通常`admin-action-required`

「approved」は「deployed」「active」「published」「signed」「scanned」を意味しない。
