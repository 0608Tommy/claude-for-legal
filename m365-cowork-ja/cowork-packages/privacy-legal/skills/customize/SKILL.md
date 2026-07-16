---
name: customize
description: >
  privacy実務profileを1項目ずつ安全に変更する。会社情報、法域、risk posture、担当者、DPA playbook、policy commitments、PIA、DSAR、matter、保存・接続設定を、全初期設定をやり直さずexact SharePoint recordへ反映する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: privacy-legal
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Privacy profile customization

旧来の参照labelは `/privacy-legal:customize [section name, or describe change]`。

## 必須gate

1. `references/common/cowork-runtime-contract.md`を読む。local configを編集しない。
2. exact company/practice profileと現在利用者の`user-profile`を読む。missing、paused、`[PENDING]`なら変更せず`cold-start-interview`を案内する。
3. company共通、privacy practice、user、matter、stateのscopeを判定する。matter secretをshared profileへ入れない。
4. matter-specific changeはactive/authorized/unexpired bindingとmatter `status: active`を要求する。archived/revokedでは拒否する。
5. jurisdiction、law、deadline、threshold、2026年改正statusを変える場合はcurrent primary sourceを確認する。
6. viewers、retention、legal hold、保存・flow DLPを確認する。
7. legal position、fallback、never、exemption、approval threshold、日本法review statusを人のreviewなしに緩和しない。
8. section、history、auditをdeleteしない。廃止statusと影響を示す。
9. 一度に1変更。current→proposed→downstream impact→confirmation。
10. exact`itemId`、latest`eTag`、unique`idempotencyKey`でconditional updateする。conflictでは停止する。

## Customizable map

`references/profile-fields.md`を使い、current valueを1行で添える。

- Company / who you are
- Regulatory footprint
- Risk posture
- People / escalation
- DPA playbook
- Privacy policy commitments / surfaces
- PIA house style
- DSAR process
- Matter / workflow
- Integrations / storage

## 会話state

`select-section` → `show-current` → `collect-new` → `verify-source` → `check-consistency` → `explain-impact` → `confirm` → `conditional-update` → `audit`

複数changeは順番を決め、各changeごとにfresh confirmationと別idempotencyを使う。

## Impact examples

- subprocessor notice 30→14 days: future DPA reviewのdeviation thresholdが変わる。existing DPAは自動改訂しない。
- DSAR internal SLA変更: clock dashboardが変わる。applicable statutory deadlineは変更されない。
- risk posture→conservative: PIA REQUIRED、escalation、redline候補が増える。
- `ja-JP`追加: draft Japan moduleを追加適用するが、qualified review completeにはならない。
- policy item変更: policy-monitor scope/cursor fingerprintが変わる。old cursorを再利用しない。
- systems list追加: future DSAR search scopeが増える。past requestを自動再開しない。

## Consistency

- processor-only orientationなのにcontroller playbookを唯一のstandardとしている
- EU in scopeなのにtransfer routeなし
- Japan in scopeなのに`ja-JP` moduleなし
- policy says no trainingだがDPA fallbackはunrestricted training
- matter isolation onだがcross-matter default true
- Cowork DLP mandatoryだがproduction enabled
- Japanese private-sector PIAを一律statutory mandatoryと記録
- 2026 amendmentをeffectiveとして記録

矛盾を示し、人にどちらを直すか選んでもらう。

## Guardrail degradation

次は構造上必須で無効化しない。

- `[review]` / source tag / current-law check
- no fabricated authority
- user/session/matter isolation
- archived/revoked rejection
- destination / privilege check
- large-input coverage
- recoverable-error bias
- human send/delete/sign/approve gate
- exact ID/eTag/idempotency
- immutable audit
- Cowork DLP unsupported blocker

削除依頼は拒否し、目的を満たす安全な調整を提案する。

## Scope / write

- company level → company profile
- privacy-specific → privacy practice profile
- user role/contact → user profile
- matter-specific → matter record
- DSAR/cursor/setup → state record

update前にcurrent recordとlatest`eTag`を再取得し、差分とdownstream impactを示す。成功後、changed field、itemId、old/new eTag、review status、unresolved conflictを示し、auditへ追記する。

## Complete

> 変更を保存しました。次回の出力から反映されます。既存のDPA、PIA、DSAR、policy reportは自動更新していません。

次の変更を自動開始せず、続けるか人に尋ねる。
