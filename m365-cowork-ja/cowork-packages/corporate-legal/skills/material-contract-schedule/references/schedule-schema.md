> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、日本のMaterial Contract schedule向けに変更した派生ファイルです。

# Schedule records

## Prong

```yaml
prongId: "[stable ID]"
label: "[PA label]"
exactText: "[verbatim definition text]"
sourceLocation: "[section/page]"
exceptions:
  - "[exception]"
measurementPeriod: "[period or N/A]"
threshold: "[value or qualitative test]"
```

## Contract assessment

```yaml
contractId: "[stable source-linked ID]"
sourceItemId: "[item ID]"
sourceVersion: "[version]"
transactionStructure: "[canonical value]"
japaneseEntity: "[entity]"
counterparty: "[name]"
title: "[title]"
date: "[ISO date or unknown]"
governingLaw: "[law]"
subjectOfTransfer: "[asset/claim/obligation/position/licence]"
transferMechanism: "[consent/notice/universal-succession/individual-transfer/unknown]"
consentNoticePerfection: "[details]"
licenceTreatment: "[details]"
prongsMet:
  - "[prongId]"
include: true
state: answered | unclear | needs_review
```

## External schedule

PAの他scheduleと同じheading、numbering、party/date表記を使う。VDR referenceを
買主・相手方へ出すかはdeal protocolで確認する。

## Internal overlay

```yaml
scheduleEntryId: "[schedule number]"
consentRequired: true
noticeRequired: false
perfectionRequired: false
conditions: "[condition]"
owner: "[person/role]"
due: "[date or unknown]"
source: "[contract section]"
closingCandidate: true
```

external scheduleとinternal overlayを別artifactにする。
