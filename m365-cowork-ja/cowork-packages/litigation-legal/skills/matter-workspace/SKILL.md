---
name: matter-workspace
description: >
  litigation matterをnew、list、switch、close、noneの会話stateで管理するPower Platform front end。expiring non-null binding、fresh-session practice mode、fence-first active-only revoke、restricted/clean-team/evidence/hold ACLをcanonical keyで強制する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: litigation-legal
  migration-target: power-platform
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Matter workspace

canonical labels:

- `/litigation-legal:matter-workspace new <slug>`
- `/litigation-legal:matter-workspace list`
- `/litigation-legal:matter-workspace switch <slug>`
- `/litigation-legal:matter-workspace close <slug>`
- `/litigation-legal:matter-workspace none`

## Mandatory isolation / security gate

1. `references/common/cowork-runtime-contract.md`を読み、gateway、matter/state/audit、
   ACL、conditional writeをlive preflight。失敗時はread-only list/intake draft。
2. exact current`user-profile`を
   `tenantId + practiceId + userObjectId`
   で読む。
3. `matterWorkspaces.enabled: false`はin-house practice modeのexpected stateだが、
   restricted/clean-team matter isolationを無効化しない。
4. active sourceは
   `tenantId + practiceId + userObjectId + sessionId`
   のserver bindingのみ。会話名、display name、memoryから推測しない。
5. active bindingは非null`matterId`、`expiresAt`を持ち、
   `status: active`, `expiresAt > now`, matter `status: active`を要求。
6. practice modeはfresh sessionでbinding不在。`matterId: null` active binding禁止。
7. new/switch/close/noneは別operation、exact diff、fresh confirmation。
8. switch/noneはcurrent sessionを停止し、新conversationを要求。
9. closeはmatterを先にfenceし、全bindingをenumerateしてactiveだけをrevoke。
   already-revokedはsatisfiedとし、zero active後だけarchivedへfinalize。
10. Cowork内DLP必須ならconfidential matterを投入せず停止。

## State

| state | action |
|---|---|
| `new <slug>` | intake後、matterをconditional create |
| `list` | authorized active/archived matterを表示 |
| `switch <slug>` | current binding revoke、新sessionでnew binding create |
| `close <slug>` | fence → enumerate → active-only revoke → zero active確認 → archived finalize |
| `none` | current binding revoke、新sessionでpractice mode |

## `new <slug>`

slugはuser-facing label。opaque matter IDを正本とする。gateway unique constraintで
active/archived duplicateをfail closedし、unauthorized matterの存在を漏らさない。

intake:

- represented party / counterparty
- source compatibility type/role
- proceeding type / jurisdiction
- confidentiality:
  `standard | heightened | restricted | clean-team`
- key facts
- matter-specific override
- related matter IDs
- authorized Entra groups
- hold/evidence/identity mapping ACL
- retention / DLP
- conflicts/engagement status declared by human

`expectedAbsent: true`とunique idempotencyでcreate。auto-switchしない。

## `list`

- current user authorized matterだけ
- active/archived別
- active markerはserver binding
- pseudonymous ID、type、procedure、court、confidentiality、status、updated
- scope/query-specific cursor
- restricted fact、counterparty、existenceをunauthorized userへ表示しない

10件超ならdashboardを提案するが自動生成しない。

## `switch <slug>`

1. exact target matter/latest eTag/access/status/ACL/retention/hold。
2. current bindingがあればexact keyで再取得。fresh practice sessionなら不在。
3. old→new、破棄context、新session requirementを表示。
4. fresh confirmation。
5. current bindingがあればconditional revokeし、current sessionで停止。
6. binding不在でもcurrent sessionでtarget sourceを読み始めず停止。
7. new conversation/new session IDでtarget bindingをconditional create。exact matter
   `itemId`、latest `eTag` / `version`またはbinding-generation token、
   expected active statusをbinding absenceと同一transactionで評価。
8. old/new matter/session、expiry、actor、outcomeをaudit。

same-session switch禁止。

## `close <slug>`

`matter-close`のclose checklistを使う。最初のatomic conditional operationでmatterを
`close-pending`等のnon-active stateへfenceする。fence成功後に全bindingを
enumerateし、activeだけをrevocation対象としてrevoke、already-revokedはsatisfied
として再更新しない。zero active確認後だけ`archived`へconditional finalizeする。
fence前にcommitしたcreateは
enumerationで捕捉され、fence後のcreateはmatter preconditionで失敗する。途中失敗は
fenced stateを維持してfail closed。delete、folder move、retention expiry deletionを
しない。

## `none`

current bindingを表示、confirmation後revokeして停止。新conversationのfresh sessionで
practice modeを明示し、bindingを作らない。

## Cross-matter

default`false`。explicit comparative request、exact matter IDs、permission、purpose、
confidentialityを確認。clean-team、hold/evidence restriction、client duty、trade secretが
あれば拒否。shared verificationはauthority-level factだけ。

## Completion

matter/binding IDs、status、item/eTag/version、expiry、ACL、unresolved conflict/
retention、auditを示す。substantive workを自動開始しない。

## 行わないこと

- local folder create/move/archive
- same-session switch/none
- null-matter active binding
- close時current bindingだけrevoke
- archive-first / revoke-every close
- conflict/engagement/retention delete
- restricted isolationの無効化
- Power Platform solution/schedule実行の主張
