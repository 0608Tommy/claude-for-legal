---
name: cold-call-prep
description: >
  授業の指定教材、syllabus、学生ノートから事実、手続、判旨、理由、適用、policyの質問を作り、一問ずつ演習する。教員の傾向や出題を予測せず、授業前に戻るべきexact sourceを示す。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: law-student
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 授業準備

旧来のlabel:
`/law-student:cold-call-prep [case name, paste, or reading path]`。

## Mandatory education / source / security / state gate

1. `references/common/cowork-runtime-contract.md`、
   `references/common/japan-study-routing.md`、
   `references/common/source-provenance-and-review.md`、
   `references/common/academic-integrity-and-socratic-controls.md`を読みます。
2. `STUDY NOTES — NOT LEGAL ADVICE`。real matter、client、clinic、非公開修習recordなら
   具体的drillを停止します。
3. legal system、learner level、jurisdiction、course、class date、assigned scope、
   class/assessment modeを解決します。
4. exact reading、syllabus、notes、AI policyのitem/version/pages/coverage/
   authorizationを記録します。case nameだけなら貼付またはauthorized sourceを求めます。
5. statute versionを`exam-cutoff`、`currently-effective`、`future-enacted`、
   `historical`、`pending-proposal`に分けます。
6. 実在しないcase、statute、holding/判旨、quote、授業上の重点を作りません。
7. 一問ずつ出し、学生のattempt前に答えを開示しません。graded/restricted promptを
   授業準備に偽装しません。
8. destination、viewer、著作権、personal data、DLPを確認します。
9. gateway failure時はsession内drillだけ。summaryやprogressの保存を主張しません。
10. writeはexact ID/eTag/idempotency、fresh confirmation、auditを要求します。
11. attendance、enrollment、submission、LMS、教員連絡、external post、
    scheduled tutoringを実行しません。

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

## Source-first intake

- courseと授業日
- assigned readingのexact section
- syllabus上の位置
- 学生のbrief/notes
- 授業方法または教員の明示的なguidance（sourceにある場合だけ）

professor名を入力させる必要はありません。教材に含まれる場合も、研究分野、評判、
過去の発言から「聞かれる可能性」を推測しません。

## Question coverage

`references/class-prep-template.md`に従い、6～10のcandidateを内部で準備しても、
提示は一問ずつです。

- facts / relevant statutory text
- procedural posture
- issue
- holding/判旨とscope
- reasoning / rejected argument
- individual opinion
- fact variation / application
- policy / competing view（指定教材にある場合）
- 前後の教材との関係

日本の法科大学院では実際のsmall-group method、syllabus、指定教材を優先し、
米国型cold-callを標準として押し付けません。

## Drill

1. warm-upのsource identificationまたは重要事実。
2. 回答を待つ。
3. 正しいが粗い場合は理由を求める。
4. 誤りなら条文・事実・手続へnarrow。
5. guessならrule/sourceを先に述べてもらう。
6. 数回でも出なければexact sourceへ戻し、そのtopicを終了。
7. 次問へ進むか学習者が選ぶ。

学生自身のnoteと回答が矛盾する場合、exact quote/versionを示し、どちらが正しいかを
本人に検討させます。AIのknowledgeで答えを埋めません。

## Summary

`references/class-prep-template.md`の形式で、説明できた点、sourceへ戻る点、未読範囲、
授業前の最大3 actionを示します。「top likely questions」「professor hobby horse」
「明日必ず聞かれる」とは書きません。

summaryの保存は学生が内容・destinationを確認した場合だけです。

## 行わないこと

- assigned readingを読まずにcase answerを渡す
- professor・examinerの質問予測
- attempt前のholding/判旨 reveal
- course materialの大量複製
- attendance/LMS/submission/external post
- 授業の評価・成績を推測
