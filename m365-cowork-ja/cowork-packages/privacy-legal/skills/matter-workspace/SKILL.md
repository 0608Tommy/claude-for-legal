---
name: matter-workspace
description: >
  複数依頼者・案件のprivacy contextを分離するSharePoint / Power Platform front end。案件を会話でnew、list、switch、close、noneへ遷移させ、server-side session–matter binding、権限、保持、監査をexact IDとconcurrency controlで管理する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: privacy-legal
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Matter workspace

旧来の参照label:

- `/privacy-legal:matter-workspace new <slug>`
- `/privacy-legal:matter-workspace list`
- `/privacy-legal:matter-workspace switch <slug>`
- `/privacy-legal:matter-workspace close <slug>`
- `/privacy-legal:matter-workspace none`

Coworkではsubcommandを実行せず、会話stateとして選ぶ。

## 目的

private practice等で、PIA、DPA、DSAR、regulator inquiry、incidentの資料・判断が別client/matterへ漏れないようにする。in-house単一組織では既定でoffとし、practice-level contextを使う。

## 必須gate

1. **保存契約:** `references/common/cowork-runtime-contract.md`を読む。local folderを作らない。
2. **Setup/user:** `matterWorkspaces.enabled`と現在利用者のexact`user-profile`を確認する。`false`ならexpected stateとして説明し、別利用者のrole/bindingを流用しない。
3. **Binding:** `tenantId + practiceId + userObjectId + sessionId`のserver recordだけをactive sourceとする。会話名、表示名、memoryからmatterを推測しない。
4. **Status:** matter-scoped substantive skillが使えるのはbinding
   `status: active`かつmatter `status: active`だけ。archived/revokedは拒否する。
5. **Conflicts/access:** workspace作成はconflict clearance、受任、access authorizationを意味しない。client、counterparty、authorized viewersを人が確認する。
6. **Jurisdiction:** `request > matter > practice-profile > tenant-default`で使うmatter jurisdictionを取得する。空欄なら実質作業開始前に解消する。
7. **Confidentiality:** `standard | heightened | clean-team`、cross-matter、retention、legal hold、保存・flow DLPを確認する。
8. **Human/irreversible:** switch、close、archive、binding解除、sharing changeは差分・影響を示し明示確認後に行う。deleteしない。
9. **Concurrency:** createとupdateを分ける。exact item、eTag、idempotencyが不足すれば停止する。
10. **Power Platform:** state-changing flowは別途承認・導入された場合だけ使う。flowがない場合、動作中と表示しない。

## 会話state

| state | action |
|---|---|
| `new <slug>` | intake後、SharePoint `matters`へcreate |
| `list` | 許可されたactive/archived matterをscope別に表示 |
| `switch <slug>` | current bindingをrevokeし、新sessionでbindingをcreate |
| `close <slug>` | matterを`archived`へ条件付きupdate |
| `none` | current bindingをrevokeし、新sessionでpractice-levelへ戻る |

意図不明なら5つを提示する。

## `new <slug>` — Create protocol

slugはlowercase alphanumeric + hyphen。active/archivedを同じ`tenantId + practiceId`で検索し、重複時は別slugを求める。

intake:

- Client / represented party
- Counterparty
- Matter type: `PIA | DPA review | DSAR | regulator inquiry | transfer review | incident | policy project | other`
- Confidentiality: `standard | heightened | clean-team`
- Key facts（2～5文）
- Matter-specific overrides
- Related matters
- Jurisdictions
- Retention / legal hold / DLP
- Authorized viewers

`references/matter-records.md`のcanonical keyと一意な`idempotencyKey`でconditional createする。成功responseの`matterId`、`itemId`、`eTag`を記録する。duplicate/timeoutでは再createせず照合する。

create後に自動switchしない。switchは別confirmation。

## `list`

利用者が閲覧できるmatterだけを表示する。

| Slug | Client | Matter type | Status | Opened | Active | Jurisdictions |
|---|---|---|---|---|---|---|

active markerはserver bindingから決める。archivedは別表。権限のないmatterは存在も漏らさない。global cursorを使わず、practice/user/query scopeのcursorを使う。

## `switch <slug>` — Update protocol

1. exact matter itemとlatest`eTag`を取得。
2. `status: active`、access、confidentiality、retention、legal holdを確認。
3. current bindingをexact key/item/eTagで再取得。
4. old→new matter、読み込むprofile要約、破棄するcontextを示す。
5. human confirmation。
6. 同じconversationでbindingを書き換えず、current bindingを`revoked`へ
   conditional updateして停止する。
7. 新しいCowork conversationでnew matterを選び、新session bindingを
   conditional createする。
8. auditへold/new matter ID、old/new session ID、user、time、resultを追記。

別matterのcache、citation、draft、cursorを持ち込まない。verified hard
context resetが提供・検証されるまで同一session switchを許可しない。

## `close <slug>` — Update protocol

closeはdeleteではない。

1. exact matterとlatest`eTag`を取得。
2. open DSAR、unsaved draft、deadline、legal hold、retention、shared linksを確認。
3. close date、reason、approver、下流影響を示す。
4. fresh confirmation。
5. `status: archived`へconditional update。
6. そのmatterIdを参照する全bindingを`revoked`へ条件付きupdateし、各結果を
   auditする。current bindingだけを解除して終わらない。
7. revocation failureがあればblock eventを残し、archived matterへの実質
   accessを拒否する。
8. auditへ追記。

archived後はすべての既存bindingを拒否し、substantive accessを継続しない。retention満了後のdeleteは範囲外。

## `none` — Update protocol

current bindingを表示し、確認後に`revoked`へ更新して停止する。旧matter
contextがconversationに残るため、新しいCowork conversationで
practice-levelを明示する。verified hard context resetなしに同一sessionで
続行しない。

## Cross-matter

default`false`。`true`でも「過去5件を比較」等の明示依頼がある場合だけ、許可されたmatter、purpose、confidentialityを確認する。clean-team、client duty、guardian/subject confidentiality等に抵触する場合は拒否する。

## Automation

`references/automation-contract.md`を読む。Power Automate等はleast privilege、exact scope、retry/backoff、dead-letter、partial success、immutable auditを満たす。AIはflowを作成・有効化・実行したと主張しない。

## 完了

変更したmatter ID、binding、status、itemId/eTag、保存先、未解決のconflict/retention事項を示す。substantive workを自動開始しない。
