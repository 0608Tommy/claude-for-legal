---
name: deadlines
description: >
  clinic matterのdeadline candidateをadd、report、update、complete、closeで扱うSharePoint / Power Platform front end。日本のforum別effective-dated rule card、trigger、送達、経過措置を使い、責任弁護士とdocket ownerの二重確認前はcalendar factにしない。scheduled alert、calendar write、提出をpackageが実行すると主張しない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: legal-clinic
  migration-target: power-platform
  logical-target-id: ja-jp.power.legal-clinic.deadlines
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Deadlines

canonical label:
`/legal-clinic:deadlines [--add | --report | --update <id> | --complete <id> | --close <id> | --horizon=N]`

## Mandatory deadline / matter / automation gate

1. `references/common/cowork-runtime-contract.md`と
   `references/common/power-platform-automation-contracts.md`、
   `references/common/clinic-state-payloads.schema.json`を読む。
2. scopeを`matter-mode | portfolio-mode`で先に確定する。
3. `matter-mode`はexact userと**1件だけ**のactive non-null expiring matter binding、
   conflict/engagement/scope、authorized ACLを要求する。add/update/complete/closeは
   matter-modeだけ。
4. `portfolio-mode`はfresh unbound session、explicit portfolio authority、
   pseudonymous minimum metadataだけ。active binding又はclient identityがあれば停止。
   itemを開く場合はportfolio conversationを終了し、新しいconversationでfresh binding。
5. gateway、state/audit、exact list IDs、conditional write、retention/preservation、
   storage/flow DLPをlive preflight。失敗時はread-only/manual candidate draft。
6. deadlineは`candidate`。current official source、effective date、forum、trigger、
   effective service、holiday、transition、case orderを確認する。
7. 責任弁護士とdocket ownerの二重verification前にcalendar factとしない。
8. calendar writeは別identity、別operation、exact candidate versionへのfresh approval。
9. court-set dateをstatutory defaultへ置換しない。civil、criminal、administrative、
   family、labor、immigration、housing、benefitsのclockを混同しない。
10. `criminal | immigration | housing | benefits`はapproved current source cardなしに
    deadlineを計算せず、emergency/referral routeだけ。
11. urgent/overdue/missed candidateはresponsible lawyerとapproved docket/emergency routeへ
   即時escalateするが、response、remedy、extensionを約束しない。
12. package、skill、manifestをscheduleの証拠にしない。
13. Cowork内DLPが必須ならconfidential matter dataを投入しない。

Japan:
`references/common/ja-jp/procedure-deadlines.md`。

## Mode

| mode | behavior |
|---|---|
| `add` | candidate create |
| `report` | authorized open candidates rollup |
| `update` | source/calculation/statusのversioned patch |
| `complete` | actual action evidence確認後にcomplete |
| `close` | 不適用理由とlawyer approvalでclose |

defaultは`report`。

## Scope modes

### `matter-mode`

one active bindingのexact `matterId`だけを読む。`tracker-record` +
`payload.trackerType: deadline`のstrict payloadでwriteし、outer `scopeId`とpayload
`matterId`の一致、duplicated tenant/practice identityをsemantic validateする。
別matter候補、bindingなし、
複数bindingではfail closed。

### `portfolio-mode`

fresh unbound sessionでread-only `report`だけ。表示可能field:

- pseudonymous matter ID
- deadline class、forum、candidate/verified status
- candidate/verified date又はunknown
- owner group、priority、last checked

source document、client identity、safe-contact、calculation detail、decision notesを
表示しない。cursorはportfolio authority/query固有。item open、verification、writeは
新しいbound conversationで行う。

## `add`

required fields:

- matter ID、forum type、deadline class、label
- exact trigger document item/version
- trigger timestamp、effective service timestamp又はunknown
- official authority URL、article/order、law revision
- civil electronic-service event fields
- period value/unit、start event、start-day rule、timezone、last-day/holiday/cutoff
- governing regime、`cpc95Applies`、CPC95 applicability source、
  Administrative Organs Holiday Act applicability、special-rule source
- 民法上のcompletion-postponement groundとrenewal groundを別field
- proceeding commenced date、2026-05-21 transition regime、case direction
- candidate date又はnull
- owner student、responsible lawyer、docket owner

lawyer-approved effective-dated rule cardを使う。rule card missing/stale、trigger/service
unknownなら`candidateDate: null`, `confidence: low`, `needsVerification: true`。
intakeからのmandatory handoffは1trigger 1candidateとし、duplicate keyを事前照合する。
machine payloadはschemaの`deadlinePayload`へvalidateする。

民事訴訟法95条のextensionを行政・契約・benefits・immigration等へ自動適用せず、
行政機関休日法も対象機関/行為/special ruleを確認してから使う。

criminal deadlineは`governingTimeComputationRegime:
criminal-procedure-code-55`とapplicable criminal special provisionを要求する。
民事訴訟法95条、民法138～143条、又は民事訴訟法55条を代用しない。
`civilElectronicService`は`not-applicable`でcivil metadataなし、transitionは
`procedure-specific`でなければschema rejectする。

create:

1. preview source/calculation/unknowns。
2. fresh confirmationはcandidate record作成だけに限定。
3. `expectedAbsent: true`、unique idempotency。
4. returned exact item ID/eTag/version。
5. audit append。

## `report`

group:

- overdue/unresolved
- due candidate today/3/7/14 days
- unknown date urgent calculation tasks
- verification owner/status
- forum/practice area
- unassigned

verifiedとcandidateを同じ色・labelにしない。10行超ならcounts、timeline、sortable tableの
dashboardを提案できるが自動作成しない。restricted matterの存在又はclient identityを
unauthorized portfolio viewerへ表示しない。

## `update`

exact item ID、latest ETag/versionを再取得し、old/new source、trigger、service、
calculation、candidate date、statusを示す。old candidateをdeleteせず、
`verified | rejected | superseded`へversioned updateする。verificationとcalendar writeを
1confirmationにまとめない。

calendar lifecycleは
`not-requested | approval-pending | write-pending | created | failed | removed`。
calendar entry ID、approval、writer、failure auditを別fieldで保持する。

## `complete`

file/submit/service/hearing等のactual evidence item/version、actor、timestampを人が確認する。
completion evidence/version、completed actor/timeをstrict payloadへ記録する。draft
completion又は予定だけでcompleteにしない。AIはfile/serveしない。

## `close`

case settled、order changed、candidate duplicate等で不適用となった理由、
**exact closure source item ID/version/effective date/retrieval/review status**、
responsible lawyer approval、closed actor/timeを記録する。versioned closure source
evidenceが1件もなければ`closed`へtransitionしない。matter close又はrecord deleteを
実行しない。

## Automation status

solution ID/version、`deadline-source-reader`、`candidate-deadline-mapper`,
`deadline-state-writer`、calendar writer、delivery identity、recurrence、scope、
last successful run、destinationをstateから確認する。証拠がなければ:

`次回reviewはscheduledではありません。承認済みautomation又は人による再実行が必要です。`

## Artifact separation

deadline recordは`tracker-record`。legal analysisは`internal-memo`、clientへの説明は
`client-safe-draft`、court/agency submissionは`filing-draft`。candidateをclient又は
courtへ自動送信しない。

## 行わないこと

- state plausibility band又は米国defaultで日本deadlineを計算
- candidateのautomatic calendar registration
- lawyer/docket dual verificationをcalendar approvalとみなす
- extension、relief、timely filingを保証
- source evidenceなしにcomplete/closed
- auto-notify、send、post、file、serve、matter close
- Power Platform solution/scheduleのprovision claim
