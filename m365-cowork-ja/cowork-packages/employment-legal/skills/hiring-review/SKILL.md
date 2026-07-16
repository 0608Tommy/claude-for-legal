---
name: hiring-review
description: >
  日本の労働条件通知書、雇用契約、fixed-term、労働時間制、採用差別・合理的配慮、background check、restrictive covenant、employee invention、visa・社会保険をcurrent sourceと事業場factsでreviewする。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: employment-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Hiring review

旧来のlabel:
`/employment-legal:hiring-review [offer letter file, or describe the hire]`。

## Mandatory hiring / privacy / security gate

1. `references/common/cowork-runtime-contract.md`を読み、exact user/practice profile、
   source item/version、destinationを確認します。gateway failure時もread-only draftは
   可能ですが、保存・送信を主張しません。
2. jurisdictionはactual work location、establishment、entityで解決します。日本なら
   `references/common/jurisdictions/ja-jp/hiring-work-rules.md`を使います。
3. accommodation/medical、sensitive background、contested offer等はrestricted matterを
   提案し、active bindingなしに他matter dataを読みません。
4. employment-condition、minimum wage、working-time system、covenant、visa、
   insurance、2026 future-law statusはcurrent official sourceを確認します。
5. sourceが薄い場合はbroaden/different source/flag-and-stopを人に選んでもらい、
   silent supplementしません。
6. AIはhire、offer send、background order、visa filing、insurance/payroll setupを
   決定・実行しません。
7. Cowork内DLP必須ならcandidate personal dataを投入せずproduction停止です。

provenance/reviewer noteは
`references/common/source-provenance-and-review.md`、
checklistは`references/hiring-review-checklist.md`。

## 会話state

`intake` → `resolve-jurisdiction` → `classify-contract` →
`review-conditions` → `screen-equality-privacy` → `review-covenants-ip` →
`visa-insurance` → `draft-findings` → `human-review`

## Intake

provided factsを再質問せず、gapだけを1 blockで確認します。

- employing entity、establishment、actual work location/prefecture
- candidate pseudonym、role、actual duties、change scope
- start、term/renewal、probation
- working-time system、schedule、36 agreement
- wage components、fixed overtime、minimum wage source
- part-time/dispatch/fixed-term status
- background check/data flow
- covenant/IP/equity
- visa/status
- union/CBA/work rules

## Japan review

### Contract/conditions

`労働条件通知書 / 雇用契約書`についてentity、workplace/dutiesと変更範囲、term、
renewal criteria/cap、indefinite conversion、working time、wage、retirement/
dismissal、work rules/CBAを確認します。募集情報と条件差異も確認します。

日本matterを`exempt/non-exempt`やat-willへ分類しません。manager/supervisor、
discretionary work等はnarrow statutory procedureを事実で確認します。

### Equality/harassment/accommodation

sex、pregnancy、age、disability、reasonable accommodation、leave-related
disadvantageを個別法でscreenします。fair recruitment guidance全体を単一のprotected
class listにしません。2026-10-01前は求職者sexual harassment新措置をfuture
readinessとします。

### Background/privacy

APPI purpose、necessity、proper acquisition、sensitive data、consent、vendor、
foreign transfer、retention、securityを確認します。職務関連性のない情報を求める
workflowを推奨しません。

### Covenant/IP

Civil Code Article 90/current case lawによりlegitimate interest、role、duration、
geography、scope、compensation、burdenを分析します。米国州別tableを使いません。
employee inventionはPatent Act Article 35と社内規程・相当の利益を確認します。

### Visa/insurance

status/work authorization、sponsor、role/location、foreign-worker notification、
health/pension/employment/workers compensation onboarding ownerを確認します。

## Output

> **⚠️ レビュー担当者向け注記**
> [common format]

```markdown
## 採用review — [pseudonym / role]

**Jurisdiction / establishment:** [...]
**Status:** Draft ready for qualified review | Changes required | Blocked

### 労働条件・contract type
[findings/source]

### Working time・wage
[findings/source]

### Equality・accommodation・privacy
[findings/source]

### Covenant・IP
[findings/source]

### Visa・insurance
[owner/open item]

### Before issue
- [ ] [exact change/review]
```

candidate-facing draftからinternal reviewer note、risk analysis、privileged labelを
除きます。`ready`はAIのsend/approvalではありません。

## Consequential gate

final offer/send前にexact document/version、work location、open flags、qualified
reviewer、approver、destinationを確認し、marked draftで停止します。non-lawyerには
attorney briefを作ります。

## 行わないこと

- hire/compensation/benefitを決定
- at-will/FLSA/FCRA等をJapan defaultにする
- source未確認のthreshold/covenant conclusion
- offer/background requestをsend
- employee dataをpractice profile/auditへ複製
