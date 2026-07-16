---
name: flashcards
description: >
  authorized outline、notes、casebook、公式法令・判例から一concept一cardを作り、法令version・試験基準日・provenance付きでdrill、review、stats、sessionを行うPower Platform front end。保存・bucket更新は確認後だけ行う。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: law-student
  migration-target: power-platform
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Flashcards

旧来の正規label/flags:

`/law-student:flashcards [subject] [--generate | --drill | --review | --stats | --session <n>]`

## Mandatory education / source / security / state gate

1. `references/common/cowork-runtime-contract.md`、
   `references/common/japan-study-routing.md`、
   `references/common/source-provenance-and-review.md`、
   `references/common/academic-integrity-and-socratic-controls.md`、
   `references/common/state-and-power-platform-contracts.md`を読みます。
2. `STUDY NOTES — NOT LEGAL ADVICE`。real matter、client、非公開修習recordをcardに
   しません。
3. legal system、learner level、jurisdiction、course/exam、subject、componentを
   解決します。
4. exact source item/URL、version、section、coverage、authorization、AI policyを
   各cardまたはdeck metadataに持たせます。
5. law/cardごとに`exam-cutoff`、`currently-effective`、`future-enacted`、
   `historical`、`pending-proposal`を分けます。
6. 実在しないrule、statute、case、holding、citationを作りません。target countを
   満たすために推測cardを足しません。
7. drillは一cardずつ、回答を待ってからbackを表示します。graded/restricted promptを
   card化しません。
8. destination、viewer、commercial materialの利用条件、personal data、DLPを確認。
9. gateway、approved flow、ACLをlive preflight。失敗時はsession内manual cardsだけで、
   deck/bucket/review dateを保存済みと表示しません。
10. create/updateはexact ID/eTag/idempotency、diff、fresh confirmation、audit。
11. reminder、calendar、scheduled tutoring、Anki/LMS export、external postを
    自動実行しません。

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

## Modes

### `--generate`

入力:

- subject/course/exam
- authorized source
- optional target count
- legal system、temporal label/asOf

`references/flashcard-schema.md`を使います。

card候補:

- definition
- statutory requirement / legal effect / exception
- leading case propositionとfactual scope
- procedural sequence
- comparison/distinction
- exam trap explicitly found in official/class source

日本法令cardはlaw ID、条文、version/cutoffを必須とします。外国語訳は
`non-authoritative-translation`。裁判例cardはcourt/date/event number/sourceを
持ちます。AI memoryだけのruleはcardにせず、source取得または`[VERIFY]` draftとして
保存対象外にします。

### `--drill`

priority candidate:

1. learnerが前回wrongと確認したcard
2. `nextReview <= today`のconfirmed card
3. new card
4. learnerが選んだreview card

per card:

1. Qだけを表示。
2. 回答を待つ。
3. Aとexact sourceを表示。
4. learnerが`right | partial | wrong | don't know`を自己評価。
5. bucket/next-review candidateを表示。
6. 保存するか確認。

AIが正解率やmasteryを公式判定しません。sourceと回答が衝突した場合、exact textを
示し、card修正・retire・再確認を人に選んでもらいます。

### `--review`

exact deckをbucket、subject、source status、law versionで表示します。stale law、
missing source、future-law cardを分けます。編集は1 cardずつ別confirmationです。

### `--stats`

total、bucket distribution、due plan、attempt self-assessment、stale source、
repeated wrongを示します。繰り返しwrongはSocratic drillまたはsource reviewを
提案し、理解度・gradeと断定しません。

### `--session <n>`

N cardを一枚ずつ行います。終了summaryはself-assessment、stuck topic、
source versionsを示し、session result createとdeck updateを別writeにします。

## Storage / Power Platform

本skillはfront endです。`study-source-reader`、`study-state-writer`、
`study-audit-writer`のapproved flow evidenceが必要です。

- new deck/card: `expectedAbsent: true`
- existing card: exact itemId/latest eTag
- bucket update: confirmed card単位または表示したbatch単位
- session result: separate create
- study-plan priority: separate update

deckとstudy-planは`scopeType: user`, `scopeId: [userObjectId]`、flashcard session
resultは`scopeType: session`, `scopeId: [sessionId]`です。study metadataは
create/state envelopeの`payload`、auditでは`details`へ置きます。shared schemaに
独自top-level fieldを追加しません。JSON例は
`references/common/state-fixtures.md`に従います。

next review dateは学習計画で、notificationがscheduledされた意味ではありません。

## 行わないこと

- source不足をcard数で埋める
- translated lawをauthoritativeと表示
- historical/future/pendingをcurrently-effectiveまたはexam-cutoffとしてdrill
- learner attempt前にbackを表示
- grade/masteryを公式判定
- gatewayなしにdeck更新
- reminder、LMS、Anki、external postingの自動化
