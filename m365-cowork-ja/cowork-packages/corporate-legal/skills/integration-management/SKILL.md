---
name: integration-management
description: >
  post-closing legal integrationをtransaction structure別にinit、contract review、report、update、export、rebuildへ遷移させ、consent、承継、登記、FIEA/TDnet、FEFTA、労働、個人情報、知財、許認可をSharePoint stateで追跡する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: corporate-legal
  migration-target: power-platform
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Integration management

旧来の参照label/flags:

- `/corporate-legal:integration-management`
- `--init`
- `--contracts`
- `--report`
- `--update`
- `--export [--format csv|table] [--section all|consents|contracts|workplan]`
- `--deal [code]`
- `--rebuild`

Coworkではflagをconversation stateへ変換する。local trackerを作らず、
SharePoint / Power Platform state front endとして動く。

## 目的

business integration全体ではなく、legal workstreamを管理する。consent、
contract/asset/employee/data/IP/licence succession、corporate record、registration、
PA obligation、FIEA/JFTC/FEFTA/TDnet等を追跡する。

## Mandatory structure / filing / rebuild / privilege / security gate

1. **Runtime/preflight:** `references/common/cowork-runtime-contract.md`を読み、
   state gateway、ACL、conditional create/update、audit appendをlive preflight。
   失敗時はread-only/manual draft mode。
2. **Matter:** exact expiring binding、matter `status: active`、deal code、
   close/effective date、authorized viewersを確認する。
3. **Transaction structure first:**
   `share sale | business transfer | merger | company split | share exchange |
   share transfer | share delivery | other`
   を確定する。
4. **Source:** PA、closing checklist、disclosure schedules、outside-counsel
   checklist、contract listのexact item/versionとcoverageを読む。
5. **Structure rule:** share saleはparty/employer continuityを通常のstartとし、
   business transferはindividual transfer、merger/splitはuniversal successionと
   special exceptionを確認する。全structureを同じassignment workflowにしない。
6. **Current filing:** commercial registration、tax/social/labour、FIEA/TDnet、
   FEFTA、JFTC、licence、IP recordalのfiler、deadline、system、evidenceを
   official sourceで確認する。
7. **Privilege/security:** clean-team解除、MNPI、competition-sensitive data、
   APPI purpose/notice/foreign transfer、trade secret、My Number、DLPを確認する。
8. **Human action:** consent outreach、novation、employee communication、
   filing、registration、recordal、send、signature、waiverを自動実行しない。
9. **Rebuild:** current tracker、source set、mapping、history impact、exportを
   示し、fresh explicit confirmation後にsuperseding versionをcreateする。
10. **Export:** external share用からinternal risk/privilege/clean-team notesを除き、
    formula injectionを防止する。
11. **DLP:** Cowork内DLP必須ならproduction useを停止する。

日本workflowは
`references/common/ja-jp/integration-entity.md`、
`references/common/ja-jp/ma-regulatory.md`、
`references/common/ja-jp/diligence-overlays.md`、
provenanceは
`references/common/source-provenance-and-review.md`を使う。

## State gateway fallback

preflight失敗時:

- source documentsからstarter workplan/report/export candidateをdraftできる
- exact current stateをreadできる場合だけread-only report
- initialized/updated/rebuiltと表示しない
- local YAML/CSVをcanonical trackerにしない
- Power Platform flowを実行したと表示しない

## 会話state

| state | canonical input | action |
|---|---|---|
| `initialize` | `--init [--deal code]` | PA/closing artifactsからtracker candidate |
| `contracts` | `--contracts [--deal code]` | contract listをstructure別にclassify |
| `report` | `--report [--deal code]` | current stateのstatus/critical path |
| `update` | `--update [--deal code]` | exact itemをmanual/report sourceから変更 |
| `export` | `--export ...` | selected sectionのCSV/table draft |
| `rebuild` | `--rebuild [--deal code]` | superseding tracker versionをcontrolled create |

`--format`: `csv | table`。
`--section`: `all | consents | contracts | workplan`。
conflicting/invalid valueは人に再選択してもらう。

## Initialize

input priority:

1. full PA
2. PA + closing checklist + disclosure schedules
3. deal summary/outside-counsel workplan
4. plain-language facts

partial inputはstarter trackerでありcompleteと表示しない。

extract:

- Required Consentsとdeadline
- post-closing covenant
- rep survival（general/fundamental/tax等を別々に）
- escrow release
- earnout milestone（owner `finance`）
- outstanding closing item
- structure-specific corporate/registry/labour/data/licence/IP action

phase:
`day_1 | day_30 | day_90 | day_180`。
phaseはinternal control、`deadline_basis`は
`pa-obligation | regulatory | best-practice`のsource enumを保持し、日本版では
law/listing sourceをnotes/legal basisで明示する。

candidateを示し、coverage/unknown/item count/source versionを確認してから
conditional createする。

## Structure-specific workplan

### Share sale

- shareholder register/share certificate/restricted-share evidence
- representative/officer/signatory/registry
- control-change consent/licence
- FEFTA/JFTC/FIEA/TDnet post action
- bank/insurance/KYC
- data/system access and clean-team

### Business transfer

- asset/claim/obligation/contractual position
- consent/novation/notice/perfection
- employee consent/consultation
- APPI purpose/notice/foreign transfer
- licence reapplication/consent
- real estate/IP recordal

### Merger/company split

- universal succession scope/special exception
- creditor/employee procedure
- registration/effective date
- licence/data/IP special rule

`Secretary of State ownership notification`、generic `USPTO recordal`を使わない。

## Contracts

source path:

- approved connected repository
- exact uploaded list
- Material Contract schedule

minimum: Contract Name、Counterparty。helpful: type、value、exact clause/source。

classification:

| Mechanism | Meaning |
|---|---|
| `consent-required` | explicit consent restriction |
| `coc-provision` | CoC consent/termination/notice |
| `auto-assign` | actual explicit permissionまたはverified structure rule |
| `silent` | clause silent。governing law/structure reviewが必要 |
| `not_reviewed` | source/quoteを取得できない |

source tierを保持する:

- Tier 1: Required Consents
- Tier 2: material + consent required/silent needing review
- Tier 3: CoC
- Tier 4: verified no action/auto-assign

silentをTier 4へ自動移動しない。PA Required ConsentはTier 1。

## State enum

workplan:

- owner: `legal-owns | legal-supports`
- workstream:
  `legal | hr | it | finance | real-estate | other`
- priority: `critical | high | medium | low`
- deadline_basis:
  `pa-obligation | regulatory | best-practice`
- status:
  `not_started | in_progress | complete | blocked | deferred`

consent:

`not_started | outreach_sent | in_negotiation | obtained | waived | refused`

contract:

`not_reviewed | no_action | consent_pending | outreach_sent | in_negotiation |
consent_obtained | assignment_complete | waived | refused | coc_triggered`

canonical keys/schemaは`references/integration-records.md`。

## Report

show:

- Day N post-close
- Required Consents deadline/progress/refused/at risk
- contract tiers/status
- legal-owned overdue/due-this-week/completed
- corporate/registry/FIEA/TDnet/FEFTA/labour/data/IP/licence
- blockers/decisions
- key dates
- source/evidence/currency gaps

`complete`はevidenceに基づく。10行超ならdashboardを提案するが、自動生成しない。

## Update

manual statementまたはexact uploaded status documentからcandidateを作る。

1. source item/versionを読む。
2. exact tracker itemへmatch。near-matchを人へ提示。
3. current/proposed/evidence/downstream effectを示す。
4. fresh confirmation。
5. exact item/eTag/idempotencyでconditional update。
6. stale/partialでは再読取り。
7. audit append。

refused consent、missed PA deadline、licence failureはoutside counsel/specialistへ
escalateし、indemnification/breach結論をAIが決めない。

## Export

sectionごと:

- Workplan: id, phase, description, owner, workstream, priority, deadline,
  deadline_basis, status, blocker, legal_basis, evidence
- Consents: id, counterparty, contract_type, required_consent, pa_deadline,
  status, assigned_to, obtained_date, conditions, source
- Contracts: id, name, counterparty, contract_type, annual_value,
  assignment_mechanism, tier, required_consent, pa_deadline, status, source

OneDrive draft。SharePoint promotion/external sharingは別confirmation。

## Rebuild

1. exact tracker version/item count/dependencies/cursorsを読む。
2. new source set/version/coverageをfreeze。
3. old→new mappingを`retain | change | add | supersede | unresolved`で表示。
4. pre-rebuild export candidateを作る。
5. fresh explicit confirmation。
6. old trackerをdeleteせず`superseded`、new versionをconditional create。
7. partial failure/unmatchedをauditし、自動retryしない。

source/gateway/confirmation不足ならread-only planだけ。

## 行わないこと

- business integrationのownerになる
- outreach/novation/assignment/signature
- registration/authority/IP filing
- earnout performanceを計算・承認
- tracker report時にsource contractを読んだと偽る
- scheduled status reportを推測
- old tracker/history/auditをdelete
- local trackerへfallback
