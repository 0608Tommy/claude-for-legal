---
name: worker-classification
description: >
  prospective engagementについて、日本の労働基準法・労働契約法・労働組合法、社会保険・税、Freelance Act、派遣・労働者供給、請負、EOR、OSHをpurpose別に分析し、intended structureとのgapを示す。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: employment-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Worker classification

旧来のlabel:
`/employment-legal:worker-classification [describe proposed arrangement]`。

## Prospective-only hard gate

最初に「workは既に開始したか」を確認します。

既に開始していれば、restricted matter、Japanese labor/tax/social-insurance counsel、
remediation scopeへrouteして停止します。explicitにforward-looking structure analysisを
求められた場合だけ、existing exposure、back pay、tax/insurance、penaltyを分析しない
scope mismatchを明示して続行します。

## Mandatory worker-supply / current-law gate

1. `references/common/cowork-runtime-contract.md`を読み、exact scope/sourceを確認。
2. Japanなら
   `references/common/ja-jp/wage-worker-status.md`を使います。
3. purposeを別trackにします:
   `labor-standards | labor-contract | labor-union | social-insurance |
   tax | freelance-act | dispatch-worker-supply | osh`。
4. EOR/vendor/staffingではcost比較前にdaily direction、licence、genuine employer、
   dispatch/supply/outsourcing characterizationを確認します。
5. current statute、guidance、case law、effective dateを取得し、thin sourceでは停止。
6. strict/contested/existing arrangementはqualified counselへescalate。
7. AIはclassification、contract execution、reclassification、payroll/insurance、
   remediationを決定・実行しません。

recordは`references/classification-records.md`。

## 会話state

`prospective-gate` → `intake` → `identify-purposes` → `research-tests` →
`apply-factor-by-factor` → `dispatch-eor-gate` → `gap-analysis` →
`human-options`

## Intake

single block:

- actual day-to-day work、core/peripheral、project/end
- schedule/location/method control、supervision
- pay、equipment、exclusivity、profit/loss、business organization
- direct freelancer/vendor/dispatch/EOR intent
- contract party、who pays、who directs、who disciplines
- duration、team integration、similar employees
- physical work location/establishment
- each legal purpose

provided factsを再質問せず、unknownを明示します。

## Apply tests

each purposeにcurrent test/source/effective dateを示し、factor/prongを省略せず表に
します。LSA Article 9ではsubstance/use-dependenceを分析し、contract label、invoice、
corporationを決定的としません。Labor Union Act worker statusが別結果になる可能性を
示します。

Freelance Actはtransaction obligationsを追加しますがemployee status safe harbor
ではありません。social insurance/tax answerをlabor answerから推測しません。

## Dispatch/EOR blocker

次がunknownまたは不適合なら🔴:

- genuine employer
- daily instructions
- dispatch licence/placement authorization
- outsourcing independence
- work rules/36/payroll/insurance/OSH owner
- prohibited worker-supply risk

🔴のままEOR/entityを「viable」と書きません。

## Gap output

```markdown
## Worker status analysis

**Intended structure:** [...]
**Jurisdiction/purposes:** [...]
**Status:** Prospective draft | Existing-arrangement escalation | Blocked

### Purpose-by-purpose tests
| Purpose | Authority | Factors | Result |

### Dispatch / EOR legality
[gate]

### Gap analysis
🔴 [significant conflict]
🟠 [high]
🟡 [uncertain]
🟢 [supporting fact]

### Human options
[employee / restructure / licensed dispatch / genuine outsourcing / counsel]
```

upstream severityをfloorとして保持します。

## Consequential gate

engagement structure/contract/payrollを決める前にqualified Japanese labor、
tax、social-insurance review、exact contract/operations、approverを確認し、
analysis draftで停止します。

## 行わないこと

- existing arrangementのremediation/back-pay calculation
- label/entityをsafe harborにする
- U.S. ABC/economic-realities/1099をJapan defaultにする
- EOR legalityをcostで上書き
- worker status/payroll/insuranceを実行
