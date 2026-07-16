> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、日本のentity compliance state向けに変更した派生ファイルです。

# Entity records

## Entity profile

```yaml
recordType: corporate-entity-profile
tenantId: "[tenant id]"
practiceId: "[practice id]"
scopeType: practice | matter
scopeId: "[practiceId or matterId]"
entityId: "[immutable ID]"
trackerVersion: 1
recordId: "entity:[entityId]:v[trackerVersion]"
legalName: "[name]"
entity_form: KK | GK | other
corporateNumber13: "[13-digit 法人番号]"
companyCorporateNumber12: "[12-digit 会社法人等番号]"
registered_head_office: "[address]"
formationDate: "[ISO date or unknown]"
organ_design: "[design]"
articlesItemId: "[itemId]"
articlesVersion: "[version]"
publicNoticeMethod: "[method]"
shareCertificateStatus: "[status]"
restrictedShares: true | false | unknown
listedMarket: "[market or null]"
edinetCode: "[code or null]"
entityStatus: active | dormant | dissolving | dissolved
recordLifecycle: active | superseded
```

## Obligation state

canonical key:
`tenantId + practiceId + scopeType + scopeId + recordType + recordId`

```yaml
recordType: entity-obligation
recordId: "[entityId:vTrackerVersion:obligationId:period-or-trigger]"
payload:
  entityId: "[ID]"
  obligationType: event | periodic
  obligationId: "[stable ID]"
  layer: law | listing | guidance | contract | internal
  legal_basis: "[source]"
  source_version: "[version]"
  effective_date: "[date]"
  trigger_date: "[date or null]"
  due_date: "[date or null]"
  filing_system: "[system or N/A]"
  evidence_required: "[evidence]"
  evidence_item_ids:
    - "[itemId]"
  status: not_started | in_progress | filed_pending | complete | blocked | unknown
  owner: "[person/role]"
  notes: "[minimal]"
```

## Rebuild mapping

```yaml
oldRecordId: "[ID or null]"
newRecordId: "[ID or null]"
action: retain | change | add | supersede | unresolved
reason: "[reason]"
sourceItemId: "[itemId]"
sourceVersion: "[version]"
```

old versionをdeleteしない。

rebuild時は`trackerVersion + 1`のnew entity/profile・obligation recordを
conditional createし、全schema/coverage/relationshipを検証する。次に
`entity-active-version` pointerをexact`itemId`/`eTag`でnew versionへ切り替え、
成功後に旧recordの`recordLifecycle`を`superseded`へupdateする。pointer更新前に
旧versionをsupersedeしない。旧record更新だけが失敗した場合はnew pointerを
維持し、remediation eventをauditする。
