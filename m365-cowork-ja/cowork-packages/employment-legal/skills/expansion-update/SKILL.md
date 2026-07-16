---
name: expansion-update
description: >
  exact international-expansion project/item stateを読み、複数itemの変更をsingle intakeで受け、dependency unblocking、overdue、current-law refresh、owner、due、evidenceを再計算し、人が確認したitemだけconditional updateする。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: employment-legal
  migration-target: power-platform
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# International expansion — update

旧来のlabel:
`/employment-legal:expansion-update [country]`。

compiled international-expansion frameworkのupdate behaviorを実行します。

## Mandatory tracker / source / write gate

1. `references/common/cowork-runtime-contract.md`を読み、gatewayとcurrent user
   accessをlive preflightします。projectがmatter scopeならactive unexpired
   binding、practice scopeならfresh sessionにbindingがないことを確認します。
   失敗時はread-only status/update planだけです。
2. exact project `recordId: expansion:[countryCode]:[projectId]`とall authorized
   item stateをscope-specific cursorで読みます。
3. missing projectならkickoffを案内し、new projectをsilent createしません。
4. legal-feasibility blockをcost/timeline updateで解除しません。
5. law、licence、visa、insurance、deadline、EOR characterizationが変更/完了したitemは
   current source/effective dateを再確認します。
6. status/due/owner/evidenceはexact itemごとにdiff、fresh confirmation、
   `itemId`/`eTag`/idempotencyでupdateします。
7. AIはEOR/entity、hire、payroll、insurance、visa、filing、sendを決定・実行しません。
8. schedule/notification flowがあると推測しません。

## 会話state

`resolve-project` → `show-current` → `collect-updates-single-block` →
`verify-evidence-law` → `recalculate-dependencies` → `show-item-diffs` →
`confirm-updates` → `conditional-update-each` → `audit`

## Current state

```text
[Country] expansion — last updated [date]
Open [N] | In progress [N] | Done [N] | Blocked [N]
Legal feasibility: [status]
Next priorities: [dependency/due/source based]
```

10行超ならdashboardを提案しますが自動生成しません。

## Collect updates

「動いたitem、新item、due/owner/evidence変更」をsingle blockで求めます。each updateを
existing exact itemへmatchし、ambiguous near-matchは人に選んでもらいます。

`done` candidateにはevidence item ID、source/effective date、human owner confirmationを
要求します。tax/finance/HR/counsel statementをAIが法律上のclearanceへ格上げしません。

## Dependency / overdue

newly done itemでunblocked candidateを示しますが、downstream statusを自動変更しません。
due date超過はrecorded dueから計算し、法定deadlineを推測しません。legal dueはcurrent
authorityを確認します。

## Write

project summary updateとeach item updateを分けます。batch confirmationでもeach
conditional update outcomeをcanonical auditへappendし、partial failureを報告します。
cursorはhuman acknowledgment後の別operationで更新します。

## Completion

closed/open/blocked/unblocked counts、next priority、law/source gaps、saved/failed item
IDs、automation statusを示します。outside-counsel emailやowner notificationを自動送信
しません。

## 行わないこと

- local YAML tracker
- legal blockのsilent downgrade
- evidenceなしのdone
- dependencyのauto status change
- schedule/notificationの推測
