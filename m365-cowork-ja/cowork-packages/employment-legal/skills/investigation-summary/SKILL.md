---
name: investigation-summary
description: >
  restricted investigation memoからHR、leadership、outside counsel、external draftのaudience別summaryを作り、entry ID、credibility methodology、legal exposure、whistleblower identity、medical detail、attorney mental impressionをneed-to-knowでstripする。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: employment-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Investigation — audience summary

旧来のlabel:
`/employment-legal:investigation-summary [matter] [audience]`。

compiled frameworkのMode 5だけを実行します。

## Mandatory audience / destination gate

1. `references/common/cowork-runtime-contract.md`を読み、active restricted matter、
   authorized memo version、current userを確認します。
2. audience、decision/action、exact destination、need-to-know、forwarding riskを
   先に確認します。
3. whistleblower identityはappointed-handler permissionとneedがない限り除外。
4. medical/accommodation、personal data、witness detailsをminimizeします。
5. internal legal analysisとemployee/regulator-facing artifactを分けます。
6. source memoがpreliminary/coverage-limitedならsummaryも同じfloorを保持します。
7. AIはdiscipline、termination、external response、send/fileを決定・実行しません。
8. Cowork内DLP必須ならrestricted contentを投入せずproduction停止です。

## 会話state

`select-audience` → `confirm-purpose-destination` → `load-memo-version` →
`apply-stripping` → `show-removed-categories` → `draft` →
`qualified-review`

## Audience

### HR

- factual summary、configured finding、human action options
- legal exposure、credibility methodology、entry IDs、counsel mental impressionsを除外
- header:
  `機密 — 人事対応検討用 — 再配布禁止`

### Leadership

- allegation/scope、key findings、high-level impact、governance options
- detailed evidence/identity/legal analysisを除外

### Outside counsel

- full relevant context、open evidence、credibility issues、significant documents、
  legal questions
- secure destinationとengagement relationshipを確認

### Employee/regulator/external

internal memoを要約するだけでは作りません。admission、waiver、privacy、defamation、
retaliation、deadlineをqualified counselがreviewするsanitized separate draftです。
internal header/reviewer noteをoutward artifactへ入れません。

## Stripping report

summary前に内部review用として:

- included source memo/version
- removed categories
- identity minimization
- unresolved findings/coverage
- destination risk

を示します。summary本文へmeta commentaryを散らしません。

## Consequential gate

external/employee/regulator responseはforum/deadline、exact source、qualified counsel、
approver、destinationを確認し、draftで停止します。send/respond/fileしません。

## 行わないこと

- no memoからconclusionを作る
- HRへlegal/credibility detailを漏らす
- whistleblower identityをbroad summaryへ入れる
- preliminary findingをfinalへ格上げ
- external send
