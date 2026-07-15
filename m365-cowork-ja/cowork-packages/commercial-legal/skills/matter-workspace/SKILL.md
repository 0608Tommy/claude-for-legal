---
name: matter-workspace
description: >
  複数依頼者・案件のcontextを分離する。SharePointのmatter recordとserver-side session–matter bindingを、new、list、switch、close、noneの会話状態で管理し、権限、confidentiality、retention、cross-matter isolationを維持する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: commercial-legal
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Matter workspace

旧来の参照label:

- `/commercial-legal:matter-workspace new <slug>`
- `/commercial-legal:matter-workspace list`
- `/commercial-legal:matter-workspace switch <slug>`
- `/commercial-legal:matter-workspace close <slug>`
- `/commercial-legal:matter-workspace none`

Coworkではsubcommandを会話stateとして扱う。本skillはSharePoint / Power Platform stateのfront endであり、managed solutionやscheduled automationを含まない。

## 必須gate

1. **保存契約:** `references/common/cowork-runtime-contract.md`を必ず読む。local folderを作成・移動しない。
2. **Setup/user:** practice profileの`matterWorkspaces.enabled`と、現在利用者の`user-profile`をexact keyで読む。`false`ならerrorにせず、in-house等のpractice-level運用であることを説明する。
3. **Binding:** active matterの唯一のsourceはserver-side binding record。会話履歴、表示名、個人profileから推測しない。
4. **Jurisdiction:** new matterにjurisdictionが不明なら、実質作業を開始できるactive matterとして確定しない。resolutionは`request > matter > practice-profile > tenant-default`。
5. **Source/permission:** exact matter item、status、authorized viewers、client/counterpartyを読む。権限のないmatterは存在も漏らさない。
6. **Confidentiality:** `standard | heightened | clean-team`、legal hold、retention、保存境界DLP、cross-matterを確認する。
7. **Human review:** workspace作成はconflicts clearance、engagement acceptance、retention decisionではない。
8. **Write:** `new`はcanonical composite key、`matterId`、unique
   `idempotencyKey`による条件付きcreateを使い、返された`itemId`/`eTag`を
   保存する。`switch`, `close`, `none`はexact`itemId`、latest`eTag`、
   unique`idempotencyKey`によるupdateとする。削除しない。

## 会話state

| state | action |
|---|---|
| `new <slug>` | intake後、SharePoint `matters`へrecord作成 |
| `list` | authorized active/archived matterを一覧 |
| `switch <slug>` | server-side bindingを変更 |
| `close <slug>` | recordを保持して`archived`へ |
| `none` | binding解除、practice-levelへ |

意図不明なら5つを提示する。移行元のargument変数やfilesystemは使わない。

## `new`

slugはlowercase alphanumericとhyphen。例: `acme-msa-2026`, `zenith-renewal`, `vendor-xyz-nda`。

同一`tenantId + practiceId`のactive/archived双方で重複を確認する。

取得:

- client / represented party
- counterparty
- matter type: `vendor MSA | customer agreement | NDA | SaaS subscription | amendment | renewal | other`
- confidentiality: `standard | heightened | clean-team`
- key facts（2～5文）
- matter-specific playbook override
- related matter IDs
- jurisdictions
- retention / legal hold / DLP
- authorized viewers

作成後に自動switchしない。別stateとしてswitchするかを確認する。

## `list`

authorized matterだけをscope-specific cursorで取得する。

| Slug | Client | Matter type | Status | Opened | Active | Jurisdictions |
|---|---|---|---|---|---|---|

activeはserver bindingから`*`。archivedは別表。10件超ならstatus、client、jurisdiction、updatedでfilterできるdashboardを提案するが、自動生成しない。

## `switch`

1. exact matter recordと`eTag`を読む。
2. `status: active`、viewer権限、confidentiality、legal holdを確認する。
3. current→new matter IDと読み込まれるprofile要約を示す。
4. 同じ会話内でbindingを書き換えない。旧matterのdocument、quote、draftが
   conversation contextに残るため、current bindingをrevokedへ更新して停止し、
   新しいCowork conversationを開始してnew matterを選ぶよう案内する。
5. new sessionで新しいbindingをconditional createする。
6. `audit`へold/new matter ID、old/new session ID、actor、time、
   idempotency keyを追記。
7. verified hard context resetがMicrosoftに提供・検証されるまで、同一sessionの
   switchを許可しない。

## `close`

「close」はdeleteではない。

1. matterと、その`matterId`を参照する全session bindingを確認。
2. unsaved draft、open renewal、pending proposal、unrouted escalation、legal hold、retention、sharing linkを確認。
3. close date、reason、approver、影響を示す。
4. 明示確認後`status: archived`。
5. その`matterId`を参照する全bindingを`revoked`へ条件付き更新し、各sessionの
   actor、旧binding、revocation reasonをauditする。current sessionだけを
   解除して終わらない。
6. revocationに失敗したbindingが1件でもあれば、archived matterを実質作業で
   使用しないようblock eventを残し、管理者対応へ回す。
7. closeと各binding revocationをauditへ追記。

retention満了後のdeleteは本skill範囲外。

## `none`

current bindingを示す。同じconversationにmatter資料が残るため、bindingを
revokedへ更新して停止し、新しいCowork conversationでpractice-levelを選ぶ。
verified hard context resetなしに同一sessionでmatterless作業へ続行しない。

## Cross-matter

defaultは`false`。`true`でも「過去5案件を比較」等の明示依頼がある場合だけ、exact matter IDs、permission、purposeを確認する。clean-team、client restriction、conflictがあれば拒否する。

## Record

`references/matter-records.md`を使う。matter contentとbindingを同じrecordへ混ぜない。

## 完了

changed matter ID、binding、status、destination、unresolved conflict/retentionを示す。substantive reviewを自動開始しない。

## 行わないこと

- conflicts check、engagement acceptance
- retention delete
- cross-matter共有の適法性を最終判断
- external send
- local folder operation
- Power Platform solutionの作成・変更
