---
name: matter-workspace
description: >
  IP matterを`new`、`list`、`switch`、`close`、`none`の会話stateで管理するSharePoint/Power Platform front end。非null・期限付きserver binding、fresh-session switch/none、fence-first active-only revoke、conflict・clean-team・未公開発明の分離を強制する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: ip-legal
  migration-target: power-platform
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Matter workspace

正規label:

- `/ip-legal:matter-workspace new <slug>`
- `/ip-legal:matter-workspace list`
- `/ip-legal:matter-workspace switch <slug>`
- `/ip-legal:matter-workspace close <slug>`
- `/ip-legal:matter-workspace none`

## Mandatory isolation/security gate

1. [保存契約](references/common/cowork-runtime-contract.md)を読み、tenant-approved
   gateway、SharePoint matters/state/audit、ACL、conditional create/updateを
   live preflight。失敗時はread-only list/intake draftだけ。
2. exact current `user-profile`を
   `tenantId + practiceId + userObjectId`で読みます。
3. general workspaceがoffならexpected stateとして説明し、private-practice/
   multi-clientで必要ならadmin setupへroute。
4. active sourceは
   `tenantId + practiceId + userObjectId + sessionId`
   のserver bindingだけ。display name、slug、conversation memoryから推測しません。
5. substantive workにはbinding `status: active`、`expiresAt > now`、non-null
   `matterId`、matter `status: active`、current user accessが必要。
6. practice modeはfresh sessionでbinding不在。`matterId: null` active bindingを
   作りません。
7. conflict/engagement/authority、viewer、retention、legal hold、DLPを人が確認。
8. `new`、`switch`、`close`、`none`は別operation、exact diff、fresh confirmation。
9. `switch`/`none`はnew session。`close`はmatterを先にfenceし、全bindingを
   enumerateしてactiveだけをrevoke。already-revokedはsatisfiedとし、
   zero active後だけarchivedへfinalize。
10. Cowork内DLP必須ならtrade secret/未公開発明matterのproduction利用を停止。

[matter record](references/matter-records.md)、
[日本の秘密性](references/common/ja-jp/privilege-security.md)を使います。

## Conversation state

| state | action |
|---|---|
| `new <slug>` | intake後にSharePoint matterをconditional create |
| `list` | authorized active/archived mattersをscope cursorで表示 |
| `switch <slug>` | current binding revoke後、新sessionでnew binding |
| `close <slug>` | fence → enumerate → active-only revoke → zero active確認 → archived finalize |
| `none` | current binding revoke後、新sessionでbindingなし |

## `new`

slugはlowercase alphanumeric + hyphen。active/archivedの重複をgateway unique
constraintでfail closedし、unauthorized matterの存在を漏らしません。

intake:

- represented organization/client
- counterparty/other interested party
- type:
  `trademark-clearance | trademark-enforcement | copyright-platform |
  patent-fto | patent-infringement | invention | design | trade-secret |
  ip-transaction | oss | portfolio | other`
- confidentiality:
  `standard | heightened | restricted | clean-team`
- pseudonymous code
- key facts
- jurisdictions
- authorized viewers/groups
- outside counsel/patent attorney
- invention-security/export restriction
- retention/legal hold/storage-flow DLP
- related exact matter IDs

full key、`expectedAbsent: true`、unique `idempotencyKey`でcreateします。自動switch
しません。

## `list`

- current user authorized matterだけ
- active/archivedを別表
- active markerはserver binding
- pseudonymous code、type、confidentiality、jurisdiction、status、updated
- scope-specific cursor

unauthorized matterは存在も表示しません。10件超ならdashboardを提案します。

## `switch`

1. exact target、latest `eTag`、status/access/retention/legal hold。
2. current bindingをexact keyで再取得。
3. old→new、discarded context、新session requirementを表示。
4. fresh confirmation。
5. current bindingがある場合だけconditional revokeしてcurrent sessionを停止。
6. new Cowork conversationでnew bindingをconditional create。exact matter
   `itemId`、latest `eTag` / `version`またはbinding-generation token、
   expected active statusをbinding absenceと同一transactionで評価。
7. old/new matter/session、actor、outcomeをaudit。

verified hard context resetなしにsame-session switchを許可しません。

## `close`

1. exact active matter、latest `eTag` / `version`、current binding generation。
2. open deadline、C&D/takedown draft、Customs/platform route、filing/renewal、
   shared link、legal hold、retentionを確認。
3. close date/reason/approver/fence/impactとfresh confirmation。
4. 最初のatomic conditional operationでmatterを`close-pending`等のnon-active
   stateへtransitionし、new binding createをfence。
5. fence成功後、targetを参照する全bindingをexact query。
6. activeだけをrevocation対象とし、already-revokedはsatisfiedとして再更新しない。
7. active bindingだけをexact item/eTagで`revoked`へconditional updateし、
   each outcomeをcanonical auditへappend。
8. 全bindingを再照合し、zero activeを確認。
9. zero active確認後だけpost-fence matterを`archived`へconditional finalize。
10. fence前にcommitしたcreateはstep 5で捕捉され、fence後のcreateはmatter
    preconditionで失敗。途中失敗はfenced stateを維持してfail closed。

deleteはscope外です。

## `none`

current bindingを表示し、confirmation後にrevokeしてcurrent sessionを停止します。
new conversationのfresh sessionにはbindingを作りません。

## Cross-matter

default`false`。explicit comparative request、exact matter IDs、permission、purpose、
confidentialityを確認します。clean-team、unpublished invention、trade secret、
different clients、provider/court restrictionがあれば拒否します。

## 行わないこと

- local folder create/move/archive
- same-session switch/none
- null-matter active binding
- close時current bindingだけrevoke
- archive-first / revoke-every close
- conflict clearance/engagement/retention delete
- substantive reviewの自動開始
- Power Platform solution/scheduleが存在すると主張
