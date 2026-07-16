> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Study plan schema

```yaml
payload:
  userObjectId: "[Microsoft Entra object ID]"
  studyScopeType: "course | exam | general"
  studyScopeId: "[scope]"
  legalSystem: "JP | US | other"
  planType: "judicial-exam | preliminary-exam | law-school-exam | semester | judicial-training | us-bar | other"
  examYear: null
  examComponent: null
  bar_or_exam:
    exam_format:
      value: null
      source_system: null
      source_item_id: null
      source_version: null
      verified_at: null
    attempt_cap:
      status: "none-within-eligibility-period | numeric | unknown | not-applicable"
      count: null
  componentPrerequisite:
    status: "met | not-met | practice-only-out-of-sequence | unknown | not-applicable"
    basis: null
  examDate: null
  temporalBasis:
    label: "exam-cutoff | currently-effective | future-enacted | historical | pending-proposal"
    asOf: null
    examCutoffRelation: "included | excluded-post-cutoff | not-applicable | unknown"
  createdAt: "[ISO-8601]"
  lastUpdatedAt: "[ISO-8601]"
  hoursPerWeek: 0
  daysPerWeek: 0
  lifeContextChecked: false
  restDays: []
  prepCourse: null
  prepCourseMode: "supplement | replace | null"
  phases:
    - name: "[foundation | synthesis | practice | review | taper]"
      start: "[date]"
      end: "[date]"
      focus: []
  subjects:
    - subjectId: "[ASCII ID]"
      priority: "high | medium | low"
      evidence: "[self-report/session history/source]"
      weeklyMinutes: 0
      methods: []
  schedule:
    - date: "[date]"
      sessions:
        - subjectId: "[ID]"
          method: "[method]"
          durationMinutes: 0
          count: null
  sessionHistoryRefs: []
  confidenceFlags: []
```

JP examは法務省のexact official dates、component、subject、versioned exam format、
component prerequisite、temporal basisを使います。
「high yield」は公開問題の明示的なsample/countなしに使いません。live examのtopicを
予測しません。

hoursはjob、family、commute、health、clinic等の生活制約を確認し、持続可能性を
優先します。prep course利用時はsupplementかreplaceの一方です。

scheduleは学習計画であり、Outlook予定、通知、scheduled tutoring、LMS assignment、
自動sessionではありません。
