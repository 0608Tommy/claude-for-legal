---
name: wage-hour-qa
description: >
  日本の事業場・都道府県、就業規則、36協定、working-time system、actual time records、minimum wage、賃金支払、fixed overtime、annual leave、manager/supervisorをcurrent official sourceで確認し、Q&Aと計算candidateを示す。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: employment-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Wage/hour Q&A

旧来のlabel:
`/employment-legal:wage-hour-qa [question]`。

## Mandatory jurisdiction / source gate

1. `references/common/cowork-runtime-contract.md`を読み、user/profile/matter scopeを
   確認します。
2. actual establishment、prefecture、worker status、work rules/CBAを確認します。
   不明ならgeneric answerを出さず質問します。
3. Japan lawは
   `references/common/jurisdictions/ja-jp/wage-worker-status.md`。
4. minimum wage、Article 36、premium、working-time system、effective dateをその
   会話でofficial sourceからrefreshします。
5. source/inputs不足では計算を停止し、推測値を出しません。
6. wage claim、medical/long-hours、discipline/termination related matterはrestricted
   isolationを提案します。
7. AIはpayroll correction、time record edit、wage payment、disciplineを実行・決定
   しません。

calculationは`references/japan-calculation-checklist.md`、
provenanceは`references/common/source-provenance-and-review.md`。

## 会話state

`identify-question` → `resolve-establishment` → `collect-system-and-records` →
`research-current-rule` → `apply` → `calculate-if-complete` →
`flag-close-call` → `human-options`

## Japan workflow

### Foundation

- 8 hours/day、40 hours/weekの原則
- break、weekly rest day
- statutory overtime、holiday、night categories
- Article 36 agreement/special clause/current cap
- objective actual-time records

Article 36 agreementはotherwise prohibited overtimeを可能にする手続で、premium payを
置き換えません。fixed overtime allowanceもagreement、cap、actual liabilityを
置き換えません。

### Special status/system

Article 41 manager/supervisorはtitle/salaryだけでなくauthority、treatment、schedule
realityを確認し、night-workを別検討します。discretionary/highly skilled systemは
target work、procedure、consent、health measuresをcurrent sourceで確認します。

### Wage

- prefectural/industry minimum wage
- covered wage components
- direct/full/regular payment、deductions
- digital payment conditions
- part-time/fixed-term/dispatch parity
- annual paid leave and five-day duty

minimum wageやpremiumをnational fixed numberとして保存しません。

## Calculation

actual time、wage components、paid posture、target period、current rate/
combination、Article 36 status、limitationが揃った場合だけformula/inputを表示します。
numberには`[verify — Japanese wage-hour counsel review required]`を付けます。

back-pay、fixed-overtime reconciliation、manager misclassificationはspecialist
reviewへrouteします。税・社会保険影響を別trackとします。

## Conversational output

```markdown
**[Establishment / prefecture]:** [current rule and source]

**Application:** [facts → rule]

**Calculation candidate:** [formula/inputs/result or not calculated]

**Close call / missing:** [review items]
```

rule、guidance、work rule、internal policyを分けます。他prefecture/establishmentとの
material differenceを1行で示します。

## Consequential gate

wage correction、classification、schedule、discipline等のaction前にexact time/pay
records、qualified counsel/payroll review、approverを確認し、calculation/checklistで
停止します。

## 行わないこと

- U.S. regular-rate/damages/limitation scaffoldをJapanへ適用
- national minimum wageを仮定
- titleだけでmanager status
- Article 36なしのovertimeをlawfulと表示
- payroll/time recordを変更
