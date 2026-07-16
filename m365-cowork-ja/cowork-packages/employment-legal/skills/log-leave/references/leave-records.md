> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Leave case records

## Canonical state

```yaml
tenantId: "[tenant id]"
practiceId: "[practice id]"
scopeType: matter
scopeId: "[restricted matterId]"
recordType: leave-case
recordId: "leave:[leaveId]"
payload:
  leaveId: "[opaque ID]"
  employeePseudonym: "[EMP-0001]"
  substantiveRecordItemId: "[restricted matter document item ID]"
  establishment: "[establishment ID]"
  prefecture: "[prefecture]"
  leaveType: "[maternity | childcare | post-birth-childcare | child-care-days | family-care | family-care-days | annual-leave | occupational-injury | disability-accommodation | company-leave | other]"
  lifecycle: open | approved | active | returned | closed | cancelled
  eligibilityStatus: "[verified | pending | not-applicable]"
  nextDecisionPoint: "[opaque summary]"
  nextDueCandidate: "[date or unknown]"
  ownerObjectId: "[human owner]"
  controllingSources: []
  asOfDate: "[date]"
  reviewStatus: pending
  actualReturn: "[date or null]"
  closedAt: "[ISO-8601 or null]"
  closedBy: "[object ID or null]"
  lastCheckedAt: "[ISO-8601]"
```

child DOB、family relationship、medical/accommodation facts、schedule、requested/
approved periods、insurance benefit、annual-leave accounting、job-protection
analysis、notesはgeneric stateへ入れず、`substantiveRecordItemId`が指すrestricted
matter documentに保存する。

```yaml
recordType: leave-details-document
leaveId: "[opaque ID]"
requestedStart: "[date]"
requestedEnd: "[date or null]"
approvedStart: "[date or null]"
approvedEnd: "[date or null]"
intermittent: false
normalSchedule: "[actual schedule]"
childDateOfBirth: "[date or null]"
coveredFamilyCategory: "[category or null]"
exclusionAgreementChecked: false
employerProcedure:
  individualNoticeAt: "[date or null]"
  intentionConfirmedAt: "[date or null]"
  intentionHeardAt: "[date or null]"
  accommodationReviewedAt: "[date or null]"
jobProtection: {}
insuranceBenefit: {}
annualLeaveAccounting: {}
healthAccommodation: {}
notes: "[minimum necessary]"
```

new caseは`expectedAbsent: true`、updateはexact`itemId`、latest`eTag`、unique
`idempotencyKey`。氏名・診断はstate key/auditへ入れません。

lifecycle transitionはcurrent valueとevidenceを示してfresh confirmation後に
conditional updateする。`returned | closed | cancelled`はopen alert queryから除外し、
reopenは別の明示transitionとauditを要求する。

## Alert candidate

```yaml
leaveId: "[leaveId]"
decisionPoint: "[what must be decided]"
owner: "[human owner]"
legalClockOwner: "[employer | employee | insurer | none-internal]"
dueCandidate: "[date or unknown]"
source: "[official source/effective date]"
calculationInputs: {}
missingFacts: []
severity: "[🔴 | 🟠 | 🟡 | 🟢]"
automationScheduled: false
```

alertはleave approval/denial、accommodation、payroll/benefit、termination decision
ではありません。
