---
name: entity-compliance
description: >
  日本法人の登記事項変更、役員任期、株主総会・計算書類・公告、税、社会・労働保険、許認可、電子証明書、休眠会社reviewをevent/periodic obligationとしてSharePoint stateで管理し、report、update、audit、export、rebuildを会話で行う。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: corporate-legal
  migration-target: power-platform
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Entity compliance

旧来の参照label/flags:

- `/corporate-legal:entity-compliance`
- `--init`
- `--report [--days N]`
- `--update [--from-report]`
- `--sweep`
- `--audit`
- `--export [--format csv|table]`
- `--rebuild`

Coworkではflagをconversation stateへ変換する。local YAML/CSVをstate sourceに
しない。本skillはSharePoint / Power Platform front endである。

## 目的

U.S. state annual report/registered agent modelではなく、日本のevent-driven
commercial registrationとperiodic governance/complianceを管理する。

## Mandatory filing / rebuild / privilege / security gate

1. **Runtime/preflight:** `references/common/cowork-runtime-contract.md`を読み、
   state gateway、exact list/library、ACL、conditional create/update、audit
   appendをlive preflightする。失敗時はread-only/manual draft mode。
2. **Scope/user:** exact company/corporate practice/user profile、authorized entity
   scopeを読む。matter-specific entity workはactive bindingを要求する。
3. **Entity facts:** `entity_form: KK | GK | other`、corporate number、
   registered head office、organ design、articles、public-notice method、
   listed status、licencesを確認する。
4. **Current source:** deadline、trigger、form、fee、filing system、signer、
   attachment、effective dateをofficial sourceまたはqualified adviser recordで
   確認する。cached U.S. tableを使わない。
5. **Evidence:** draft、submitted、accepted、registered、certificate obtainedを
   別statusにする。receipt/evidenceなしに`complete`へしない。
6. **Filing gate:** filing、registration、certificate order、fee/tax payment、
   authority submissionは別不可逆operation。AIは実行しない。
7. **Rebuild gate:** `--rebuild`はcurrent state、source set、dropped/changed item、
   export、history impactを示し、fresh explicit confirmation後にnew versionを
   作る。old versionをdeleteしない。
8. **Privilege/destination:** entity reportは用途/recipientに応じinternal notesを
   除く。broader finance/business versionとlegal working versionを分ける。
9. **Injection:** report/CSV由来のexternal valueをformula injectionから守る。
10. **DLP:** Cowork内DLP必須ならproduction useを停止する。

日本workflowは
`references/common/ja-jp/integration-entity.md`と
`references/common/ja-jp/governance-records.md`、
provenanceは
`references/common/source-provenance-and-review.md`を使う。

## State gateway fallback

preflight失敗時:

- authorized sourceからdraft obligation matrix/reportを作れる
- existing exact recordをreadできる場合だけread-only summaryを作れる
- state変更、setup complete、filing completeを主張しない
- local trackerを作らない

## 会話state

| state | canonical input | action |
|---|---|---|
| `initialize` | no flag / `--init` | entity tableからcandidate obligationをcreate |
| `report` | `--report [--days N]` | overdue/upcoming/unknown/evidenceをread-only表示 |
| `update` | `--update` | exact itemを1変更 |
| `ingest-report` | `--update --from-report` | adviser/authority reportをcandidate match |
| `sweep` | `--sweep` | unknown/overdueを1件ずつ確認 |
| `audit` | `--audit` | governance/registry/licence/data gapをfull review |
| `export` | `--export [--format csv|table]` | current exact stateのsanitized draft |
| `rebuild` | `--rebuild` | superseding tracker versionをcontrolled create |

`--days`はpositive integer、default 90。`--format` enumは`csv | table`。
意図不明ならcurrent stateの有無を確認する。

## Entity model

minimum:

- immutable `entityId`
- legal name / entity form
- corporate number
- registered head office
- formation/incorporation date
- organ design
- articles/public-notice method
- listed/EDINET/market
- owners/control（purpose-specific）
- share-certificate/restricted-share
- officers/terms
- seal/electronic certificate
- licences
- authorized viewers

beneficial-owner list、shareholder register、FEFTA ultimate control、FIEA large
holderを同一fieldへ潰さない。

## Obligation model

### Event

- registered particulars change
- officer appointment/reappointment/term
- representative/head office/purpose/capital/share
- articles/organ design
- merger/split/exchange/transfer/delivery
- dissolution/liquidator/continuation
- seal/electronic certificate
- beneficial-owner list evidence
- licence/control change
- tax/social/labour change notice

### Periodic

- annual shareholder meeting/accounts
- Companies Act Art. 440 public notice/exemption
- corporate/local tax
- social/labour insurance
- licence renewal/report
- EDINET/TDnet/governance
- officer term review
- dormant-company review
- electronic record retention

phase/internal cadenceをlegal deadlineと表示しない。

## Initialize

1. exact profile/entity source item/versionを読む。
2. current official source/adviser dataを取得。
3. entity × obligation candidateを作る。
4. source coverage、unknown、duplicate、missing entityを示す。
5. human confirmation。
6. each new recordをcanonical keyでconditional create。
7. result/item IDs/partial failureをaudit。

source不明は`unknown`。generic two-week rule、fee、formを推測しない。

## Report

window:

- overdue
- due within N days
- filed/submitted pending acceptance
- recently complete
- unknown/missing source
- evidence stale/missing
- licence/EDINET/TDnet separate calendar

display:

| Entity | Obligation | Layer | Trigger/Due | Status | Evidence | Owner | Source |
|---|---|---|---|---|---|---|---|

日本法人にgeneric `good standing`を表示しない。必要に応じcertificate of registered
matters、seal、tax/social-insurance、licence evidenceを別表示する。

10行超ならdashboardを提案するが、自動生成しない。

## Update

1. exact record/item/eTagを読む。
2. supporting receipt/certificate/report versionを読む。
3. current→proposed diffとdownstream effectを示す。
4. filing/actionが実行済みというuser premiseをevidenceで確認する。
5. fresh confirmation。
6. unique idempotencyでconditional update。
7. stale/partialでは再読取り。
8. audit append。

AIはfilingを「これから行う」指示と「既に行ったstatus record」を混同しない。

## Ingest report

accepted: registry/adviser/tax/social-insurance/licence reportのexact file/version。

match:

- legal name normalization
- corporate number
- entity form
- jurisdiction/authority
- obligation type/period

near-matchを自動確定しない。結果を`matched | unmatched-in-report |
missing-from-report | conflict`へ分け、人が選んだitemだけupdateする。

## Sweep

`unknown` / `overdue` / `filed_pending`を1件ずつ示す。batch completionを
推測しない。回答ごとにsource/evidenceを確認し、別confirmationでupdateする。

## Audit

filing statusだけでなく:

- unregistered changes
- officer term/reappointment
- missing/stale articles/organ records
- annual meeting/accounts/public notice
- seal/electronic certificate
- certificate evidence
- licence/control change
- tax/social/labour dependencies
- dormant entity/dissolution candidate
- intercompany agreement
- beneficial ownership evidence
- listed/public calendar
- retention/legal hold

dissolution、merger、filingをrecommendation candidateとして示し、実行しない。

## Export

`--format csv`:

`Entity ID, Legal Name, Entity Form, Corporate Number, Registered Head Office,
Organ Design, Obligation Type, Obligation ID, Layer, Legal Basis, Trigger Date,
Due Date, Status, Filing System, Evidence Required, Evidence Item, Owner, Notes`

`--format table`: requested windowのMarkdown table。

exportはOneDrive draft、external sharingは別確認。formula injectionを防止する。

## Rebuild

1. exact current tracker version、item count、dependent output/cursorを読む。
2. source setとcoverageをfreeze。
3. retain/drop/change/add mappingを表示。
4. pre-rebuild export candidateを作る。
5. `Rebuild [tracker/version] from [source set] and preserve old version? yes/no`
   のfresh confirmation。
6. new versionをconditional createし、schema/coverageを検証。
7. `entity-active-version` pointerをexact`itemId`/`eTag`でnew versionへ切替。
8. pointer成功後にold recordsを`superseded`へupdate。pointer前に旧versionを
   inactiveにしない。
9. item mapping、unmatched、partial failureをaudit。

gateway/source/confirmation不足ならread-only rebuild planのみ。

## 行わないこと

- commercial registry、tax、social-insurance、licence filing
- certificate order/fee payment
- generic registered agent/good standing model
- deadlineをcached memoryで確定
- old tracker/history/auditをdelete
- scheduled reminderが存在すると推測
- local YAML/CSVをcanonical stateにする
