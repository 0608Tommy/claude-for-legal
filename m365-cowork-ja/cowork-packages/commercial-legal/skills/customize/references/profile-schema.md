> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Commercial profile records

## Company profile

```yaml
recordType: company-profile
tenantId: "[tenant id]"
organizationName: "[name]"
entityType: "[type]"
industry: "[industry]"
businessDescription: "[what is sold/bought]"
practiceSetting: "Solo / small firm | Midsize / large firm | In-house | Government / legal aid / clinic | Other"
jurisdictions:
  - "[jurisdiction]"
riskAppetite: conservative | middle | aggressive
```

## User profile

```yaml
recordType: user-profile
tenantId: "[tenant id]"
practiceId: "[practice id]"
userObjectId: "[Microsoft Entra object id]"
role: lawyer | legal-professional | non-lawyer-with-attorney | non-lawyer-without-attorney
attorneyContact: "[name/team/referral route]"
approvalAuthority:
  currency: "[ISO currency]"
  amount: "[number or null]"
```

## Commercial practice profile

```yaml
recordType: commercial-practice-profile
tenantId: "[tenant id]"
practiceId: "[practice id]"
pluginId: commercial-legal
setupStatus: complete | paused | draft
activeSide: sales | purchasing | both
playbooks:
  sales:
    reviewStatus: draft | approved
    limitationOfLiability:
      directCap: "[position]"
      indirectDamages: "[position]"
      carveouts:
        - "[position]"
      capBase: "[position]"
      fallbacks:
        - "[position]"
      never:
        - "[position]"
    indemnification: {}
    dataProtection: {}
    termTermination: {}
    governingLaw: {}
    ndaPositions: {}
    saasPositions: {}
    aiMlTrainingRights: {}
    oneThing: "[deal-breaker]"
  purchasing: {}
escalation:
  levels:
    - canApprove: "[role]"
      withoutEscalation: "[scope/threshold]"
      escalatesTo: "[name/role]"
      via: "[channel]"
  automaticTriggers:
    - "[trigger]"
houseStyle:
  redlineTone: "[tone]"
  stakeholderAudience: "[audience]"
  stakeholderLength: "[length]"
  draftDestination: OneDrive
  sharedOutputDestination: "[SharePoint outputs location]"
  renewalAlertDestination: "[destination]"
reviewPreferences:
  confirmRouting: true
ndaTriagePreferences:
  closingAction: "[text]"
matterWorkspaces:
  enabled: false
  crossMatterAccess: false
playbookMonitor:
  patternThreshold: 5
  lookbackMonths: 12
jurisdictionModules:
  - ja-JP
japanLawReviewStatus: pending
primarySourcesCheckedThrough: "2026-07-16"
```

空のmapをapprovedと扱わない。sales/purchasing各側の`reviewStatus`を別に持つ。

## Seed provenance

```yaml
seedDocuments:
  - itemId: "[exact SharePoint itemId]"
    version: "[version]"
    title: "[title]"
    agreementType: "[type]"
    counterparty: "[name]"
    signedDate: "[ISO date or null]"
    readCoverage: "[coverage]"
    notableTerms:
      - "[term]"
    oneOff: false
```

## Integration

```yaml
integrations:
  - id: Ironclad
    status: connected | configured-unverified | not-connected
    checkedAt: "[ISO datetime]"
    probeEvidence: "[tool call/event id or null]"
```

statusをconfiguration declarationだけで`connected`にしない。
