---
name: session
description: >
  subjectとfixed countを確認し、日本routeの短答・論文・口述・起案または米国routeのMBE・essayを一問ずつ実施する。--flashcardsはcanonical flashcards --sessionへの明示的handoffとし、結果保存はaudited study-plan handoffへ分離する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: law-student
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Focused session

旧来のlabel:
`/law-student:session <subject> <n> [--mbe | --essay | --flashcards]`。

Japan追加flags:
`--tanto | --ronbun | --koutou | --kian`。

## Mandatory education / source / security / state gate

1. `references/common/cowork-runtime-contract.md`、
   `references/common/japan-study-routing.md`、
   `references/common/source-provenance-and-review.md`、
   `references/common/academic-integrity-and-socratic-controls.md`、
   `references/common/state-and-power-platform-contracts.md`を読みます。
2. `STUDY NOTES — NOT LEGAL ADVICE`。real matter、client、live/restricted exam、
   非公開修習recordなら具体的sessionを停止します。
3. legal system、learner level、jurisdiction、course/exam、versioned
   `bar_or_exam.exam_format`、component/prerequisite、subject、N、methodを
   解決します。JP routeで`--mbe`をdefaultにしません。
4. exact source、version、coverage、AI policyとprior session/plan recordを確認します。
5. ruleごとに`exam-cutoff`、`currently-effective`、`future-enacted`、
   `historical`、`pending-proposal`を分けます。
6. 実在しないquestion、case、statute、holding、citationを作りません。
7. 一問ずつ出し、attemptを待ちます。graded/restricted/live promptのanswerを
   開示しません。
8. destination、viewer、commercial source、personal data、DLPを確認します。
9. gateway failure時はsession内だけ。result/plan/deckを保存済みと表示しません。
10. writeはexact ID/eTag/idempotency、fresh confirmation、audit。session resultと
    plan/deck updateは別operationです。
11. official score、grading、submission、LMS、external post、scheduled tutoringを
    実行・表示しません。

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

## Compiled routing

Coworkで他skillを動的にload/executeできるとは仮定しません。
`references/session-routing.md`へquestion routingをcompileし、`--flashcards`は
canonical `flashcards --session <n>`への明示的handoffにします。

### JP

- `--tanto`: exam/component/subject matrixとofficial exam formatを確認した短答演習。
- `--ronbun`: judicial/preliminaryを分け、actual prerequisiteを確認してpromptを
  一つ提示し、学生答案後に形成的feedback。
- `--koutou`: 予備試験だけ。written examination passをactual prerequisiteとして
  確認し、民事・刑事実務基礎を一問ずつ。
- `--kian`: 公開・synthetic素材だけ。実在の修習・事件recordは禁止。
- `--flashcards`: deck/cardをsession内で処理せずcanonical handoffを表示して停止。

司法試験はshort-answer/essayのみでoralを拒否します。予備試験のout-of-sequence
practiceは`practice-only-out-of-sequence`と表示し、official stageへ保存しません。

### US

- `--mbe`: traditional UBEの場合だけclassic MBE。NextGenならcurrent released
  sample formatへroute。
- `--essay`: UBE/NextGen/state-specificのexact format。
- `--flashcards`: canonical handoffのみ。

flagなしではprofile/course/examから候補を示し、人に選んでもらいます。

`bar_or_exam.exam_format.value`、source item、source version、verified timeのいずれかが
欠ける、古い、またはexam/componentと矛盾する場合はsessionを開始せずrefreshします。

### Explicit `--flashcards` handoff

`references/session-routing.md`のhandoff objectを表示し、利用者に
`/law-student:flashcards [subject] --session <n>`またはCoworkの`flashcards` skillを
選んでもらいます。handoff後のdeck read、prioritization、bucket transition、
session resultは`flashcards`が所有します。本skillは実行済みと表示しません。

## Start

subjectまたはNがない場合:

> どの法体系・course/examの、どの科目を、何問、どのmethodで行いますか。

prior session historyを使う場合、exact scopeだけを読みます。weaknessはlearner
self-assessmentとobserved missを区別し、別course/examからcarryしません。

## Per-item flow

1. question modeでは一問だけ提示。flashcards modeはhandoffで停止。
2. 回答を待つ。
3. reasoning/source alignmentを確認。
4. policyが許せばfeedbackを表示。
5. self-assessmentを取得。
6. 次へ進むか、sourceへ戻るか、終了するかを聞く。

論文・起案では完成answerを書かず、学生のattempt後にissue、source/rule、
application、counterargument、organizationを返します。口述では質問をまとめて
提示しません。

## End summary

`references/session-routing.md`のschemaで、requested/completed count、
self-assessment、strong/weak reasoning、exam formatの`value`、`source_system`、
`source_item_id`、`source_version`、`verified_at`、component prerequisite、
explicit attempt-cap status/count、temporal basis、next choicesを示します。

scoreが必要なmultiple-choiceでもlearner self-assessmentとcorrect-key sourceを
表示し、学校・試験機関のofficial gradeとは表示しません。

## Persistence handoff

保存を選んだ場合:

1. summaryを確認。
2. `scopeType: session`, `scopeId: [sessionId]`でsession-resultをconditional create。
3. `scopeType: user`, `scopeId: [userObjectId]`のstudy-plan priority/schedule updateは
   別confirmation。
4. create payloadと返却state envelopeの`bar_or_exam.exam_format`全5 fieldを
   round-trip比較し、欠落・差異なら停止。
5. `bar_or_exam.attempt_cap.status`を必須とし、`numeric`の場合だけ正の整数countを許可。
6. study metadataは`payload`、auditでは`details`へ入れる。
7. exact item IDs/eTags/idempotency/audit resultを表示。

plan writerが未導入ならmanual summaryだけです。session終了を理由に自動updateしません。

## 行わないこと

- dynamic skill executionが成功したと表示
- `--flashcards` handoff後にdeck/sessionが実行済みと表示
- JP modeのMBE default
- N問をまとめてanswer付きで提示
- official score/grade/pass estimate
- real judicial-training recordの利用
- session終了時の暗黙save
- scheduled next session、calendar、LMS、external post
