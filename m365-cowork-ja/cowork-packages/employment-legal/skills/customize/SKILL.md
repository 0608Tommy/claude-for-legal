---
name: customize
description: >
  employment practice profileを1項目ずつ安全に変更する。事業場、就業規則、36協定、採用、termination、leave、investigation、worker status、EOR、保険、restricted isolation、保存・接続設定をcurrent→proposed→impact→confirmでexact SharePoint recordへ反映する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: employment-legal
  migration-target: admin
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Employment profile customization

旧来のlabel:
`/employment-legal:customize [section name, or describe what you want to change]`。

## Mandatory gate

1. `references/common/cowork-runtime-contract.md`を読み、gatewayをlive preflight。
   失敗時はread-only change planで停止します。
2. exact company/employment practice/user profileをcanonical keyで読みます。missing、
   paused、substantive `[PENDING]`ならcold-startへrouteします。
3. company、practice、user、restricted matter、stateのscopeを判定し、employee/
   matter secretをshared profileへ入れません。
4. matter-specific changeはactive、unexpired bindingとmatter `status: active`。
5. law、threshold、deadline、minimum wage、employment rate、insurance、work-rule/
   36 status、visa、future-law statusの変更はcurrent official sourceを確認します。
6. access、retention、legal hold、whistleblower/medical separation、保存・flow DLPを
   確認します。
7. 一度に1 change。複数はqueueとし、each changeにfresh confirmation、
   separate idempotencyを使います。
8. exact`itemId`、latest`eTag`でconditional update。stale/partialは停止します。
9. Cowork内DLP必須なのにproduction enabledへする依頼は拒否します。

## 会話state

`select-section` → `show-current` → `collect-new` → `verify-source` →
`check-consistency` → `explain-impact` → `confirm` →
`conditional-update` → `audit`

confirmation前にwriteせず、success後に次changeを自動開始しません。

## Map

`references/profile-fields.md`からcurrent valueを1行で示します。

- Company / user / escalation
- Footprint / entity / establishment / headcount
- Work rules / Article 36 / working time
- Hiring / termination / classification
- Leave / accommodation / insurance
- Investigation / whistleblowing / evidentiary standard
- Restricted isolation / access / retention
- International / EOR / immigration
- Integrations / storage / DLP
- Outputs / reviewer / dashboard

## Impact examples

- new prefecture: minimum wage、local establishment、work-rule/36 coverageをrefresh。
- 9→10 regular workers: work-rule filing/opinion/notice readinessをflag。
- EOR provider追加: costより先にdispatch/supply legality gate。
- leave alert window変更: internal controlだけ変更。statutory deadlineは変更しない。
- investigation standard変更: future caseだけ。existing conclusionを自動rewriteしない。
- restricted isolation off: sensitive triggerがあるため拒否。
- `ja-JP` authority date更新: source/effective date/counsel statusを別々に保存。
- Cowork DLP mandatory: productionをblockedへ。

## Consistency

flag:

- Japan employeeだがentity/establishment/work locationなし
- 10+なのにwork rules filing/notice evidenceなし
- overtime operationだが36 agreement不明
- EORなのにdaily direction/dispatch characterization不明
- general workspace offとrestricted isolation off
- whistleblower identityがgeneral investigation record
- medical detailがpractice profile/audit
- 2026-10-01/12-01 future changeをeffectiveとして保存
- connector declarationだけでconnected
- counsel review pendingをapprovedへ変更

どちらを直すか人に選んでもらいます。

## Guardrail degradation

次は無効化しません。

- current-law/provenance/`[review]`
- exact user/session/matter isolation
- sensitive restricted matter
- expiring binding、fresh practice mode、new-session switch/none
- close時全binding revoke
- create/update separation、ETag/idempotency、immutable audit
- no autonomous hire/discipline/termination/leave/payroll/benefit/send/file
- Cowork DLP blocker
- original-jurisdiction/Japan counsel review pending

## Write

exact current recordを再取得し、current→proposed diff、source/currency、downstream
impact、destination/viewerを示し、`Confirm this one change? yes/no`後にupdateします。

gateway failure時は「保存しました」と言わず、change planとblockerを示します。
