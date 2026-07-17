---
name: cold-start-interview
description: >
  corporate/M&A実務のinitial、resume、quick、full、redo、redo-section、check-integrations、module追加、new-dealを会話で行い、会社・利用者・日本法機関設計・公開会社・M&A・entity・保存設定を分離したSharePoint profile/stateへ構成する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: corporate-legal
  migration-target: admin
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Cold-start interview

旧来の参照label/flags:

- `/corporate-legal:cold-start-interview`
- `--full`
- `--redo`
- `--redo <section>`
- `--new-deal`
- `--check-integrations`
- `--module [m&a | board | public | entities]`

Coworkではflagをconversation stateへ変換する。

## 目的

M&A、Board & Secretary、Public Company、Entity Managementからactive moduleを
選び、generic U.S. defaultsではなく、actual entity、organ、Japan/public-company
footprint、house format、materiality、approver、seed documentsをprofileへ保存する。

## Mandatory setup / filing / privilege / security gate

1. **Gateway live preflight:** `references/common/cowork-runtime-contract.md`を読み、
   SharePoint profiles/matters/outputs/state/audit、OneDrive、tenant-approved
   gateway、ACL、conditional create/update、audit appendを実際に確認する。
   失敗時はread-only/manual setup draftで停止し、setup complete/saveを主張しない。
2. **Record separation:** company、corporate practice、user、setup session、
   matter/dealを別recordにする。共有practice profileへ単一user role/active matterを
   保存しない。
3. **Create/update:** new profileはconditional create。existing profileはexact
   `itemId`、latest`eTag`、unique`idempotencyKey`でconditional update。差分を
   先に示す。
4. **Fresh session practice mode:** setupはpractice-level。bindingなしのfresh
   sessionを使う。`matterId: null` active bindingを作らない。deal seedを使う場合は
   authorized active matterを明示する。
5. **No local migration:** local config/cache/home historyを探索・copyしない。
   userがmigration artifactを指定した場合だけsource/version/ownerを確認して
   import candidateにする。
6. **Jurisdiction:** `request > matter > practice-profile > tenant-default`。
   entity、listing、assets、employees、data、investor、licencesから法域を確認する。
7. **Legal facts:** article、threshold、deadline、listing status、corporate number、
   EDINET code等をprofileへ書く前にofficial/authorized sourceで確認する。
8. **Seed source:** exact item/version、coverage、confidentiality、viewerを記録する。
   readしていないdocumentからhouse formatを作らない。
9. **No silent gap:** skipped answerは`[PENDING]`または
   `[DEFAULT — human review required]`。completeに見せない。
10. **Mandatory profile fields for Japan:** entity form、registered head office、
    corporate number、organ design、articles、public-notice method、
    share-certificate/restricted-share、listed market/EDINET、Art. 370 authorization。
11. **Deal fields:** transaction structure、target listing、foreign investor/
    ultimate control、Japan turnover、voting-right bands、designated/core business、
    sector licences。
12. **Privilege/security:** user role、attorney route、destination、clean-team、
    MNPI、VDR terms、APPI、retention、DLPを確認する。
13. **DLP blocker:** Cowork内DLP必須ならproduction enableを記録せず停止。

Japan module:

- `references/common/ja-jp/README.md`
- `references/common/ja-jp/source-register.md`
- `references/common/ja-jp/governance-records.md`
- `references/common/ja-jp/ma-regulatory.md`

## 会話state

| state | intent |
|---|---|
| `initial` | profileなし。quick/fullを選ぶ |
| `resume` | paused setupのpending questionだけ再開 |
| `quick` | role、setting、module、jurisdiction、minimum Japan fields |
| `full` | full interview + seed documents |
| `redo` | current profile全体を差分reviewして再設定 |
| `redo-section` | `--redo <section>`の1 sectionだけ更新 |
| `check-integrations` | live probe結果だけ更新 |
| `module` | `--module [m&a | board | public | entities]`を追加/refresh |
| `new-deal` | `--new-deal`のdeal-specific profile |

migration-map canonical core:
`initial | resume | quick | full | redo-section | check-integrations`を必ず認識する。

## Start detection

- corporate practice profileなし → `initial`
- setup session `status: paused` → `resume`
- `[PENDING]`あり → open items表示
- `setupStatus: complete` → redo/module/check/new-deal、またはquick/default-backed
  profileを明示的に`full`へupgradeする場合以外は上書きしない
- profile record conflict/duplicate → fail closed

## Orientation

3～4行:

> このpackageはM&A diligence、board minutes/consent、closing、integration、
> entity complianceを支援します。
>
> quickは約2分、fullは約10～15分です。日本法moduleはqualified Japanese
> counsel review pendingです。
>
> 途中で「一時停止」と言えばapproved state gatewayへsetup sessionを保存します。
>
> quickとfullのどちらにしますか。

gatewayがない場合、「保存」ではなくsession内draftとしてのみ続ける。

## Interview pacing

- 1 turnに2～3 answerable promptまで。
- documentにありそうな情報はexact SharePoint item/linkを先に求める。
- upload/readが必要ならanswerを待つ。silent skipしない。
- pause時はanswered sectionsとpending questionsをstateへ保存する。
- full output前にopen/PENDING/default/source gapを一覧にして確認する。

## Company profile

existing shared profileがあればorganization、practice setting、industry、
jurisdictions、risk postureを1行で確認し、変更がなければ再質問しない。

new:

- practice setting:
  `Solo / small firm | Midsize / large firm | In-house |
  Government / legal aid / clinic | Other`
- organization/business、industry、products/services、size
- operation/customer/employee/investor jurisdictions
- regulators/licences
- risk posture
- escalation roles

matter secret、single user role、active matterをshared company profileへ入れない。

## User profile

1. `Lawyer / legal professional`
2. `Non-lawyer with attorney access`
3. `Non-lawyer without regular attorney access`

Non-lawyerもdraft/researchを使えるが、minutes adoption、consent execution、
filing、closing certification、external send前にattorney reviewへrouteする。
role/contactはuser profileへ保存する。

## Module selection

- `m&a`
- `board`
- `public`
- `entities`

inactive moduleのseed documentを求めない。public moduleは独立skillではなく、
board、diligence、schedule、closing、integration、entityのFIEA/JPX overlayを
有効にする。

## Quick

minimum:

- user role / practice setting
- active modules
- primary jurisdictions
- organization/entity summary
- Japan entity form/organ/listing status
- M&A transaction tendency
- basic materiality/internal format defaults
- board/consent precedent availability
- entity owner
- escalation
- storage/integration live status

未設定は`[DEFAULT — human review required]`。defaultがfuture skillへどう影響するか
示す。

## Full

`references/full-interview.md`を使う。section:

1. user/practice/integrations/security
2. Japan entity/governance/public-company foundation
3. M&A posture/request list/materiality/issues memo
4. board minutes/consent precedent
5. public-company/FIEA/JPX controls
6. entity/event/periodic obligations
7. matter/clean-team/retention
8. outputs/escalation/approvals

## Seed documents

M&A:

- request list
- prior closed issues memo
- PA/schedule example

Board:

- 5–6 prior closed minutes if available
- 3–5 prior consents/deemed-resolution records
- articles/board regulation/committee charter

Entities/public:

- org chart/entity list
- current registry evidence/articles
- disclosure calendar/internal rule
- licence list

extract actual structure、resolution language、discussion depth、materiality、
category、approval matrix、not just filename. source/version/coverageを記録する。

## Connection check

SharePoint、OneDrive、optional Box/Google Drive/iManage/Slack等をlive probeする。

- `connected`: live probe success
- `configured-unverified`: declaration only
- `not-connected`: missing/failed

declarationだけでconnectedと表示しない。external connectorにはadmin/per-user
consent、least privilege、retention、storage-flow DLPが必要。
`connectors.draft.json`はpackage capabilityではない。

## Pause / resume

setup state:

```yaml
recordType: setup-session
tenantId: "[tenant id]"
practiceId: "[practice id]"
pluginId: corporate-legal
userObjectId: "[Microsoft Entra object ID]"
sessionId: "[Cowork session ID]"
scopeType: user
scopeId: "[userObjectId]"
recordId: "setup:[sessionId]"
setupStatus: paused
pausedAt: "[section]"
answeredSections:
  - "[section]"
pendingQuestions:
  - "[question]"
profileItemId: "[itemId or null]"
```

resumeでanswered sectionを再質問しない。

## New deal

`--new-deal`はhouse profileを上書きせずdeal/matter-specific candidateを作る。

- deal code
- side
- transaction structure
- target/acquirer
- listed status/market/EDINET
- foreign investor/ultimate control
- Japan turnover/voting-right before/after
- designated/core business/licences
- VDR exact source
- deal lead/outside counsel
- signing/closing/effective dates
- deal-specific materiality
- clean-team/MNPI/APPI/retention

matter create/switchは`matter-workspace`の別state/confirmation。new-deal後に
自動bindingしない。

## Pre-save / save

show:

- confirmed facts
- document-derived fields
- interview-derived unapproved position
- defaults
- pending/contradiction
- legal premise/currency
- coverage
- destination/viewers/retention/DLP
- create vs update

schemaは`references/profile-record-schema.md`。substantive required itemがopenなら
paused。conditional write後、item IDs、old/new eTag、idempotency、approver、
pending counsel reviewをauditする。

## Complete

active modules、Japan/public/company/deal fields、seed coverage、connections、
defaults/pendingを短く示す。最初のskillを人に選んでもらい、自動開始しない。

## 行わないこと

- local config/cache/historyを読む・書く
- placeholder/defaultをcompleteと表示
- Form 4/HSR/CFIUS/registered-agent defaultを日本profileに残す
- public-company moduleをSEC fieldsだけで構成
- connector declarationをconnectedと表示
- gatewayなしにsetup保存済みと表示
- new dealを自動matter switch
