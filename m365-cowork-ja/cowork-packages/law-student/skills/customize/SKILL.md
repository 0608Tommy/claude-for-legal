---
name: customize
description: >
  law-student profileの法体系、学習段階、course、試験component、選択科目、法令基準日、source、学習方法、outline、AI policy、保存・接続設定を一度に1項目だけcurrentからproposedへ安全に更新する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: law-student
  migration-target: admin
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Study profile customization

旧来のlabel:
`/law-student:customize [section name, or describe the change]`。

## Mandatory education / source / security / state gate

1. `references/common/cowork-runtime-contract.md`、
   `references/common/japan-study-routing.md`、
   `references/common/source-provenance-and-review.md`、
   `references/common/academic-integrity-and-socratic-controls.md`、
   `references/common/state-and-power-platform-contracts.md`を読みます。
2. exact current user/profileをcanonical keyで読み、missing、paused、required
   `[PENDING]`ならcold-startへrouteします。
3. `ui_locale`、legal system、learner level、jurisdiction、course/examを分離します。
4. school policy、exam date/component、temporal basis、statute等の変更はexact official/
   institution source、version、coverageを確認します。
5. `exam-cutoff`、`currently-effective`、`future-enacted`、`historical`、
   `pending-proposal`を混ぜません。
6. 実在しないpolicy、case、statute、exam factを作りません。
7. academic integrity、no-rewrite、answer-reveal controlを無効化する変更を拒否します。
8. destination、viewer、retention、DLP、source authorizationを確認します。
9. gatewayをlive preflightし、失敗時はread-only change planだけです。
10. 一度に1 change。exact itemId/eTag、diff、fresh confirmation、unique idempotency、
    append-only audit。stale/partialは停止。
11. enrollment、submission、LMS、external post、scheduled tutoringを変更・実行したと
    表示しません。

日本法内容はDRAFTで、有資格者review pendingです。

### 共通必須事項（本文全体に適用）

- profile changeも`STUDY NOTES — NOT LEGAL ADVICE`の教育目的を外れません。
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

## 会話state

`select-section` → `show-current` → `collect-new` → `verify-source` →
`check-consistency` → `explain-impact` → `confirm` →
`conditional-update` → `audit`

confirmation前にwriteせず、success後に次changeを自動開始しません。

## Field map

`references/profile-fields.md`の各fieldを1行current summaryで示します。

JP固有:

- stage: `legal-profession-course | undergraduate-law | law-school | ...`
- law-school track: `mishu-3-year | kishu-2-year`
- 予備試験/司法試験、year、短答/論文/口述、選択科目
- versioned `bar_or_exam.exam_format` object
- component prerequisite、eligibility basis/period
- `bar_or_exam.attempt_cap` statusと、statusがnumericの場合だけのcount
- 司法修習cohortとpublic/synthetic source only
- temporal basis label/asOf
- school-specific citation/AI policy source

US固有:

- JD/LLM level
- NextGen/UBE/state-specific、jurisdiction、date
- MBE/essay等のmethod
- Bluebook/ALWDまたはschool-specific

UI localeとlegal systemを同時変更扱いにしません。

## Impact examples

- `ui_locale`だけ変更: displayのみ。substantive law routeは維持。
- `study_legal_system: JP → US`: subject、exam authority、citation、sourceを再確認。
- `mishu-3-year`→`kishu-2-year`: institutional track変更。習熟度や単位認定を
  自動推測しない。
- exam year変更: official dates、component、exam format object、temporal basisをrefresh。
- exam format変更: valueだけでなくsource item/version/verified timeを一緒に更新。
- component変更: judicial oralを拒否し、preliminary essay/oral prerequisiteを再確認。
- `bar_or_exam.attempt_cap`変更: `none-within-eligibility-period | numeric | unknown |
  not-applicable`を明示し、`numeric`の場合だけ正の整数countを保存。
- elective変更: study plan/flashcard scopeへの候補impactを示す。
- AI policy source更新: graded-work permissionを再判定。
- temporal basis変更: exam/current/future/historical/pendingの差と既存artifactの
  stale候補を示す。
- DLP mandatory: productionをblockedへ。

existing artifactを自動rewriteせず、stale候補として人に選んでもらいます。

## Consistency

flag:

- Japanese UIだけでJP law
- JP routeにMBE default
- US routeに司法試験科目
- legal-profession-courseとgeneric undergraduateの混同
- law-school trackが旧`unlearned/learned`または未解決
- exam format valueとsource versionの不一致
- judicial-examにoral
- preliminary essay/oralのactual prerequisite未確認
- `bar_or_exam.attempt_cap` status/count不整合
- national examにforecast enabled
- exam yearとofficial cutoffの不一致
- graded workにAI policy versionなし
- judicial trainingにreal record pointer
- translated statuteだけをauthoritative
- connector declarationだけでconnected
- DLP requiredとproduction enabled
- review pendingをapproved

どのfieldを直すか人に選んでもらいます。

## Write

current recordを再取得し、current→proposed、source/version、downstream impact、
destination/DLPを示し、`Confirm this one change? yes/no`後にupdateします。

plan/deck/tracker等のsaved progressを変更する場合は`scopeType: user`,
`scopeId: [userObjectId]`、session recordは`scopeType: session`,
`scopeId: [sessionId]`を使い、study metadataは`patch.payload`、auditでは
`details`へ置きます。

gateway failure時は「保存しました」と言わず、manual change planとblockerを示します。

## 行わないこと

- section/audit historyのdelete。archiveを提案
- 複数changeの一括confirmation
- guardrail・review pending・DLP blockerの解除
- stale eTag overwrite
- profile changeをenrollment/LMS/exam registrationへ反映したと表示
