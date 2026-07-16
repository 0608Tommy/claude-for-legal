---
name: case-brief
description: >
  指定された判決・決定またはcaseを、法体系に応じた書誌情報、法令version、重要事実、手続、争点、判旨・holding、射程、個別意見、後続取扱いのscaffoldで学生自身に整理させる。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: law-student
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Case brief

旧来のlabel:
`/law-student:case-brief [case name or citation, or paste the case]`。

## Mandatory education / source / security / state gate

1. `references/common/cowork-runtime-contract.md`、
   `references/common/japan-study-routing.md`、
   `references/common/source-provenance-and-review.md`、
   `references/common/academic-integrity-and-socratic-controls.md`を読みます。
2. 出力は`STUDY NOTES — NOT LEGAL ADVICE`。real matter、client、非公開の修習・
   clinic recordなら停止します。
3. legal system、jurisdiction、learner level、course、assignment/assessment modeを
   解決し、日本の裁判例をUS common-law briefへ強制しません。
4. exact judgment/casebook item、version、pages、coverage、authorizationとAI policyを
   確認します。case nameだけでは完成briefを書きません。
5. relevant statuteを`exam-cutoff`、`currently-effective`、`future-enacted`、
   `historical`、`pending-proposal`に分けます。
6. 実在しないcase、citation、event number、holding/判旨、quote、later treatmentを
   作りません。検索missを不存在と表示しません。
7. 学生がfacts、issue、holding/判旨を先に試みるまで答えを渡しません。graded/
   restricted workではsource extractionもpolicy範囲内だけです。
8. destination、viewer、著作権、DLPを確認し、商用casebookや個人情報を過剰複製しません。
9. gateway failure時はsession内scaffoldだけ。保存済みbriefやprogressを主張しません。
10. writeはexact ID/eTag/idempotency、diff、fresh confirmation、auditを要求します。
11. grading、submission、LMS、外部投稿、scheduled tutoringを実行しません。

日本法内容はDRAFTで、有資格者review pendingです。

### 共通必須事項（本文全体に適用）

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

## Learning-mode boundary

完成briefを代筆しません。

- 学生に何を読んだか、重要事実、争点、判旨/holdingを順に述べてもらう。
- blank scaffoldと各欄の質問を示す。
- 薄い欄をpointed follow-upで深める。
- exact source textがある場合、裁判所自身の言葉をquoteとして指し示せる。
- 学生の理解とsourceが衝突したら、双方のexact quote/versionを示して再検討させる。

`explain-to-me`は欄の意味を説明するmodeで、briefを書くmodeではありません。
何度読んでもholdingのphraseだけ作れないというungraded practiceでも、対象caseの
starter sentenceを原則出さず、court quoteと構造promptを使います。

## Japan route

`references/brief-template.md`を使います。

case identification / verification metadata:

```text
裁判所・法廷 / 判決・決定・命令 / 裁判年月日 / 事件番号 /
source system・item・version・retrieved time・coverage
```

rendered citation:

```text
裁判所・法廷 / 判決・決定・命令 / 裁判年月日 /
公的判例集巻号頁（あれば） / 商業判例誌巻号頁（authorized sourceにある場合）
```

事件番号はrendered citationから除き、controlling school/journal/court styleが
source/version付きで明示的に要求する場合だけ含めます。

重要事実、手続経過、争点、結論、判旨、事案の射程、個別意見、その後の取扱い、
授業上の位置づけを分けます。party-name titleや一文のportable ruleを必須にせず、
法令本文、裁判所階層、判旨と射程を中心にします。

citation metadataとverification metadataを分け、後者にsource system/item、
version、retrieved time、coverage、provenanceを記録します。URLや確認日をcitationへ
混ぜてverification済みと表示しません。「法律文献等の出典の表示方法（2014年版）」は
民間の非拘束的guideで、学校・journal ruleがあればそちらを優先します。

裁判所websiteの収録限界を明示し、public databaseをcomprehensive treatment
serviceと表示しません。日本法令外国語訳だけから判旨・法令を確定しません。

## US / other route

US modeではsource pluginのFacts、Procedural posture、Issue、Holding、Reasoning、
Rule、Notes scaffoldを保持します。法体系不明なら法域を質問します。判例本文なしの
memory-based説明は`[model knowledge — verify]`で、brief completionには使いません。

## Drill flow

1. 「この判決の結論またはholdingを一文で」と質問。
2. 重要事実を2～4点に限定させる。
3. procedural postureを確認。
4. narrow issueとbroader questionを分ける。
5. reasoning、rejected argument、individual opinionを確認。
6. rule/判旨の射程を事実・法令versionと結ぶ。
7. course sourceで位置づける。

基礎部分が出なければexact pageへ戻し、その欄で停止します。

## Output / persistence

reviewer note、scaffold、学生が記入した内容、source/versionを分けます。OneDriveまたは
SharePointへ保存する場合、学生が最終内容とdestinationを確認した後だけconditional
writeします。

## 行わないこと

- case nameだけから完成brief
- summary依頼を理由に学習作業を代替
- party argument、dissent、dictaをholding/判旨として表示
- fabricated cite・quote・later treatment
- citationとverification metadataの混同
- 日本の裁判例をUS precedent modelへ単純化
- graded submissionの作成・提出
