> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# IP portfolio records

## Version

```yaml
tenantId: "[tenant id]"
practiceId: "[practice id]"
scopeType: practice | matter
scopeId: "[practiceId or matterId]"
recordType: ip-portfolio-version
recordId: "portfolio:[portfolioId]:version:[version]"
payload:
  portfolioId: "[immutable portfolio ID]"
  version: 1
  status: building | active | superseded | failed
  sourceSet:
    - sourceSystem: "[system]"
      sourceItemId: "[item ID]"
      sourceVersion: "[version]"
      checkedAt: "[ISO-8601]"
  assetCount: 0
  createdAt: "[ISO-8601]"
itemId: "[SharePoint item ID]"
eTag: "[eTag]"
version: 1
updatedAt: "[ISO-8601]"
```

active pointer:

```yaml
recordType: portfolio-active-version
recordId: "portfolio:[portfolioId]:active"
payload:
  activeVersionRecordId: "[version record ID]"
  activatedAt: "[ISO-8601]"
  activatedBy: "[Entra object ID]"
```

初回はversion recordと全assetを検証して`active`にした後、pointerを
`expectedAbsent: true`でcreateする。rebuildはnew version配下の全assetを
materialize・検証してからpointerをupdateする。

## Asset

```yaml
recordType: ip-asset
recordId: "portfolio:[portfolioId]:version:[version]:asset:[assetId]"
payload:
  assetId: "[immutable asset ID]"
  type: trademark | patent | utility-model | design | copyright | domain
  jurisdiction: "[jurisdiction]"
  route: "[national | PCT | Madrid | Hague | other]"
  markOrTitle: "[authorized value]"
  ownerOfRecord: "[entity]"
  representative: "[person/firm or null]"
  status: pending | registered | granted | active | lapsed | abandoned | cancelled | expired | unknown
  applicationNumber: "[number or null]"
  registrationNumber: "[number or null]"
  filingDate: "[YYYY-MM-DD or null]"
  priorityDate: "[YYYY-MM-DD or null]"
  registrationOrGrantDate: "[YYYY-MM-DD or null]"
  filingCohort: "[cohort or null]"
  classesOrClaims:
    - "[value]"
  officialSource:
    url: "[https URL]"
    sourceItemId: "[official record ID]"
    sourceVersion: "[version/timestamp]"
    checkedAt: "[ISO-8601]"
    checkedBy: "[Entra object ID]"
  deadlines:
    - deadlineId: "[ID]"
      type: "[canonical event type]"
      dueDate: "[YYYY-MM-DD or null]"
      graceEnd: "[YYYY-MM-DD or null]"
      status: upcoming | due_soon | overdue | grace | lapsed | filed | paid | unknown
      legalBasis: "[article/procedure]"
      ruleVersion: "[version]"
      sourceUrl: "[https URL]"
      sourceCheckedAt: "[ISO-8601]"
      humanVerified: true | false
      evidenceItemId: "[item ID or null]"
  agentManaged: true | false
  businessOwner: "[object/team ID or null]"
  notes: "[minimal notes]"
```

## Rules

- deadline `dueDate`を確定するにはcurrent official sourceと`humanVerified: true`。
- `filed`/`paid`はreceipt/evidence itemが必要。
- updateはexact item/eTag。new version/assetはconditional create。
- old versionをdeleteしない。
- record IDへsecret、発明内容、claim strategyを入れない。
