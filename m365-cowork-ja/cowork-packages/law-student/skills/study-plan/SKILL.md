---
name: study-plan
description: >
  日本の司法試験・予備試験、法科大学院試験、semester、司法修習の公開範囲または米国barについて、公式日程、法令基準日、科目、弱点、生活制約、学習方法を確認し、実行可能なplanを作成・更新するPower Platform front end。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: law-student
  migration-target: power-platform
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Study plan

旧来の正規label/flags:
`/law-student:study-plan [--build | --update | --status | --cram]`。

## Mandatory education / source / security / state gate

1. `references/common/cowork-runtime-contract.md`、
   `references/common/japan-study-routing.md`、
   `references/common/source-provenance-and-review.md`、
   `references/common/academic-integrity-and-socratic-controls.md`、
   `references/common/official-sources-and-2026-exams.md`、
   `references/common/state-and-power-platform-contracts.md`を読みます。
2. `STUDY NOTES — NOT LEGAL ADVICE`。real matter、client、非公開修習recordをplanへ
   入れません。
3. legal system、learner level、jurisdiction、course/exam、year、versioned
   `bar_or_exam.exam_format`、component/prerequisite、target dateを解決します。
4. official schedule/subject/temporal basis、syllabus、AI policy、prior plan/sessionの
   exact source/version/coverage/authorizationを記録します。
5. `exam-cutoff`、`currently-effective`、`future-enacted`、`historical`、
   `pending-proposal`を分けます。
6. 実在しないexam date、subject、weighting、high-yield frequency、school policyを
   作りません。
7. planはgraded answerを生成せず、live exam topicを予測しません。
8. destination、viewer、personal schedule、health/family data、DLPを確認し、
   life contextは必要最小限だけ取得します。
9. gatewayとapproved flowをlive preflight。失敗時はmanual plan draftだけで、
   plan/status/session historyを保存済みと表示しません。
10. writeはexact ID/eTag/idempotency、diff、fresh confirmation、audit。plan create、
    session history、schedule updateを分けます。
11. calendar、reminder、scheduled tutoring、LMS、enrollment、submission、
    external postを実行・保証しません。

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

## Modes

- `--build`: planなし、または明示的new plan。
- `--update`: confirmed historyを読み、priorityと次の期間を提案。
- `--status`: 今日/今週のplan data、未実施、source staleをread-only表示。
- `--cram`: learnerが明示した短期集中。予測ではなくcoverage tradeoffを示す。

defaultはrecordの有無から候補を示し、人に選んでもらいます。

## What are we planning for

1. 司法試験
2. 司法試験予備試験
3. 法科大学院・学部の試験
4. semester study cadence
5. 司法修習の公開・synthetic課題
6. US bar
7. other

`references/study-plan-schema.md`を使います。

## Inputs — one at a time

1 turnに一問、回答を待ちます。

- official exam/course date
- versioned exam format
- component、actual prerequisite status、subjects、elective
- judicial-exam eligibility basis/periodまたはpreliminary unrestricted entry
- explicit `bar_or_exam.attempt_cap.status`。`numeric`の場合だけ正の整数count
- exact syllabus/official scope
- strongest/weakest/avoided
- realistic hours/week
- job、family、commute、health、clinic等のlife constraint
- preferred methods
- rest days
- prep course
- source availability

life contextの共有を断られた場合は尊重し、
`Life-context check declined; hours are unverified`をconfidence flagにします。
健康・家族detailを保存しません。

## Japan planning

official 2026 dates、subject、CBT、exam format、component prerequisite、
temporal basisは
`references/common/official-sources-and-2026-exams.md`を毎回確認します。

- legal-profession-courseとgeneric undergraduateを別plan scope。
- law school: `mishu-3-year | kishu-2-year`、term、syllabus、actual assessment。
- preliminary exam: short-answer→essay→oralのactual prerequisiteを別phase。
- judicial exam: short-answer/essay、短答threshold後の総合判定、elective、CBT
  constraint。oral phaseを作らない。
- judicial training: public/synthetic素材だけ。

MBE frequency、Barbri schedule、US high-yieldをJP planへ使いません。過去問frequencyを
使う場合、official released set、count、denominator、yearsを明示し、predictionとは
表示しません。

## US planning

NextGen/UBE/state-specific、jurisdiction、official subject listを確認します。
structured prep course利用時は:

1. `supplement`: prep courseがprimary。weak-area drillだけ追加。
2. `replace`: full planを作り、course calendarと二重運用しない。

両方を同時にfull curriculumとして組みません。

## Build phases

exact weeks-to-examを計算し、状況に応じて:

- foundation / source learning
- synthesis / outlining
- practice / drill
- review / weak-topic repair
- taper / rest

を使います。weak subjectはconfirmed evidenceに基づき多く配分し、strong subjectも
完全には除外しません。最初の1～2週をday-by-day、それ以降は週単位候補にできます。
休養とslackを入れます。

`--cram`ではfull coverageができないことを明示し、official scopeと本人のweaknessから
tradeoff optionsを出します。「必ず出る」「high yieldだから捨てる」とは言いません。

## Confirm before write

保存前に:

```markdown
STUDY NOTES — NOT LEGAL ADVICE

**Scope:** [exam/course]
**Exam format:** [value / source item / source version / verified time]
**Component prerequisite:** [status / basis]
**bar_or_exam.attempt_cap:** [none-within-eligibility-period / numeric N / unknown / not-applicable]
**Official dates / temporal basis:** [source/version/label/asOf]
**Hours:** [weekly / days / life-context status]
**Phases:** [summary]
**Weakness evidence:** [self-report / confirmed session]
**First period:** [summary]
**Confidence flags:** [unknowns]
```

too ambitious / too light / missing subjectを確認し、調整後にwriteします。

## Update

confirmed session historyだけを使います。

- repeated difficultyはpriority candidate。
- source staleはcontent drill前にrefresh。
- missed sessionsは怠慢と推測せず、hours/coverageを再確認。
- aheadならdeeper practiceをoptionとして提示。

session result createとplan priority/schedule updateを別confirmationにします。
session resultは`scopeType: session`, `scopeId: [sessionId]`、planは
`scopeType: user`, `scopeId: [userObjectId]`です。study metadataは`payload`、
audit scope/study metadataは`details`へ置きます。

## Power Platform boundary

本skillはfront endです。approved `study-source-reader`、`study-state-writer`、
`study-audit-writer`が必要です。solution ID/version/owner/scope/last runの証拠がない
場合、「automation」「scheduled」と表示しません。

create/update/state envelope/audit例は
`references/common/state-fixtures.md`のschema-valid fixtureに従います。

planのdate/timeはdataで、Outlook event、notification、tutoring sessionを作りません。

## 行わないこと

- pass guarantee、exam prediction
- JP planへのMBE/US prep-course default
- official countなしのhigh-yield claim
- life constraintsを無視した過大plan
- prep courseとfull parallel curriculum
- gatewayなしのplan保存
- calendar、reminder、LMS、scheduled tutoringの自動化
