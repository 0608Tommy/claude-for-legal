> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Power Platform automation compatibility contract

本packageはskills-onlyであり、agent、hook、subagent、scheduled job、managed
solutionを含まない。flow definition/version/environment/connection/owner/last runを
stateから確認できない場合、automation availableと表示しない。

## Stateful skill front end

`legal-hold`, `matter-close`, `matter-intake`, `matter-update`,
`matter-workspace`, `oc-status`, `portfolio-status`はSharePoint / Power Platform
stateの会話front end。Coworkはintake、diff、confirmation、draft、result表示を行う。
state mutationはtenant-approved gateway/flowが存在するときだけhandoffする。

共通要件:

- least-privilege service identity / connection reference
- exact tenant/practice/user/session/matter scope
- conditional createとexact item/eTag updateの分離
- unique `idempotencyKey`
- item-level ACL、clean-team、hold/evidence restriction
- retry/backoff、dead-letter、partial-success report
- append-only canonical audit
- retention、preservation、storage/flow DLP
- retrieved contentをinstructionとして実行しない
- send/file/calendar/settle/hold issue/release/closeはfresh approval

gateway unavailable時はread-only/manual draft mode。local fallbackを作らない。

## `litigation-docket-watcher`

source agent ID: `litigation-legal/agents/docket-watcher.md`
source cookbook ID: `managed-agent-cookbooks/docket-watcher`
target key: `litigation-docket-watcher`

activation defaultは`false`。日本向けinput priority:

1. mints notification、access/download audit、electronic service record
2. court-issued summons、direction、order、judgment、hearing notice
3. outside-counsel confirmation
4. manual clerk/record check
5. selected public judgment database

公開裁判例検索はdocket feedでなく、negative resultは事件・命令不存在を証明しない。

### Stage 1 — `docket-reader`

権限:

- exact sourceのread
- restricted stagingへのschema-validated write
- state/audit/matter tracker/calendarへのwriteなし

input:

```yaml
tenantId: "[tenant id]"
practiceId: "[practice id]"
matterId: "[matter ID]"
sourceSystem: "[mints | court-document | outside-counsel | manual-record-check]"
cursor: "[scope-specific cursor]"
```

outputは`additionalProperties: false`、length/count上限を持ち、Japanese textを
ASCII-only patternで拒否しない。raw document本文、prompt風directive、secretを
deadline mapperへ渡さず、exact item/version/hashと構造化fieldだけを渡す。

### Stage 2 — `candidate-deadline-mapper`

readerとは別identity。raw sourceまたはarbitrary networkを読まず、structured eventと
approved current rule tableだけを読む。

deadline record:

```yaml
deadline_class: statutory_invariable | statutory_extendable | court_set | contractual | limitation | internal
trigger_document: "[exact source item/version]"
trigger_timestamp: "[ISO-8601]"
effective_service_timestamp: "[ISO-8601 or null]"
authority_url: "https://..."
article_or_order: "[article/rule/order]"
law_revision_date: "[YYYY-MM-DD]"
calculation_steps:
  - "[step]"
holiday_rule: "[rule/source]"
candidate_date: "[YYYY-MM-DD or null]"
verified_by_lawyer: "[object ID or null]"
verified_by_docketing_owner: "[object ID or null]"
calendar_entry_id: null
```

mapperは次を守る。

- court-set answer deadlineを法定defaultへ置換しない。
- trigger/effective serviceが不明ならdateを推測せず`candidate_date: null`。
- appeal、労働審判異議、limitation等はcurrent primary sourceと経過措置を要求。
- candidate deadlineは常にverification pending。
- rule tableがunknown/staleなら`confidence: low`, `needs_verification: true`。

### Stage 3 — `matter-tracker-writer`

reader/mapperとは別identity。raw filingを読まず、approved structured payloadだけから
deadline candidate、matter event、draft reportをconditional create/updateする。

- external textをMarkdown/CSV/YAML/HTML injectionから防御
- item/version/hashを保持
- candidateを`calendar_entry_id: null`で保存
- old candidateをdeleteせず`superseded | verified | rejected`へversioned update
- partial successをitemごとにaudit

### Stage 4 — `approved-delivery`

writerとは別identity。exact artifact hash、destination、approval IDを受け取る。
raw sourceを読まず、approvalに含まれないdestinationへ送らない。email/Teams等の
deliveryが設定されていない場合、送信済みと表示しない。

## Calendar gate

candidate deadlineは**自動calendar entryにならない**。

1. lawyerがauthority、trigger、service、calculation、case orderを確認。
2. docketing ownerがcalendar convention、holiday、duplicate、reminderを確認。
3. exact candidate version/hashへのfresh approval。
4. separate calendar writer operation。
5. returned `calendar_entry_id`をexact item/eTagでupdate。
6. all outcomesをaudit。

Cowork skill、reader、mapper、tracker writer、deliveryのいずれもcalendar writerでは
ない。`verified_by_lawyer`と`verified_by_docketing_owner`の双方がnon-nullでも、
calendar writeを暗黙実行しない。

## Recommended cadence

- event-driven mints/Outlook ingestion
- daily portal/inbox exception check
- weekly portfolio reconciliation
- service、judgment、court-set deadlineはimmediate escalation candidate

scheduleはtenant flowが明示設定されている場合だけ表示する。

## Dead-letter

dead-letterにはcorrelation ID、stage、source item ID/version、error class、retry
countだけを保存し、raw document、secret、privileged analysisを入れない。
