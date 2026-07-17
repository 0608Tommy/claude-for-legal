---
name: subpoena-triage
description: >
  canonical IDを保持しつつ、日本案件ではRule 45相当を発明せず、当事者照会、調査嘱託、文書提出命令、送付嘱託、証拠保全、証人呼出し、弁護士会照会、当局要請等を実際の根拠へ分類し、期限・scope・秘密性・対応案をdraftする。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: litigation-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Court order and evidence-request triage

canonical label:
`/litigation-legal:subpoena-triage [path-to-subpoena] [--slug=custom-slug]`

source classification token
`third-party-docs | third-party-depo | party | CID | grand-jury`はforeign/source import
互換のため保持するが、日本instrumentをRule 45相当として押し込まない。

## Mandatory gate

1. `references/common/cowork-runtime-contract.md`を読む。
2. exact incoming item/version/hash、service/receipt evidence、recipient entityを確認。
3. exact user/profile、matter relation、access、evidence/clean-team ACLを確認。
4. Japanなら
   `references/common/ja-jp/evidence-confidentiality-preservation.md`、
   `civil-procedure-and-digital.md`、`source-register.md`を読む。
5. issuing authority、instrument、actual statutory/court basisをcurrent official sourceで
   確認。名称だけで分類しない。
6. deadlineはtrigger/service/order/holidayを分離し、candidateをcalendar登録しない。
7. criminal/regulatory/sector requestはspecialistへescalateし、civil templateを流用しない。
8. AIはobjection/response file、production、appearance、calendar、preservation issueを
   実行しない。

## Japan classification

```yaml
instrumentTypeJP: party-inquiry | court-commission | document-production-order | document-transmission-request | pre-action-inquiry | pre-action-evidence-collection | formal-evidence-preservation | witness-summons | bar-association-inquiry | patent-inspection | execution-information | authority-request | foreign-subpoena | other
```

確認する事項:

- issuing authority / court / division
- parties / caption / case number
- legal basis and article/order
- service/receipt/effective timestamp
- requested documents/information/testimony
- holder/custodian/system
- fact to prove / stated purpose
- confidentiality/order/sector restriction
- response, objection, compliance, appearance date
- appeal/review/meet-and-confer route if actual law provides

grand jury/criminal、regulator、foreign subpoenaはimmediate specialist route。

## Analysis

### Scope

actual instrumentのstatutory elementsを満たすか。文書提出命令ではdocument、
purport、holder、fact to prove、production duty basis等を確認する。一般的な
relevance fishing expedition analysisだけで終えない。

### Burden / possession

custodian、system、date range、volume、collection/translation、third-party data、
trade secret、cost。`small | medium | large | extreme` tokenを保持する。

### Confidentiality / refusal

弁護士法23条、民訴法197/220、self-use document、court confidentiality、
Patent Act order、contract、personal data等をactual basisで確認する。一般US
privilege/work productと書かない。

### Deadline

```yaml
deadline_class: statutory_invariable | statutory_extendable | court_set | contractual | limitation | internal
trigger_document: "[item/version]"
trigger_timestamp: "[timestamp]"
effective_service_timestamp: "[timestamp or null]"
authority_url: "https://..."
article_or_order: "[article/order]"
candidate_date: "[date or null]"
verified_by_lawyer: null
verified_by_docketing_owner: null
calendar_entry_id: null
```

FRCP 45 objection window、100-mile rule、motion-to-quash defaultを日本modeに使わない。

## Response framework

final filingではなくinternal framework。

- comply / partial comply / seek clarification / seek direction / challenge / specialist route
- legal basis
- applies to which category
- strength: `strong | reasonable | weak`
- fact/source needed
- deadline candidate
- approver

production planはformatを相手文書とcourt directionから確認し、TIFF/load fileをdefaultに
しない。

## Output

```markdown
> **⚠️ レビュー担当者向け注記**
> [common block]

# Court order / evidence request triage

**Inbound request ID:** [...]
**Instrument:** [instrumentTypeJP]
**Source compatibility class:** [token or N/A]
**Issuing authority / case:** [...]
**Received / effective service:** [...]

## Requested scope
[numbered categories]

## Portfolio relation
[authorized matter / standalone]

## Scope / burden / possession
[analysis]

## Confidentiality / refusal bases
[exact basis + unresolved]

## Response framework
| Route | Basis | Applies to | Strength | Counsel review |
|---|---|---|---|---|

## Deadline candidates
[structured fields; no auto calendar]

## Collection / response plan candidate
[custodians、systems、review、format、translation]
```

saveは`inbound-request` conditional create。matter link、preservation assessment、
deadline stateは別confirmation。

## Completion

instrument、deadline gaps、scope/burden、confidentiality、specialist route、save stateを
示し、次から選んでもらう。

1. counsel response framework
2. clarification/direction request draft
3. collection facts
4. preservation/deadline candidate review
5. other

## 行わないこと

- Rule 45 equivalentの発明
- final objection/response/production
- motion/file/appearance
- automatic calendar/hold/matter create
- criminal/regulatory specialistの代替
- local filesystem、agent、hook、subagent
