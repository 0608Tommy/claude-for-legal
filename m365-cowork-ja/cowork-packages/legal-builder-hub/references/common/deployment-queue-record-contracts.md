> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Deployment queue record contracts

queueはtenant appまたはcatalogを実行するAPIではない。承認済みoperationを人の
deployment operatorへ渡し、exact execution/read-back evidenceを追跡するrecordである。

## Canonical operations

`install | update | disable | enable | remove | registry-add |
registry-pause | policy-change | package-approve`

user-facing `uninstall`は`remove`。rollbackは
`operation: update`, `target.updateMode: rollback`。

## Queue envelope

```yaml
requestId: "[opaque ID]"
tenantId: "[exact Entra tenant ID]"
practiceId: "[practice ID]"
operation: "[canonical operation]"
state: draft | submitted | preflight | awaiting-approval | approved | admin-action-required | executing | succeeded | failed | retry | dead-letter | cancelled | rejected | expired | superseded
requesterObjectId: "[exact Entra object ID]"
reviewerObjectIds: []
approverObjectIds: []
deploymentOperatorObjectId: null
target: {}
audience: {}
rollbackScope: {}
approvalId: null
targetBindingSha256: "[target canonical hash]"
audienceBindingSha256: "[audience canonical hash]"
idempotencyKey: "[16-256 characters]"
itemId: "[row ID]"
eTag: "[row version]"
adminEvidence: []
immutableEvidenceLog: true
executionReadBackMatch: false
createdAt: "[ISO-8601]"
updatedAt: "[ISO-8601]"
```

manual draftでは`itemId`、`eTag`、`approvalId`を創作しない。

## Operation-specific targets

### `install`

target:

- `kind: package-install`
- app/package/skill IDs
- source snapshot ID/hash
- target package hash/version
- target catalog ID
- `intendedStatus: active`

audienceはnon-empty exact Entra group IDsとdestination IDs。
rollback scopeはprior packageがあればそのID/hash/version、なければnullを明示し、
group、destination、owner、evidence、restore modeを必須にする。

### `update`

target:

- `kind: package-update`
- app/package/skill IDs
- source snapshot ID/hash
- current/target package hash
- full diff hash
- current/target version
- `updateMode: forward | rollback`
- target catalog ID、`intendedStatus: active`

`updateMode: rollback`ではrollback source package ID/hash/versionが必須。
rollback scopeはprior approved package、group、destination、owner、evidenceへ束縛する。

### `disable`

`kind: package-disable`、current package/hash/version、catalog ID、
`intendedStatus: disabled`。audienceとre-enable rollback scopeを必須にする。

### `enable`

`kind: package-enable`、current package/hash/version、catalog ID、
`intendedStatus: active`。audienceとdisable-state rollback scopeを必須にする。

### `remove`

`kind: package-remove`、current package/hash/version、catalog ID、
`intendedStatus: removed`、non-empty
`removalScope: assignment | availability | related-flow`。

配布解除とdata/config/audit/source deletionを分離する。rollback scopeにはreinstall用
prior approved package、group、destination、ownerを保持する。

### `registry-add`

target:

- `kind: registry-add`
- registry ID、canonical registry URI、publisher ID
- `currentPolicySha256: null`
- target policy hash、policy diff hash
- `intendedStatus: approved`

audienceはexact tenantとnon-empty destination IDs。rollback scopeはregistry remove
candidate、URI、publisher、destination、ownerへ束縛する。

### `registry-pause`

target:

- `kind: registry-pause`
- registry ID、canonical URI、publisher ID
- current/target policy hash、policy diff hash
- `intendedStatus: paused`

rollback scopeはprior approved policy/statusへ束縛する。

### `policy-change`

target:

- `kind: policy-change`
- policy ID/type
- current/target policy hash、policy diff hash
- `intendedStatus: active`

audienceはnon-empty affected group IDsとdestination IDs。rollback scopeはprior policy
hash、target policy hash、affected groups、destination、owner、evidence。

### `package-approve`

exact package/snapshot/hash/version、catalog ID、planned groups/destinationsと
install rollback scopeを要求する。

## State gates

```text
draft → submitted → preflight → awaiting-approval
→ approved → admin-action-required → executing → succeeded
                                ↘ failed → retry | dead-letter
```

`approved`以降:

- non-empty reviewer/approver exact Entra IDs
- approval ID
- requester/reviewer/approver/deployer separation evidence

`executing`以降:

- exact deployment operator Entra ID

`succeeded`:

- non-empty reviewer/approver/operator IDs
- operation-specific non-empty target/audience/rollback scope
- immutable successful `execution` evidence
- immutable successful `read-back` evidence
- both evidence records match request ID、operation、target binding hash、
  audience binding hash、operator
- `executionReadBackMatch: true`

gatewayはschema validation後にcross-record equalityとactor cross-set distinctnessを
検証する。不一致なら`succeeded`を拒否する。

## Actor separation

requester、全reviewer、全approver、deployment operatorはexact Entra IDかつ相互に
distinct。array内uniqueだけでなくcross-set比較を必須にする。

```yaml
actorSeparation:
  requesterObjectId: "[ID]"
  reviewerObjectIds: ["[ID]"]
  approverObjectIds: ["[ID]"]
  deploymentOperatorObjectId: "[ID]"
  distinctActorIds: ["[all IDs once]"]
  allActorIdsDistinct: true
  verificationEvidenceId: "[ID]"
  verifiedAt: "[ISO-8601]"
```

## Immutable admin evidence

```yaml
evidenceId: "[immutable ID]"
evidenceType: execution | read-back
requestId: "[same request ID]"
operation: "[same canonical operation]"
operatorObjectId: "[same deployment operator]"
performedAt: "[ISO-8601]"
adminSurface: "[tenant-validated current surface]"
targetBindingSha256: "[same target hash]"
audienceBindingSha256: "[same audience hash]"
before: {}
after: {}
returnedOperationId: "[ID or null]"
result: succeeded | failed | partial
immutable: true
evidenceSha256: "[event hash]"
previousEvidenceSha256: "[prior hash or null]"
```

execution evidenceだけ、screenshotだけ、read-backだけでは`succeeded`にしない。
before/afterはoperation-specific schemaを使う。

### Package state

`install`, `update`, `disable`, `enable`, `remove`, `package-approve`:

```yaml
stateType: package
appId: "[exact app ID]"
packageId: "[exact package ID]"
catalogId: "[exact catalog ID]"
packageSha256: "[hash or null only when absent]"
version: "[version or null only when absent]"
status: absent | proposed | approved | active | disabled | removed
assignmentIds:
  - "[assignment ID]"
```

operationごとにbefore/after statusを固定する:

- install: `absent → active`
- update: `active|disabled → active`
- disable: `active → disabled`
- enable: `disabled → active`
- remove: `active|disabled → removed`
- package-approve: `proposed → approved`

### Registry state

`registry-add`, `registry-pause`:

```yaml
stateType: registry
registryId: "[exact registry ID]"
registryUri: "https://..."
publisherId: "[exact publisher ID]"
status: absent | approved | paused | denied
policySha256: "[hash or null only when absent]"
```

- registry-add: `absent/null → approved/target policy hash`
- registry-pause: `approved/current policy hash → paused/target policy hash`

package-only stateはregistry evidenceとしてschema invalid。

### Policy state

`policy-change`:

```yaml
stateType: policy
policyId: "[exact policy ID]"
policyType: registry | publisher | license | connector | qa | security | privacy | retention | dlp | deployment
status: draft | active | expired | superseded | denied
policySha256: "[exact policy hash]"
```

beforeは`draft|active` current hash、afterは`active` target hash。package-only stateは
policy evidenceとしてschema invalid。

gatewayはevidenceのregistry/package/policy IDs、URI、publisher、status、hashをqueue
targetのexact valueと比較する。不一致なら`executionReadBackMatch`をtrueにしない。

## Mandatory remediation / refusal

confirmed prompt overrideまたはruntime secret/credential requestがあるsnapshotは、
`SOME CONCERN`のrisk acceptanceでqueueへ入れない。

- removable design defect: remediation-required
- override、secret capture/use/store/transmit、credential theft/exfiltration:
  `REFUSE`

修正後のnew snapshot/hash/approvalだけをqueueへ送る。

## Retry and dead-letter

- 同じidempotency keyは同じlogical result
- retry前にcurrent state/evidenceを再取得
- succeeded operationを再実行しない
- partialはgroup/itemごとに記録
- dead-letterはrequest/correlation/stage/error/retry countだけ
- raw source、package、secret、client dataをdead-letterへ入れない

request、approval、transition、evidence、read-back、errorはappend-only。
queue recordの存在はdeployment、signing、scan、rollback実行の証拠ではない。
