---
name: termination-review
description: >
  日本の解雇、懲戒、fixed-term中途解約、雇止め、退職、retirement solicitation、RIFを、労働契約法、労働基準法、就業規則、CBA、current case law、保護活動、final amounts、offboardingでreviewする。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: employment-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Termination review

旧来のlabel:
`/employment-legal:termination-review [describe or attach documentation]`。

## Mandatory dismissal / restricted / current-law gate

1. `references/common/cowork-runtime-contract.md`を読みます。contested termination、
   discipline、whistleblowing、medical/leave関連は一般workspace設定にかかわらず
   restricted matterを要求します。
2. exact user/practice profile、active unexpired binding、matter `status: active`、
   authorized source item/versionを確認します。
3. categoryを混同しません:
   `indefinite dismissal | disciplinary action | fixed-term midterm |
   nonrenewal | retirement/resignation | mutual separation |
   workforce reduction`。
4. current statute、work rules/CBA、dismissal/RIF/nonrenewal case lawを確認します。
   official courts databaseだけで網羅的と表示しません。
5. protection、whistleblower identity、medical data、retention/legal hold、
   destinationを確認します。
6. AIはdiscipline、termination、retirement solicitation、severance、access cutoff、
   filingを決定・実行しません。
7. Cowork内DLP必須ならrestricted factsを投入せずproduction停止です。

Japan lawは
`references/common/jurisdictions/ja-jp/termination-investigations.md`、
checklistは`references/termination-review-checklist.md`。

## 会話state

`intake` → `classify-exit` → `validate-basis` → `protected-activity-scan` →
`documentation-comparator` → `rif-if-applicable` → `offboarding` →
`draft-options` → `counsel-review`

## Intake

- pseudonym、entity/establishment/jurisdiction
- category、proposed date、decision owner
- contract type/term/renewal history
- proposed reason and actual evidence
- work rules/CBA basis
- warnings/PIP/investigation/defense opportunity
- complaints、leave、pregnancy、disability、whistleblowing、union/safety
- comparators、recent positive records
- group reduction/selection
- severance/release proposal

## Validity

indefinite dismissalはLCA Article 16のobjectively reasonable grounds/social
acceptabilityを先に確認します。LSA Article 20 notice/payは追加procedureであり、
valid causeを置き換えません。LSA Article 19 restrictionも確認します。

disciplineはLCA Article 15、work-rule basis、fact finding、notice/opportunity、
proportionality、consistency、comparators。fixed-term midtermはArticle 17、
conversion/nonrenewalはArticles 18/19/current case lawを確認します。

## High-risk scan

- recent complaint/harassment/whistleblowing
- childcare/family-care/maternity/annual leave、occupational injury
- disability/accommodation/medical restriction
- pregnancy/sex/age/other applicable discrimination
- union/CBA/protected activity
- thin/inconsistent documentation
- comparator or retaliatory timing
- contract/work-rule promise
- wage/hour/worker-status exposure

flagがあればnamed counsel/GCへescalateし、go recommendationを出しません。

## Workforce reduction

business necessity、avoidance measures、selection、explanation/consultationを
current jurisprudenceで分析します。日本の`WARN`相当statutory testとは書きません。
mass separation/reemployment-plan、older worker、union/CBA、foreign-worker noticeを
確認します。

## Final amounts / offboarding

LSA Article 23の請求後7日以内のundisputed money/propertyを確認し、自動same-day
final payと書きません。retirement allowanceはwork rules/contract/CBA。
certificate、employment insurance、social insurance、foreign-worker notification、
property/access、legal holdをowner別checklistにします。

severanceは一般的statutory entitlementと推測しません。releaseはcurrent Japanese
law、public policy、waiver scope、consideration、confidentialityをqualified counselが
reviewします。米国固有のconsideration/revocation clockを使いません。

## Output

```markdown
## Termination review — [pseudonym]

**Category:** [...]
**Status:** Hold | Changes required | Draft options for counsel

### Legal basis and procedure
[law/work rules/CBA/source]

### Protected-activity flags
[each flag]

### Documentation/comparators
[assessment/gaps]

### RIF analysis
[if applicable]

### Final amounts/offboarding
[owner/source/open item]

### Human options
[do not choose]
```

## Consequential gate

termination/discipline/solicitation/severance delivery前にexact facts/source、
qualified Japanese employment counsel、approver、destination、meeting planを確認し、
draft/checklistで停止します。non-lawyerにはattorney briefを先頭にします。

## 行わないこと

- dismissal/discipline substantiationを決定
- notice payだけでvalidと判断
- U.S. release/mass-layoff/benefit default
- final amount/access/insurance filingを実行
- restricted matter factsをshared profileへ移す
