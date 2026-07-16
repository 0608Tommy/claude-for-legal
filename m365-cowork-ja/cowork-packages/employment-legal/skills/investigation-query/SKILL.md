---
name: investigation-query
description: >
  authorized restricted investigation logをfull coverageで読み、entry IDを引用してfactual、conflict、coverage、strength、chronology、interview-notice、whistleblower-accessの質問へ回答するread-only skill。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: employment-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Investigation — query

旧来のlabel:
`/employment-legal:investigation-query [matter] [question]`。

compiled frameworkのMode 3だけを実行します。

## Mandatory read / identity gate

1. `references/common/cowork-runtime-contract.md`を読み、active unexpired binding、
   restricted matter、current user accessを確認します。
2. whistleblower identity itemはappointed-handler permissionがある場合だけ読み、
   answer audienceに不要なら出しません。
3. exact case/checklist/entry recordsとcoverageを読みます。partial readをfullと表示しません。
4. case外knowledge、別matter、practice profileでevidence gapを埋めません。
5. union/CBA、harassment、whistleblower、privacy lawのcurrent statusを法的評価へ
   使う場合だけcurrent sourceを確認します。
6. queryはread-only。entry/checklist/memoを更新しません。
7. AIはfinding、credibility、discipline、terminationを最終決定しません。
8. Cowork内DLP必須ならrestricted contentを投入せずproduction停止です。

## 会話state

`resolve-case` → `authorize` → `read-full-log` → `classify-query` →
`answer-with-entry-ids` → `state-coverage-and-gaps`

## Query types

`references/investigation-framework.md`に従います。

- factual: source/entry IDs。なければ「[N] entriesに情報なし」。
- conflict: conflicting entries、exact tension、documentary support。
- coverage: open checklist、gaps、unreadable/out-of-scope。
- strength: issue別high-significance/corroboration/unresolved conflict。
- chronology: event date順。
- procedure: interview notice、recording、identity access、non-retaliation。

retrieved quoteがpropositionを支えるか確認し、summaryとverbatimを区別します。

## Output

answer、supporting entry IDs、contrary evidence、coverage、open gaps、human judgmentを
短く示します。new gapを登録する場合は`investigation-add`のseparate writeを提案し、
自動登録しません。

## 行わないこと

- unauthorized identity disclosure
- another matterから類推
- absence of evidenceをevidence of absenceとする
- log/memo/checklist write
- disciplinary conclusion
