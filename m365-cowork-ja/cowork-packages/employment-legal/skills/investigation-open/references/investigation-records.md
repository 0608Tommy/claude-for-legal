> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Investigation state records

すべて`scopeType: matter`, `scopeId: [restricted matterId]`です。

## Case

```yaml
recordType: investigation-case
recordId: "investigation:[matterId]"
payload:
  matterId: "[matterId]"
  pseudonymousCode: "[INV-0001]"
  openedAt: "[ISO-8601]"
  types: []
  counselDirected: "[true | false | mixed | unknown]"
  whistleblowerApplicable: false
  whistleblowerIdentityItemId: "[restricted item ID or null]"
  substantiveRecordItemId: "[restricted matter document item ID]"
  appointedHandlerObjectIds: []
  publicSector: false
  evidentiaryStandard: "[internal enum]"
  status: open | paused | closed
  legalHold: false
  controllingSources: []
  asOfDate: "[date]"
```

## Entry

```yaml
recordType: investigation-entry
recordId: "investigation:[matterId]:entry:[entryId]"
payload:
  entryId: "[opaque sequential/collision-safe ID]"
  entryType: interview | document | investigator-note | gap
  eventDate: "[date or unknown]"
  loggedAt: "[ISO-8601]"
  sourceItemId: "[ID]"
  sourceVersion: "[version]"
  sourceType: complainant | respondent | witness | document | investigator-note
  issues: []
  significance: high | medium | background
  entryDocumentItemId: "[restricted matter document containing summary/quote/analysis]"
  pullCriteria: []
  disposition: surfaced | reviewed-nothing-significant | unreadable-manual-review | out-of-scope
```

allegation、conduct facts、interview summary、quote、credibility、medical/whistleblower
identity、analysisはgeneric state payloadへ入れず、item-level ACL付きrestricted
matter documentに保存する。stateはopaque ID、lifecycle、coverage metadataだけ。

## Batch coverage

```yaml
recordType: investigation-review-batch
recordId: "investigation:[matterId]:batch:[batchId]"
payload:
  batchId: "[opaque ID]"
  sourceScope: "[custodian/date/type scope]"
  startedAt: "[ISO-8601]"
  completedAt: "[ISO-8601 or null]"
  sourceItems:
    - sourceItemId: "[ID]"
      sourceVersion: "[version]"
      disposition: surfaced | reviewed-nothing-significant | unreadable-manual-review | out-of-scope
      entryRecordId: "[entry record ID or null]"
  counts:
    reviewed: 0
    surfaced: 0
    nothingSignificant: 0
    unreadable: 0
    outOfScope: 0
  coverageFailures: []
```

every source item/versionをbatch ledgerへ残し、surfaced itemだけを記録して
「全件review済み」と主張しない。

## Checklist

```yaml
recordType: investigation-checklist
recordId: "investigation:[matterId]:sources"
payload:
  items:
    - itemId: "[ID]"
      source: "[source]"
      priority: high | medium | low
      status: open | in-progress | complete | not-applicable
      evidenceItemIds: []
      decidedBy: "[human object ID or null]"
```

## Memo/version

memoはOneDrive draftまたはrestricted matter documentです。stateにはdocument item ID、
version、covered entry IDs、as-of date、statusだけを保存します。memo textをauditへ
複製しません。

## Write protocol

case/checklist first createは`expectedAbsent: true`。entryは1 entry = 1 create。
checklist/memo state updateはexact`itemId`/`eTag`、fresh confirmation。all writesを
canonical audit envelopeへappendします。
