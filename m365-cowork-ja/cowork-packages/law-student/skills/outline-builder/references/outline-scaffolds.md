> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Outline scaffolds

## JP statute/system

```markdown
# [科目 / temporal label + asOf / source versions]

## [制度・法領域]
### 法源
- [法令ID・条文・version]
### 要件
- [学生がsourceから記入]
### 法的効果
- [学生がsourceから記入]
### 解釈上の論点
- [対立 / source]
### 裁判例
- [court/date/event number / 判旨 / 射程]
### 学説・反対論
- [指定教材にある場合]
### あてはめpattern
- [自分の例]
### 例外・経過措置・temporal status
- [`exam-cutoff` / `currently-effective` / `future-enacted` / `historical` /
  `pending-proposal`を分離]
```

## US casebook

明示されたUS modeではtopic → subtopic → rule → case → exception、rules-only、
flowchart等のsource plugin formatを保持します。

## Gap markers

- `[GAP — 指定資料で補う]`
- `[NEEDS CASES — ruleはあるが裁判例なし]`
- `[CHECK CLASS NOTES — 授業上の重点未確認]`
- `[EXCEPTION UNCLEAR — sourceで確認]`
- `[VERIFY: source/version]`

syllabusだけから完成outlineを作らず、scaffoldを作ります。学生のnotes、casebook、
briefからexact contentをintegrateし、矛盾は双方のquote/versionを示します。
