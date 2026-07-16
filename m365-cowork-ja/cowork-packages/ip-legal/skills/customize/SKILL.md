---
name: customize
description: >
  IP practice profileを1項目ずつ安全に変更する。practice mix、法域、role、approver、enforcement、portfolio、brand watch、employee invention、OSS、matter、connector、DLPをcurrent→proposed→impact→confirmでexact SharePoint recordへ反映し、guardrailを緩和しない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: ip-legal
  migration-target: admin
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# IP profile customization

旧来の参照label:
`/ip-legal:customize [section name, or describe what you want to change]`。

## Purpose

full setupをやり直さず、profile/stateの1 changeをreviewして反映します。

## Mandatory gate

1. [保存契約](references/common/cowork-runtime-contract.md)を読み、state gatewayを
   live preflight。失敗時はread-only change plan。
2. exact company/IP practice/user profileをcanonical keyで読みます。
   missing、paused、substantive `[PENDING]`ならcold-startへ案内。
3. company、practice、user、matter、portfolio/stateのscopeを判定。
   matter secretをshared profileへ入れません。
4. matter-specific changeはactive/unexpired bindingとmatter `status: active`を要求。
5. law、case、deadline、fee、JPO status、Nice/guideline versionを変える場合はcurrent
   official source確認。
6. viewer、retention、legal hold、clean-team、patent secrecy、保存・flow DLP。
7. legal position、approval threshold、review statusをhuman reviewなしに緩和しません。
8. section/history/auditをdeleteしません。廃止はstatus/reason/impact。
9. 一度に1 change。複数changeはqueueにし、fresh confirmationとseparate
   idempotency。
10. exact `itemId`、latest `eTag`、unique `idempotencyKey`でconditional update。
11. `production.enabled`を直接変更しません。original/Japan legal review、
    state gateway、tenant smoke test、Cowork DLP requirementの全gateがapprovedで
    なければ拒否し、満たした場合もauthorized administratorのdeployment actionへ
    routeします。

[profile fields](references/profile-fields.md)と
[source rule](references/common/source-provenance-and-review.md)を使います。

## Conversation state

`select-section` → `show-current` → `collect-new` → `verify-source` →
`check-consistency` → `explain-impact` → `confirm` →
`conditional-update` → `audit`

success後に次changeを自動開始しません。

## Customizable map

- Company / organization
- User role / bengoshi / benrishi / attorney route
- Practice mix
- Jurisdictions / filing routes
- Enforcement posture / approvers
- Trademark / brand watch / clearance
- Patent / invention / employee invention / secrecy
- Copyright / platform
- Trade secret
- OSS policy
- IP clauses / recordal
- Portfolio / source / verifier / alert candidate
- Matter / clean-team
- Integrations / storage / DLP
- Outputs / reviewer / dashboard

何を変えるか明確なら全mapを表示せず、その項目へ進みます。

## Impact examples

- posture `measured → aggressive`: future C&D option orderが変わる。existing draftは
  自動変更しない。
- new trademark watch class: future watch/report scope候補。scheduleは作らない。
- new blocked OSS licence: future reviewがblock candidate。past shipを遡及変更しない。
- `ja-JP`追加: Japan draft moduleを適用するがqualified review completeにしない。
- portfolio source変更: versioned rebuild candidate。自動rebuildしない。
- employee invention rule変更: exact work-rule version/effective dateを確認。
- matter isolation on: gateway/ACL/bindingが必要。profile flagだけで分離済みにしない。
- Cowork DLP mandatory: `production.enabled: false`とblocker。

## Consistency

- patent practice activeだがpatent secrecy ownerなし
- employee invention sourceなしでArt. 35 policy approved
- trademark out-of-scopeだがwatch active
- aggressive postureと全件external counsel approval
- auto alert candidateだがapproved solution evidenceなし
- Japan scopeだがJapanese professional review routeなし
- matter isolation onでcross-matter default allow
- Cowork DLP mandatoryでproduction enabled

AIが優先順位を決めず、人にどちらを直すか選んでもらいます。

## Guardrail degradation

無効化しない:

- `[review]`, provenance, current-law/source check
- no fabricated authority/registration/claim
- non-null expiring matter binding
- fresh-session practice/switch/none
- close時全binding revoke
- destination/clean-team/patent secrecy
- C&D/takedown draft-only
- no file/pay/renew/abandon
- exact ID/eTag/idempotency/create-update separation
- versioned rebuild/history
- immutable canonical audit
- Cowork DLP blocker
- qualified counsel review pending

削除依頼は拒否し、安全なadjustmentを提案します。

## Write

1. exact current record/latest `eTag`。
2. current→proposed exact diff。
3. source/currency/downstream impact。
4. destination/viewer/retention/DLP。
5. `Confirm this one change? yes/no`。
6. conditional update。
7. item ID、old/new eTag、idempotency、review statusをaudit。

gateway failure時は「保存しました」と言いません。

## 行わないこと

- full setupのsilent overwrite
- multiple changeのbatch approval
- matter secretをshared profileへ移す
- law/deadline/statusをuser assertionだけで変更
- review pending/guardrailを解除
- existing artifacts/portfolioを自動rebuild
- local config、agent、hook、subagentを使う
