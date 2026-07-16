---
name: portfolio
description: >
  SharePointのIP portfolioでtrademark、patent、utility model、design、copyright、domainのreport、add、update、audit、versioned rebuildを会話で行う。JPO等のcurrent official deadline・fee・statusを人が検証し、file、pay、renew、abandon、scheduleを自動実行・決定しない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: ip-legal
  migration-target: power-platform
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# IP portfolio

正規label/flags:

- `/ip-legal:portfolio`
- `/ip-legal:portfolio --report [--days N]`
- `/ip-legal:portfolio --add`
- `/ip-legal:portfolio --update`
- `/ip-legal:portfolio --audit`
- `/ip-legal:portfolio --rebuild`

no flagは`report`、default `windowDays: 90`。`--days`はpositive integer。

## Mandatory state/deadline gate

1. [保存契約](references/common/cowork-runtime-contract.md)を読み、state gateway、
   exact list/library、ACL、conditional create/update、audit appendをlive preflight。
   失敗時はread-only/manual report/rebuild planだけ。
2. exact company/IP practice/user profile、authorized portfolio scopeを読みます。
3. matter-specific assetはactive/unexpired binding、practice portfolioはauthorized
   practice scope。別matterをglobal cursorで読まない。
4. deadline、fee、form、grace、holiday、filing cohort、owner/recordal、statusは
   current JPO/WIPO/official recordまたはqualified adviser recordで確認。
5. source URL、source version、checked date、official-record timestampを保存。
6. `filed | paid | registered | renewed | abandoned`はreceipt/official evidenceを
   確認し、人がstatus updateを承認した場合だけ。
7. new asset/versionはcreate、existing asset/pointerはupdate。混同しない。
8. `--rebuild`はdestructive-impact gateを通し、old versionをdeleteしない。
9. AIはfile、pay、renew、abandon、restore、notice、takedownをしません。
10. scheduled behaviorはapproved Power Platform evidenceがある場合だけ表示。
11. Cowork内DLP必須ならconfidential portfolioのproduction利用を停止。

[portfolio schema](references/portfolio-records.md)、
[JPO source register](references/common/jurisdictions/ja-jp/source-register.md)、
[automation contract](references/common/power-platform-automation-contracts.md)を使います。

## Conversation state

| state | intent |
|---|---|
| `initialize` | first portfolio version and active pointerを作る |
| `report` | next 90 days |
| `window` | `--report --days N` |
| `add` | one asset conditional create |
| `update` | one exact asset/deadline/status update |
| `audit` | source/deadline/title/use/owner/coverage health check |
| `rebuild` | superseding portfolio versionをcontrolled create |

## Japanese deadline floor

current official dataで確認する候補:

- patent examination request: filingから3年
- publication: 原則18か月
- patent first three fees: grant decision service後30日
- later patent annuities: next year前、late route/surcharge
- patent opposition: gazette publicationから6か月
- trademark: registrationから10年、6-month pre-expiry renewal window、
  late route/surcharge
- Japanese trademarkにU.S. §8/§71はない。3-year non-use cancellation risk用に
  genuine-use evidenceを保持
- design: current cohortはfilingから25年、annual fee。renewalと表示しない
- related design: Art. 10 current 10-year window
- utility model: separate 10-year/annual fee
- copyright: maintenanceなし。term category/sourceを確認
- Paris/PCT/Madrid/Hague: actual official route/record
- office action: actual noticeのdesignated period
- Patent Act Art. 3 holiday adjustment
- 2026-04-01 online dispatchのdeemed-delivery
- procedure-specific restoration / `not intentional` standard

generic tableよりactual notice、transition cohort、official docketが優先します。

## `initialize`

portfolio/pointerが存在しない場合だけ:

1. canonical `portfolioId`とversion 1 recordを`status: building`でconditional create。
2. source setをfreezeし、全asset recordをversion 1配下へconditional create。
3. expected asset count、schema、official-source coverage、duplicate/unmatchedを検証。
4. version recordを`status: active`へconditional update。
5. `portfolio-active-version` pointerを`expectedAbsent: true`でconditional create。
6. pointer create失敗時は既存pointerを照合し、二重portfolioを作らない。
7. old versionは存在しない。全outcomeをcanonical auditへappend。

gateway/source/confirmation不足ならinitialization planだけを出し、作成済みと
表示しません。

## `report`

実行時に各assetのsource/status/deadlineをrefresh candidateとして確認します。

| Bucket | Meaning |
|---|---|
| 🔴 `lapsed / grace / overdue-critical` | immediate human verification |
| ⏰ `due_soon` | within window |
| 🟡 `upcoming` | next band |
| 🌐 `agent_managed` | foreign associate/IPMS manages; confirm directly |
| ❓ `unknown` | missing source/date/status |

display:

| Asset ID | Type | Jurisdiction | Right/title | Action | Due | Grace | Owner | Source checked |
|---|---|---|---|---|---|---|---|---|

closing:

`Current official record and human verification required before filing or paying.`

「期限なし」reportでもsource coverage/last checkを示します。10行超ならdashboardを
提案します。

## `add`

one asset:

- immutable asset ID
- type:
  `trademark | patent | utility-model | design | copyright | domain`
- jurisdiction/route
- mark/title
- owner of record、business owner、representative
- application/registration/grant/priority numbers/dates
- classes/claims/design relation
- status/source system/item/version
- filing cohort、entity/fee reduction
- use evidence、licence/recordal
- official deadline candidates

new recordを`expectedAbsent: true`でcreateし、自動で`filed`または`verified`にしません。

## `update`

1. exact asset/item/latest`eTag`。
2. official record/receipt/evidence。
3. current→proposed diff、next lifecycle effect。
4. source/date/verifier。
5. fresh confirmation。
6. unique idempotencyでconditional update。
7. stale/partialでは再読取り。
8. audit append。

actionを「これから行う」instructionと「既に実行されたstatus record」に分けます。

## `audit`

- missing/stale official source
- unknown/grace/lapsed/evidence gap
- pending application without current status
- trademark non-use evidence
- owner/recordal inconsistency
- patent/design/utility model cohort/term
- copyright category/term
- assignment/licence/co-ownership
- unmonitored valuable mark
- Customs/platform enforcement route
- retention/legal hold/ACL
- automation solution evidence

## `rebuild`

1. exact current portfolio version、item count、active pointer、dependent cursor/output。
2. source set、query、coverageをfreeze。
3. retain/drop/change/add mappingとunmatched itemを表示。
4. pre-rebuild export candidate。
5. `Rebuild [portfolio/version] from [source set] and preserve old version? yes/no`
   のfresh explicit confirmation。
6. new versionを`status: building`でconditional create。
7. retain/change/add対象の全asset recordをnew version配下へmaterializeし、
   expected count、schema、source coverage、unmatchedを検証。
8. new versionを`status: active`へupdate。
9. `portfolio-active-version` pointerをexact `itemId`/`eTag`でnew versionへupdate。
10. pointer success後にold versionを`superseded`へupdate。
11. item mapping、partial failure、old/new versionをaudit。

pointer前にold versionをinactiveにせず、history/auditをdeleteしません。

## Automation status

`ip-renewal-watcher`は別solutionです。次のidentityを分離:

`portfolio-reader → deadline-verification-analyzer →
portfolio-alert-writer → approved-alert-delivery`

solution ID/version/owner/scope/connections/last successful run/next configured runを
stateで確認できない限り「weekly」「scheduled」「通知済み」と表示しません。

## 行わないこと

- JPO/WIPO/registryへfileまたはpay
- renew/abandon/restoreを決定
- stored calculationをofficial truthと表示
- actual receiptなしにstatusをcomplete
- old portfolio/history/auditをdelete
- scheduleをpackage capabilityとして主張
- local YAML/CSV/calendarをcanonical stateにする
- agent、hook、subagentを実行
