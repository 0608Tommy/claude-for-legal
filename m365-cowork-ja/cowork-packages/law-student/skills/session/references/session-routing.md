> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Session routing・compiled behavior

Coworkでskill-to-skill dynamic executionを仮定しません。sourceのquestion routingを
本contractへcompileし、flashcardは明示的canonical handoffにします。

## Flags

JP:

- `--tanto`: short-answer
- `--ronbun`: essay
- `--koutou`: oral
- `--kian`: public/synthetic drafting exercise
- `--flashcards`: canonical `flashcards --session <n>` handoff

US:

- `--mbe`
- `--essay`
- `--flashcards`: canonical `flashcards --session <n>` handoff

flagなしではprofileのlegal system、exam/course、componentを確認し、JPでMBEへ
defaultしません。

## Versioned exam format

session開始時にprofile/planの`bar_or_exam.exam_format` objectを読みます。

```yaml
bar_or_exam:
  exam_format:
    value: "[canonical format]"
    source_system: "[official authority]"
    source_item_id: "[URL or item ID]"
    source_version: "[version/date/eTag]"
    verified_at: "[ISO-8601]"
```

valueとsource versionが欠ける、古い、矛盾する場合は質問・refreshし、sessionを
開始しません。

component prerequisite:

- judicial exam: short-answer/essayのみ。oralなし。
- preliminary essay: short-answer pass required for actual stage。
- preliminary oral: written examination pass required for actual stage。
- practice-onlyの場合はout-of-sequence labelを付ける。

## `--flashcards` canonical handoff

`session`内でdeckを読み、priority、bucket、transitionを実行しません。次のhandoffを
表示して停止します。

```yaml
handoffType: "canonical-skill"
targetSkillId: "flashcards"
targetLabel: "/law-student:flashcards"
targetMode: "--session"
subjectId: "[subject]"
count: 5
studyScopeId: "[scope]"
deckRecordId: "[exact deck record ID or null]"
reason: "fixed-count flashcard session"
```

利用者がCoworkで`flashcards`を選ぶかcanonical labelを実行します。handoffを
実行済み、deck更新済み、session開始済みと表示しません。
このhandoff objectは会話上のrouting dataであり、shared state envelopeではありません。

## Result

```yaml
payload:
  userObjectId: "[Microsoft Entra object ID]"
  sessionId: "[Cowork session ID]"
  sequence: 1
  studyScopeType: "course | exam | general"
  studyScopeId: "[scope]"
  legalSystem: "JP | US | other"
  bar_or_exam:
    exam_format:
      value: "[canonical format]"
      source_system: "[official authority]"
      source_item_id: "[URL or item ID]"
      source_version: "[official source version]"
      verified_at: "[ISO-8601]"
    attempt_cap:
      status: "none-within-eligibility-period | numeric | unknown | not-applicable"
      count: null
  componentPrerequisite:
    status: "met | practice-only-out-of-sequence | unknown | not-applicable"
  mode: "[canonical flag/mode]"
  subject: "[subject]"
  requestedCount: 10
  completedCount: 10
  selfAssessment:
    right: 0
    partial: 0
    wrong: 0
  weakSubtopics: []
  strongSubtopics: []
  sourceVersions: []
  temporalBasis:
    label: "exam-cutoff | currently-effective | future-enacted | historical | pending-proposal"
    asOf: null
    examCutoffRelation: "included | excluded-post-cutoff | not-applicable | unknown"
  academicPolicyVersion: null
```

AIのofficial scoreではなくlearner self-assessmentとobserved reasoningを分けます。

session-result create payloadと返却されたstate envelopeをround-trip比較し、
`bar_or_exam.exam_format`の`value`、`source_system`、`source_item_id`、
`source_version`、`verified_at`が全て同一であることを確認します。欠落・差異があれば
保存成功と表示せず、plan updateへ進みません。

`bar_or_exam.attempt_cap`はnullable scalarにせず、statusを必須とします。`numeric`の場合だけ
countを正の整数にし、それ以外はnullです。

## Persistence handoff

session result createは`scopeType: session`, `scopeId: [sessionId]`、
study-plan updateは`scopeType: user`, `scopeId: [userObjectId]`です。study metadataは
`payload`だけに置きます。summaryを見せ、exact plan/session item ID、latest eTag、
別idempotency keyでwriteします。plan updateを断ってもsessionは完了できます。
