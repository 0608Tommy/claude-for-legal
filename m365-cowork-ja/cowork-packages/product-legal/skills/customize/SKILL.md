---
name: customize
description: >
  Product legal profileを1項目ずつ安全に変更する。company/product、法域・sector、launch process、review framework、risk calibration、claims posture、担当者、matter、storage/connection、watcher preferenceをexact SharePoint recordへ差分反映する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: product-legal
  migration-target: admin
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Product legal profile customization

正規labelは `/product-legal:customize [section or change]`。

## Mandatory gate

1. [保存契約](references/common/cowork-runtime-contract.md)を読み、state gateway、
   exact profiles、ACL、conditional update、auditをlive preflightする。失敗時は
   proposed diffのread-only/manual draftだけを返し、saved/updatedと表示しない。
2. exact company/practice profileとcurrent user profileを読む。missing、paused、
   `[PENDING]`ならwriteせず`cold-start-interview`へrouteする。
3. company共通、product-legal practice、user、matter、stateのscopeを判定する。
   matter secretをshared profileへ入れない。
4. matter-specific changeはactive/unexpired non-null bindingとactive matterを要求。
   practice modeはfresh sessionでbinding不在。
5. jurisdiction、law、guidance、platform rule、deadline、threshold、future statusを
   変える場合はcurrent official sourceを確認する。
6. viewer、retention、legal hold、storage/flow DLP、MNPI/clean-teamを確認する。
7. legal floor、claims evidence、source tag、review flag、isolation、human gate、
   DLP blockerを緩和しない。
8. section/history/auditをdeleteしない。廃止statusとdownstream impactを示す。
9. 1度に1変更。current→proposed→impact→fresh confirmation。
10. exact `itemId`、latest `eTag`、unique `idempotencyKey`でconditional update。
    stale/duplicate/partialでは停止し再読取りする。

## Customizable map

[profile fields](references/profile-fields.md)を使い、current valueを1行で添える。

- Company / product / customer / stage
- Jurisdictions / sector / regulators
- Launch intake / lead time / formal-advisory posture
- Review framework
- Risk calibration
- Marketing claims / commerce screens
- People / escalation / user role
- Matter / confidentiality / cross-matter
- Integrations / storage / DLP
- Watcher preference candidate

## Conversation state

`select-section` → `show-current` → `collect-new` → `verify-source` →
`check-consistency` → `explain-impact` → `confirm` →
`conditional-update` → `audit`

複数changeは順番を決め、各changeごとにfresh confirmationと別idempotencyを使う。

## Impact examples

- `FYI`→`requires work`: quick triage/launch reviewでflagが増える。past reviewは
  自動更新しない。
- new framework category: future launch draftへ追加。existing memoは変更しない。
- comparative claims tightening: future claims reviewのevidence/reword triggerが増える。
- `ja-JP`追加: draft Japan moduleを適用するがqualified review completeではない。
- public/listed status変更: IR/MNPI overlayを追加。
- matter isolation on: future sessionはnon-null expiring bindingを要求。
- watcher desired horizon/cadence変更: preference recordだけ。running flow/scheduleを
  作成・変更したとは表示しない。
- connector status変更: live probe結果だけを更新。declarationはconnectedではない。

## Consistency

- Japan usersがいるのに`ja-JP` moduleなし
- consumer subscriptionなのにrendered final-screen reviewなし
- claims evidence-before-publication offだがabsolute/medical/financial claimを許容
- AI featureをframeworkから外したがAI product surfaceあり
- matter isolation onだがcross-matter default true
- listed companyだがpublic disclosure/MNPI ownerなし
- Cowork DLP mandatoryだがproduction enabled
- 2026 APPI amendmentをcurrent effectiveとして記録
- Atlassian/Asana source SSEをadapterなしでconnected扱い

矛盾を示し、人にどちらを直すか選んでもらう。

## Guardrail degradation

次は構造上必須で無効化しない。

- `[B]/[G]/[P]/[I]/[F]/[X]`とprovenance tag
- current-law/platform check
- no fabricated authority/evidence
- user/session/matter isolation
- non-null expiring binding
- fresh-session practice/switch/none
- archived/revoked rejection
- destination/confidentiality/privilege
- large-input coverage
- upstream severity floor
- no send/post/publish/approve/clear
- exact ID/eTag/idempotency
- append-only audit
- Cowork DLP blocker

削除依頼は拒否し、目的を満たす安全な調整を提案する。

## Scope/write

- company level → company profile
- product-legal-specific → practice profile
- user role/contact → user profile
- matter-specific → matter record
- setup/cursor/automation evidence → state record

update前にcurrent recordとlatest`eTag`を再取得し、exact diff、source、downstream
impactを示す。成功後、changed field、itemId、old/new eTag、review status、
unresolved conflictを示し、canonical auditへappendする。

## Complete

保存できた場合だけ「変更済み」と表示する。existing launch memo、claims review、
risk assessment、tracker draft、automationは自動更新していないことを示す。次の
変更またはskillを自動開始しない。
