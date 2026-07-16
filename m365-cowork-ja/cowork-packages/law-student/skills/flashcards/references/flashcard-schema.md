> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Flashcard schema

```yaml
cardId: "[stable ASCII ID]"
subjectId: "[scope subject ID]"
legalSystem: "JP | US | other"
examOrCourse: "[scope]"
question: "[one concept]"
answer: "[short answer]"
source:
  sourceSystem: "[system]"
  sourceItemId: "[item or official URL]"
  sourceVersion: "[eTag/version/date]"
  section: "[page/article/section]"
  provenance: "[tag]"
temporalBasis:
  label: "exam-cutoff | currently-effective | future-enacted | historical | pending-proposal"
  asOf: "[date or null]"
  examCutoffRelation: "included | excluded-post-cutoff | not-applicable | unknown"
translationAuthority: "original-japanese | non-authoritative-translation | not-applicable"
bucket: "new | learning | review | mastered"
lastReviewed: null
nextReview: "[planning date, not scheduled notification]"
attempts:
  right: 0
  partial: 0
  wrong: 0
status: "draft | source-checked | retired"
```

一card一concept、frontはquestion、backは短いrule/sequenceです。日本法令cardは
law ID、条文、version、temporal label/asOfを持ち、外国語訳をauthoritativeにしません。
判例cardはcase identification metadataとしてcourt/date/event number/sourceを
持ちますが、rendered citationへ事件番号を自動挿入しません。source不足をtarget
countで埋めません。

exam cutoff後に施行され現在有効なruleは`currently-effective`かつ
`examCutoffRelation: excluded-post-cutoff`です。未施行の場合だけ
`future-enacted`です。

Leitner候補:

| self-assessment | bucket | next review plan |
|---|---|---|
| right | 1段階上 | new +1d / learning +3d / review +7d / mastered +21d |
| partial | 同じ | +1d |
| wrong / don't know | 1段階下 | +4h候補 |

日付は学習計画値で、reminder、scheduled tutoring、calendar登録ではありません。
bucket更新はsummary確認後のconditional writeです。
