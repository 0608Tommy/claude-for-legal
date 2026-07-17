---
name: cold-start-interview
description: >
  employment-legalのinitial、resume、quick、full、redo-section、check-integrationsを会話で行い、日本の事業場、就業規則、36協定、労使、休暇、調査、社会保険、移民、restricted matter設定を分離したSharePoint profile/stateへ構成する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: employment-legal
  migration-target: admin
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Cold-start interview

旧来の正規label/flags:

- `/employment-legal:cold-start-interview`
- `--full`
- `--redo`
- `--redo <section>`
- `--check-integrations`

Coworkではflagを会話stateへ変換します。

## Mandatory setup / law / security gate

1. `references/common/cowork-runtime-contract.md`を読み、tenant-approved gateway、
   profiles/matters/outputs/state/audit、ACL、conditional create/updateをlive
   preflightします。失敗時はread-only setup draftだけで、保存/completeを主張しません。
2. company、employment practice、user、setup session、matterを別recordにします。
   共有practice profileへ単一user role、active matter、従業員情報を入れません。
3. newはconditional create、existingはexact `itemId`、latest `eTag`、unique
   `idempotencyKey`によるupdate。diffを先に示します。
4. setupはfresh practice-level session。binding不在を確認し、
   `matterId: null` active bindingを作りません。
5. local config/cache/historyを探索・copyしません。指定されたmigration artifactだけを
   source/version/owner確認後にimport candidateとします。
6. 法域は`request > matter > practice-profile > tenant-default`。勤務地、事業場、
   entity、CBA、EOR/dispatchを確認します。
7. legal fact、threshold、deadline、work-rule filing、36 agreement、insurance、
   visa、future-law statusはofficial/current sourceで確認してから保存します。
8. skipped fieldは`[PENDING]`または
   `[DEFAULT — human review required]`。silent gapをcompleteに見せません。
9. investigation、whistleblowing、medical/accommodation、leave、discipline、
   contested terminationのrestricted isolationを一般workspace設定と独立して構成します。
10. Cowork内DLP必須ならproduction enableを記録せず停止します。

Japan sourceは
`references/common/ja-jp/README.md`、
`references/common/ja-jp/source-register.md`、
`references/common/currency-watch.md`を使います。

## 会話state

| state | intent |
|---|---|
| `initial` | profileなし。quick/fullを選ぶ |
| `resume` | paused setupのpendingだけ再開 |
| `quick` | role、setting、footprint、minimum Japan fields |
| `full` | full interview + seed documents |
| `redo` | 全profileを差分reviewして再設定 |
| `redo-section` | `--redo <section>`相当の1 sectionだけ |
| `check-integrations` | live probe結果だけ更新 |

canonical core
`initial | resume | quick | full | redo-section | check-integrations`を必ず認識します。

## Start detection

- profileなし → `initial`
- setup session `status: paused` → `resume`
- substantive `[PENDING]` → open items表示
- populated profile → explicit redo/full-upgrade/check以外で上書きしない
- duplicate/conflicting record → fail closed

## Orientation

3～4行で、採用、termination、leave、investigation、work rules、classification、
expansionを支援すること、quick約2分/full約10～15分、日本法review pending、
pause可能と説明し、quick/fullを選んでもらいます。

gatewayなしでは「保存」ではなくsession内draftと説明します。

## Interview pacing

- 1 turnに2～3 answerable prompt。
- documentにありそうな情報はexact SharePoint item/linkを先に求める。
- typed answer/uploadが必要なら待つ。
- pause時は`references/profile-record-schema.md`のsetup sessionを保存。
- resumeでanswered sectionを再質問しない。
- pre-saveでpending/default/source gapを一覧化する。

## Quick

minimum:

- user role、attorney/escalation route、practice setting
- primary country/prefecture、employing entity、establishments/headcount
- work rules/36 agreementの有無とowner
- union/CBA
- hiring/termination review triggers
- leave/HRIS source
- investigation handler
- restricted matter trigger/access groups
- social insurance/immigration owner
- storage/integration live status
- Cowork DLP requirement

未設定はdefault markerとdownstream impactを示します。

## Full

`references/full-interview.md`を使います。Japan minimum:

- establishmentごとの常時headcountと10+ work-rule filing
- current disability employment-rate scope、gender disclosure scope
- work rules、36 agreement、working-time system、objective time record
- hiring condition/contract、fixed-term、background、covenant/IP
- discipline/dismissal/nonrenewal/RIF process
- childcare/family-care/maternity/annual leave/accommodation
- whistleblower/harassment/investigation
- freelancer/dispatch/EOR
- social/labor insurance、foreign-worker/visa
- 2026-10-01/2026-12-01 readiness

## Seed documents

current work rules/handbook、filing/notice evidence、36 agreement/CBA、
employment-condition/contract templates、recent termination/discipline/nonrenewal
memos、leave/accommodation procedure、investigation protocol/memo、contractor/
dispatch/EOR templateを対象にします。

source item/version/date/coverage/viewerを記録し、未読documentからhouse styleを
創作しません。large inputはcoverageを明示します。

## Integration check

SharePoint、OneDrive、HRIS、optional Slack/Google Drive等をlive probeします。

- `connected`: live probe success
- `configured-unverified`: declaration only
- `not-connected`: missing/failed

connector declarationや`connectors.draft.json`だけでconnectedと表示しません。
HRIS connectorはread scope、medical minimization、no writeを確認します。

## Pre-save / save

show:

- confirmed/document-derived/interview-derived/default/pending fields
- authority/effective date
- restricted access、retention/legal hold/DLP
- company/practice/user/setupのcreate vs update
- original-jurisdiction and Japan counsel review pending

substantive required fieldがopenならpaused。write後、exact IDs、old/new eTag、
idempotency、approver、review statusをcanonical auditへappendします。

## Complete

footprint、Japan foundation、triggers、seed coverage、connections、defaults/pending、
future-law readinessを短く示します。最初のskillは人に選んでもらい、自動開始しません。

## 行わないこと

- local profile/register/folderを作る
- placeholder/defaultをcompleteと表示
- 米国固有defaultをJapan profileへ残す
- connector declarationをconnectedと表示
- gatewayなしに保存済みと表示
- legal-review pendingを解除
- restricted isolationを一般workspace offと一緒に無効化
