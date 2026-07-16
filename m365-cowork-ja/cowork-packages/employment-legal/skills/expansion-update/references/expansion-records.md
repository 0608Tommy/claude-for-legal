> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Expansion project records

## Project

```yaml
tenantId: "[tenant id]"
practiceId: "[practice id]"
scopeType: practice | matter
scopeId: "[practiceId or country-expansion matterId]"
recordType: expansion-project
recordId: "expansion:[countryCode]:[projectId]"
payload:
  projectId: "[opaque ID]"
  country: "[official country name]"
  countryCode: "[ISO code]"
  matterId: "[matterId or null for practice scope]"
  kickoffDate: "[date]"
  firstHireTarget: "[date or null]"
  headcount12mo: "[integer or unknown]"
  roles: []
  strategicCommitment: testing | long-term | unknown
  structureStatus: EOR | entity | undecided | blocked-illegal-candidate
  legalFeasibility: pending | cleared-by-counsel | blocked
  outsideCounselEngaged: false
  peRiskFlagged: false
  privacyTransferFlagged: false
  reviewStatus: pending
  asOfDate: "[date]"
```

## Item

```yaml
tenantId: "[tenant id]"
practiceId: "[practice id]"
scopeType: practice | matter
scopeId: "[practiceId or matterId]"
recordType: expansion-item
recordId: "expansion:[projectId]:item:[itemId]"
payload:
  itemId: "[opaque ID]"
  category: structure | tax | finance | hr | privacy | immigration | outside-counsel | compliance
  item: "[single action]"
  owner: "[human/function]"
  status: open | in-progress | done | blocked
  due: "[date or null]"
  dependsOn: []
  questions: []
  authority: "[source/effective date or null]"
  evidenceItemIds: []
  notes: ""
```

project/itemsはseparate conditional creates。updateは1 itemずつexact`itemId`/`eTag`。
batch confirmationでもeach outcomeをauditし、partial failureを隠しません。
