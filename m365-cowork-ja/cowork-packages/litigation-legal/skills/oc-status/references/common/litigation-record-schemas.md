> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Litigation canonical record schemas

schemaはconversation outputのshape。writeは必ずstate gatewayのcreate/update envelopeを
使い、`additionalProperties: false`相当のvalidationを行う。

## Matter

source compatibility fields:

```yaml
id: "[matter ID]"
name: "[matter name]"
type: contract | employment | ip | regulatory | investigation | product | other
role: plaintiff | defendant | claimant | respondent | investigated
counterparty: "[name]"
jurisdiction: "[forum]"
status: active | close-pending | archived
bindingGeneration: 0
posture: threatened | filed | other
sourceStatus: "[raw imported status such as closed/dismissed or null]"
stage: "[source stage token]"
source: demand-letter | complaint-served | subpoena | regulator-inquiry | internal-report | pre-suit-threat
risk: high | medium | low | critical
materiality: reserved | disclosed | monitored | none
exposure_range: "[amount/range or null]"
related_matters: []
opened: "[YYYY-MM-DD]"
last_updated: "[YYYY-MM-DD]"
```

Japan fields:

```yaml
proceedingType: pre_suit | ordinary_civil | provisional_remedy | mediation | labor_tribunal | patent_infringement | JPO_trial | appeal | execution | other
court: "[court]"
division: "[division or null]"
caseNumber:
  era: "[era]"
  year: "[year]"
  caseSymbol: "[symbol]"
  serial: "[serial]"
mintsCaseId: "[ID or null]"
recordRegime: legacy_case_paper | legacy_case_repealed_mints_transition | new_case_mints_new_regime | other_procedure_partial
partyProceduralRoles: []
claimAndRelief: []
claimValueAndFees: "[value/fees]"
filedAt: "[ISO-8601 or null]"
servedAtEffective: "[ISO-8601 or null]"
nextHearing: "[ISO-8601 or null]"
deadlineIds: []
evidenceRegisterId: "[record ID]"
confidentialityOrderIds: []
preservationAssessmentId: "[record ID or null]"
provisionalRemedyStatus: "[status or null]"
appealFinality: "[status]"
executionStatus: "[status]"
confidentiality: standard | heightened | restricted | clean-team
authorizedGroupIds: []
```

`next_deadline`はsource import compatibilityだけ。日本のactive stateは
`deadlineIds[]`を正本とし、複数deadlineを1値へ潰さない。

## Deadline candidate

```yaml
deadlineId: "[ID]"
matterId: "[matter ID]"
deadline_class: statutory_invariable | statutory_extendable | court_set | contractual | limitation | internal
label: "[label]"
trigger_document: "[item/version]"
trigger_timestamp: "[ISO-8601]"
effective_service_timestamp: "[ISO-8601 or null]"
authority_url: "https://..."
article_or_order: "[article/rule/order]"
law_revision_date: "[YYYY-MM-DD]"
calculation_steps: []
holiday_rule: "[source]"
candidate_date: "[YYYY-MM-DD or null]"
confidence: high | medium | low
needs_verification: true
verified_by_lawyer: "[object ID or null]"
verified_by_docketing_owner: "[object ID or null]"
calendar_entry_id: null
status: candidate | verified | rejected | superseded
```

candidate create、verification update、calendar writeは別operation。

## Evidence register

```yaml
evidenceId: "[ID]"
matterId: "[matter ID]"
exhibitNumber: "[甲第1号証 | 乙第1号証 | 未採番]"
title: "[title]"
originalCopyElectronic: original | copy | electronic | mixed | unknown
custodianPseudonymousId: "[ID or null]"
sourceSystem: "[system]"
sourceItemId: "[item ID]"
sourceVersion: "[version]"
hashAlgorithm: "[algorithm or null]"
hashValue: "[hash or null]"
collectionMethod: "[method]"
collectedAt: "[ISO-8601 or null]"
collectedBy: "[object ID or null]"
accessGroupIds: []
autoDeleteSuspended: true | false | unknown
language: ja | en | other | mixed
translationReviewed: true | false | not-applicable
chainOfCustody: []
```

## Preservation control

```yaml
preservationId: "[stable ID]"
mode: issue | refresh | release | status
basisType: internal-control | CCP-234 | court-order | sector-rule | contract | foreign-proceeding | other
basisCitation: "[exact basis or null]"
scope: []
custodianIds: []
systems: []
dateRange:
  from: "[date or null]"
  through: ongoing
issuedAt: "[ISO-8601 or null]"
version: 1
lastRefreshAt: "[ISO-8601 or null]"
nextRefreshAt: "[ISO-8601 or null]"
releasedAt: "[ISO-8601 or null]"
status: draft | active | released
```

6か月refreshはinternal policy defaultであり、statutory intervalではない。

## Hold custodian

```yaml
recordType: hold-custodian
recordId: "matter:[matterId]:preservation:[preservationId]:custodian:[pseudonymousId]"
payload:
  preservationId: "[stable ID]"
  custodianPseudonymousId: "[ID]"
  noticeArtifactItemId: "[item ID]"
  noticeArtifactVersionOrHash: "[version/hash]"
  deliveryStatus: pending | delivered | failed
  deliveredAt: "[ISO-8601 or null]"
  deliveryEvidenceItemId: "[item ID or null]"
  acknowledgmentStatus: pending | acknowledged | refused | unavailable
  acknowledgedAt: "[ISO-8601 or null]"
  acknowledgmentEvidenceItemId: "[item ID or null]"
  itActionStatus: pending | completed | failed | not-applicable
  itActionEvidenceItemIds: []
  lastCheckedAt: "[ISO-8601]"
```

## Matter event

source category tokenを`sourceEventType`へ保持:

```yaml
sourceEventType: Procedural | Discovery | Substantive | Strategy | Risk re-assessment | Stakeholder | Administrative
eventTypeJP: filing | effective-service | order | hearing | evidence | settlement | preservation | judgment | finality | appeal | execution | other
eventAt: "[ISO-8601]"
summary: "[summary]"
sourceItemIds: []
fieldChanges: []
materialityCheck: no-change | changed
```

eventはappend-only。過去eventをeditせずcorrection eventを追加する。

## Demand / inbound

```yaml
demandType: payment | breach-cure | cease-desist | employment-separation | preservation | other
legalCharacterJP: rights-assertion | contractual-cure-notice | statutory-notice | Civil-Code-150-demand | settlement-communication | other
strategic_block: answered | partial | skipped
status: intake | ready-to-draft | drafted | sent | closed
statedDeadline: "[date or null]"
contractualDeadline: "[date or null]"
statutoryDeadline: "[date or null]"
courtDeadline: "[date or null]"
internalDecisionDeadline: "[date or null]"
```

## Close

close fenceは`active -> close-pending`と同じconditional operationで
`bindingGeneration`を1増やす。fence後にactive bindingだけをrevokeし、
already-revokedはsatisfiedとして再更新しない。zero active確認後にgenerationを
変えず`close-pending -> archived`へfinalizeする。`active -> archived`の直接遷移、
archive-first、revoke-every、generation減少を拒否する。

source `outcome`:

```yaml
outcome: settled | dismissed | judgment-for-us | judgment-against-us | withdrawn | consolidated | other
```

Japan detail:

```yaml
outcomeDetailJP: private-settlement | court-settlement | judgment-rendered | judgment-final | withdrawal | abandonment-or-acceptance | appeal-pending | execution-complete | consolidated | other
resolutionAt: "[ISO-8601]"
finalityAt: "[ISO-8601 or null]"
appealStatus: "[status]"
executionStatus: "[status]"
preservationDisposition: continue | partial-release | release-approved | unresolved
```

`dismissed with/without prejudice`を日本の終局形態へ翻訳適用しない。
