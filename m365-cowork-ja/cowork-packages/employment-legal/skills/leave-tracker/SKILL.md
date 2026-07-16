---
name: leave-tracker
description: >
  source leave-tracker skillとagentを統合し、日本のmaternity、childcare、family-care、annual leave、occupational injury、insurance benefit、disability accommodationをcurrent lawとactual scheduleで確認し、decision-pointだけを提示する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: employment-legal
  migration-target: power-platform
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Leave tracker

旧来のlabel:
`/employment-legal:leave-tracker`。

source agentのcurrent-law、actual schedule、decision alert、clean summary、coverage、
non-scheduling behaviorを本skillへmergeしています。

## Mandatory leave / medical / automation gate

1. `references/common/cowork-runtime-contract.md`を読み、gateway、exact current user、
   practice、restricted matter accessをlive preflightします。失敗時はuser-provided
   dataのread-only draft analysisだけで、register updateを主張しません。
2. leave/medical/accommodation caseは一般workspace設定にかかわらずrestricted
   isolationを使い、pseudonymous central indexとidentity mappingを分けます。
3. sourceはapproved HRIS read-only connectionまたはexact SharePoint state。
   connector declarationだけでHRIS connectedと表示しません。
4. applicable law、eligibility、procedure、deadline、benefit、actual scheduleを
   each runでcurrent official sourceから確認します。
5. job protection、employer procedure、insurance benefit、annual-leave accounting、
   health accommodationを別trackにします。
6. profileのalert windowは[I]であり法定clockではありません。未設定なら数値を
   勝手に入れません。
7. AIはleave/accommodation/medical/payroll/benefit/return/terminationを決定しません。
8. scheduleは`references/automation-contract.md`のproofがある場合だけ表示します。
9. Cowork内DLP必須ならmedical/leave dataを投入せずproduction停止です。

Japan:
`references/common/jurisdictions/ja-jp/leave-harassment.md`。
record: `references/leave-records.md`。

## 会話state

| state | intent |
|---|---|
| `review-open` | authorized open casesをreview |
| `review-one` | exact `leaveId`のdecision points |
| `coverage` | source/read/unknownの確認 |
| `automation-status` | approved solution/schedule proofだけ表示 |
| `draft-follow-up` | human owner向け質問・通知案 |

defaultは`review-open`。state writeは別operationです。

`review-open`は`lifecycle: open | approved | active`だけを対象にし、
`returned | closed | cancelled`を除外します。actual returnまたはcloseを
推測せず、evidence付きの明示transitionだけを使います。

## Source/read

HRIS readerからはpseudonymous ID、jurisdiction、actual schedule、leave type/date、
procedure fields等のminimum dataだけを取得します。medical narrative、diagnosis、
unrelated HR fileを取得しません。

manual spreadsheet/documentが提供された場合、session内でcoverageを示して分析できますが、
local registerへ保存しません。stateへ取り込むには`log-leave`またはapproved writerの
separate confirmationが必要です。

## Japan case analysis

caseごとに:

- maternity/childcare/post-birth/child-care-days/family-care/family-care-days
- annual paid leave/five-day duty
- occupational injury/job-protection
- disability/health accommodation
- company leave
- employment/health insurance benefit

を該当factsで分類します。child DOB/age、family category、eligibility/exclusion
agreement、requested/approved period、individual notice、intention confirmation/
hearing、accommodation、overtime/night restriction、flexible measureを確認します。

numeric entitlement/deadlineを保存済みmemoryから使わずcurrent sourceで確認します。
actual normal scheduleを使用し、固定週を仮定しません。

## Decision-point alerts

action/decisionが必要なcaseだけをmain sectionへ出します。

```text
[Pseudonym] — [track / issue]
Decision needed: [human decision]
Owner: [human owner]
Due candidate: [date or unknown]
Clock owner: [employer / employee / insurer / internal]
Source/effective date: [official]
Inputs/missing: [facts]
Do not do automatically: [leave/payroll/accommodation/termination action]
```

severityはverified due date、risk、missing factで判断します。profile alert windowを
法定deadlineとして引用しません。clean casesは1行summaryにします。

10件超ならcounts、timeline、sortable tableのdashboardを提案しますが自動生成しません。

## Automation status

`employment-leave-tracker`のsolution ID/version、`hris-reader`,
`current-law-analyzer`, `leave-state-writer`, `delivery` identity、recurrence、
scope、last successful run、destinationをstateから確認します。

証拠がなければ:

`次回reviewはscheduledではありません。承認済みautomationまたは人による再実行が必要です。`

「毎週」「Monday」「自動alert」と主張しません。

## Update separation

review結果はcandidateです。case calculation/source/statusをupdateする場合:

1. exact leave record、restricted details document、latest `eTag`。
2. proposed patch/source/impact。
3. fresh confirmation。
4. `leave-state-writer`またはgatewayでconditional update。
5. canonical audit。

deliveryは別approvalです。
`returned | closed | cancelled`へのtransitionでは`actualReturn`、`closedAt`,
`closedBy`, `lastCheckedAt`とevidenceを記録し、reopenは別confirmationです。

## 行わないこと

- U.S. leave/certification/reinstatement clockをJapanへ適用
- PTO/benefit/company leaveを法定leaveと混同
- leave/accommodation/termination decision
- HRIS/payroll/insurance write
- scheduleがあると推測
