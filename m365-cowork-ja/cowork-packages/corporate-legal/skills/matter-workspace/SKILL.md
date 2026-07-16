---
name: matter-workspace
description: >
  corporate/M&A matterをnew、list、switch、close、noneの会話stateで管理するSharePoint / Power Platform front end。expiring server-side session–matter binding、fresh-session practice mode、全binding revoke、ACL、clean-team、retention、監査をcanonical keyで強制する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: corporate-legal
  migration-target: power-platform
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Matter workspace

旧来の参照label:

- `/corporate-legal:matter-workspace new <slug>`
- `/corporate-legal:matter-workspace list`
- `/corporate-legal:matter-workspace switch <slug>`
- `/corporate-legal:matter-workspace close <slug>`
- `/corporate-legal:matter-workspace none`

Coworkではsubcommandを会話stateとして扱う。local folderの作成、移動、archiveは
行わない。

## Mandatory isolation / conflict / privilege / security gate

1. **Gateway:** `references/common/cowork-runtime-contract.md`を読み、tenant-approved
   state gateway、SharePoint matters/state/audit、ACL、conditional create/updateを
   live preflightする。失敗時はread-only list/intake draftだけ。
2. **User:** current `user-profile`を
   `tenantId + practiceId + userObjectId`
   で読む。別userのrole、attorney contact、authorityを流用しない。
3. **Enabled:** `matterWorkspaces.enabled`がfalseならexpected stateとして説明し、
   fresh-session practice-levelを使う。errorやhidden matterを作らない。
4. **Binding source:** active matterの唯一のsourceは
   `tenantId + practiceId + userObjectId + sessionId`
   のserver record。会話名、display name、memory、shared profileから推測しない。
5. **Expiry/status:** matter-scoped substantive workではbinding `status: active`、
   `expiresAt > now`、matter `status: active`が必要。matter管理自体はfresh
   practice-level sessionからauthorized targetを選べる。revoked/expired/
   archived bindingを実質作業に使わない。
6. **Practice mode:** practice-levelはfresh sessionでbindingが存在しない状態。
   `matterId: null`のactive bindingを作らない。
7. **Access/conflicts:** workspace作成はconflict clearance、engagement acceptance、
   legal authorityを意味しない。client、counterparty、represented party、
   authorized viewersを人が確認する。
8. **Confidentiality:** `standard | heightened | clean-team`、MNPI、
   competition-sensitive data、retention、legal hold、DLPを確認する。
9. **Jurisdiction:** `request > matter > practice-profile > tenant-default`。
   unknownならsubstantive workを開始できるactive matterにしない。
10. **Human/write:** new、switch、close、noneは別operation。exact diff/impactと
    fresh confirmation、exact item/eTag/idempotencyを要求する。
11. **Close:** target matterを参照する全bindingをrevokeする。currentだけで
    終わらない。
12. **Switch/none:** old contextがconversationに残るため、binding revoke後に
    停止し、新しいCowork sessionを要求する。
13. **DLP:** Cowork内DLP必須ならconfidential matterを投入せずproduction停止。

privilegeは
`references/common/jurisdictions/ja-jp/privilege-security.md`、
Power Platformは
`references/common/power-platform-automation-contracts.md`を使う。

## Canonical binding

```yaml
recordType: session-matter-binding
tenantId: "[tenant id]"
practiceId: "[practice id]"
userObjectId: "[Microsoft Entra object ID]"
sessionId: "[Cowork session ID]"
matterId: "[matter ID]"
status: active | revoked
boundAt: "[ISO-8601]"
boundBy: "[Microsoft Entra object ID]"
expiresAt: "[ISO-8601]"
revokedAt: "[ISO-8601 or null]"
revokedBy: "[Microsoft Entra object ID or null]"
revocationReason: "[reason or null]"
```

additional/renamed fieldでactive bindingを代用しない。

## 会話state

| state | action |
|---|---|
| `new <slug>` | intake後、SharePoint mattersへmatter recordをconditional create |
| `list` | authorized active/archived matterをscope-specific cursorで表示 |
| `switch <slug>` | current bindingをrevokeし、新sessionでnew bindingをcreate |
| `close <slug>` | matterをarchivedへupdateし、全bindingをrevoke |
| `none` | current bindingをrevokeし、新sessionでpractice-levelへ戻る |

意図不明なら5つを提示する。

## `new <slug>`

slugはlowercase alphanumeric + hyphen。active/archivedを同じ
`tenantId + practiceId`で検索し、重複時は別slugを求める。hidden unauthorized
matterの存在は漏らさず、gateway側unique constraintでfail closedする。

intake:

- client / represented party
- counterparty
- matter type:
  `M&A buy-side | M&A sell-side | financing | board matter |
  entity reorg | integration project | public-company matter | other`
- transaction structure（applicable）
- confidentiality:
  `standard | heightened | clean-team`
- key facts（2–5文）
- matter-specific playbook override
- related matter IDs
- jurisdictions
- retention / legal hold / storage-flow DLP
- authorized viewers/groups
- conflict/engagement status as declared by human

`references/matter-records.md`のrecordをcomplete key、`expectedAbsent: true`、
unique `idempotencyKey`でcreateする。success responseのmatter/item/eTagを記録。
duplicate/timeoutでは再createせず照合する。

create後に自動switchしない。switchは別confirmation/new session。

## `list`

- current userがauthorizedなmatterだけ
- active/archivedを別表
- active markerはserver bindingから決める
- jurisdiction、confidentiality、status、last updatedを表示
- global cursorを使わずuser/practice/query scope cursor
- unauthorized matterは存在も漏らさない

10件超ならfilter/dashboardを提案するが、自動生成しない。

## `switch <slug>`

1. exact target matter item/latest`eTag`を読む。
2. `status: active`、access、confidentiality、retention、legal holdを確認。
3. current bindingがあればexact key/item/eTagで再取得する。fresh
   practice-level sessionでbindingがなければrevocation対象なしと記録する。
4. old→new matter、破棄するcontext、new session requirementを示す。
5. fresh confirmation。
6. current bindingがある場合だけ`revoked`へconditional updateし、current
   sessionで停止する。bindingがない場合もcurrent sessionでmatter資料を
   読み始めず停止する。
7. userが新しいCowork conversationを開始。
8. new session IDでtarget matter bindingをconditional create。
9. old/new matter/session、actor、outcomeをaudit。

verified hard context resetがMicrosoftで提供・検証されるまで同一session switchを
許可しない。old document、quote、draft、cursorを持ち込まない。

## `close <slug>`

closeはdeleteではない。

1. exact matterとlatest`eTag`を読む。
2. target `matterId`を参照する全bindingをexact queryで取得。
3. open checklist/integration/entity action、unsaved draft、deadline、shared link、
   legal hold、retentionを確認。
4. close date、reason、approver、impactを示す。
5. fresh confirmation。
6. matterを`archived`へconditional update。
7. **全binding**を`revoked`へitemごとにconditional update。
8. each outcomeをcanonical audit envelopeへappend。
9. failureがあればblock eventを残し、archived matter accessを拒否。

retention満了後のdeleteはscope外。

## `none`

current bindingを表示し、confirmation後に`revoked`へupdateして停止する。
同じconversationにmatter contextが残るため、新しいCowork conversationで
practice-levelを明示する。fresh sessionにはbindingをcreateしない。

## Cross-matter

default`false`。`true`でもexplicit comparative request、exact matter IDs、
permission、purpose、confidentialityを確認する。clean-team、client duty、
MNPI、competition restriction、conflictがあれば拒否する。

shared verificationはauthority-level factだけ。matter factはmatter scope。

## Completion

changed matter/binding IDs、status、itemId/eTag、expiry、destination、
unresolved conflict/retentionを示す。substantive skillを自動開始しない。

## 行わないこと

- conflict check/engagement acceptanceの代替
- local folder create/move/archive
- same-session switch/none
- `matterId: null` active binding
- close時current bindingだけrevoke
- retention delete
- cross-matter disclosureの最終判断
- Power Platform solution/scheduleの作成・実行を主張
