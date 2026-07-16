> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、日本のcorporate profile state向けに変更した派生ファイルです。

# Profile record schema

## Company profile

```yaml
recordType: company-profile
tenantId: "[tenant id]"
organizationId: "[organization id]"
itemId: "[SharePoint itemId]"
eTag: "[eTag]"
name: "[organization name]"
practiceSetting: "[setting]"
industry: "[industry]"
productsAndServices: "[products/services]"
size: "[employee/entity/public-company scale]"
jurisdictions:
  - "[jurisdiction]"
primaryJurisdiction: "[jurisdiction]"
regulators:
  - "[regulator]"
overallRiskAppetite: conservative | middle | aggressive | pending
```

## Corporate practice profile

```yaml
recordType: corporate-practice-profile
tenantId: "[tenant id]"
practiceId: "[practice id]"
pluginId: corporate-legal
locale: ja-JP
setupStatus: complete | paused
companyProfileItemId: "[SharePoint itemId]"
riskPosture: conservative | middle | aggressive | pending
activeModules:
  - m&a
  - board
  - public
  - entities
jurisdictionModules:
  - ja-JP
japanLawReviewStatus: pending
primarySourcesCheckedThrough: "2026-07-16"
appi2026AmendmentStatus: passed-promulgation-and-effective-date-unconfirmed
companiesAct2026ProposalStatus: pending-not-law
coworkPromptDlpSupported: false
productionBlockedWhenCoworkDlpMandatory: true
integrations:
  stateGateway: not-configured | configured-unverified | connected
  sharepoint: not-configured | configured-unverified | connected
  onedrive: not-configured | configured-unverified | connected
  vdr: not-configured | configured-unverified | connected
  boardPortal: not-configured | configured-unverified | connected
  entitySystem: not-configured | configured-unverified | connected
  registryFiling: not-configured | configured-unverified | connected
integrationProbe:
  checkedAt: "[ISO-8601]"
  checkedBy: "[userObjectId]"
  resultsItemId: "[audit itemId]"
boardAndConsent:
  boardSize: "[number or pending]"
  committees:
    - "[committee]"
  calendar: "[cadence]"
  minutesStyle: "[style/source]"
  consentStyle: "[style/source]"
  article370Authorized: true | false | unknown
  electronicSignaturePolicy: "[policy]"
  shareholderMeetingRules: "[rules]"
entityWorkflow:
  entitySystem: "[system/manual]"
  registeredAgent: "[provider/owner]"
  filingOwner: "[role]"
  periodicReviewCadence: "[cadence]"
  rebuildApprovalRequired: true
integrationWorkflow:
  defaultWorkplan: "[source/baseline]"
  consentOwner: "[role]"
  contractTransferOwner: "[role]"
  employeeTransferOwner: "[role]"
  licenceTransferOwner: "[role]"
```

## Japan entity foundation

```yaml
entityId: "[ID]"
entity_form: KK | GK | other
legalName: "[name]"
registered_head_office: "[address]"
corporateNumber13: "[13-digit 法人番号]"
companyCorporateNumber12: "[12-digit 会社法人等番号]"
organ_design: "[design]"
articlesItemId: "[itemId]"
articlesVersion: "[version]"
publicNoticeMethod: "[method]"
shareCertificateStatus: "[status]"
restrictedShares: true | false | unknown
art370Authorized: true | false | unknown
listedMarket: "[market or null]"
edinetCode: "[code or null]"
```

## M&A profile

```yaml
typicalSide: buy-side | sell-side | both
transactionStructures:
  - share sale
materiality:
  contractInternalThreshold: "[value]"
  litigationInternalThreshold: "[value]"
issueMemo:
  severity: "[scheme]"
  format: "[format]"
aiReview:
  tool: Luminance | Kira | none | other
  trustLevel: use as-is | spot-check | full re-review
  externalTransferApprovalRequired: true
```

## Public company profile

```yaml
listed: true | false
exchange: "[exchange]"
market: "[market]"
edinetCode: "[code]"
fiscalYearEnd: "[date]"
filingCalendar:
  annualSecuritiesReport: "[rule]"
  halfYearReport: "[rule]"
  internalControlReport: "[rule]"
  confirmation: "[rule]"
  extraordinaryReport: "[rule]"
  tdnet: "[rule]"
  governanceReport: "[rule]"
insiderControls:
  art163Owner: "[role]"
  arts166167Owner: "[role]"
  preclearance: "[process]"
  tradingWindow: "[process]"
largeHoldingOwner: "[role]"
tenderOfferOwner: "[role]"
```

## Deal profile

```yaml
recordType: corporate-deal-profile
tenantId: "[tenant id]"
practiceId: "[practice id]"
scopeType: practice | matter
scopeId: "[practiceId or matterId]"
recordId: "deal:[dealCode]"
dealCode: "[code]"
matterId: "[matter ID or null until matter-workspace completes]"
side: buy-side | sell-side
transactionStructure: share sale | business transfer | merger | company split | share exchange | share transfer | share delivery | other
target: "[name]"
targetListed: true | false
foreignInvestorFacts: "[facts]"
ultimateControl: "[facts]"
japanTurnover:
  acquiringGroup: "[value]"
  targetGroup: "[value]"
votingRights:
  before: "[percent]"
  after: "[percent]"
designatedOrCoreBusiness:
  - "[business]"
sectorLicences:
  - "[licence]"
```

## User profile

```yaml
recordType: user-profile
tenantId: "[tenant id]"
practiceId: "[practice id]"
userObjectId: "[Microsoft Entra object ID]"
role: Lawyer / legal professional | Non-lawyer with attorney access | Non-lawyer without regular attorney access
attorneyContact: "[person/route]"
eTag: "[eTag]"
```

company、practice、user、deal、setup stateを別recordにする。single active matterを
practice profileへ保存しない。
