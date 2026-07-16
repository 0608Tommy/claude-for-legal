> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Case brief scaffold

## 日本の裁判例

```markdown
STUDY NOTES — NOT LEGAL ADVICE

# [裁判所・法廷 / 判決・決定・命令 / 裁判年月日]

## Case identification metadata

**事件番号:** [exact]

## Rendered citation

**公的判例集:** [巻号頁またはなし]
**商業判例誌:** [authorized sourceで確認した巻号頁またはなし]
**関連法令:** [law ID / 条文 / version / temporal label / asOf]
**授業source:** [item/version/pages]

## Verification metadata

**Source system / item:** [court URL、database item等]
**Source version / retrieved at:** [exact]
**Case match key:** [事件番号]
**Coverage / treatment check:** [範囲と限界]
**Provenance:** [tag]

## 重要事実
[判旨の射程に必要な事実を学生が記入]

## 手続経過
[学生が記入]

## 争点
[裁判所が判断した問い]

## 結論
[主文・結果]

## 判旨
[原文quoteまたは学生の要約。どちらかをlabel]

## 判旨の射程
[どの事実・法令versionに依存するか]

## 個別意見
[反対・補足意見を多数意見と分離]

## その後の取扱い
[確認できた範囲。検索coverageを明示]

## 授業上の位置づけ
[syllabus・notesから学生が記入]
```

party-name titleやportable common-law ruleを強制しません。citation metadataと
verification metadataを混ぜません。検索missを不存在、
下級審の判断を最高裁判旨、当事者主張をcourt holdingとして扱いません。

rendered citationには事件番号を通常含めません。学校・journal等のcontrolling
styleが明示的に要求する場合だけ、そのstyle source/versionを記録して含めます。

「法律文献等の出典の表示方法（2014年版）」は民間の非拘束的guideです。学校・
journal ruleがあればそちらを優先します。

## USまたはother

明示された法体系ではsource pluginのFacts / Procedural posture / Issue / Holding /
Reasoning / Rule / Notes scaffoldを使えます。case textなしに完成briefを書きません。
