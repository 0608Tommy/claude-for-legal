---
name: exam-forecast
description: >
  全国試験ではforecastを無効化して公開済み公式問題の過去問分析・学習配分を作り、学校試験では提供されたpast paperの形式・topic・設問傾向を観測値として示す。将来の出題や教員・試験委員の関心を予測しない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: law-student
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 過去問分析・学習配分

旧来のlabel:
`/law-student:exam-forecast [class]`。

canonical IDは保持しますが、日本の全国試験で「予測」は行いません。

## Mandatory education / source / security / state gate

1. `references/common/cowork-runtime-contract.md`、
   `references/common/japan-study-routing.md`、
   `references/common/source-provenance-and-review.md`、
   `references/common/academic-integrity-and-socratic-controls.md`、
   `references/common/official-sources-and-2026-exams.md`を読みます。
2. `STUDY NOTES — NOT LEGAL ADVICE`。real matter、非公開試験、leak、修習recordなら
   分析を停止します。
3. legal system、learner level、jurisdiction、national/school exam、course、
   assessment mode、exam yearを解決します。
4. exact official past paperまたはuser-authorized paper、version、year、pages、
   coverage、AI policyを記録します。
5. 各年の`exam-cutoff`、`currently-effective`、`future-enacted`、
   `historical`、`pending-proposal`を分けます。
6. 実在しない問題、topic、採点実感、教員傾向、試験委員関心、citationを作りません。
7. live/restricted exam content、受験者再現、漏えいを使いません。graded current examの
   解答支援へ転用しません。
8. destination、viewer、著作権、DLPを確認し、commercial past paperを過剰複製しません。
9. gateway failure時はsession内analysisだけ。forecast/analysis recordを保存済みと
   表示しません。
10. writeはexact itemId/eTag/idempotency、fresh confirmation、auditを要求します。
11. official forecast、grading、submission、LMS、external post、scheduled tutoringを
    実行・主張しません。

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

## Routing

### Japanese national examination

司法試験・予備試験ではforecastを完全に無効化します。
`references/historical-analysis-template.md`で、公開済み公式問題の観測値だけを示します。

- question countとdenominator
- year/component/subject
- official formatとtime/page constraints
- 出題趣旨・採点実感で明示された観点
- current syllabus/weaknessとの学習配分候補
- sample biasとunknown

2026-07-16時点の司法試験は実施中です。2026問題の公式公開前は2025年以前だけを
対象にし、試験委員、受験者の記憶、commercial速報からtopicを推測しません。

出題趣旨、採点実感、口述テーマは
`examType + examYear + component + subject + materialType + sourceVersion`
でqualifyします。2025司法試験の採点実感を予備試験、別年、別componentのrubricへ
一般化しません。

### School examination

提供されたpast paperだけを読みます。

- format、question count、time、open/closed book
- topic coverageと比率
- issue-spotter、single-issue、policy、short-answer等のobserved type
- fact-pattern density
- observed recurring structure/trap
- policy/doctrine ratio
- current syllabusとのoverlap

3未満はthin sampleです。1件からpatternを作りません。professor名がpaperにあっても、
「hobby horse」「likely question」「必ず出る」と書きません。

### US bar

NCBE/jurisdictionの公開資料についても、historical distributionをpredictionへ変えません。
NextGen/UBE/state-specificを分け、current official scopeを優先します。

## Workflow

1. exam/course、sample set、years、format、current syllabusを確認。
2. duplicate、answer key、unreleased/restricted materialを除外。
3. paperごとにobserved factsを抽出。
4. count、denominator、coverageを計算。
5. stable/variable/absentを記述するが、future likelihoodへ変換しない。
6. learner weaknessと照合し、学習時間のoptionsを示す。
7. unknownとsource gapを別欄にする。

topic countは分類ruleを明示し、同一問題の重複countやsubject名の揺れをnormalizeします。
分類が主観的なら`[review]`です。

## Output

`references/historical-analysis-template.md`を使い、タイトルを
「過去問分析・学習配分」とします。`Forecast weight`や確率を出さず、
`observed count`、`current coverage`、`allocation option`を使います。

10行超のtableはdashboardを提案できますが自動作成しません。HTML化する場合は
untrusted textをescapeし、URL schemeを制限します。

保存はOneDrive draftまたはconfirmed SharePoint outputへ別operationで行います。
analysis progress/stateを保存する場合は`scopeType: user`,
`scopeId: [userObjectId]`とし、exam/year/component/material metadataは`payload`、
auditでは`details`へ置きます。

## 行わないこと

- 全国試験の出題予測
- professor/examiner identityからtopic推測
- live exam leak、受験者再現、未公開問題の利用
- sample sizeを隠したfrequency/percent
- observed absenceを「出ない」と解釈
- external posting、submission、LMS update
