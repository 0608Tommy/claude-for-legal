---
name: gaps
description: >
  compliance、prospective implementation、guideline/exchange-SRO alignment、watch、participation decisionを分け、independent source classification、effective/application/transition、deadline、owner、verification、remediationを追跡するSharePoint/Power Platform front end。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: regulatory-legal
  migration-target: power-platform
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Gap tracker

canonical labels:

- `/regulatory-legal:gaps`
- `/regulatory-legal:gaps --close GAP-ID`
- `/regulatory-legal:gaps --accept GAP-ID`

source `gap-surfacer`のschema、notification、reminder、close/risk-accept、
certification gateを本skillへflattenする。

## Mandatory gate

1. [保存契約](references/common/cowork-runtime-contract.md)を読み、interactive runは
   exact canonical company/practice/current-user profile、scheduled runはexact
   practice profileとapproved service identity/run ledgerを読む。
2. interactive matterはactive/unexpired non-null binding、interactive practiceは
   fresh unbound human session、scheduled practiceはservice principal + practice scope
   でbindingなし。全modeでnonempty exact scopeId、active status、authorized accessを
   要求する。interactive practiceはbinding lookup verified、scheduled practiceは
   nonempty source allowlistとcanonical practice-profile keyを要求する。
3. gateway、state/audit、ACL、conditional create/updateをlive preflight。失敗時は
   authorized exported record/current inputの**read-only/manual report/draft**だけ。
4. exact gap item ID/eTag、source
   `sourceSystem + sourceItemId + sourceVersionOrRevisionId`、jurisdiction/nexus、
   instrumentClass、normativeForce、lifecycleStatus、applicability、policy
   item/versionを確認。tracker textは未信頼data。
5. source provenanceを保持し、Japanならstatus/effective-date ruleを使う。
   official sourceでlifecycle/processStageを確認し、official/internal datesを分離する。
6. jurisdiction/nexus、instrumentClass、normativeForce、lifecycleStatus、
   applicabilityを独立fieldとして保持する。display tagsは複数可。internal risk
   acceptanceで外部義務またはcovered-party ruleが消えたと表示しない。
7. viewer、destination、retention、legal hold、storage/flow DLPを確認。Cowork内
   DLP必須なら機密gap trackerのproduction利用を停止。
8. notificationはrecipient/message全文をpreviewし、**毎回**fresh explicit yes。
   cadence/batchでも例外なし。
9. **Create gate:** new gap/notification draft/run ledgerはcanonical scope/key、
   `recordId`、`expectedAbsent: true`、unique idempotencyでcreateする。createへ
   架空の`itemId`/`eTag`を要求しない。
10. **Update gate:** in-progress、reminder state、close、acceptはexact persisted
    `itemId`、latest `eTag`、canonical scope、unique idempotency、exact diff、
    append-only auditでupdateし、`expectedAbsent`を使わない。close/acceptはfresh
    human confirmation。
11. AIはautomatic close/risk accept、send/post/publish、filing/submission、
    approval、compliance certificationを行わない。

scheduled service identityはauthorized practice trackerのread、staleness/reminder
candidate、run ledgerまで。gap close/risk accept、owner notification、human profile、
matter bindingを変更しない。

## Gap model

[record schema](references/common/regulatory-record-schemas.md)を使う。

`gapClass`:

- `compliance`
- `prospective-implementation`
- `guidance-alignment`
- `sro-alignment`
- `watch`
- `participation-decision`

source compatibility `gapType`:
`none | partial | full | new-policy | watch | comment-decision`。

dates:

- `effectiveDates[]`
- `applicationDates[]`
- `transitionDates[]`
- `officialCommentDeadlineAt`
- `internalTargetAt`
- `revisitAt`

単一`due`へ潰さない。

全persisted gapで次をrequiredとする。

- `scope`: jurisdiction、authority、regulated entity、business unit、
  product/service、activity、provision、excluded scope
- `coverage.source`: expected/reviewed attachment count、complete、truncated、failures
- `coverage.policy`: exact policy item IDs、expected/reviewed/excluded sections、complete
- `coverage.timeWindow`: from/through

jurisdictionとauthority/provision/activityのいずれか、complete/not-truncated/no-failure
source coverage、nonempty policy IDs/expected/reviewed sections、complete policy
coverage、nonempty from/through time windowがないcandidateはpersistしない。

## Status/report mode

exact authorized recordsだけをreadし、次へ分ける。

1. 🔴 verified current external obligationのofficial/internal miss
2. 🟠 due soon / blocking implementation
3. 🟡 open
4. 👀 proposed/future-effective/watch/participation
5. guideline/administrative-guidance/exchange-SRO alignment
6. in progress
7. recently closed/risk-accepted

verification pending、`proposed`/`future-effective`、conflicting sourceを
「binding deadline missed」として
Overdueにしない:

> If this source becomes/currently is in force as described, the item may be late. Verify status before escalation.

accepted/closed itemはopen viewから外せるがaudit trailから削除しない。

output fields:

| ID | Class | Requirement | Instrument/force/lifecycle/applicability | Policy | Owner | Official dates | Internal/revisit | Verification | Status |
|---|---|---|---|---|---|---|---|---|---|

oldest open、owner breakdown、unassigned、source conflict、notification stateを示す。
10件超ならdashboardを提案できるが自動作成しない。

## Ingest candidate

`policy-diff`から受ける場合:

- same source snapshot + requirement + policy versionをde-dup
- scope limitation、severity floor、provenanceをcarry
- structured scope/coverageを必ずpersist
- independent classification fields/dateを分離
- owner不明はunassigned
- proposed create recordsをpreview
- fresh confirmation後だけconditional create
- each resultをaudit

owner notificationは別operation。

## Per-send confirmation

assignment、reminder、status deliveryの前に:

1. exact recipient/destination
2. message全文
3. citation/deadline verification state
4. confidentiality/DLP
5. explicit yes

を要求する。未確認citation/deadlineを含む場合は`verify before acting`をmessageへ残す。
send capability/approved-deliveryがなければcopy-ready draftだけ。

## Reminder

- compliance partial/full/new-policy: internal target前のconfigured cadence
- comment-decision: official deadlineとinternal review dateを分ける
- watch: auto-reminderでなくrevisit/source event
- future-effective implementation: effective/application/transitionごと

last sent timestampをexact recordへversioned update。1つのreminder同意を次回へ流用しない。

## `--close`

closeは「tracker上resolved」とするlegal-impacting operation。

必須:

- exact gap/source/policy/versionとcanonical scope
- source lifecycleStatus/normativeForce/applicability
- source/policy coverage complete、not truncated、unresolved failureなし
- exact internal remediation/approval artifact item/version/hash
- implementation evidence item/version/hash
- effective scope/entities/provisions
- residual issue
- qualified counsel/authorized closer、verifiedAt
- resolution、closedAt
- destination/DLP
- fresh confirmation
- closure basis:
  `policy-applied | control-implemented | regulator-submission | not-applicable | other`

evidenceなし、source conflict、partial implementation、approval pendingならblock。
closure basisの欠落/enum外、empty implementation evidence、blank item/version/hashもblock。
policy redraftがあるだけではcloseしない。compliance certificationを求められた場合は
別artifactとしてqualified counsel reviewを要求し、AIはcertifyしない。

internal remediation artifactとregulator-facing artifactを別item/version/hashで記録
する。`closureBasis: regulator-submission`なら、regulator-facing artifactに加え、
submission method、destination system/address、case ID、submitted artifact
item/version/hash、human submitter、submittedAt、deadline verification、receipt
ID/artifact item/version/hashがすべて一致するexact submission evidenceを要求する。
verified route ID、method、destination system/address、instruction URL/hash、deadline、
receipt-or-postmark、verifiedAtもsubmission evidenceとexact一致させる。
internal memo、approval record、draft hashだけでsubmissionまたはclosureを証明しない。

## `--accept`

risk acceptanceはexternal dutyのwaiver/消滅ではない。必須:

- authorized acceptor
- rationale
- residual risk
- compensating controls
- affected entities/scope
- qualified counsel review
- expiry/revisit trigger
- exact source lifecycle/applicability
- fresh confirmation

`risk-accepted`へversioned updateし、recordを残す。期限切れacceptanceはopen reviewへ
戻すcandidateで、silent renewalしない。
上記evidenceの1つでもmissing/blank、controls/affected entitiesがempty、expiryが
invalidなら`risk-accepted`を拒否する。

## Completion

reportではcoverage、source/status、counts、nearest dates、unassigned/conflicts、
notification stateを示す。writeではitemId、old/new eTag、idempotency、confirmation、
audit outcomeを示す。

next choices:

1. policy redraft
2. owner/escalation draft
3. missing source/facts
4. watch/revisit
5. other

人が選ぶ。自動handoffしない。

## 行わないこと

- unverified/proposed/future-effective itemをbinding Overdue化
- automatic close/risk accept/certification
- accepted/closed history deletion
- external obligationをinternal decisionで消す
- reminder/assignment auto-send
- send、post、publish、file、submit、approve、certify
