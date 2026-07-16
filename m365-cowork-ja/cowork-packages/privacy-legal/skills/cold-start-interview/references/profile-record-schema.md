> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Privacy profile record schema

## Company profile

```yaml
recordType: company-profile
tenantId: "[tenant id]"
organizationId: "[organization id]"
itemId: "[SharePoint itemId]"
eTag: "[eTag]"
name: "[organization name]"
practiceSetting: "[setting]"
jurisdictions:
  - "[jurisdiction]"
industry: "[industry]"
productsAndServices: "[products, services, users]"
size: "[employee/user/relevant size]"
primaryJurisdiction: "[jurisdiction]"
regulators:
  - "[regulator]"
openRegulatoryMatters:
  - "[matter or none]"
overallRiskAppetite: conservative | middle | aggressive | pending
worstDay: "[material privacy failure]"
leadershipQuestion: "[recurring leadership question]"
```

## Practice profile

```yaml
recordType: privacy-practice-profile
tenantId: "[tenant id]"
practiceId: "[practice id]"
pluginId: privacy-legal
locale: ja-JP
setupStatus: complete
companyProfileItemId: "[SharePoint itemId]"
orientation:
  - controller
organizationContexts:
  - B2B | B2C | employer | public-function
dataSubjectGroups:
  - "[customers / users / employees / applicants / children / other]"
activityRoles:
  - activity: "[processing activity]"
    role: controller | processor | joint-controller | APPI-outsourcing | other
dataLocations:
  - "[country/system]"
privacyTeam:
  lead: "[role]"
  dpo: "[role or N/A]"
  securityPartner: "[role]"
regulatoryFootprint:
  laws:
    - "[law/regime]"
  regulators:
    - "[authority]"
  transferCorridors:
    - "[from → to]"
  openInquiries:
    - "[inquiry or none]"
jurisdictions:
  - ja-JP
jurisdictionModules:
  - ja-JP
japanLawReviewStatus: pending
primarySourcesCheckedThrough: "2026-07-16"
appi2026AmendmentStatus: enacted-promulgation-pending-not-effective
riskPosture: conservative | middle | aggressive | pending
integrations:
  sharepoint: connected
  onedrive: connected
  Slack: configured-unverified
  Google Drive: not-connected
dpaPlaybook:
  processor:
    audit:
      standard: "[position]"
      fallback: "[position]"
      never: "[position]"
    incident:
      standard: "[position]"
      fallback: "[position]"
      never: "[position]"
    subprocessor:
      standard: "[position]"
      fallback: "[position]"
      never: "[position]"
    locationTransfer:
      standard: "[position]"
      fallback: "[position]"
      never: "[position]"
    deletionBackup:
      standard: "[position]"
      fallback: "[position]"
      never: "[position]"
    liability:
      standard: "[position]"
      fallback: "[position]"
      never: "[position]"
    independentUseTraining:
      standard: "[position]"
      fallback: "[position]"
      never: "[position]"
  controller:
    security:
      require: "[position]"
      acceptable: "[position]"
      never: "[position]"
    incident:
      require: "[position]"
      acceptable: "[position]"
      never: "[position]"
    subprocessor:
      require: "[position]"
      acceptable: "[position]"
      never: "[position]"
    locationTransfer:
      require: "[position]"
      acceptable: "[position]"
      never: "[position]"
    deletionBackup:
      require: "[position]"
      acceptable: "[position]"
      never: "[position]"
    liability:
      require: "[position]"
      acceptable: "[position]"
      never: "[position]"
    audit:
      require: "[position]"
      acceptable: "[position]"
      never: "[position]"
    independentUseTraining:
      require: "[position]"
      acceptable: "[position]"
      never: "[position]"
  oneThing: "[automatic reject]"
  reviewStatus: pending | reviewed
policyCommitments:
  sourceItemId: "[itemId]"
  sourceVersion: "[version]"
  dataCategories:
    - "[category]"
  purposes:
    - "[purpose]"
  retention:
    - "[rule]"
  recipients:
    - "[recipient/category]"
  rights:
    - "[right]"
commitmentSurfaces:
  websitePolicyItemId: "[itemId]"
  cmpConfigItemId: "[itemId or null]"
  appStoreLabelItemId: "[itemId or null]"
  googleDataSafetyItemId: "[itemId or null]"
  employeeNoticeItemId: "[itemId or null]"
  sectorNoticeItemIds:
    - "[itemId]"
piaHouseStyle:
  trigger: "[internal trigger]"
  format: "[source or baseline]"
  depth: "[depth]"
  signOff: "[role]"
  sections:
    - "[section]"
  riskScale:
    - "[severity label and meaning]"
dsarProcess:
  handler: "[role]"
  systems:
    - "[system ID]"
  identityMethod: "[method]"
  internalSla: "[target]"
  secureDelivery: "[method]"
escalation:
  - issue: "[issue]"
    escalateTo: "[role]"
    trigger: "[trigger]"
seedDocuments:
  - type: privacy-policy
    itemId: "[itemId]"
    version: "[version]"
    reviewedOn: "[date]"
    readCoverage: "[coverage]"
outputs:
  libraryId: "${M365_OUTPUTS_LIBRARY_ID}"
  namingConvention: "[no person names]"
  policySweepCursorRecordType: policy-sweep-cursor
deploymentReadiness:
  stateGatewayStatus: not-configured | configured-unverified | connected
  coworkDlpSupported: false
  coworkDlpRequired: true | false
  productionBlocked: true
matterWorkspaces:
  enabled: false
  crossMatterAccess: false
```

## User profile

```yaml
recordType: user-profile
tenantId: "[tenant id]"
practiceId: "[practice id]"
userObjectId: "[Entra object ID]"
role: "Lawyer / legal professional"
attorneyContact: "[name/team/N/A]"
eTag: "[eTag]"
```

## Session binding

```yaml
recordType: session-matter-binding
tenantId: "[tenant id]"
practiceId: "[practice id]"
userObjectId: "[Entra object ID]"
sessionId: "[Cowork session ID]"
matterId: "[matter ID]"
status: active | revoked
boundAt: "[ISO-8601]"
boundBy: "[Entra object ID]"
expiresAt: "[ISO-8601]"
revokedAt: "[ISO-8601 or null]"
revokedBy: "[Entra object ID or null]"
revocationReason: "[reason or null]"
```

shared profileへsingle user roleまたはsingle active matterを保存しない。
