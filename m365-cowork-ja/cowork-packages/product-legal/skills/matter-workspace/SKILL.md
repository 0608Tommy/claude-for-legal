---
name: matter-workspace
description: >
  Product legal matterをnew、list、switch、close、noneの会話stateで管理するSharePoint/Power Platform front end。非null・期限付きserver binding、fresh-session practice/switch/none、fence-first active-only revoke、confidentiality、MNPI、cross-matter isolationを強制する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: product-legal
  migration-target: power-platform
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Matter workspace

正規label:

- `/product-legal:matter-workspace new <slug>`
- `/product-legal:matter-workspace list`
- `/product-legal:matter-workspace switch <slug>`
- `/product-legal:matter-workspace close <slug>`
- `/product-legal:matter-workspace none`

本skillはSharePoint / Power Platform stateのconversation front endであり、
managed solution、agent、schedule、flowを含まない。

## Mandatory isolation/security gate

1. [保存契約](references/common/cowork-runtime-contract.md)を読み、tenant-approved
   gateway、SharePoint matters/state/audit、ACL、conditional create/updateをlive
   preflightする。失敗時はauthorized list/intakeのread-only/manual draftだけ。
2. exact current `user-profile`を
   `tenantId + practiceId + userObjectId`で読む。
3. workspaceがoffならexpected stateとして説明し、in-house practice modeを使う。
   multi-clientで必要ならadmin setupへrouteする。
4. active matterの唯一のsourceは
   `tenantId + practiceId + userObjectId + sessionId`
   のserver binding。display name、slug、conversation memoryから推測しない。
5. substantive workにはbinding `status: active`、`expiresAt > now`、non-null
   `matterId`、matter `status: active`、current user accessが必要。
6. practice modeはfresh sessionでbinding不在。
   `matterId: null` active bindingを作らない。
7. conflict/engagement/authority、viewer、retention、legal hold、storage/flow DLP、
   clean-team、MNPIを人が確認する。
8. `new`、`switch`、`close`、`none`は別operation、exact diff、fresh human
   confirmation。
9. `switch`/`none`はnew session。`close`はmatterを先にfenceし、全bindingを
   enumerateしてactiveだけをrevoke。already-revokedはsatisfiedとし、
   zero active後だけarchivedへfinalize。
10. Cowork内DLPがmandatoryなら機密launch/MNPI matterのproduction利用を停止。

[matter record](references/matter-records.md)と
[Power Platform contract](references/automation-contract.md)を使う。

## Conversation state

| state | action |
|---|---|
| `new <slug>` | intake後にSharePoint matterをconditional create |
| `list` | authorized active/archived mattersをscope cursorで表示 |
| `switch <slug>` | current binding revoke後、新sessionでnew binding |
| `close <slug>` | fence → enumerate → active-only revoke → zero active確認 → archived finalize |
| `none` | current binding revoke後、新sessionでbindingなし |

intent不明なら5つを提示する。sourceのfilesystem operationへ変換しない。

## `new`

slugはlowercase alphanumeric + hyphen。active/archivedの重複をgateway unique
constraintでfail closedし、unauthorized matterの存在を漏らさない。

intake:

- represented organization/client
- counterparty/partner/vendor
- type:
  `launch | feature-review | marketing-claims | risk-deep-dive |
  product-area | incident | regulator-inquiry | other`
- confidentiality:
  `standard | heightened | restricted | clean-team`
- pseudonymous code/title
- key facts and launch date
- jurisdictions、seller/operator、affected users
- public/listed/MNPI status
- authorized viewers/groups
- human owners/attorney route
- retention/legal hold/storage-flow DLP
- related exact matter IDs
- matter-specific calibration/framework override

full canonical key、`expectedAbsent: true`、unique `idempotencyKey`でcreateする。
workspace作成はconflict clearance、engagement acceptance、launch approvalではない。
自動switchしない。

## `list`

- current user authorized matterだけ
- active/archivedを別表
- active markerはserver binding
- pseudonymous code、type、confidentiality、jurisdiction、launch date、status、updated
- scope-specific cursor

unauthorized matterは存在も表示しない。10件超ならdashboardを提案できるが自動作成
しない。

## `switch`

1. exact target matter、latest `eTag`、status/access/retention/legal hold/DLP。
2. current bindingをexact keyで再取得。
3. old→new、discarded context、新session requirementを表示。
4. fresh human confirmation。
5. current bindingがある場合だけconditional revokeし、current sessionを停止。
6. new Cowork conversationでnew bindingをconditional create。exact matter
   `itemId`、latest `eTag` / `version`またはbinding-generation token、
   expected active statusをbinding absenceと同一transactionで評価。
7. old/new matter/session、actor、outcomeをcanonical auditへappend。

verified hard context resetなしにsame-session switchを許可しない。old matterの
document、quote、draft、source、cursorをcarryしない。

## `close`

1. exact active matter、latest `eTag` / `version`、current binding generation。
2. open launch condition、unsaved draft、claim evidence、incident、regulator/
   disclosure action、shared link、legal hold、retentionを確認。
3. close date、reason、human owner、fence、impact、fresh confirmation。
4. 最初のatomic conditional operationでmatterを`close-pending`等のnon-active
   stateへtransitionし、new binding createをfence。
5. fence成功後、target matterを参照する全bindingをexact query。
6. activeだけをrevocation対象とし、already-revokedはsatisfiedとして再更新しない。
7. active bindingだけをexact item/eTagで`revoked`へconditional updateし、
   each outcomeをcanonical auditへappend。
8. 全bindingを再照合し、zero activeを確認。
9. zero active確認後だけpost-fence matterを`archived`へconditional finalize。
10. fence前にcommitしたcreateはstep 5で捕捉され、fence後のcreateはmatter
    preconditionで失敗。途中失敗はfenced stateを維持してfail closed。

deleteはscope外。

## `none`

current bindingを表示し、confirmation後にrevokeしてcurrent sessionを停止する。
new conversationのfresh practice sessionにはbindingを作らない。

## Cross-matter

default`false`。explicit comparative request、exact matter IDs、permission、purpose、
confidentialityを確認する。different client、clean-team、MNPI、trade secret、
regulator restrictionがあれば拒否する。

## Complete

changed matter ID、binding、status、itemId/eTag、destination、unresolved
conflict/retention/DLPを示す。substantive reviewを自動開始しない。

## 行わないこと

- local folder create/move/archive
- same-session switch/none
- null-matter active binding
- close時current bindingだけrevoke
- archive-first / revoke-every close
- conflict clearance/engagement/retention delete
- Power Platform solution/flow/scheduleが存在すると主張
- send、post、publish、approve、clear
