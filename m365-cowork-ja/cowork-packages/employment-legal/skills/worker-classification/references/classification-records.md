> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Worker classification analysis record

```yaml
jurisdiction: "[country/prefecture]"
prospective: true
intendedStructure: "[employee | freelancer | dispatch | outsourcing | EOR | vendor]"
purposes:
  - labor-standards
  - labor-contract
  - labor-union
  - social-insurance
  - tax
  - freelance-act
  - dispatch-worker-supply
  - osh
facts:
  work: {}
  control: {}
  economics: {}
  integration: {}
  entityAndContract: {}
tests:
  - purpose: "[purpose]"
    authority: "[source/effective date]"
    factors: []
    result: "[employee-leaning | nonemployee-leaning | fails | mixed | unknown]"
gaps:
  - severity: "[🔴 | 🟠 | 🟡 | 🟢]"
    factor: "[factor]"
    fact: "[fact]"
    authority: "[source]"
eorDispatchGate:
  genuineEmployer: "[yes | no | unknown]"
  dailyDirectionOwner: "[entity]"
  legalCharacterization: "[dispatch | placement | outsourcing | worker-supply | unknown]"
reviewStatus: pending
```

existing arrangementでは`prospective: false`としてremediation/counsel routeだけを作り、
このrecordをfinal classificationやback-pay scopeとして使いません。
