> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 法体系・学習段階・試験mode routing

## 独立したprofile dimensions

```yaml
ui_locale: "ja-JP"
study_legal_system: "JP | US | other"
education_track:
  system: "JP | US | other"
  stage: "legal-profession-course | undergraduate-law | law-school | preliminary-exam | judicial-exam | judicial-training | doctrinal-study | jd | llm | bar-prep | other"
  law_school_track: "mishu-3-year | kishu-2-year | null"
  exam_component: "short-answer | essay | oral | null"
  exam_year: 2026
  elective_subject: null
  judicial_training_cohort: null
institution_sources:
  syllabus_item_ids: []
  grading_rubric_item_ids: []
  ai_policy_item_ids: []
citation_style: "school-specific | japanese-2014-private-guide | bluebook | alwd | other"
bar_or_exam:
  exam_type: "judicial-exam | preliminary-exam | nextgen | traditional-ube | state-specific | course-specific | other | null"
  exam_format:
    value: "judicial-exam-short-answer-and-essay | preliminary-exam-short-answer-essay-oral-sequential | nextgen | traditional-ube | state-specific | course-specific | other"
    source_system: "[official authority]"
    source_item_id: "[URL or item ID]"
    source_version: "[version/date/eTag]"
    verified_at: "[ISO-8601]"
  attempt_cap:
    status: "none-within-eligibility-period | numeric | unknown | not-applicable"
    count: null
temporal_basis:
  label: "exam-cutoff | currently-effective | future-enacted | historical | pending-proposal"
  as_of: null
  exam_cutoff_relation: "included | excluded-post-cutoff | not-applicable | unknown"
```

`ui_locale`は表示言語、`study_legal_system`は実体法・試験制度です。別々に解決します。

## Resolution order

1. requestの明示的な法体系・試験・course。
2. exact study scope binding。
3. user study profile。
4. tenant default。
5. なお不明なら質問。言語、氏名、学校名だけで推測しない。

同じsessionでJP/US/otherが混在する比較法は、propositionごとに法体系をlabelします。

## 日本route

- `legal-profession-course`: 文部科学省制度上の法曹コース。genericな法学部・
  undergraduate studyと区別し、連携先法科大学院、course認定、institutional
  curriculumのexact sourceを確認する。
- `undergraduate-law`: 法曹コースではない一般の学部法学・法学科目。法曹コースの
  short-trackや法科大学院進学routeを自動適用しない。
- `law-school`: 法科大学院。institutional trackを`mishu-3-year`または
  `kishu-2-year`で記録し、一般的な「未修/既修」だけや米国の学年で代用しない。
- `preliminary-exam`: 予備試験。短答、論文、口述を分離。
- `judicial-exam`: 司法試験。短答、論文、選択科目、試験年を分離。
- `judicial-training`: 公開・synthetic教材だけ。実在の修習記録、事件、当事者情報を
  入れない。
- `doctrinal-study`: 一般学習。目的、法域、教材を先に確認。

日本の答案scaffoldは必要に応じて
`論点提示 → 法源・規範 → あてはめ・反対論 → 結論`を使えますが、公式に定められた
唯一の書式とは表示しません。学校rubric、法務省の出題趣旨・採点実感が優先します。

## Exam formatとcomponent prerequisite

`bar_or_exam.exam_format`はscalarではなく、value、official source item、
source version、verification timeを持つversioned objectです。profile、
customize、study-plan、sessionで同じobjectを使い、古いformatを黙って再利用しません。

`bar_or_exam.attempt_cap.status`はnullable scalarにしません。司法試験の確認済み
current ruleは`none-within-eligibility-period`、source未確認は`unknown`です。
`numeric`の場合だけ`count`へ正の整数を入れ、それ以外は`count: null`です。

### `judicial-exam`

- `exam_format.value: judicial-exam-short-answer-and-essay`
- componentは`short-answer | essay`だけ。`oral`を拒否。
- 司法試験は短答式と論文式による同一試験で、短答式の必要成績を得た者について
  両成績を総合して合否判定する。essayを独立したofficial stageとして表示しない。
- eligibility basisは`law-school-graduate | preliminary-exam-pass |
  certified-in-school`のexact sourceを必要とする。

### `preliminary-exam`

- `exam_format.value: preliminary-exam-short-answer-essay-oral-sequential`
- 最初の短答式には学歴・回数による受験資格制限を設定しない。
- actual essay stageはshort-answer passがprerequisite。
- actual oral stageはwritten examination passがprerequisite。
- out-of-sequence practiceは可能だが`practice-only-out-of-sequence`と明示し、
  official stage eligibility、pass、registrationへ保存しない。

## 米国route

`study_legal_system: US`を明示した場合だけ、source pluginのJD/LLM、1L/2L/3L、
NextGen、traditional UBE、state-specific、MBE/MEE/MPT、Bluebook/ALWD、
prep-course supplement/replace logicを使います。exam formatとjurisdictionを
NCBE/jurisdiction authorityで確認し、majority/UBEとstate-specific ruleを分けます。

## False-equivalence禁止

| 米国概念 | 日本routeでの扱い |
|---|---|
| 1L/2L/3L JD | `mishu-3-year`、`kishu-2-year`、`legal-profession-course`と同義にしない |
| UBE/NextGen/state bar | 日本の司法試験は全国試験で、資格・科目・修習が別 |
| MBE | 司法試験・予備試験の短答式と同義にしない |
| MEE | 日本の論文式と同義にしない |
| bar passage = lawyer | 司法試験合格、司法修習生採用、修習・司法修習生考試、弁護士資格、日弁連登録を分ける |
| IRAC mandatory | 日本答案の公式必須headingとは表示しない |
| Bluebook/ALWD | assignmentが選んだ場合だけ |
| party-name citation | 日本の裁判例識別へ強制しない |
| common-law portable rule | 法令、裁判所階層、判旨、事案の射程を分析 |
| cold-call culture | 実際のsyllabus・指定教材・授業方法を優先 |

## Canonical labels

skill ID、slash command、flagはASCIIのままです。日本routeのsession flags:

- `--tanto`: 短答式
- `--ronbun`: 論文式
- `--koutou`: 口述式
- `--kian`: 公開・synthetic素材による起案

米国routeでは`--mbe`、`--essay`、`--flashcards`等を保持します。JP routeで
`--mbe`をdefaultにしません。

## Judicial training・資格・登録

- 在学中受験資格で司法試験に合格した者は、司法修習生採用に法科大学院課程の
  修了要件が別途ある。試験合格の有効性と採用資格を混同しない。
- 裁判所法上、少なくとも1年の修習後に司法修習生考試へ合格すると修習を終える。
- 弁護士法上、司法修習を終えることは弁護士となる資格を得る段階。
- 弁護士として活動するには、さらに所属予定弁護士会を経て日本弁護士連合会の
  弁護士名簿へ登録される必要がある。資格取得を登録済み・弁護士就業開始と
  表示しない。
