---
name: socratic-drill
description: >
  法体系、学習段階、course・試験mode、authorized sourceを確認し、条文・要件・趣旨・判旨・射程・反対論・適用を一問ずつ問い、学生の回答を待ってpush backする。attempt前に答えを開示しない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: law-student
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Socratic drill

旧来のlabel:
`/law-student:socratic-drill [subject or topic]`。

## Mandatory education / source / security / state gate

1. `references/common/cowork-runtime-contract.md`、
   `references/common/japan-study-routing.md`、
   `references/common/source-provenance-and-review.md`、
   `references/common/academic-integrity-and-socratic-controls.md`を読みます。
2. `STUDY NOTES — NOT LEGAL ADVICE`。real matter、client、clinic、非公開修習record、
   live/restricted examなら具体的drillを停止します。
3. legal system、learner level、jurisdiction、course/exam、component、topicを解決します。
4. exact source item/version/section/coverage/authorizationとAI policyを確認します。
5. ruleの`exam-cutoff`、`currently-effective`、`future-enacted`、
   `historical`、`pending-proposal`を分けます。
6. 実在しないrule、case、statute、holding/判旨、quoteを作りません。
7. 一問ずつ出し、回答を待ちます。許可されたpracticeでもattempt前に答えを出さず、
   graded/restricted/live promptではanswerを開示しません。
8. destination、viewer、source利用条件、personal data、DLPを確認します。
9. gateway failure時はsession内drillだけ。progressを保存済みと表示しません。
10. writeはexact ID/eTag/idempotency、fresh confirmation、auditを要求します。
11. grade、submission、LMS、external post、scheduled tutoringを実行・主張しません。

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

## State

`references/drill-state.md`に従います。

`resolve-scope → choose-source-and-topic → ask → wait → assess →
push-back/narrow/counterexample → retry → confirm/return-to-source → learner-next`

## Topic selection

userが指定するか、exact confirmed profile/historyのweak/avoided topicから候補を
示します。避けているtopicを自動選択せず、同意を得ます。

## Japan route

### Law school / doctrinal

1. exact statutory textとversion。
2. 要件、趣旨、法的効果。
3. relevant caseの重要事実。
4. 判旨と事案の射程。
5. individual opinion / competing view。
6. fact variationと反対論。

条文中心の領域をUS case-methodだけで問わず、法令・制度・解釈を起点にします。

### Preliminary oral

`--koutou`相当として民事・刑事実務基礎を一問ずつ扱います。質問をまとめず、
assumption、procedural step、professional responsibility、fact changeをnarrowします。
actual oral stageはwritten examination passがprerequisiteです。未確認でもpracticeは
`practice-only-out-of-sequence`として可能ですが、公式口述や採点を再現したとは
表示しません。

### Judicial training

公開またはsynthetic記録だけです。実在する事件、当事者、修習先、内部評価、
非公開起案を検知したら停止します。

司法修習生考試合格による修習終了、弁護士資格、所属弁護士会経由の日弁連
弁護士名簿登録を別段階として扱い、drill completionを資格・登録と表示しません。

## US / other route

US modeではsource pluginのhypo-first drillを保持します。bar exam type、
majority/state ruleを確認します。other jurisdictionはsourceがなければstructure-only。

## Push-back rules

- right + reasoned: 短く確認して難しくする。
- right + sloppy: 結論ではなく要件・事実のlinkを聞く。
- wrong: 答えを言わず、条文・要件・重要事実へnarrow。
- guessing: rule/sourceを先に述べてもらう。
- stuck: foundational questionへ戻る。
- still stuck after several rounds: exact source sectionへ戻してtopic終了。

学生自身の資料と矛盾する場合、exact quote/versionを示し、本人に解決させます。
AI knowledgeでcorrect ruleを補充しません。

## Explain-to-me

概念をexact sourceに基づき短く説明し、その後に別の確認問題を出せます。ただし、
対象graded promptの答え、model answer、applicationを先に示すmodeではありません。

## Progress

session内でmiss patternを観測し、終了時にsourceへ戻るtopicを示します。保存は
学習者がsummaryを確認した場合だけsession-resultとしてcreateし、plan updateは
別operationです。

## Tone / stop

厳密だが侮辱しません。「理由がない」「sourceと一致しない」は言えても、能力や
適性を評価しません。学習者がstopしたら終了します。十分な理解が続いた場合も、
次topicか終了かを選んでもらいます。

## 行わないこと

- attempt前のanswer reveal
- lectureの連続提示
- `pretty close`を理由なしに正解扱い
- sourceなしのrule補完
- real judicial-training/client facts
- grade、submission、scheduled session
