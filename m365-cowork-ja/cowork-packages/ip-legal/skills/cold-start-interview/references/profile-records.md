> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# IP profile records

## Practice profile

```yaml
recordType: ip-practice-profile
recordId: "ip-practice:[practiceId]"
payload:
  pluginId: ip-legal
  setupStatus: draft | paused | complete
  practiceSetting: Solo / small firm | Midsize / large firm | In-house | Government / legal aid / clinic | Other
  practiceAreas:
    - patent
    - utility-model
    - trademark
    - copyright
    - trade-secret
    - oss
    - design
    - transactions
    - portfolio
  jurisdictions:
    primary:
      - "[jurisdiction]"
    filingRoutes:
      - "[PCT | Madrid | Hague | national]"
  enforcement:
    defaultPosture: aggressive | measured | conservative
    approvers:
      ceaseDesist: "[role/object ID]"
      takedown: "[role/object ID]"
      litigation: "[role/object ID]"
    automaticEscalations:
      - "[trigger]"
  portfolio:
    sourceSystem: "[IPMS/manual/none]"
    owner: "[object/team ID]"
    lastAudit: "[ISO-8601 or null]"
    alertCadenceCandidate: weekly | monthly | quarterly | on-demand
  brand:
    watchedMarks:
      - "[mark]"
    jurisdictions:
      - "[jurisdiction]"
    service: "[service or none]"
  oss:
    policySourceItemId: "[item ID or null]"
    accepted:
      - "[licence]"
    review:
      - "[licence]"
    blocked:
      - "[licence]"
  legalReview:
    originalJurisdictionTranslation: pending | in-review | approved | blocked
    japanLawLocalization: pending | in-review | approved | blocked
  matterWorkspaces:
    enabled: false
    crossMatterAccess: false
    cleanTeamDefault: false
  integrations:
    stateGateway: not-connected | configured-unverified | connected
    sharepoint: not-connected | configured-unverified | connected
    onedrive: not-connected | configured-unverified | connected
    ipms: not-connected | configured-unverified | connected
    jpoSource: not-connected | configured-unverified | connected
    researchConnectors: not-connected | configured-unverified | connected
    checkedAt: "[ISO-8601]"
    checkedBy: "[userObjectId]"
  production:
    coworkPromptDlpRequired: true | false
    readiness: blocked | eligible
    enabled: false
    requiredGates:
      originalJurisdictionReviewApproved: false
      japanLawReviewApproved: false
      stateGatewayConnected: false
      tenantSmokeTestPassed: false
      coworkDlpRequirementSatisfied: false
    blocker: "[reason or null]"
```

`production.enabled`はdirectly editableなpreferenceではなく、全required gateが
trueでauthorized administratorがdeploymentを有効化した結果としてのみ変更する。

## User profile

```yaml
recordType: user-profile
recordId: "user:[userObjectId]"
payload:
  role: Lawyer / legal professional | Registered patent agent | Non-lawyer with attorney access | Non-lawyer without attorney access
  japanProfessionalRole: bengoshi | benrishi | supervised legal professional | other | not-applicable
  registrationJurisdictions:
    - "[jurisdiction]"
  attorneyContact: "[object/authorized record ID or null]"
  supervisingAttorney: "[object/authorized record ID or null]"
```

single user valueをshared practice profileへ保存しません。
