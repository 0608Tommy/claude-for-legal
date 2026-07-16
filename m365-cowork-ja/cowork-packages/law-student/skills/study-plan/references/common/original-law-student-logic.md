> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 移行元law-studentの教育workflow

本書は移行元の教育上の意図をCoworkで失わないためのbehavior inventoryです。
local filesystem、Claude-specific agent/hook、unsupported frontmatterは移しません。

## 共通core

- learning modeであり、学生の読解・執筆・判断を置き換えない。
- real matterを検知したらstudy hypotheticalへ戻すか、適切な専門家・監督workflowへ
  redirectする。
- 全study outputは`STUDY NOTES — NOT LEGAL ADVICE`。
- school honor codeとprofessor/course AI policyを確認する。
- `drill-me`と`explain-to-me`を選べるが、どちらもgraded workを書かない。
- sourceがないrule、case、citationを創作せず、`[VERIFY]`、`[UNCERTAIN]`、
  `[GAP]`を使う。
- large inputのcoverageを明示する。
- uncertaintyは黙って埋めず、sourceへ戻す。

## Skill behavior

### `cold-start-interview`

initial/resume/quick/full/redo-section/check-integrationsを保ち、role、学習段階、
course、exam、learning style、strong/weak/avoid、outline preference、seed
materials、integrationを段階的に取得します。pause/resumeと`LIMITED DATA`相当の
source coverage flagを維持します。CoworkではSharePoint profile/stateへ移します。

### `customize`

profileを一度に1変更し、current value、new value、downstream impact、consistency、
confirmationを示します。section削除ではなくarchiveを提案し、learning/academic
guardrailを解除しません。

### `socratic-drill`

一問ずつ質問し、回答を待ち、理由が粗ければpush backし、誤答ならnarrowし、
基礎ruleが出なければ教材へ戻します。学生自身の資料との矛盾はexact quoteを示して
本人に解決させます。

### `case-brief`

学生が読んだ内容からfacts、procedural posture、issue、holding/判旨、reasoning、
rule/scope、notesを埋めるscaffoldです。case nameだけから完成briefを書きません。
原文がある場合はcourt自身の言葉をexact quoteとして指し示せます。

### `outline-builder`

syllabus・既存outlineからtopic tree、subtopic、case/exception slotを作り、学生の
notes・casebook・briefから内容を入れます。sourceがなければ`[GAP]`。既存formatを
優先し、完成outlineをAI知識だけで作りません。

### `bar-prep-questions`

exam type、jurisdiction、component、tested subjectsを最初に確認し、weak topicと
historyを重み付けします。一問ずつ出題し、attempt後にruleと選択肢の理由を示します。
米国routeではNextGen、traditional UBE、state-specificを分け、majority/UBEと
state ruleのdivergenceをrule単位でlabelします。

### `flashcards`

`--generate | --drill | --review | --stats | --session <n>`を保持します。
一card一concept、frontはquestion、backは短いrule、sourceを必須とし、Leitner風の
new/learning/review/masteredとreview dateを使います。source不足をcard数で埋めません。

### `study-plan`

bar、school exam、semesterを分け、exam date、subjects、strength/weakness、
realistic hours、life constraints、methods、days offを一問ずつ確認します。
prep course利用時はsupplement/replaceを選び、二重curriculumを避けます。
phase、day-by-day first stretch、adaptive priorityを作りますが自動実行しません。

### `session`

subject、N、methodを解決し、N問を一問ずつ行い、miss、weak subtopic、prior pattern、
next recommendationをまとめます。question routingをskill-localにcompileし、
`--flashcards`はcanonical `flashcards --session <n>`への明示的handoffにします。
保存はaudited plan handoffへ分離します。

### `irac-practice`

student-providedまたはskill-generated practice hypoに対し、issue、rule、
application、conclusion、organizationの形成的feedbackを出します。全文rewrite、
model answer、精密点数を出しません。pattern trackerは本人確認後だけ更新します。

### `legal-writing`

draftを全体から読み、memo/brief/paper/exam essay等のtypeを確認し、structure、
analysis depth、clarity、citationの順でfeedbackします。本文を書き直さず、
genericなstructural exampleを最大1～2個だけ示します。

### `cold-call-prep`

指定reading、syllabus、notesからfacts、holding/判旨、reasoning、application、
policyの質問を作り、Socraticに演習します。professor名・傾向を勝手に推測せず、
「聞かれそう」と断定しません。

### `exam-forecast`

past examのformat、topic coverage、question style、density、trap、policy/doctrineを
観測し、sample sizeとcurrent syllabusを併記します。日本の全国試験ではforecastを
無効化し、学校試験でも観測されたpatternだけを示します。

## Source marker

移行元の`argument-hint`はtarget frontmatterから除き、canonical ASCII label/flagを
本文に保持します。source pluginにはagentがなく、hookは空です。よって本packageは
agent、hook、schedulerを提供すると主張しません。

## Target audit corrections

- `legal-profession-course`とgeneric `undergraduate-law`を分ける。
- 法科大学院は`mishu-3-year | kishu-2-year`をinstitutional trackとして使う。
- versioned `bar_or_exam.exam_format`をsetup/customize/plan/sessionで共有する。
- 司法試験と予備試験のcomponent prerequisiteを分ける。
- saved progressはshared `scopeType`/`scopeId` schemaへ正確に合わせる。
- temporal basisは`exam-cutoff | currently-effective | future-enacted |
  historical | pending-proposal`。
- citation metadataとverification metadataを分ける。
