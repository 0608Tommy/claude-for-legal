---
name: closing-checklist
description: >
  SharePoint / Power Platform front endとして、取引構造別のconditions、corporate approvals、JFTC、FEFTA、FIEA/TDnet、登記、労働、許認可、deliverablesをinitialize、ingest、update、blocking-reportへ遷移させ、evidenceとcritical pathを管理する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: corporate-legal
  migration-target: power-platform
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Closing checklist

旧来の参照label:

- `/corporate-legal:closing-checklist`
- `/corporate-legal:closing-checklist [item ID + status update]`

source Mode 1–4を会話stateへ変換する。本skillはSharePoint / Power Platform
stateのfront endであり、filing、consent、schedule、automation solutionを含まない。

## Mandatory filing / materiality / privilege / security gate

1. **Runtime/preflight:** `references/common/cowork-runtime-contract.md`を読み、
   tenant-approved state gateway、list/library、ACL、conditional create/update、
   audit appendをlive preflightする。失敗時はread-only/manual draft mode。
2. **Matter:** exact expiring binding、matter `status: active`、current user access、
   transaction structureを確認する。practice-level checklistをmatter checklistの
   代用にしない。
3. **Source:** signed/near-final PA、disclosure schedule、closing memo、diligence
   finding、official ruleのexact item/versionを使う。
4. **Transaction structure:**
   `share sale | business transfer | merger | company split | share exchange |
   share transfer | share delivery | other`
   ごとにapproval、creditor、appraisal、employee、registry、licenceを分ける。
5. **Materiality:** PA condition/waiver、statutory requirement、internal
   priorityを分ける。internal thresholdでmandatory itemを削らない。
6. **Current filing:** JFTC、FEFTA、FIEA/EDINET、JPX/TDnet、registry、labour、
   sector filingのfiler、threshold、effective date、deadline、waiting period、
   system、signer、evidenceをofficial sourceで確認する。
7. **Required fields:** `legal_basis`, `source_version`, `effective_date`,
   `evidence_required`, `filing_system`, `waiting_period_end`, `waivable`を
   regulatory/corporate itemで省略しない。
8. **Privilege/destination:** internal checklist/statusとcounterparty/board-facing
   versionを分ける。日本のprivilege差異、clean-team、MNPIを確認する。
9. **Human action:** create、ingest、status update、waiver、certificationは別々に
   exact diffとfresh confirmationを得る。AIはfile、send、sign、approve、
   certify、funds releaseを行わない。
10. **DLP:** Cowork内DLP必須ならproduction useを停止する。

日本workflow:

- `references/common/jurisdictions/ja-jp/ma-regulatory.md`
- `references/common/jurisdictions/ja-jp/governance-records.md`
- `references/common/jurisdictions/ja-jp/integration-entity.md`

provenanceは
`references/common/source-provenance-and-review.md`を使う。

## State gateway fallback

preflight失敗時に許されるもの:

- PA/documentからcandidate checklist draft
- read-only status summary（exact state readができる場合）
- missing gateway/configurationの説明

禁止:

- checklist作成済み/更新済みと表示
- item status、cursor、auditを書いたと表示
- Power Platform flowを実行したと表示
- local YAML/Excelをstate sourceとして作る

## 会話state

| state | source mode | action |
|---|---|---|
| `initialize` | Mode 1 | PAとofficial ruleからcandidate checklistを作成 |
| `ingest` | Mode 2 | diligence/schedule/summary handoffをdedupe・merge |
| `update-item` | Mode 3 | exact itemのstatus/evidence/owner等を1変更 |
| `blocking-report` | Mode 4 | current stateからblocking/critical pathをread-only集計 |
| `certification-draft` | consequential | ready-to-close/closing memo候補をdraft |

意図不明ならcurrent checklistの有無を確認し、`initialize`または
`blocking-report`を選んでもらう。

## Initialize

PAから:

- every condition precedent
- closing deliverable
- pre-closing covenant/deadline
- bring-down/MAC/MAE wording
- Required Consents
- corporate approval
- regulatory condition
- waiver mechanics

Japan screen:

- Companies Act approvals/disclosure/creditor/appraisal
- restricted shares/shareholder register
- JFTC notification/wait
- FEFTA prior notification/post-report
- FIEA/EDINET/tender offer/large holding
- JPX/TDnet
- labour notice/objection/consent
- registry
- licence/permit
- real-estate/IP perfection
- tax/social-insurance evidence

`certificate of good standing`をgeneric itemにせず、certificate of registered
matters、seal certificate、tax/social-insurance certificate、licence evidence等へ
分ける。

candidateを提示し、source coverage、missing official rule、item count、
state destinationを確認した後にconditional createする。create/updateを混ぜない。

## Ingest

accepted sources:

- `diligence-issue-extraction`
- `material-contract-schedule`
- `deal-team-summary`
- approved external/counsel status

canonical source fieldsを保持する:

```yaml
item: "[one-line action]"
category: "[category]"
source: "[source item/version/location]"
blocking: true
severity: "[🔴 | 🟠 | 🟡 | 🟢]"
counterparty: "[name or N/A]"
guarantor: "[name/condition or N/A]"
conditions: "[conditions or N/A]"
notice_deadline: "[date/period or unknown]"
approval_body: "[body or N/A]"
approval_threshold: "[threshold or unknown]"
statutory_or_charter_source: "[source or N/A]"
estimated_time_to_complete: "[estimate or unknown]"
must_occur_before: "[signing | closing | post-closing | unknown]"
legal_basis: "[source]"
source_version: "[version]"
effective_date: "[date or null]"
evidence_required: "[evidence]"
filing_system: "[system or null]"
waiting_period_end: "[date or null]"
waivable: false
```

dedupeはcounterparty名だけでなく、action type、legal basis、source item、
filing/approval bodyで行う。consentとrelease等を誤ってmergeしない。fieldは
mergeし、new sourceでold populated fieldをsilent overwriteしない。

upstream severityをfloorとして保持する。

## Update item

1. `references/checklist-records.md`のcanonical keyでexact stateを読む。
2. item ID、current value、latest`eTag`、source/evidenceを取得。
3. proposed diff、downstream effect、approverを示す。
4. fresh confirmation。
5. unique`idempotencyKey`でconditional update。
6. stale/partial/duplicateでは再読取りし、推測でretryしない。
7. canonical audit envelopeへappend。

filing receipt、consent、certificateを確認できない場合、`complete`へしない。

## Blocking report

show:

- target close / days remaining
- total / complete / in progress / not started / blocked / unknown
- 🔴 blocking/at risk
- blocking/on track
- waiting periods
- evidence pending
- critical path
- source/currency gaps

critical path candidate:
`remaining time < verified estimated time`、dependency、non-waivable waitを考慮する。
estimate不明はsafe-looking greenへせず`unknown`。

10行超ならdashboardを提案するが、自動生成・送信しない。

## Certification gate

`ready to close`, `all CPs satisfied`, closing memo/funds-release signalの前:

- full CP listとsource versions
- outstanding/waived items
- mandatory vs waivable
- waiting period end
- evidence sufficiency
- bring-down/MAC facts
- counsel/approver
- destination

を示し、fresh reviewを要求する。Non-lawyerにはattorney briefを作る。
AIはfinal certification、waiver、funds releaseを行わない。

## Dataroom automation gap

`references/common/power-platform-automation-contracts.md`の
`corporate-dataroom-watcher`は`closing-checklist-status`をread-onlyで作るだけで、
checklistを更新しない。new document由来のactionはhuman-reviewed `ingest`を
通す。scheduled behaviorを主張しない。

## 行わないこと

- consent取得、filing、registry、waiver
- PAがblockingと定めていないitemを最終決定
- checklist stateをgatewayなしで変更
- scheduled watcher/notificationを推測
- ready-to-closeをcertify
- local checklist fileへfallback
