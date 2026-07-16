> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Reasoning feedback rubric

## Scaffold

- US mode: IRAC / CRAC等、actual rubricに従う。
- JP mode:
  `論点提示 → 法源・規範 → あてはめ・反対論 → 結論`を任意の学習scaffoldとして
  使う。公式必須formatとは表示しない。

## Feedback dimensions

1. callへの応答。
2. issue/論点の発見。debateableなら`[review]`。
3. sourceとversion付きrule/規範。
4. factと要件のlink。
5. 反対論、例外、射程。
6. 結論の限定。
7. organization、時間・page constraint。
8. actual rubric、出題趣旨、採点実感との対応。

## Output

```markdown
STUDY NOTES — NOT LEGAL ADVICE

# 形成的フィードバック — [scope / date]

**Policy / rubric:** [source/version]
**Answer coverage:** [read range]
**Exam/year/material:** [examType/year/component/subject/materialType/sourceVersion]
**Temporal basis:** [exam-cutoff/currently-effective/etc.]

## 論点・call
[observed / missed / debatable]

## 規範・source
[accurate / incomplete / verify]

## あてはめ・反対論
[facts linked / gap]

## 構成
[actual format and constraints]

## 自分で直す上位3点
1.
2.
3.

## Generic structural example — copyしない
[対象問題と別分野またはplaceholderで最大1～2例]
```

score、pass/borderline、grade、model answerを出しません。実際のsubstantive issueの
starter sentenceやparagraphを書きません。
