> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Customize field map

一度に1 fieldだけ変更します。

- UI locale
- study legal system
- role / education stage
- legal-profession-course vs undergraduate-law
- law-school track: mishu-3-year / kishu-2-year
- institution / course / term / assessment mode
- exam year / component / elective / cohort
- `bar_or_exam.exam_format.value`
- exam format source system / item ID / source version / verified time
- component prerequisite status / basis / source version
- judicial-exam eligibility basis / start / earlier endpoint
- `bar_or_exam.attempt_cap.status`: none-within-eligibility-period / numeric / unknown / not-applicable
- `bar_or_exam.attempt_cap.count`（statusがnumericの場合だけ）
- jurisdiction / comparative jurisdiction
- syllabus / rubric / AI policy source pointer
- learning mode / pushback / strong / weak / avoided
- outline format / depth / source pointer
- citation style / writing preference
- exam date / temporal label and asOf / prep course / supplement-or-replace
- source inventory / LIMITED DATA
- SharePoint / OneDrive / optional connector status
- destination / DLP requirement
- source-workflow review / Japan qualified review status

## Consistency flags

- `ui_locale: ja-JP`だけを理由に`study_legal_system: JP`
- JP routeに1L/MBE/UBEをdefault
- US routeにmishu-3-year/kishu-2-year・司法試験科目をdefault
- legal-profession-courseをgeneric undergraduateへ適用
- law-schoolなのにmishu-3-year/kishu-2-year未解決
- exam format valueとsource versionの片方だけ変更
- judicial-examにoral、preliminary oralにwritten-pass prerequisiteなし
- `bar_or_exam.attempt_cap.status`がnumeric以外なのにcountあり
- `bar_or_exam.attempt_cap.status`がnumericなのにcountが正の整数でない
- national examでcourse professor forecast
- exam yearがあるのに`exam-cutoff`のasOf/source versionなし
- graded workなのにAI policy source/versionなし
- judicial trainingなのにreal recordの保存pointer
- Japanese translationをauthoritative statute source
- connector declarationだけでconnected
- DLP requiredなのにproduction enabled
- review pendingを根拠なしにapproved

archiveは可能ですが、sectionやaudit historyを削除しません。

`bar_or_exam.exam_format`はobject全体を一変更として扱います。valueだけを更新して
source versionを古いまま残さず、source item/version/verified timeを同時に示して
fresh confirmationを得ます。

`bar_or_exam.attempt_cap`はnullable値で更新せず、statusとcountの整合を一緒に示します。
