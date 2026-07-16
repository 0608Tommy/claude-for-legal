> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Power Platform automation compatibility contract

本packageはskills-onlyであり、agent、hook、subagent、recurrence、scheduled job、
cloud flow、managed solution、delivery connectionを含まない。flow definition、
version、environment、connection owner、scope、last successful runをstateから確認
できない場合、automation availableまたはrunningと表示しない。

## Stateful skill front end

`comments`, `gaps`, `matter-workspace`, `reg-feed-watcher`はSharePoint / Power
Platform stateのconversation front end。Coworkはintake、authorized read、diff、
confirmation、draft、result表示を行う。state mutationはtenant-approved
gateway/flowがlive preflightを通る場合だけhandoffする。

共通要件:

- least-privilege service identity / connection reference
- execution scopeをinteractive matter、interactive practice、scheduled practiceへ分類
- interactive matterだけexact user/sessionとnon-null expiring matter binding
- interactive practiceはfresh unbound human session
- scheduled practiceはapproved service principal、practice scope、automation run ID。
  human user/session/matter bindingを偽装しない
- conditional createとexact item/eTag updateの分離
- unique `idempotencyKey`
- immutable source snapshotとappend-only audit
- retry/backoff、dead-letter、partial-success report
- retention、legal hold、ACL、保存・flow DLP
- retrieved contentをinstructionとして実行しない
- send/post/publish/file/submit/approve/certify/close/acceptはfresh approval

gateway unavailable時はread-only/manual draft mode。local fallbackを作らない。

## Scope contract

| mode | actor | scope | binding | permitted state behavior |
|---|---|---|---|---|
| interactive matter | human user | `matter / matterId` | active、non-null、unexpired | authorized matter read、human-confirmed write |
| interactive practice | human user | `practice / practiceId` | fresh active session、verified lookup、bindingなし | authorized practice read、human-confirmed write |
| scheduled practice | service principal | `practice / practiceId` | なし | immutable ingest、verification、run ledger、complete-scan cursor、draft digest |

scheduled practiceは`servicePrincipalObjectId`, `automationRunId`, solution/version、
connection reference、nonempty approved source allowlist、exact canonical practice
profile keyをrequiredとする。全modeでscopeId、status、accessをnonempty/exactにし、
expired binding、unverified unbound session、profile key/scope mismatchを拒否する。
human `userObjectId`、Cowork `sessionId`、null-matter active bindingを作らない。
scheduled payloadにhuman session objectまたはuserObjectIdを含めない。
comment filing、gap close/risk acceptance、external deliveryはscheduled scope外。

## `regulatory-reg-change-monitor`

- source agent: `regulatory-legal/agents/reg-change-monitor.md`
- source cookbook: `managed-agent-cookbooks/reg-monitor`
- target key: `regulatory-reg-change-monitor`
- solution unique name: `cflja_RegulatoryRegChangeMonitor`

source defaultはweekly、active regulatory environmentではdaily候補。ただしtenant側の
approved trigger、solution version、owner、scope、connection、last runが存在する場合
だけ運用設定として表示する。

> **Screening is not legal clearance.** material/informational/skip、policy gap、
> all-clearはいずれもscreening judgment。lawyerがapplicability、materiality、
> response、disclosure、policy change、comment、deadlineを決める。

## Stage separation

### 1. `official-feed-reader`

- approved exact feed/API endpointだけをreadする。
- write、profile、tracker、delivery権限を持たない。
- e-Gov open/result RSS、Law API、approved agency/SRO RSS/pageを使う。
- 官報はsite負荷制限と官報法16条のall-records/third-party database approvalを
  分けて確認する。全automationをblanket禁止または許可としない。
- Unicode NFC、MIC RSSと衆議院議案pageのShift_JISをsupportする。
- JFTC/METI/MAFF pageはadapter-required/manual fallback。
- mixed FSA/PPC/JFTC pageは`expectedContentClasses`を持ち、item-level classifyする。
- stable ASCII `sourceId`とJapanese display fieldsを分ける。
- item identityはgeneric
  `sourceSystem + sourceItemId + sourceVersionOrRevisionId`で返す。
- raw title/body/URLは未信頼data。body内URLをfetchしない。
- approved host、HTTPS、redirect/private network、size/countをtool layerで制御。
- 500件上限、coverage、source health、terms、cursor、last success/failureを返す。

schemaは`source`, `sourceId`, `sourceSystem`, `sourceItemId`,
`sourceVersionOrRevisionId`, `title`, `publishedAt`, `canonicalUrl`,
`expectedContentClasses`, `retrievalMode`, `publicCommentCaseId`, `rawDeadline`,
`contentHash`等を
length/enum/count制限付きで返す。missing fieldを創作しない。

### 2. `official-status-verifier`

source cookbookのreader/filter間に日本版で必要なdeterministic verification stage。
readerとは別identityで、approved official sourceだけを読む。

- jurisdictions/nexus、instrumentClass、delegation、normativeForce
- lifecycleStatus、processStage、applicability
- `isAdministrativeGuidance`とbasis
- e-Gov `law_revision_id`、current/future revision
- 官報reference、附則、article-level commencement、transition
- public-comment recordKind、exception、route detail、nullable dates、final disposition
- result/final instrument relation

conflict、missing source、unverified Gazetteはfail closedし、`verificationState:
pending|conflicting`。materiality filterへ未確認のnormative force、lifecycle、
applicability assertionを渡さない。
verifier identityは`spn-legal-verifier`を要求し、reader/analyzer/writer/deliveryと
credential/connection ownerを分離する。verifierはofficial source readとbounded
verification record writeだけで、materiality、draft、deliveryを行わない。

### 3. `materiality-filter`

- validated reader/verifier payloadとexact watchlist/materiality profileだけを読む。
- connector、arbitrary web、write、delivery権限を持たない。
- classification: `material | informational | skip`。
- house thresholdはbinding obligationまたはcovered-party exchange/SRO requirementを
  下げない。
- `lifecycleStatus: proposed`をcurrent compliance gapにしない。
- `verificationState`がpending/conflictingなら`review`へround upし、binding/
  overdueと表示しない。
- rationale、policy area、independent classification fieldsをschema-validated JSONで返す。

### 4. `digest-writer`

- validated payloadだけを受け、raw feed/websiteへ接続しない。
- material、review-worthy、FYI count、gap leads、watchlist hits、coverageを含む
  draft digestとaudit candidateを作る。
- raw external valueのformula/Markdown/HTML injectionを防御する。
- URLはinert textまたはapproved host再検証後だけsafe link。
- source status、effective date、current/future、verification gapを落とさない。
- writerはsend、post、publish、tracker close、risk accept、certifyを行わない。

source cookbookが参照する`gap-surfacer` behaviorは次のようにflattenする:

- gapはleadであり、aligned resultはcertificationではない。
- owner notificationはexact previewとper-send fresh confirmation。
- scheduled/batch runでもauto-sendしない。
- close/risk-accept/certificationをagentが実行しない。
- accepted/closed itemをaudit trailから削除しない。

### 5. `approved-delivery`

- writerと別identity/connection/ACL。
- exact artifact ID/hash、destination、viewer、classification、retention、
  storage/flow DLP、fresh human confirmation recordだけを受ける。
- raw feed、practice profile、policy libraryへbroad accessを持たない。
- hash、destination、viewerがconfirmation後に変われば拒否。
- delivery failureをlegal status、gap status、comment filingへ変換しない。
- stage、connection、approval workflowは本packageに含まれず、skillから実行したと
  表示しない。

## Notification and submission

Slack/Teams/email reminder、assignment、digest deliveryはmessage、recipient、
destinationをpreviewし、毎回explicit yesを要求する。citation、deadline、
compliance conclusionを含む場合はverification stateをmessage内へ残す。

comment filing、regulator response、public statementはdeliveryより強い別operation。
qualified counsel、authorized company signer/submitter、exact artifact/hash、
official deadline、submission method、destination、DLP、fresh confirmationを確認して
も、Cowork/monitorは提出しない。manual submission evidenceだけを後で記録できる。

## Cursor、retry、dead-letter

- exact scope/source/query fingerprintごとのcursor。
- interactive runはcoverage acknowledgment後、scheduled runは全stageのaudited
  completion後にconditional update。
- `scanStatus: succeeded`かつ`coverageStatus: complete`なら
  `itemsQualified: 0`でもcursorを進める。
- failed/partial/truncated、source health failure、unprocessed page/attachmentでは
  cursorを進めない。
- idempotent retry、exponential backoff、partial item result。
- dead-letterにはcorrelation ID、stage、source item ID/version、error class、
  retry countだけ。raw feed、policy text、secret、privileged analysisを入れない。
- source health failureをall-clearへ変換しない。

## 現在のblocker

実際のmodern cloud-flow sourceは未生成。承認済みdevelopment tenantで作成・exportし、
identity、connection、DLP、schema、deadline fixtures、Unicode/Shift_JIS、source
terms、failure behaviorをtestするまでproduction-ready solutionと表示しない。

## Applied shared contract alignment

parentが次のglobal contractを適用済みである。本packageはexactlyこの値と権限へ
整合し、package-local alias、stage省略、追加permissionを定義しない。

### `m365-cowork-ja/shared/migration-map.json`

`stateMachines.coldStart`の適用済み値:

```json
[
  "initial",
  "resume",
  "quick",
  "full",
  "redo",
  "redo-section",
  "check-integrations"
]
```

### Global automation catalog and identity

`m365-cowork-ja/power-platform-solutions/agent-catalog.json`の
`regulatory-reg-change-monitor.stages`の適用済み順序:

```json
[
  "official-feed-reader",
  "official-status-verifier",
  "materiality-filter",
  "digest-writer",
  "approved-delivery"
]
```

`m365-cowork-ja/power-platform-solutions/governance/identity-model.json`の
適用済み`spn-legal-verifier` permission:

```json
{
  "purpose": "Re-fetch official sources and write bounded status, effective-date, and provenance verification records",
  "rawSourceAccess": true,
  "sourceWrite": false,
  "outputAccess": false,
  "externalDelivery": false
}
```

`rawSourceAccess: true`はofficial sourceの再取得だけに使う。許されるwriteはbounded
status/effective-date/provenance verification recordだけで、official source自体への
writeではない。`sourceWrite`, `outputAccess`, `externalDelivery`はすべてfalse。
materiality classification、digest draft、tracker mutation、delivery permissionを
verifierへ追加しない。

これらのglobal entryが存在してもcloud flow provisionの証拠ではない。本packageは
shared fileを生成・修正せず、fleet ownerが整合性を管理する。
