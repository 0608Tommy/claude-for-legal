> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Product legal profile records

company、practice、userの各blockはSharePoint `profiles`に保存するdomain payload
descriptorである。tenant/practice/userのscope、exact `itemId`、`eTag`、
idempotencyはgateway envelopeで管理し、payloadへactive matterや別利用者の値を
混在させない。setup sessionだけはSharePoint `state`の共通schemaに従う。

## Company profile

```yaml
recordType: company-profile
recordId: product-legal-company
payload:
  profileType: company
  organization: "[name]"
  businessModel: "[description]"
  products:
    - "[product]"
  productSurfaces:
    - web | app | marketplace | platform | hardware | other
  channels:
    - "[channel]"
  customers: consumer | b2b | both
  stage: "[stage]"
  listedOrReportingStatus: "[status]"
  jurisdictions:
    - ja-JP
  jurisdictionNexus:
    - jurisdiction: ja-JP
      bases:
        - users
        - data
        - operations
        - seller
        - operator
  sectors:
    - "[sector]"
  regulators:
    - "[regulator]"
  riskPosture: "[posture]"
  version: 1
```

## Practice profile

```yaml
recordType: product-legal-practice-profile
recordId: "product-legal:[practiceId]"
payload:
  pluginId: product-legal
  setupStatus: draft | paused | complete
  practiceSetting: Solo / small firm | Midsize / large firm | In-house | Government / legal aid / clinic | Other
  reviewProcess:
    intake: "[source]"
    leadTimeDays: 10
    posture: formal-gate | advisory
    outputFormat: "[format]"
    owners:
      productManager: "[Entra object/group or authorized record ID]"
      productLegal: "[Entra object/group or authorized record ID]"
      security: "[Entra object/group or authorized record ID]"
      privacy: "[Entra object/group or authorized record ID]"
      marketing: "[Entra object/group or authorized record ID]"
      publicDisclosure: "[Entra object/group or authorized record ID]"
  framework:
    categories:
      - id: contractual
        enabled: true
        evidenceRequired:
          - "[artifact type]"
    japanOverlays:
      - consumer-commerce
      - privacy-telecom
      - product-safety
      - platform-content
      - accessibility-minors
      - regulated-sectors
      - public-disclosure
    foreignOverlays:
      - id: "[overlay ID]"
        jurisdictions:
          - "[jurisdiction]"
        enabled: true
        evidenceRequired:
          - "[artifact type]"
    autoSkipFacts: []
    evidenceRequirements:
      - category: "[category or overlay ID]"
        requiredArtifacts:
          - "[artifact type]"
        minimumStandard: "[standard]"
  calibration:
    usuallyBlocks:
      - category: "[category or overlay ID]"
        pattern: "[pattern]"
        why: "[reason]"
        resolution: "[required resolution]"
        owner: "[Entra object/group or authorized record ID]"
        typicalTimeline: "[duration]"
        sourceReviewIds:
          - "[past review item ID]"
    usuallyRequiresWork:
      - category: "[category or overlay ID]"
        pattern: "[pattern]"
        why: "[reason]"
        resolution: "[required resolution]"
        owner: "[Entra object/group or authorized record ID]"
        typicalTimeline: "[duration]"
        sourceReviewIds:
          - "[past review item ID]"
    usuallyFyi:
      - category: "[category or overlay ID]"
        pattern: "[pattern]"
        why: "[reason]"
        resolution: "[monitoring or evidence]"
        owner: "[Entra object/group or authorized record ID]"
        typicalTimeline: "[duration]"
        sourceReviewIds:
          - "[past review item ID]"
    novelPatterns:
      - category: "[category or overlay ID]"
        pattern: "[unseen pattern]"
        why: "[why novel]"
        proposedResolution: "[human decision needed]"
        humanOwner: "[Entra object/group or authorized record ID]"
        typicalTimeline: "[duration or unknown]"
        sourceReviewIds:
          - "[past review item ID or none]"
        status: untested
    seedReview:
      actualReviewCount: 0
      reviews:
        - sourceItemId: "[past legal review item ID]"
          sourceVersion: "[version]"
          launchOrReviewDate: "[date]"
          issueCategory: "[category]"
          actualDecision: "[decision]"
          conditions:
            - "[condition]"
          outcome: blocked | shipped-with-work | shipped-fyi | unknown
          escalation: "[route/result]"
          outputFormat: "[format]"
          outputTone: "[tone]"
          laterLearning: "[learning or null]"
          readCoverage: "[coverage]"
          confidentiality: standard | heightened | restricted | clean-team
          authorizedViewerIds:
            - "[Microsoft Entra user/group ID]"
      missingDocuments:
        - "[missing review/document]"
      coverage: "[coverage]"
      confidence: provisional | calibrated
  escalation:
    defaultOwner: "[Entra object/group or authorized record ID]"
    supervisingAttorneyRoute: "[authorized route or null]"
    routes:
      - trigger: "[trigger]"
        owner: "[Entra object/group or authorized record ID]"
        fallbackOwner: "[Entra object/group or authorized record ID]"
        targetResponseHours: 24
  claims:
    reviewer: "[Entra object/group or authorized record ID]"
    comparative:
      posture: "[position]"
      evidenceStandard: "[standard]"
    substantiation:
      standard: "[standard]"
      evidenceBeforePublication: true
    absoluteClaims:
      defaultPosture: "[position]"
      security: "[position]"
      ai: "[position]"
      medical: "[position]"
      financial: "[position]"
    commonRejectedClaims: []
    visualReviewRequired: true
    commerceScreens:
      subscriptionFinalScreenOwner: "[Entra object/group or authorized record ID]"
    stealth:
      owner: "[Entra object/group or authorized record ID]"
      processSourceItemId: "[item ID or null]"
      processSourceVersion: "[version or null]"
      influencerInstructions: "[process]"
      reviewSolicitation: "[process]"
      reviewModeration: "[process]"
      disclosureStandard: "[standard]"
      syntheticPersonOrReviewRule: "[rule]"
    platformPolicyOwner: "[Entra object/group or authorized record ID]"
  sectorRules:
    privacyTelecom:
      triggers: []
      requiredEvidence: []
      defaultPosture: "[posture]"
      owner: "[owner]"
    consumerClaims:
      triggers: []
      requiredEvidence: []
      defaultPosture: "[posture]"
      owner: "[owner]"
    productSafetyPlatform:
      triggers: []
      requiredEvidence: []
      defaultPosture: "[posture]"
      owner: "[owner]"
    accessibilityMinors:
      triggers: []
      requiredEvidence: []
      defaultPosture: "[posture]"
      owner: "[owner]"
    paymentsFinance:
      triggers: []
      requiredEvidence: []
      defaultPosture: "[posture]"
      owner: "[owner]"
    medicalHealth:
      triggers: []
      requiredEvidence: []
      defaultPosture: "[posture]"
      owner: "[owner]"
    cyberAiIp:
      triggers: []
      requiredEvidence: []
      defaultPosture: "[posture]"
      owner: "[owner]"
    publicDisclosure:
      triggers: []
      requiredEvidence: []
      defaultPosture: "[posture]"
      owner: "[owner]"
  matterWorkspaces:
    enabled: false
    crossMatterDefault: false
  integrations:
    stateGateway:
      status: not-connected | configured-unverified | connected
      connectionReferenceId: "[reference ID or null]"
      solutionVersion: "[version or null]"
      checkedAt: "[ISO-8601]"
      checkedBy: "[userObjectId]"
    sharepoint:
      status: not-connected | configured-unverified | connected
      siteId: "[site ID or null]"
      profilesId: "[list/library ID or null]"
      mattersId: "[list/library ID or null]"
      outputsId: "[list/library ID or null]"
      stateId: "[list ID or null]"
      auditId: "[list ID or null]"
      sourceVersion: "[version or null]"
      checkedAt: "[ISO-8601]"
      checkedBy: "[userObjectId]"
    onedrive:
      status: not-connected | configured-unverified | connected
      driveId: "[drive ID or null]"
      draftFolderId: "[folder ID or null]"
      sourceVersion: "[version or null]"
      checkedAt: "[ISO-8601]"
      checkedBy: "[userObjectId]"
    optionalSources:
      - sourceId: "[connector/source ID]"
        declaredTransport: "[transport]"
        targetTransport: "[transport or null]"
        status: not-connected | configured-unverified | adapter-required | connected
        connectionReferenceId: "[reference ID or null]"
        sourceVersion: "[version or null]"
        checkedAt: "[ISO-8601]"
        checkedBy: "[userObjectId]"
  storageControls:
    retentionPolicyIds: []
    dlpPolicyIds: []
    legalHoldPolicyIds: []
    approvedDestinationIds: []
  legalReview:
    originalJurisdictionTranslation: pending | in-review | approved | blocked
    japanLawLocalization: pending | in-review | approved | blocked
  japanModule:
    jurisdictionModules:
      - ja-JP
    japanLawReviewStatus: pending
    primarySourcesCheckedThrough: "2026-07-16"
    appi2026AmendmentStatus: diet-passed-2026-07-10-unpromulgated-main-effective-within-two-years
    cyberReporting2026Status: future-effective-2026-10-01-scope-check-required
    electionAiStatus: future-effective-2027-03-01-not-general-label
  watcherPreference:
    desiredHorizonDays: 30
    desiredCadence: daily
    trackerScope:
      sourceSystem: "[tracker/source]"
      sourceItemOrQueryId: "[scope ID]"
      sourceVersion: "[version]"
    triggerCategories:
      - "[category]"
    proposedDestination: "[destination or null]"
    proposedViewerIds:
      - "[Microsoft Entra user/group ID]"
    automationStatus: not-provisioned
  configurationSources:
    - area: review-process | framework | calibration | escalation | claims | sector
      sourceSystem: "[SharePoint or approved connector]"
      sourceItemId: "[item ID]"
      sourceVersion: "[version]"
      checkedAt: "[ISO-8601]"
      checkedBy: "[userObjectId]"
  production:
    coworkPromptDlpRequired: true | false
    readiness: blocked | eligible
    enabled: false
    blocker: "[reason or null]"
  version: 1
```

watcher preferenceはautomation evidenceではない。
`production.enabled`はsetup preferenceではなく、legal review、gateway、tenant
acceptance、DLP等のrequired gateを管理者が確認した結果としてのみ変更する。

## User profile

```yaml
recordType: user-profile
recordId: "user:[userObjectId]"
payload:
  userObjectId: "[Microsoft Entra object ID]"
  role: lawyer-legal-professional | non-lawyer-with-attorney | non-lawyer-without-attorney
  attorneyContact: "[Entra ID/role or null]"
  authorizedDestinations:
    - "[destination ID]"
  version: 1
```

## Setup session

canonical mappingは`scopeType: session`、
`scopeId: [userObjectId]:[sessionId]`、`recordType: setup-session`、
`recordId: setup`である。

### Conditional create request

```yaml
tenantId: "[tenant id]"
practiceId: "[practice id]"
scopeType: session
scopeId: "[userObjectId]:[sessionId]"
recordType: setup-session
recordId: setup
idempotencyKey: "[16-256 character idempotency key]"
expectedAbsent: true
payload:
  userObjectId: "[Microsoft Entra object ID]"
  sessionId: "[Cowork session ID]"
  setupStatus: draft
  pausedAt: null
  answeredSections: []
  pendingQuestions: []
  profileItemId: null
```

### Conditional pause update

```yaml
tenantId: "[tenant id]"
practiceId: "[practice id]"
scopeType: session
scopeId: "[userObjectId]:[sessionId]"
recordType: setup-session
recordId: setup
itemId: "[exact SharePoint state item ID]"
eTag: "[latest eTag]"
idempotencyKey: "[16-256 character idempotency key]"
patch:
  setupStatus: paused
  pausedAt: "[section]"
  answeredSections:
    - "[section]"
  pendingQuestions:
    - "[question]"
  profileItemId: "[profile item ID or null]"
```

shared practice profileへsingle user role/attorney contact/active matterを入れない。
new recordは`expectedAbsent: true`、updateはexact `itemId`とlatest `eTag`を使う。
