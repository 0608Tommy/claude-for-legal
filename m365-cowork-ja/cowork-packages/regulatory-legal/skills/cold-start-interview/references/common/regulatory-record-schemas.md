> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 規制対応record schema

schemaはgateway側で`additionalProperties: false`、length/count/enum上限、Unicode NFC、
timezone、URL host validationを実装する。本書はdomain contractであり、provision済み
listまたはflowの証拠ではない。

## Regulatory source snapshot

```yaml
jurisdictions:
  - JP
nexus:
  - jurisdiction: JP
    basis: "[entity/activity/territory/venue/contract]"
    facts: []
    status: established | potential | absent | unknown
authority:
  authorityId: "[stable authority ID]"
  displayName: "[Japanese display name]"
  authorityType: ministry | agency | commission | cabinet-office-commission | exchange | non-exchange-sro | court | legislature | cabinet | other
  mandate:
    sourceSystem: "[official mandate source]"
    sourceItemId: "[law/charter ID]"
    sourceVersionOrRevisionId: "[version/revision]"
    provisions: []
    description: "[bounded mandate]"
sourceId: "[stable ASCII ID]"
sourceSystem: "[canonical source system, e.g. e-gov-law-api]"
sourceItemId: "[law/case/bill/document/item ID]"
sourceVersionOrRevisionId: "[revision/version/publication ID]"
sourceClass: gazette | law-api | public-comment | diet | cabinet | regulator | sro | secondary
instrumentClass: statute | cabinet-order | ministerial-ordinance | commission-rule | delegated-notice | administrative-guidance | official-guideline | faq | cabinet-decision | bill | consultation | council-material | exchange-rule | sro-rule | platform-policy | internal-policy | enforcement-action | judgment | other
normativeForce: binding | nonbinding | binding-on-covered-parties | contractual | internal | unknown
lifecycleStatus: proposed | current | future-effective | not-adopted | withdrawn | superseded | repealed
processStage: "[consultation-open/bill-pending/passed-not-promulgated/promulgated-not-effective/partially-effective/effective/result-published/other]"
applicability:
  status: applies | potentially-applies | does-not-apply | unknown
  basis: "[scope test]"
  coveredParties: []
  territorialScope: []
  conditions: []
displayTags: []
isAdministrativeGuidance: false
administrativeGuidanceBasis:
  basisType: apa-arts-32-through-36-3 | sector-statute | other | none | unknown
  statute: "[law/source or null]"
  provisions: []
  classificationReason: "[reason]"
marketRuleContext:
  kind: exchange | non-exchange-sro
  issuerEntity: "[exact issuer]"
  venue: "[exact venue or null]"
  approvalRequired: true | false | unknown
  approvalAuthority: "[exact authority or null]"
  approvalStatus: approved | pending | not-required | unknown
  approvalBasis:
    sourceSystem: "[official source]"
    sourceItemId: "[law/rule/exception ID]"
    sourceVersionOrRevisionId: "[pinned version]"
    provisions: []
    exactRuleOrExceptionPinned: false
  coveredParties: []
titleJa: "[verbatim]"
titleEnReference: "[reference only or null]"
lawId: "[e-Gov law ID or null]"
lawRevisionId: "[e-Gov revision ID or null]"
lawNumber: "[verbatim or null]"
gazetteDate: "[YYYY-MM-DD or null]"
gazetteKind: "[main/extra/procurement/other or null]"
issueNumber: "[verbatim or null]"
pages: "[verbatim or null]"
signatureVerified: false
publicCommentCaseId: "[案件番号 or null]"
billSession: "[number or null]"
billType: "[cabinet/member/other or null]"
billNumber: "[verbatim or null]"
proposalAt: "[ISO-8601 or null]"
commentOpenAt: "[ISO-8601 or null]"
commentCloseAt: "[ISO-8601 or null]"
commentCloseRaw: "[displayed datetime or null]"
passedAt: "[ISO-8601 or null]"
promulgatedAt: "[ISO-8601 or null]"
effectiveDates:
  - provision: "[article/scope]"
    at: "[ISO-8601 or unknown]"
applicationDates: []
transitionDates: []
transitionText: "[verbatim excerpt or null]"
enablingProvisions: []
relations:
  proposes: []
  finalizes: []
  amends: []
  implements: []
  supersedes: []
canonicalUrl: "https://..."
attachmentUrls: []
retrievedAt: "[ISO-8601]"
contentHash: "[hash]"
verificationState: verified-current | verified-future | conflicting | pending
verifiedAt: "[ISO-8601 or null]"
verifiedBy: "[object ID or null]"
conflictNotes: "[text or null]"
```

proposed、final、historical、future-unenforced textはimmutable snapshotとして別record。
relationで結び、overwriteしない。

`sourceId`はconfigured feed/source定義のstable ASCII IDである。保存・照合のgeneric
source identityは`sourceSystem + sourceItemId + sourceVersionOrRevisionId`を使う。
`lawId`、`lawRevisionId`、`publicCommentCaseId`等はdomain-specific aliasであり、
generic identityを置き換えない。

jurisdiction/nexus、instrument class、normative force、lifecycle、applicabilityを
混ぜない。`displayTags`は複数可のUI shorthandであり、外国法もbindingまたは
future-effectiveになり得る。titleに「ガイドライン」があるだけで
`isAdministrativeGuidance: true`にせず、行政手続法32条から36条の3
（32、33、34、35、36、36-2、36-3）または他のbasisを
itemごとに記録する。
`basisType: sector-statute`ではexact statute sourceとnonempty exact provisionsを
requiredとし、generic mandateやtitleだけで補わない。

`instrumentClass: exchange-rule | sro-rule`では`marketRuleContext`をrequiredとする。
exchangeは`kind: exchange`とexact venueを要求し、non-exchange SROは
`kind: non-exchange-sro`かつvenue null。approval requiredならauthorityと
`approved|pending`、not requiredならauthority nullと`not-required`、unknownなら
status `unknown`を要求する。exchange ruleはexact rule/exceptionをpinするまで
approval required/statusをunknownにする。金融商品取引法149条のgeneral approval
frameworkはapproval basisに記録するが、それだけで個別rule/exceptionを確定しない。
placeholder、`source-specific`、TBDを拒否する。
JPX group pageをissuerにせず、exchange/SRO ruleをstatuteまたはordinary platform
contractと扱わない。

## Source technical health

```yaml
sourceId: "[stable ASCII ID]"
sourceSystem: "[canonical source system]"
canonicalUrl: "https://..."
format: json | rss | atom | html | email | licensed
encoding: UTF-8 | Shift_JIS | other
retrievalMode: direct | adapter-required | manual | licensed
expectedContentClasses: []
itemLevelClassificationRequired: true
termsCheckedAt: "[ISO-8601]"
lastProbeAt: "[ISO-8601]"
lastSuccessAt: "[ISO-8601 or null]"
health: healthy | degraded | failed | unverified
fallback: "[manual/licensed/none]"
```

mixed pageへ単一`authorityClass`を付けない。`expectedContentClasses`はallowlistであり、
各itemのinstrument/force/lifecycle/applicability classificationを置き換えない。

## Gap record

source compatibility fields `requirement`, `regulation`, `policy_affected`,
`gap_type`, `owner`, `opened`, `due`, `status_verified`, `status`,
`notified`, `resolution`をimport時に保持する。日本版canonical record:

```yaml
tenantId: "[tenant ID]"
practiceId: "[practice ID]"
scopeType: practice | matter
scopeId: "[practiceId or matterId]"
recordType: regulatory-gap
recordId: "GAP-[stable ID]"
gapId: "GAP-[stable ID]"
gapClass: compliance | prospective-implementation | guidance-alignment | sro-alignment | watch | participation-decision
requirement: "[specific requirement]"
jurisdictions: []
nexus: []
instrumentClass: "[canonical instrument class]"
normativeForce: binding | nonbinding | binding-on-covered-parties | contractual | internal | unknown
lifecycleStatus: proposed | current | future-effective | not-adopted | withdrawn | superseded | repealed
applicability:
  status: applies | potentially-applies | does-not-apply | unknown
  basis: "[scope test]"
  coveredParties: []
displayTags: []
isAdministrativeGuidance: false
administrativeGuidanceBasis: {}
marketRuleContext:
  kind: exchange | non-exchange-sro | null
  issuerEntity: "[exact entity or null]"
  venue: "[exact venue or null]"
  approvalRequired: true | false | unknown | null
  approvalAuthority: "[exact authority or null]"
  approvalStatus: approved | pending | not-required | unknown | null
  approvalBasis: "[structured source/provisions/pin status or null]"
  coveredParties: []
sourceSnapshotId: "[exact snapshot ID]"
sourceSystem: "[canonical source system]"
sourceItemId: "[exact source item ID]"
sourceVersionOrRevisionId: "[exact version/revision ID]"
policyId: "[exact policy item ID or new-policy-needed]"
policyVersion: "[version/hash]"
gapType: none | partial | full | new-policy | watch | comment-decision
severity: blocking | high | medium | low
ownerObjectId: "[object ID or null]"
openedAt: "[ISO-8601]"
scope:
  jurisdictionCodes:
    - JP
  authorityIds: []
  regulatedEntityIds: []
  businessUnitIds: []
  productsOrServices: []
  activities: []
  provisions: []
  excludedScope:
    - reason: "[user-requested or source limitation]"
      detail: "[exact exclusion]"
coverage:
  source:
    expectedAttachmentCount: 0
    reviewedAttachmentCount: 0
    complete: true
    truncated: false
    failures: []
  policy:
    policyItemIds:
      - "[exact policy item ID]"
    sectionsExpected:
      - "[section]"
    sectionsReviewed:
      - "[section]"
    sectionsExcluded: []
    complete: true
  timeWindow:
    from: "[ISO-8601]"
    through: "[ISO-8601]"
effectiveDates: []
applicationDates: []
transitionDates: []
officialCommentDeadlineAt: "[ISO-8601 or null]"
internalTargetAt: "[ISO-8601 or null]"
revisitAt: "[ISO-8601 or null]"
verificationState: verified-current | verified-future | conflicting | pending
verificationEvidence:
  - sourceSystem: "[canonical source system]"
    sourceItemId: "[source item ID]"
    sourceVersionOrRevisionId: "[version/revision ID]"
    checkedAt: "[ISO-8601]"
status: open | in-progress | closed | risk-accepted
resolution: "[text or null]"
closedAt: "[ISO-8601 or null]"
closureEvidence:
  closureBasis: policy-applied | control-implemented | regulator-submission | not-applicable | other
  internalArtifact:
    itemId: "[internal remediation/approval artifact item ID]"
    versionOrRevisionId: "[version]"
    contentHash: "[hash]"
    approvedByObjectId: "[object ID]"
    approvedAt: "[ISO-8601]"
    effectiveAt: "[ISO-8601 or null]"
  regulatorFacingArtifact:
    itemId: "[exact external artifact item ID or null]"
    versionOrRevisionId: "[version or null]"
    contentHash: "[hash or null]"
  implementationEvidence:
    - itemId: "[evidence item ID]"
      versionOrRevisionId: "[version]"
      contentHash: "[hash]"
  verifiedByObjectId: "[qualified reviewer object ID]"
  verifiedAt: "[ISO-8601]"
  submissionRoute: "[verified route object or null]"
  submissionEvidence: "[exact-submission-evidence object or null]"
riskAcceptance:
  acceptedByObjectId: "[authorized object ID or null]"
  rationale: "[text or null]"
  residualRisk: "[text or null]"
  controls:
    - "[control]"
  counselReviewedBy: "[object ID or null]"
  affectedEntities:
    - "[entity ID]"
  expiresAt: "[ISO-8601 or null]"
  revisitTrigger: "[text or null]"
notification:
  destination: "[exact destination or null]"
  lastSentAt: "[ISO-8601 or null]"
  humanConfirmationId: "[record ID or null]"
```

`risk-accepted`は外部義務の消滅を意味しない。accepted/closed recordを削除しない。
unverified/future itemを「binding deadline missed」としてOverdueにしない。

`scope`と`coverage`は全persisted gapでrequired。少なくともjurisdictionと
authority/provision/activityのいずれかを持ち、source coverageはcomplete/not
truncatedで`failures`がlistかつexactly `[]`、policy coverageはnonempty
item/expected/reviewed sectionsかつ
complete、time windowはnonempty `from`/`through`を要求する。不完全なcandidateは
persistせず、manual draft/open-factとして返す。
scopeの全dimensionはarray型。jurisdictionCodes/authorityIdsはnonempty string array、
他のstring dimensionも各entryをnonblank string、excludedScopeはnonblank
reason/detail objectだけにする。scalar、null、blank-only entryを拒否する。

gap `status`はstring enum
`open | in-progress | closed | risk-accepted`だけを許可し、missing、null、number、
unknown valueを拒否する。
`risk-accepted`はauthorized acceptor、nonblank rationale/residual risk、nonempty controls、
counsel reviewer、nonempty affected entities、valid expiry、revisit triggerを全て要求する。

`status: open | in-progress | risk-accepted`では`closureEvidence: null`を許容する。
`status: closed`は次の場合だけ有効:

- `closureEvidence`がnon-null
- `closureBasis`がcanonical enumの1つ
- source/policy coverageがcompleteで、`truncated: false`、unresolved failureなし
- exact internal remediation/approval artifactがある
- qualified reviewer、verification time、nonemptyで各item/version/hashが揃った
  implementation evidenceがある
- `closureBasis: regulator-submission`ならregulator-facing artifactと後述の
  exact submission route/evidenceがあり全route fieldが一致

regulator-submissionではinternal artifactとregulator-facing artifactのitem ID、
version/revision ID、content hashがそれぞれ異なることを要求し、同一artifactを
audience labelだけ変えて代用しない。

## Comment / consultation record

source compatibilityの`CMT-ID`, `regulation`, `regulator`, `summary`, `link`,
`comment_deadline`, `detected`, `decision`, `owner`, `owner_slack`, `notified`,
`rationale`, `filed_at`, `notes`を保持する。

```yaml
tenantId: "[tenant ID]"
practiceId: "[practice ID]"
scopeType: practice | matter
scopeId: "[practiceId or matterId]"
recordType: regulatory-comment
recordId: "CMT-[stable ID]"
commentId: "CMT-[stable ID]"
recordKind: consultation | exception-notice | result-only
caseId: "[案件番号 or SRO/local ID]"
procedureType: statutory-public-comment | voluntary-consultation | sro-consultation | ministry-hearing | information-request | local-procedure
proposalSnapshotId: "[proposal snapshot or null]"
sourceSystem: "[canonical source system]"
sourceItemId: "[exact source item ID]"
sourceVersionOrRevisionId: "[record source version/revision ID]"
proposalTitle: "[verbatim or null]"
authority: "[authority]"
legalBasis: "[根拠法令条項 or null]"
proposalPublishedAt: "[ISO-8601 or null]"
commentOpenAt: "[ISO-8601 or null]"
commentCloseAt: "[ISO-8601 or null]"
commentCloseRaw: "[verbatim display]"
exceptionBasis:
  statute: "[law or null]"
  provision: "[article/paragraph/item or null]"
  reason: "[verbatim or normalized reason/null]"
noPriorConsultationProven: false
shortenedPeriodBasis:
  statute: "[law or null]"
  provision: "[article/paragraph or null]"
  reason: "[verbatim or normalized reason/null]"
submissionRoutes:
  - routeId: "[stable route ID]"
    method: web-form | email | postal | portal | hand-delivery | other | unknown
    canonicalCaseEntryUrl: "[exact case entry URL]"
    formAction: "[exact POST action or null]"
    httpMethod: POST | null
    formClassName: "[e.g. PCMIKENINPUT or null]"
    caseId: "[exact case ID]"
    destinationSystem: "[exact system]"
    destinationAddressOrEndpoint: "[exact URL/address/reference]"
    instructionUrl: "[exact instruction URL]"
    instructionContentHash: "[hash]"
    deadlineAt: "[ISO-8601]"
    receiptOrPostmark: receipt | postmark | not-applicable | unknown
    verifiedAt: "[ISO-8601]"
internalReviewAt: "[ISO-8601 or null]"
decision: undecided | filing | not_filing | filed | withdrawn
ownerObjectId: "[object ID or null]"
rationale: "[text or null]"
artifacts:
  internalAnalysis:
    itemId: "[internal analysis/decision item ID or null]"
    versionOrRevisionId: "[version or null]"
    contentHash: "[hash or null]"
    audience: internal
  regulatorFacing:
    itemId: "[exact submission artifact item ID or null]"
    versionOrRevisionId: "[version or null]"
    contentHash: "[hash or null]"
    audience: regulator-facing
submissionEvidence:
  routeId: "[must match a verified submissionRoutes entry]"
  submissionMethod: web-form | email | postal | portal | hand-delivery | other
  canonicalCaseEntryUrl: "[exact case entry URL]"
  formAction: "[exact POST action or null]"
  httpMethod: POST | null
  formClassName: "[exact form CLASSNAME or null]"
  destinationSystem: "[e-Gov/authority/SRO/local system]"
  destinationAddressOrEndpoint: "[exact URL/address/reference]"
  instructionUrl: "[exact route instruction URL]"
  instructionContentHash: "[must match route hash]"
  routeDeadlineAt: "[must match verified route deadline]"
  receiptOrPostmark: receipt | postmark | not-applicable
  routeVerifiedAt: "[ISO-8601]"
  submittedArtifactItemId: "[must equal artifacts.regulatorFacing.itemId]"
  submittedArtifactVersionOrRevisionId: "[exact submitted version]"
  submittedArtifactHash: "[must equal regulator-facing contentHash]"
  submittedByObjectId: "[authorized human object ID]"
  submittedAt: "[ISO-8601]"
  receiptOrReferenceId: "[receipt/reference ID]"
  receiptArtifactItemId: "[receipt evidence item ID]"
  receiptArtifactVersionOrRevisionId: "[receipt version]"
  receiptArtifactHash: "[receipt hash]"
  caseId: "[must equal record caseId]"
  officialDeadlineVerifiedAt: "[ISO-8601]"
filedAt: "[ISO-8601 or null]"
resultStatus: pending | result_published | final_instrument_linked
finalDisposition: adopted | not-adopted | withdrawn | null
resultSnapshotId: "[required for result-only; otherwise snapshot or null]"
resultPublishedAt: "[required ISO-8601 for result-only; otherwise ISO-8601 or null]"
finalInstrumentSnapshotId: "[snapshot or null]"
promulgatedAt: "[ISO-8601 or null]"
effectiveDates: []
verificationSchedule:
  - T-14
  - T-3
  - T-1
  - immediately-before-submission
```

`waived`は真正なlegal waiverがある場合以外`not_filing`へ移行する。RSS `dc:date`を
deadlineとしない。提出はAI operationではなく、evidenceの記録もfresh confirmation後。

`recordKind: exception-notice | result-only`でprior consultationがない場合、
proposal/open/close datesはnullを許容する。`exceptionBasis`は
`recordKind: exception-notice`かつ`noPriorConsultationProven: true`の場合だけ許容し、
consultation/result-onlyへ推測で付けない。
`recordKind: result-only`はgeneric source identityをresult sourceへ向け、
`proposalSnapshotId: null`を許容する一方、nonempty `resultSnapshotId`と
`resultPublishedAt`をrequiredとする。
`finalDisposition`は`adopted | not-adopted | withdrawn`だけを使う。

submission method/destinationはverified `submissionRoutes`から選ぶ。instruction URL、
hash、deadline、receipt-or-postmark、verifiedAtが揃わなければemail/postal等を推測せず、
`method: unknown`としてsubmissionをblockする。
filed evidenceはroute ID、method、destination system/address、instruction URL/hash、
deadline、receipt-or-postmark、verifiedAtがexactly一致し、全fieldがnonblankであること。

`decision: filed`は`artifacts.regulatorFacing`と`submissionEvidence`がすべて揃い、
case ID、artifact item/version/hashが一致する場合だけ有効。internal analysis artifactを
提出物として記録しない。`filing`は内部decision、`filed`はexact human submission
evidence付きの事実記録である。
`undecided | filing | not_filing | withdrawn`では`submissionEvidence: null`を許容する。

## Exact submission evidence

gap closureとcomment filedで共通するconditional object:

```yaml
submissionMethod: web-form | email | postal | portal | hand-delivery | other
destinationSystem: "[e-Gov/authority/SRO/local system]"
destinationAddressOrEndpoint: "[exact URL/address/reference]"
routeId: "[verified submission route ID]"
canonicalCaseEntryUrl: "[exact case entry URL]"
formAction: "[exact POST action or null]"
httpMethod: POST | null
formClassName: "[exact form CLASSNAME or null]"
instructionUrl: "[exact instruction URL]"
instructionContentHash: "[route instruction hash]"
routeDeadlineAt: "[ISO-8601]"
receiptOrPostmark: receipt | postmark | not-applicable
routeVerifiedAt: "[ISO-8601]"
caseId: "[exact case/docket/reference ID]"
submittedArtifactItemId: "[regulator-facing artifact item ID]"
submittedArtifactVersionOrRevisionId: "[exact submitted version]"
submittedArtifactHash: "[exact submitted hash]"
submittedByObjectId: "[authorized human object ID]"
submittedAt: "[ISO-8601]"
officialDeadlineVerifiedAt: "[ISO-8601]"
receiptOrReferenceId: "[receipt/reference ID]"
receiptArtifactItemId: "[receipt evidence item ID]"
receiptArtifactVersionOrRevisionId: "[receipt version]"
receiptArtifactHash: "[receipt hash]"
```

artifact item/version/hash、case ID、destination、method、human submitter、time、receiptを
省略しない。internal artifact、draft hash、approval recordだけではsubmission evidenceに
ならない。

e-Gov form routeではcanonical case entry URLとPOST form actionを分ける。
`https://public-comment.e-gov.go.jp/servlet/Public`をsubmission endpointとして保存せず、
actual action、CLASSNAME、case IDをform sourceから固定する。

## Policy version pin

```yaml
policyItemId: "[SharePoint item ID]"
policyETag: "[latest eTag]"
policyVersion: "[version]"
policyHash: "[hash]"
approvedAt: "[ISO-8601 or null]"
effectiveAt: "[ISO-8601 or null]"
ownerObjectId: "[object ID]"
authoritySnapshotId: "[exact regulatory snapshot]"
authorityRevisionId: "[law_revision_id or null]"
authorityHash: "[hash]"
```

## Matter profile

```yaml
matterId: matter-1
slug: regulatory-matter-1
clientOrBusinessUnit: business-unit-1
matterType: rulemaking
confidentiality: restricted
jurisdictions:
  - ja-JP
authorities:
  - authority-1
authorizedGroups:
  - group-1
status: active
bindingGeneration: 0
retentionClass: regulatory-standard
legalHoldStatus: none
openedAt: "2026-07-16T09:00:00+09:00"
closedAt: null
```

`status`は`active | close-pending | archived`だけ。`bindingGeneration`はBooleanでない
integerかつ`>= 0`とする。close fenceは`active -> close-pending`と同じconditional
operationでgenerationを1増やし、zero active binding確認後にgenerationを変えず
`close-pending -> archived`へfinalizeする。`active -> archived`の直接遷移、
generation減少、revocation前のfinalizeを拒否する。

slugはrouting hintであり、権限・bindingのsourceではない。

## Profile records

profileはdisplay name、filename、current conversationから推測せず、次のcanonical
keyとpayloadを使う。

### Company profile

canonical key:
`tenantId + profileType=company-profile + organizationId`

```yaml
tenantId: "[tenant ID]"
profileType: company-profile
organizationId: "[stable organization ID]"
organizationName: "[display name]"
industry: "[industry]"
productsOrServices: []
jurisdictionFootprint: []
riskPosture: "[posture]"
companyLevelPeople: []
```

### Regulatory practice profile

canonical key:
`tenantId + practiceId + pluginId=regulatory-legal + profileType=practice-profile`

```yaml
tenantId: "[tenant ID]"
practiceId: "[practice ID]"
pluginId: regulatory-legal
profileType: practice-profile
watchlist: []
sourceConfiguration: []
materialityThreshold: {}
policyIndex: []
gapProcess: {}
commentProcess: {}
cadencePreference: {}
matterWorkspaceEnabled: false
setupStatus: incomplete | complete
```

### User profile

canonical key:
`tenantId + practiceId + pluginId=regulatory-legal + userObjectId + profileType=user-profile`

```yaml
tenantId: "[tenant ID]"
practiceId: "[practice ID]"
pluginId: regulatory-legal
profileType: user-profile
userObjectId: "[Microsoft Entra object ID]"
role: lawyer-legal-professional | non-lawyer-with-attorney | non-lawyer-without-regular-attorney
attorneyRoute: "[object ID/role/null]"
personalDestinationPreference: "[destination/null]"
```

共有company/practice profileへsingle user role、attorney contact、active matter、
client secretを入れない。

## User-scoped setup session

canonical state key:

```text
tenantId + practiceId
+ scopeType=user
+ scopeId=userObjectId
+ recordType=setup-session
+ recordId=regulatory-legal:[setupSessionId]
```

```yaml
tenantId: "[tenant ID]"
practiceId: "[practice ID]"
scopeType: user
scopeId: "[must equal userObjectId]"
recordType: setup-session
recordId: "regulatory-legal:[setupSessionId]"
payload:
  tenantId: "[must equal envelope tenantId]"
  practiceId: "[must equal envelope practiceId]"
  pluginId: regulatory-legal
  setupSessionId: "[opaque unique ID]"
  userObjectId: "[Microsoft Entra object ID]"
  conversationState: initial | resume | quick | full | redo | redo-section | check-integrations
  setupStatus: in-progress | paused | complete | abandoned
  operation: create | update
  expectedAbsent: "[true for create; omitted for update]"
  itemId: "[required for update; omitted for create]"
  eTag: "[required for update; omitted for create]"
  idempotencyKey: "[nonempty]"
  currentSection: "[section/null]"
  answeredSections: []
  pendingQuestions: []
  targetProfilePins:
    - profileKey: "[canonical profile key]"
      profileItemId: "[exact item ID]"
      profileVersion: "[exact version]"
      profileETag: "[exact eTag]"
  resumeState:
    resumable: false
    pausedAt: "[ISO-8601 or null]"
    lastCompletedStep: "[step/null]"
  redoState:
    parentSetupSessionId: "[prior setup session ID or null]"
    targetSections: []
    baseProfilePins:
      - profileItemId: "[exact item ID]"
        profileVersion: "[exact version]"
        profileETag: "[exact eTag]"
    proposedPatchHash: "[hash/null]"
  createdAt: "[ISO-8601]"
  updatedAt: "[ISO-8601]"
```

`conversationState: resume`では`resumeState.resumable: true`、`pausedAt`、
`pendingQuestions`がrequired。`redo`/`redo-section`では`redoState`のparent/base
profile pinsがrequiredで、parent setup sessionとnew setup sessionは異なる。
envelope/payloadのtenantId/practiceIdはexact一致し、pluginIdは
`regulatory-legal`、setupStatusは
`in-progress | paused | complete | abandoned`だけを許可する。
profile ID/version/eTagをparallel arraysへ分けず、同一pin object内で揃える。blank field、
配列length/index依存を拒否する。
新しいinitial/redo sessionは`operation: create`、canonical key、
`expectedAbsent: true`、unique idempotency、no itemId/eTag。resume/progress/completeは
`operation: update`、persisted `itemId`、latest eTag、unique idempotency、
no expectedAbsent。`setupStatus: complete`では`resumeState.resumable: false`、
`pausedAt: null`、pending questionsなし。別利用者のpaused sessionをresumeしない。
