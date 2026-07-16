> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Examination exercise contract

## Japan

最初に`preliminary-exam | judicial-exam`、exam year、versioned
`bar_or_exam.exam_format`、`short-answer | essay | oral`、subject、elective、
temporal basisを確定します。

component gate:

- `judicial-exam`: `short-answer | essay`だけ。短答必要成績を得た者について
  短答・論文成績を総合してofficial合否を判定する。oralを拒否。
- `preliminary-exam`: actual essayにはshort-answer pass、actual oralには
  written examination passが必要。
- prerequisite未確認でもpracticeは可能だが、
  `practice-only-out-of-sequence`と表示し、official stage statusへ保存しない。

- 司法試験短答: 憲法、民法、刑法。
- 司法試験論文: 公法系、民事系、刑事系、選択科目。
- 予備試験短答: 基本7法と一般教養。
- 予備試験論文: 基本7法、選択科目、民事・刑事法律実務基礎。
- 予備試験口述: 民事・刑事法律実務基礎。

すべての生成問題に
`AI作成・公式問題ではない`、法体系、exam/year/component、subject、exam format
version、source calibration、temporal labelを表示します。公開済み公式問題、
出題趣旨、採点実感をcalibrationに使い、公式模範答案とは表示しません。

出題趣旨、採点実感、口述テーマは
`examType + examYear + component + subject + materialType + sourceVersion`
でqualifyし、別試験・別年度・別科目へ一般化しません。

2026-07-16時点の実施中司法試験について、漏えい、記憶、再現、試験委員研究分野、
topic speculationを使いません。公式公開前は2025年以前だけを使います。

CBT simulationは公式のpage/character slot、keyboard、法文条件を明示します。
予備試験論文は各科目4ページとして扱い、実際の試験systemや採点を再現したとは
表示しません。

## US

`NextGen | traditional UBE | state-specific`とjurisdictionをauthoritative sourceで
確認します。tested subjectだけを使い、majority/UBEとstate-specific ruleを
rule単位でlabelします。classic MBE、NextGen released sample、MEE/MPT、
state essayを混同しません。

## One-question flow

1. 一問だけ提示。
2. learnerのattemptを待つ。
3. 正誤ではなくreasoningとsource alignmentを確認。
4. policyが許すpracticeなら、rule、application、各選択肢/論点のfeedback。
5. `[VERIFY]`または`[UNCERTAIN]`を具体的に付ける。
6. 次問へ進むか人に選んでもらう。

official grade、pass/borderline、合格可能性、精密scoreを出しません。
