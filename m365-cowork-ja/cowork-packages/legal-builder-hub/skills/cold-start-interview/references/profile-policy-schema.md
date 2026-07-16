> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Profile / policy schema

## `builder-user-profile`

```yaml
tenantId: "[tenant ID]"
practiceId: "[practice ID]"
userObjectId: "[Entra object ID]"
role: lawyer-legal-professional | non-lawyer-with-attorney | non-lawyer-without-regular-attorney
attorneyContactId: "[ID or null]"
securityContactId: "[ID or null]"
plainLanguageMode: true
recommendationPreference: all | matching-practice-profile | none
updatePreference: notify | manual
```

## `builder-practice-profile`

```yaml
practiceAreas:
  - "[canonical category]"
industry: "[category]"
teamSize: solo | small | midsize-large | government-clinic | other
primaryWork:
  - "[category]"
toolingComfort: builder | tinkerer | just-make-it-work
jurisdictions:
  - "[canonical jurisdiction]"
deploymentContext: personal | firm-internal | product-embedding | tenant-wide
```

## `builder-setup-session`

```yaml
setupStatus: initial | in-progress | paused | complete
path: quick | full
answeredSections:
  - "[section]"
pendingQuestionId: "[ID or null]"
profileDraftHash: "[SHA-256]"
policyDraftHash: "[SHA-256]"
```

## Tenant policy draft

```yaml
registries: []
publishers: []
licenseRules: []
connectorRules: []
freshnessThresholds: {}
requiredReviewers: []
targetGroupIds: []
retentionPolicyId: "[ID or null]"
dlpPolicyId: "[ID or null]"
```

tenant policy draftはapproved policyではない。profileへcredential、matter secret、
raw package textを入れない。
