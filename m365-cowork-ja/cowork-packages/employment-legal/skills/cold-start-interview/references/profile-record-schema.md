> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Employment profile/state schema

## Company profile

`tenantId + profileType`

```yaml
profileType: company-profile
organization: "[name]"
practiceSetting: "[enum]"
industry: "[industry]"
operationJurisdictions: []
riskPosture: "[conservative | balanced | aggressive | custom]"
```

## Practice profile

`tenantId + practiceId + pluginId`

```yaml
pluginId: employment-legal
profileType: employment-practice-profile
setupStatus: "[quick | complete | paused]"
jurisdictionFootprint: []
establishments: []
workRules: []
article36Agreements: []
workingTimeSystems: []
unionsAndCbas: []
hiringReview: {}
terminationReview: {}
workerClassification: {}
leaveAndAccommodation: {}
investigation: {}
internationalEmployment: {}
socialInsurance: {}
futureLawReadiness: {}
restrictedMatterIsolation:
  enabled: true
  triggerTypes:
    - investigation
    - whistleblowing
    - medical-accommodation
    - leave
    - discipline
    - contested-termination
legalReview:
  originalJurisdictionTranslation: pending
  japanLawLocalization: pending
  checkedThrough: "2026-07-16"
```

## User profile

`tenantId + practiceId + userObjectId`

```yaml
role: "[canonical role enum]"
attorneyContact: "[name/role or N/A]"
authority: []
approvedDestinations: []
```

## Setup session

generic state key:

```yaml
tenantId: "[tenant id]"
practiceId: "[practice id]"
scopeType: user
scopeId: "[userObjectId]"
recordType: setup-session
recordId: "setup:[sessionId]"
idempotencyKey: "[unique]"
expectedAbsent: true
payload:
  pluginId: employment-legal
  userObjectId: "[Microsoft Entra object ID]"
  sessionId: "[Cowork session ID]"
  setupStatus: paused
  pausedAt: "[section]"
  answeredSections: []
  pendingQuestions: []
```

existing setup/profileはexact `itemId`、latest `eTag`、new `idempotencyKey`でupdate
します。company/practice/user/setupを1 recordへ混ぜません。
