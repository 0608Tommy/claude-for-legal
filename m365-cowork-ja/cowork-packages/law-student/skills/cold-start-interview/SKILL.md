---
name: cold-start-interview
description: >
  initial、resume、quick、full、redo-section、check-integrationsを会話で行い、表示言語と法体系、法曹コース・法科大学院・予備試験・司法試験・司法修習または米国route、course、AI policy、学習方法、sourceを分離したSharePoint profile/stateへ構成する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: law-student
  migration-target: admin
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Cold-start interview

旧来の正規label/flags:

- `/law-student:cold-start-interview`
- `--full`
- `--redo`
- `--redo <section>`
- `--check-integrations`

Coworkではflagを会話stateへ変換します。

## Mandatory education / source / security / state gate

1. `references/common/cowork-runtime-contract.md`、
   `references/common/japan-study-routing.md`、
   `references/common/source-provenance-and-review.md`、
   `references/common/academic-integrity-and-socratic-controls.md`、
   `references/common/state-and-power-platform-contracts.md`を読みます。
2. 学習用profileです。real client、clinic、externship、非公開司法修習の事実・sourceを
   profileへ保存しません。
3. `ui_locale`と`study_legal_system`を別fieldにし、learner level、jurisdiction、
   course/exam modeを明示的に取得します。日本語を理由に日本法へ固定しません。
4. syllabus、rubric、AI policy、教材はexact item/version/coverage/authorizationを
   記録します。法令・試験日等のlegal factはofficial sourceで確認します。
5. `exam-cutoff`、`currently-effective`、`future-enacted`、`historical`、
   `pending-proposal`を別fieldにします。
6. 実在しない学校policy、case、statute、試験科目、日程、qualificationを作りません。
7. graded/restricted/live examの支援範囲をprofileに明記し、answer reveal guardrailを
   解除しません。
8. user identity、destination、retention、DLP、商用教材利用条件を確認します。
9. tenant-approved gateway、exact profiles/state/audit IDs、ACL、conditional writeを
   live preflightします。失敗時はsession内profile draftだけで「setup完了」と
   表示しません。
10. create/updateを分け、exact `itemId`、latest `eTag`、unique
    `idempotencyKey`、diff、fresh confirmation、append-only auditを使います。
11. enrollment、受験資格認定、受験申込、LMS、提出、external post、scheduled
    tutoringを実行・保証しません。

日本法・日本の法曹養成内容はDRAFTで、有資格者review pendingです。

### 共通必須事項（本文全体に適用）

- setup outputも`STUDY NOTES — NOT LEGAL ADVICE`の教育目的を外れません。
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

## 会話state

| state | intent |
|---|---|
| `initial` | profileなし。quick/fullを選ぶ |
| `resume` | paused setupのpendingだけ再開 |
| `quick` | minimum viable profile |
| `full` | full interview + source intake |
| `redo` | 全profileをdiff review |
| `redo-section` | 1 sectionだけ |
| `check-integrations` | live probe結果だけ |

canonical core:
`initial | resume | quick | full | redo-section | check-integrations`。

profileなし→`initial`、paused setup→`resume`、populated profile→明示的redo/check以外で
上書きしません。duplicate/conflicting recordはfail closedです。

## Orientation

3～4行で説明します。

- 学生自身の読解・執筆を支えるlearning mode。
- quick約2分、full約10～15分、pause/resume可能。
- 法体系、学習段階、institutional track、versioned exam format、
  course/exam、learning style、sourceを設定。
- 日本法内容はreview pending、gatewayなしは保存しない。

quick/fullを選んでもらい、自動でdrillを開始しません。

## Interview pacing

- 1 turnに2～3 answerable prompt。
- documentにある情報はexact SharePoint item/linkを先に求める。
- typed answer/uploadが必要なら待つ。
- pause時はsetup sessionへanswered/pending/next sectionを保存。
- resumeでanswered sectionを再質問しない。
- pre-saveでpending/default/source gapを一覧化。

## Quick

最低限:

- `ui_locale`
- `study_legal_system`
- roleとeducation stage
- institution/courseまたはexam
- JPなら`legal-profession-course`と`undergraduate-law`を分け、法科大学院は
  `mishu-3-year | kishu-2-year`
- JPなら予備試験、司法試験、司法修習の該当route
- USならJD/LLM/bar、jurisdiction
- versioned `bar_or_exam.exam_format` object
- target date、component、component prerequisite、eligibility basis、elective
- learning mode
- syllabus/rubric/AI policy pointer
- storage/integration live status
- destination/DLP requirement

未設定は`[DEFAULT — human review required]`または`[PENDING]`で、影響を説明します。

## Full

`references/profile-schema-and-interview.md`に従い、次を取得します。

1. role、法体系、学習段階、institution、institutional track。
2. current courses、term、assessment、format、syllabus。
3. exam year/date、versioned exam format、component/prerequisite、
   eligibility basis/period、elective/cohort。
4. drill-me/explain-to-me、pushback。
5. strong、weak、avoided。
6. outline format/depth、citation style。
7. prep courseとsupplement/replace。
8. life constraintsとrealistic hours。
9. seed materials。
10. AI policy、destination、DLP、integrations。

`legal-profession-course`をgeneric undergraduateへ適用せず、法科大学院の
`mishu-3-year`/`kishu-2-year`を学校sourceで確認します。JP routeにT1～T4、
1L/2L/3L、MBE weak subjectsを要求しません。US routeではsource
pluginの該当fieldを保持します。situationがboxに合わなければfree-formで取得し、
adapted/empty fieldを明示します。

司法試験はshort-answer/essayだけで、予備試験はshort-answer→essay→oralのactual
prerequisiteを保存します。practice-only out-of-sequenceとofficial stageを
混ぜません。司法試験在学中受験は所定単位、1年以内の修了見込み、学長認定、
受験期間の早いendpoint、attempt capなし、司法修習生採用時の課程修了要件を
exact sourceで取得します。

## Academic reminder

一度だけ短く伝えます。

- graded workは学校・course・教員のAI policyを先に確認。
- study tool outputを提出しない。
- real client/clinic/externship/修習recordを入力しない。
- live exam情報を扱わない。

## Source intake

syllabus、rubric、AI policy、outline、graded feedback、公開済み過去問、notes、
casebook、予備校資料を対象にします。exact item/version/pagesと利用権限を記録し、
商用本文をprofileへ複製しません。source 10件未満は`LIMITED DATA`相当を付けます。

## Integration check

SharePoint、OneDrive、optional Slack/Google Drive/CourtListener/Descrybeをlive
probeします。

- `connected`: probe success
- `configured-unverified`: declaration only
- `not-connected`: missing/failed

CourtListenerを日本法source verificationに使いません。connector declarationだけで
connectedと表示しません。`--check-integrations`は他fieldを変更しません。

## Pre-save / save

表示:

- confirmed/document-derived/interview-derived/default/pending
- source/version/coverage
- legal system、versioned exam format、component prerequisite
- temporal label: exam-cutoff/currently-effective/future-enacted/historical/pending-proposal
- academic policy status
- destination/DLP
- create vs update
- source workflow/Japan review pending

required fieldがopenならpausedです。setup sessionは`scopeType: session`,
`scopeId: [sessionId]`で、study metadataを`payload`へ入れます。profileとsetup
sessionを別writeし、success後に
exact IDs、eTag、idempotency、audit outcomeを示します。

## Complete

route、courses/exam、learning mode、source coverage、connections、pending、DLPを
短く示し、次のskillを候補として提示します。利用者が選ぶまで実行しません。

## 行わないこと

- local profile/cache/historyの探索・copy
- placeholder/defaultをcompleteと表示
- JPとUSのeducation/exam fieldを偽って同一化
- connector declarationをconnectedと表示
- gatewayなしに保存済みと表示
- enrollment/eligibilityを認定
- review pendingを解除
- first drillを自動開始
