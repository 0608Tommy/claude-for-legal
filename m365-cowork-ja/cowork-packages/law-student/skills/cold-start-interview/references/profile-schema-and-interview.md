> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Study profile schema・interview map

## Profile

```yaml
profileType: "law-student-user-profile"
ui_locale: "ja-JP"
study_legal_system: "JP | US | other"
role: "student | graduate | judicial-trainee | self-study | other"
education_track:
  system: "JP | US | other"
  stage: "legal-profession-course | undergraduate-law | law-school | preliminary-exam | judicial-exam | judicial-training | doctrinal-study | jd | llm | bar-prep | other"
  institution: null
  law_school_track: "mishu-3-year | kishu-2-year | null"
  current_level: null
  exam_year: null
  exam_component: "short-answer | essay | oral | null"
  elective_subject: null
  judicial_training_cohort: null
jurisdiction:
  primary: null
  comparative: []
courses:
  - courseId: "[pseudonymous stable ID]"
    title: "[course]"
    term: "[term]"
    assessment_mode: "[exam/report/practice/other]"
    exam_format: "[format]"
    syllabus_item_id: null
    rubric_item_id: null
    ai_policy_item_id: null
learning:
  default_mode: "drill-me | explain-to-me"
  pushback: "light | standard | strong"
  strong: []
  weak: []
  avoided: []
outline:
  format: "traditional | statute-system | flowchart | flashcard | hybrid"
  depth: "[preference]"
writing:
  citation_style: "school-specific | japanese-2014-private-guide | bluebook | alwd | other"
bar_or_exam:
  target_date: null
  exam_type: null
  exam_format:
    value: null
    source_system: null
    source_item_id: null
    source_version: null
    verified_at: null
  component_prerequisite:
    status: "met | not-met | practice-only-out-of-sequence | unknown | not-applicable"
    basis: null
    source_item_id: null
    source_version: null
  eligibility_basis: "law-school-graduate | preliminary-exam-pass | certified-in-school | unrestricted-preliminary | other | null"
  eligibility_period:
    starts_on: null
    ends_on: null
    endpoint_rule: null
  attempt_cap:
    status: "none-within-eligibility-period | numeric | unknown | not-applicable"
    count: null
  temporal_basis:
    label: "exam-cutoff | currently-effective | future-enacted | historical | pending-proposal | null"
    as_of: null
    exam_cutoff_relation: "included | excluded-post-cutoff | not-applicable | unknown"
  prep_course: null
  prep_course_mode: "supplement | replace | null"
institution_sources:
  authorized_item_ids: []
  source_count: 0
  limited_data: true
integrations:
  sharepoint: "connected | configured-unverified | not-connected"
  onedrive: "connected | configured-unverified | not-connected"
  optional: {}
security:
  cowork_dlp_required: false
  permitted_destinations: []
review:
  source_workflow_review: pending
  japan_qualified_review: pending
```

## Interview states

`initial | resume | quick | full | redo | redo-section | check-integrations`

canonical coreの`initial | resume | quick | full | redo-section |
check-integrations`を必ず認識します。

### Quick

法体系、role、stage、law-school track、courseまたはexam、versioned
`bar_or_exam.exam_format`、component prerequisite、target date、learning mode、
AI policy pointer、minimum source pointer、DLP requirementだけを取得し、残りは
`[DEFAULT — human review required]`または`[PENDING]`。

### Full

1 turnに2～3 promptで、route、institutional track、course、assessment、
versioned exam format、component prerequisite、learning、strong/weak/avoid、
outline、writing、bar/exam、life constraints、seed materials、destination、
integrationsを取得します。documentにある情報は再入力させず、exact item/linkを求めます。

## Pause / resume

setup sessionにanswered section、pending field、source pointer、next sectionを保存します。
resume時は回答済みを再質問しません。profileとsetup sessionは別record・別writeです。

## Source intake

syllabus、rubric、AI policy、過去問、答案feedback、outline、notes、casebook、
予備校資料を対象とし、exact item/version/coverageを記録します。10未満は
`limited_data: true`。商用教材の本文をprofileへ複製しません。

学校名やcourse登録を取得しても、在籍・履修登録を検証または変更したとは表示しません。

`legal-profession-course`は制度上の法曹コースだけに使い、genericな
`undergraduate-law`と分けます。法科大学院は`mishu-3-year`または
`kishu-2-year`をinstitutional sourceで確認します。

`bar_or_exam.attempt_cap.status: numeric`の場合だけ`count`を正の整数にし、
`none-within-eligibility-period | unknown | not-applicable`では`count: null`です。
