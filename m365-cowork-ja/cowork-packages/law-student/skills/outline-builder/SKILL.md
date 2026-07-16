---
name: outline-builder
description: >
  syllabus、class notes、casebook、case brief、既存outlineから、法体系に合うtopic・制度・法源・要件・効果・判例・例外のscaffoldを作り、学生自身がsourceから埋める。sourceなしのruleを創作せず、既存formatを維持する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: law-student
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Outline builder

旧来のlabel:
`/law-student:outline-builder [subject or authorized class materials]`。

## Mandatory education / source / security / state gate

1. `references/common/cowork-runtime-contract.md`、
   `references/common/japan-study-routing.md`、
   `references/common/source-provenance-and-review.md`、
   `references/common/academic-integrity-and-socratic-controls.md`を読みます。
2. `STUDY NOTES — NOT LEGAL ADVICE`。real client、clinic、非公開修習recordをoutlineに
   入れません。
3. legal system、learner level、jurisdiction、course/exam、subject、outline purposeを
   解決します。
4. exact syllabus、notes、casebook、brief、existing outline、AI policyのitem/
   version/pages/coverage/authorizationを記録します。
5. law/sourceごとに`exam-cutoff`、`currently-effective`、`future-enacted`、
   `historical`、`pending-proposal`を分けます。
6. 実在しないrule、statute、case、holding/判旨、citationを作りません。sourceがない
   欄は`[GAP]`です。
7. graded/restricted assignmentのoutline代筆をしません。学生がsourceから内容を
   入れる前に完成outlineを渡しません。
8. destination、viewer、commercial materialの利用条件、DLPを確認します。
9. gateway failure時はsession内scaffoldだけ。outline/progressを保存済みと表示しません。
10. writeはexact ID/eTag/idempotency、diff、fresh confirmation、auditを要求します。
11. grade、submission、LMS、external post、scheduled tutoringを実行しません。

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

outlineをAIが完成させません。構造化とsource integrationを支援します。

可能:

- syllabusとexisting outlineからtopic treeを作る。
- headings、subheadings、case/exception/future-law slotを作る。
- 学生のnotes、casebook excerpt、briefからexact contentを取り込む。
- gaps、矛盾、stale versionを示す。
- topicごとにSocratic questionを出す。

不可:

- syllabusだけからruleとcaseを埋める。
- AI knowledgeでgapを隠す。
- 学生の依頼だけを理由に完成outlineを代筆する。

sourceなしでreferenceを求められた場合も、official/authorized sourceを取得するか
`[GAP — 指定資料で補う]`を残します。

## Route

### JP

`references/outline-scaffolds.md`のstatute/system scaffoldを使います。

- 法源
- 要件
- 法的効果
- 解釈上の論点
- 裁判例の判旨と事案の射程
- 個別意見
- 学説・反対論
- application pattern
- 例外、経過措置、five temporal labels

casebook型のtopic→rule→caseだけに固定せず、条文・制度を軸にします。試験outlineは
`exam-cutoff`を先頭に置き、`currently-effective`その他のlabelを別欄にします。

### US

explicit US modeではtraditional、rules-only、flowchart、casebook structure等、
existing outlineとsource pluginのpreferencesを保持します。majority/state ruleを
混ぜません。

## Workflow

1. 何から作るかを確認: syllabus、notes、casebook、brief、partial outline。
2. existing outlineがあればheadings、depth、case placement、notationをmatch。
3. syllabusからscaffoldだけを作る。
4. authorized sourceから学生が選んだsectionをintegrate。
5. 各topicでrule/sourceを学生に説明してもらう。
6. gaps、exception、missing case、stale versionをmark。
7. section completion後、閉じて短いapplication questionを出すか本人に選んでもらう。

学生の記述と自分の資料が矛盾する場合:

> その記述は[source item/version/section]の「[exact quote]」と一致しません。
> どちらをoutlineに残すべきか、sourceを確認してください。

AIのknowledgeで正解を埋めません。

## Markers

- `[GAP — 指定資料で補う]`
- `[NEEDS CASES — ruleはあるが裁判例なし]`
- `[CHECK CLASS NOTES — 授業上の重点未確認]`
- `[EXCEPTION UNCLEAR — sourceで確認]`
- `[VERIFY: source/version]`
- `[review]`

## Persistence

保存前にstudent-authored、source-extracted、placeholder、AI structural scaffoldを
区別して表示します。OneDrive draftまたはconfirmed SharePoint outputへのwriteは
destinationと内容を確認した後だけです。

## 行わないこと

- syllabusだけから完成outline
- sourceなしのrule/caseでgap埋め
- JP outlineをUS case treeへ強制
- future-enacted/historical/pending-proposalをcurrently-effective/exam-cutoffとして記載
- commercial教材の大量複製
- graded submissionの作成・提出
