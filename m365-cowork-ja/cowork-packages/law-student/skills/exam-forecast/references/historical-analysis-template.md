> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 過去問分析・学習配分template

## National examination

`exam-forecast`を無効化し、公開済み公式問題の記述統計だけを示します。

```markdown
STUDY NOTES — NOT LEGAL ADVICE

# 過去問分析・学習配分 — [exam / component / years]

**公式問題:** [N年 / exact URLs]
**Source coverage:** [全問 / subset / 未読]
**Temporal basis:** [year-specific exam-cutoff / other labels]
**Evaluation materials:** [examType/year/component/subject/materialType/sourceVersion]

| topic / format | observed count | denominator | source years | unknown |
|---|---:|---:|---|---|

## 観測できる形式
[時間、page、設問構造、出題趣旨で明示された観点]

## 現在のsyllabus・弱点との対応
[学習時間配分候補。予測ではない]

## 分からないこと
[将来の出題、未公開問題、sample bias]
```

試験委員の研究、受験者再現、commercial prediction、live exam情報を使いません。

## School examination

supplied past papersからformat、topic share、question type、fact density、
policy/doctrine、observed trapを数えます。3未満はthin sample。professorの
「hobby horse」やlikely questionと書かず、観測値とunknownを分けます。

出題趣旨、採点実感、口述テーマはexam/year/component/subjectを跨いでrubric化
しません。
