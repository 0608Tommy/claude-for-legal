---
name: bar-prep-questions
description: >
  司法試験・予備試験または明示された米国barについて、法体系、受験年、component、科目、公式基準日を確認し、公開済み公式資料でcalibrateした一問ずつの演習と形成的フィードバックを行う。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: law-student
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Examination practice

旧来の正規label:
`/law-student:bar-prep-questions [subject, or --mbe / --essay / --session <n>]`。

Japan追加labelは`--tanto`、`--ronbun`、`--koutou`です。ASCIIのまま保持します。

## Mandatory education / source / security / state gate

1. `references/common/cowork-runtime-contract.md`、
   `references/common/japan-study-routing.md`、
   `references/common/source-provenance-and-review.md`、
   `references/common/academic-integrity-and-socratic-controls.md`、
   `references/common/official-sources-and-2026-exams.md`を読みます。
2. `STUDY NOTES — NOT LEGAL ADVICE`。real client、clinic、externship、非公開の
   司法修習・事件記録なら具体的分析を停止し、approved supervised workflowまたは
   専門家へ戻します。
3. `ui_locale`と`study_legal_system`を分け、learner level、jurisdiction、
   course/exam、exam year、component、subject、electiveを解決します。不明なら
   出題前に質問し、日本語だけでJP、JPだけでMBEへdefaultしません。
4. exact syllabus、exam guide、AI policy、問題、出題趣旨、採点実感の
   source item/URL、version、page、coverage、authorizationを記録します。
5. `exam-cutoff`、`currently-effective`、`future-enacted`、`historical`、
   `pending-proposal`を分けます。
6. 実在しない判例、法令、条文、判旨、問題、出題趣旨、採点実感、引用を作りません。
7. graded/restricted/live examでは解答を開示しません。許可されたpracticeでも一問ずつ
   出し、attemptを待ってからsource付きfeedbackを示します。
8. 保存先、viewer、著作権・利用条件、個人情報、DLPを確認します。Cowork内DLP必須
   なら機密教材を投入しません。
9. state gatewayをlive preflightします。失敗時はread-only/manual sessionだけで、
   score、progress、planを保存済みとは表示しません。
10. writeはexact `itemId`、latest `eTag`、unique `idempotencyKey`、fresh human
    confirmation、append-only auditを要求します。
11. 公式採点、合否、受験申込、提出、LMS、外部投稿、scheduled tutoringを実行・
    保証しません。次問・終了・保存は学習者が選びます。

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

## Route

### Japan

次を確定します。

- `judicial-exam | preliminary-exam`
- exam year
- versioned `bar_or_exam.exam_format`
- `short-answer | essay | oral`
- actual component prerequisiteまたは`practice-only-out-of-sequence`
- judicial-exam eligibility basis/period
- subject/elective
- temporal label/asOf
- practice sourceと公開日

subject matrix、2026年の日程・CBT条件、公式sourceは
`references/exercise-contract.md`と
`references/common/official-sources-and-2026-exams.md`に従います。

司法試験はshort-answer/essayのみでoralを拒否します。短答必要成績を得た者について
短答・論文を総合してofficial合否を判定するため、essayを独立official stageと
表示しません。予備試験はactual essayにshort-answer pass、actual oralにwritten
examination passを要求します。

司法試験の修了・予備試験合格routeは各起算日から5年、在学中routeは最初に受験した
年の4月1日から修了/退学までと5年経過までの早いendpointです。current法にattempt
回数capはありません。在学中合格と司法修習生採用の課程修了要件を分けます。

すべての生成問題に次を表示します。

```text
AI作成・公式問題ではない
Mode: [exam / year / component / subject]
Exam format: [value / source version]
Component prerequisite: [status / basis]
Temporal basis: [label / asOf]
Calibrated from: [released official source/version]
```

2026-07-16時点で司法試験は実施中です。2026-07-21の公式公開前は、2026年の漏えい、
受験者の記憶・再現、試験委員情報、topic speculationを拒否し、2025年以前の
公開済み公式問題だけを使います。

短答式をMBEの四択へ機械的に変換せず、論文式をMEE、口述式を米国oral examとして
扱いません。CBT simulationは文字/page slotを守り、予備試験論文は各科目4ページ
として扱いますが、実際の試験systemや採点を再現したとは表示しません。

出題趣旨、採点実感、口述テーマは
`examType + examYear + component + subject + materialType + sourceVersion`
でqualifyし、別試験・別年度・別科目へ一般化しません。

### United States

`study_legal_system: US`の場合だけ、NextGen、traditional UBE、state-specificを
NCBEまたはjurisdiction authorityで確認します。

- traditional UBE: MBE/MEE/MPTの該当format。
- NextGen: current official subject outlineとreleased samples。
- state-specific: exact jurisdiction/component。
- majority/UBEとstate-specific ruleをrule単位でlabel。
- examに含まれないweak subjectは自動出題せず、学習目的を確認。

ruleがdivergeする場合:

```markdown
**Rule body:** [UBE/majority | jurisdiction-specific]
**Source:** [official/prep-course source/version]
**Application:** [attemptへのfeedback]
**Difference:** [verified divergence or `[VERIFY]`]
```

知らないstate ruleを作らず、exact sourceへ戻します。

### Other

法体系、exam authority、official subject list、temporal basisを取得できなければ、
structure-only practiceまたはsource取得で停止します。US/JP frameworkを代用しません。

## Session workflow

1. subject、N、component、difficulty、sourceを確認。
2. prior historyを読める場合はexact recordだけを使い、weak subtopicを重み付け。
3. 一問だけ提示し、回答を待つ。
4. reasoning、source、rule versionを確認。
5. policyが許すpracticeなら、なぜそうなるか、選択肢/論点、反対論を説明。
6. `[VERIFY]`、`[UNCERTAIN]`、`[review]`を具体的に付ける。
7. 次問へ進む前に学習者の意思を確認。

essayでは完成答案や公式模範答案を出しません。学生の答案後に、issue、source/rule、
application、counterargument、organization、time/page constraintの形成的feedbackを
示します。pass/borderline、精密score、合格可能性は出しません。

## End summary and optional persistence

```markdown
STUDY NOTES — NOT LEGAL ADVICE

# Session summary — [scope]

**Completed:** [X of N]
**Learner self-assessment:** [right / partial / wrong]
**Reasoning strengths:** [observed]
**Return to source:** [exact sections]
**Weak subtopics:** [observed, not official grade]
**Law/source versions:** [list]
**Exam format / prerequisite:** [versioned value / status]
**Temporal basis:** [label / asOf]
**Suggested next choice:** [drill / source review / stop]
```

保存を希望した場合だけ、`references/common/state-and-power-platform-contracts.md`に従い、
`scopeType: session`, `scopeId: [sessionId]`のsession-result createと、
`scopeType: user`, `scopeId: [userObjectId]`のstudy-plan updateを別operationで
確認します。study metadataは`payload`、auditでは`details`へ置きます。

## 行わないこと

- official question、official answer、official scoreと表示
- live examの漏えい・再現・予測
- JP modeをMBE/MEEへ置換
- sourceなしのrule・case・statute生成
- commercial教材の大量複製
- attempt前のanswer reveal
- plan、LMS、submission、calendar、external postの自動更新
