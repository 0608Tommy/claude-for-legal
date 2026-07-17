---
name: matter-workspace
description: >
  employment matterをnew、list、switch、close、noneの会話stateで管理するSharePoint / Power Platform front end。一般workspaceがoffでもinvestigation、whistleblowing、medical、leave、discipline、contested terminationをrestricted isolationし、expiring bindingとfence-first active-only revokeを強制する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: employment-legal
  migration-target: power-platform
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Matter workspace

正規label:

- `/employment-legal:matter-workspace new <slug>`
- `/employment-legal:matter-workspace list`
- `/employment-legal:matter-workspace switch <slug>`
- `/employment-legal:matter-workspace close <slug>`
- `/employment-legal:matter-workspace none`

Coworkではsubcommandを会話stateとして扱います。

## Mandatory isolation / security gate

1. `references/common/cowork-runtime-contract.md`を読み、gateway、SharePoint
   matters/state/audit、ACL、conditional create/updateをlive preflight。失敗時は
   read-only list/intake draftだけです。
2. exact current`user-profile`を
   `tenantId + practiceId + userObjectId`で読みます。
3. general `matterWorkspaces.enabled: false`はexpected stateですが、
   `restrictedMatterIsolation`を妨げません。
4. sensitive type:
   `investigation | whistleblowing | medical-accommodation | leave |
   discipline | termination`
   はin-houseでもrestricted matterを作れます。
   `country-expansion`はrestrictedでなくてもpractice project matterとして作れます。
5. active sourceは
   `tenantId + practiceId + userObjectId + sessionId`
   のserver bindingだけ。会話名、display name、memoryから推測しません。
6. substantive workにはbinding `status: active`、`expiresAt > now`、matter
   `status: active`、current user accessが必要です。
7. practice modeはfresh sessionでbinding不在。`matterId: null` active bindingを
   作りません。
8. conflict/engagement/authority、viewer、retention、legal hold、DLPを人が確認。
9. new/switch/close/noneは別operation、exact diffとfresh confirmation。
10. closeはmatterを先にfenceし、全bindingを列挙してactiveだけをrevokeします。
    already-revokedはsatisfiedとし、zero active後だけarchivedへfinalizeします。
    switch/noneは新sessionを要求します。
11. Cowork内DLP必須ならconfidential matterを投入せずproduction停止です。

Japan privacyは
`references/common/ja-jp/privacy-privilege.md`、
recordは`references/matter-records.md`を使います。

## 会話state

| state | action |
|---|---|
| `new <slug>` | intake後、SharePoint mattersへconditional create |
| `list` | authorized active/archived matterをscope cursorで表示 |
| `switch <slug>` | current bindingをrevokeし、新sessionでnew binding |
| `close <slug>` | fence → enumerate → active-only revoke → zero active確認 → archived finalize |
| `none` | current bindingをrevokeし、新sessionでpractice mode |

## `new <slug>`

slugはlowercase alphanumeric + hyphen。active/archivedの重複をgateway unique
constraintでfail closedし、unauthorized matterの存在を漏らしません。

intake:

- represented organization/client
- matter type
- confidentiality:
  `standard | heightened | restricted | clean-team`
- pseudonymous code
- key facts（restricted record内、2～5文）
- jurisdictions/establishments
- authorized viewers/groups
- identity mapping location
- whistleblower identity separation
- retention/legal hold/export/storage-flow DLP
- related matter IDs

一般workspace offの場合、上記restricted typeと`country-expansion`だけを
許可します。source/contentをcentral indexへ複製しません。

`references/matter-records.md`のfull key、`expectedAbsent: true`、unique
`idempotencyKey`でcreateします。create後に自動switchしません。

## `list`

- current user authorized matterだけ
- active/archivedを別表
- active markerはserver binding
- pseudonymous code、type、confidentiality、jurisdiction、status、updated
- practice/user/query scope cursor
- unauthorized matterは存在も非表示

10件超ならdashboardを提案しますが自動生成しません。

## `switch <slug>`

1. exact target、latest `eTag`、active/access/retention/legal hold。
2. current bindingをexact keyで再取得。fresh practice sessionでbinding不在なら
   revocation対象なし。
3. old→new、破棄context、新session requirementを示す。
4. fresh confirmation。
5. current bindingがある場合だけconditional revokeし、current sessionで停止。
6. 新しいCowork conversationでnew session bindingをconditional create。exact
   matter `itemId`、latest `eTag` / `version`またはbinding-generation token、
   expected active statusをbinding absenceと同一transactionで評価します。
7. old/new matter/session、actor、outcomeをaudit。

verified hard context resetなしにsame-session switchを許可しません。

## `close <slug>`

1. exact active matter、latest `eTag` / `version`、current binding generation。
2. open investigation/leave/discipline/termination/expansion、deadline、draft、
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

retention expiry後のdeleteはscope外です。

## `none`

current bindingを表示し、confirmation後にrevokeして停止します。新conversationの
fresh sessionにはbindingを作りません。

## Cross-matter

default`false`。explicit comparative request、exact matter IDs、permission、purpose、
confidentialityを確認します。whistleblower identity、medical data、clean-team、
union/CBA restrictionがあれば拒否します。shared verificationはauthority factだけで、
matter factはmatter scopeです。

## 行わないこと

- local folder create/move/archive
- same-session switch/none
- null-matter active binding
- close時current bindingだけrevoke
- archive-first / revoke-every close
- conflict clearance/retention delete
- restricted isolationの無効化
- Power Platform solution/scheduleを作成・実行したと主張
