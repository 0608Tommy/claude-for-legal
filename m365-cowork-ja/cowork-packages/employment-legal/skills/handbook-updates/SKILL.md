---
name: handbook-updates
description: >
  proposed handbook・就業規則変更をcurrent exact versionとdiffし、cross-reference、mandatory terms、事業場・都道府県・CBA annex、不利益変更、majority union/representative意見、届出・周知、transitionを確認する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: employment-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Handbook updates

旧来のlabel:
`/employment-legal:handbook-updates [proposed change]`。

## Mandatory version / work-rules gate

1. `references/common/cowork-runtime-contract.md`を読み、exact current/proposed
   item/version、coverage、destinationを確認します。
2. changeが`就業規則`またはその変更かを判定します。
3. establishment/headcount、10+ filing、majority union/representative、CBA、
   current dissemination evidenceを確認します。
4. benefit/conditionを下げる場合、LCA Article 10、reasonableness、notice、
   transition、individual consent issueをcurrent sourceで確認します。
5. work rulesと36 agreement/other labor-management agreementを分けます。
6. restricted employee matterのfactsをpolicy documentへ持ち込みません。
7. AIはpublish、file、notify、acknowledgment collectionを実行しません。

checklist:
`references/work-rules-change-checklist.md`。

## 会話state

`identify-change` → `load-exact-versions` → `diff` →
`cross-reference-scan` → `work-rules-analysis` → `annex-impact` →
`promise-transition` → `implementation-checklist` → `human-review`

## Step 1 — Change

- section/new language/reason
- planned effective date
- covered entity/establishments/employees
- current and proposed exact source/version

## Step 2 — Diff

```diff
- [current exact text]
+ [proposed exact text]
```

large handbookではread sections/coverageを示し、全体cross-referenceを完了したと
誤表示しません。

## Step 3 — Ripple

- defined terms
- other policies/forms/processes
- working-time/payroll/HRIS/training
- leave/accommodation/harassment/whistleblower
- disciplinary matrix
- privacy/monitoring/retention
- establishment/prefecture/CBA annexes

each cross-referenceを`accurate | broken | needs review | not read`へ分類します。

## Step 4 — Work-rule procedure

常時10人以上の事業場についてmandatory terms、opinion document、filing destination、
dissemination、effective dateをchecklist化します。employee representative opinionを
automatic consentと書きません。不利益変更はseparate legal analysisです。

## Step 5 — Promise/transition

accrued benefit、existing employee、fixed-term renewal、discipline、leave、retirement
等へのretroactive impactを確認し、grandfather/transition/individual notice候補を
示します。AIは採用するoptionを決めません。

## Output

```markdown
## Handbook / work-rules update — [section]

### Exact diff
[diff]

### Cross-reference impact
| Section/system | Version | Impact | Fix |

### Establishment/CBA annex impact
| Scope | Current | Proposed impact | Action |

### Work-rule procedure
[opinion/filing/dissemination/effective-date checklist]

### Promise/transition
[flags/options]
```

## 行わないこと

- source未読を「影響なし」とする
- state supplementsをJapanへ機械移植
- opinionをconsentとする
- draftをpublish/file/send
- old versionをdelete
