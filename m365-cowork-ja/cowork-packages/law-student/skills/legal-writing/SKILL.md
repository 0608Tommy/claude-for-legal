---
name: legal-writing
description: >
  法科大学院report、司法試験・予備試験答案、公開素材の起案、米国memo・brief等の学生draftを全体から読み、構成、分析、明確さ、citationを形成的にfeedbackする。本文・段落・実質的な例文を書き直さない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: law-student
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Legal writing feedback

旧来のlabel:
`/law-student:legal-writing [paste draft or authorized item]`。

## Mandatory education / source / security / state gate

1. `references/common/cowork-runtime-contract.md`、
   `references/common/japan-study-routing.md`、
   `references/common/source-provenance-and-review.md`、
   `references/common/academic-integrity-and-socratic-controls.md`を読みます。
2. `STUDY NOTES — NOT LEGAL ADVICE`。real client、clinic、externship、非公開修習の
   draftをstudy writingとして扱いません。
3. legal system、learner level、jurisdiction、course/exam、document type、
   assessment modeを解決します。
4. exact draft、prompt、rubric、AI policy、citation guide、source item/version/
   pages/coverage/authorizationを記録します。
5. substantive ruleは`exam-cutoff`、`currently-effective`、`future-enacted`、
   `historical`、`pending-proposal`を分けます。
6. 実在しないrule、case、statute、citation、school writing requirementを作りません。
7. graded/restricted workではpolicyが許す範囲だけ。学生のattemptを置き換えず、
   rewrite/model textを出しません。
8. destination、viewer、draftのpersonal/confidential data、DLPを確認します。
9. gateway failure時はsession内feedbackだけ。tracker/outputを保存済みと表示しません。
10. writeはexact ID/eTag/idempotency、fresh confirmation、auditを要求します。
11. grade、submission、LMS、external post、scheduled tutoringを実行・主張しません。

日本法内容はDRAFTで、有資格者review pendingです。

### 共通必須事項（本文全体に適用）

- learner level、jurisdiction、course/exam modeは明示的に解決します。
- exact authorized sourceの`itemId`、version/eTag、coverage、provenanceを保持します。
- `exam-cutoff`、`currently-effective`、`future-enacted`、`historical`、
  `pending-proposal`を分離し、実在しないcase/statute/holdingを
  作りません。
- academic integrityとAI policyを先に確認し、Socratic flowではattempt前にanswerを
  revealしません。
- privacy、destination、DLPを確認します。gateway preflight失敗時はread-only/manual
  fallbackだけです。
- writeはexact `itemId`、`eTag`、`idempotencyKey`、fresh confirmation、auditを
  必須とします。
- 学習者が常にhuman controlを持ち、grading、enrollment、submission、LMS、
  scheduled tutoring、external postingを実行しません。

## Hard rule: no rewriting

構造feedbackがproductです。

- 全文を書かない。
- sectionやparagraphを書き直さない。
- sentence replacementを出さない。
- 対象問題のrule/applicationを含むstarter sentenceを出さない。
- 「copyして提出できる」textを作らない。

依頼されたら:

> 書き直しはしません。あなたの文章の構造、分析の不足、source、明確さをもっと
> 具体的に指摘できます。対象paragraphを選ぶか、自分で書き直した版を見せてください。

generic structural moveを最大1～2例、別topicまたはplaceholderで示すことだけ可能です。

## Route

`references/writing-feedback-rubric.md`に従います。

### JP

- law-school report / paper
- judicial/preliminary exam essay
- public/synthetic judicial-training draft
- case note / comparative assignment

学校、媒体、公式exam sourceのformatを優先します。QP/BA/TOA、Bluebook/ALWDを
defaultにしません。

### US

explicit US modeではoffice memo、brief、paper、exam essayのsource conventionsを
保持します。assignmentが選んだcitation styleだけを使います。

## Workflow

1. draft全体をtop-to-bottomで読む。短ければ再読。
2. prompt/callとdocument typeを確認。
3. top-downでstructureを評価。
4. analysis depth、source、counterargumentを確認。
5. paragraph/transition/clarity/citationへ進む。
6. 自分で直すtop 3をpriority順に示す。
7. generic exampleが本当に必要な場合だけ最大1～2。

large draftではcoverage、未読、優先sectionをreviewer noteへ記録し、全体を読んだと
装いません。

## Feedback dimensions

- assignment/call responsiveness
- overall organization / thesis
- section order / transition
- source and rule version
- fact-to-rule analysis
- counterargument / limitation
- paragraph focus
- clarity / wordiness
- time/word/page constraint
- citation metadata

substantive correctnessはsourceがある範囲だけです。citation edge caseは`[VERIFY]`。
教員rubricがなければ一般的writing standardと明示します。

## Pattern tracking

学生が保存を選んだ場合だけ、session summaryをfeedback trackerへ追加します。
3回以上でstructure、analysis、clarity、citationのobserved patternを示せます。
trackerは`scopeType: user`, `scopeId: [userObjectId]`、session summaryは必要に応じ
`scopeType: session`, `scopeId: [sessionId]`です。study metadataは`payload`、
auditでは`details`へ置き、答案本文はauditやtrackerへ複製しません。

## 行わないこと

- rewrite、model answer、対象topicの例文
- Japan routeへの米国memo/citation format強制
- grade、score、submission readinessの保証
- sourceなしのsubstantive correction
- real client/修習draftの処理
- gatewayなしのtracker保存
