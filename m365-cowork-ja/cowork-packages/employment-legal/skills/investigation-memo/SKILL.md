---
name: investigation-memo
description: >
  restricted investigation logから日本向け内部memoをdraft/updateし、scope、methodology、issue別facts、conflict、credibility、work rules・law、configured evidentiary standard、recommendation options、chronology、coverageをentry ID付きで構成する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: employment-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Investigation — memo

旧来のlabel:
`/employment-legal:investigation-memo [matter]`。

compiled frameworkのMode 4だけを実行します。

## Mandatory memo / confidentiality gate

1. `references/common/cowork-runtime-contract.md`を読み、active restricted matter、
   current user、destination/viewers、legal holdを確認します。
2. counsel/client/purposeを確認し、日本で米国work-product protectionと同一に
   shieldされると断定しません。
3. full authorized case/checklist/entries、source versions、coverage、open gaps、
   internal evidentiary standardを読みます。
4. whistleblower identity、medical dataはmemo purposeに必要な範囲だけ。
5. harassment/whistleblower/discipline/dismissal等のcurrent law/effective dateを確認。
6. source quote、entry ID、contrary evidenceを保持し、conflictをsmooth overしません。
7. recommendationはwork rules/CBA、consistency、proportionalityへtraceします。
8. AIはsubstantiation、credibility、discipline、terminationを最終決定しません。
9. Cowork内DLP必須ならmemo contentを投入せずproduction停止です。

## 会話state

`resolve-case` → `read-coverage` → `check-prerequisites` →
`first-draft-or-update` → `show-changes` → `draft-memo` →
`qualified-review`

## Prerequisites

- each issueにevidence/explicit gap
- complainant/respondent entriesまたは不在理由
- high-priority checklist review
- source/currency
- configured internal standard
- audience/destination

不足時はpreliminary statusとlimitationsを明示し、人がdraft続行を選べます。

## Structure

`references/investigation-framework.md`に従い:

1. Executive summary
2. Background/scope/out-of-scope
3. Methodology/coverage
4. Factual findings by issue
5. Determinative credibility
6. Applicable work rules/policies/law
7. Conclusions under configured internal standard
8. Recommendations/options
9. Chronology
10. Documents reviewed/gaps

`preponderance`等を日本のstatutory ruleと書きません。demeanorはhuman observationが
recordedされている場合だけ使います。

## Update

existing memo/versionとcovered entry IDsを比較し、new entries、new issues、
resolved gaps、affected sectionsを先に示します。prior versionをdeleteせず、
superseding draftを作り、changed sections/source dateを記録します。

## Output label

`機密 — 内部法務レビュー用調査memo draft — 配布先限定`

labelはaccess controlの代替ではありません。OneDrive draftまたはrestricted matter
documentを候補とし、SharePoint outputsへの昇格は別確認です。

## 行わないこと

- privilegeを保証
- missing evidenceを補完
- statutory evidentiary standardを創作
- discipline/terminationを決定
- memoをHR/leadership/externalへそのまま配布
