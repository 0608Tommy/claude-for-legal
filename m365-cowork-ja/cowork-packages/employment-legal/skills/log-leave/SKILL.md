---
name: log-leave
description: >
  日本のleave caseをpseudonymous restricted matterへ最小限登録するSharePoint / Power Platform front end。job protection、employer procedure、insurance benefit、annual-leave accounting、health accommodationを分け、current-law source確認後にconditional createする。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: employment-legal
  migration-target: power-platform
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Log leave

旧来のlabel:
`/employment-legal:log-leave [describe the leave]`。

## Mandatory create / privacy / law gate

1. `references/common/cowork-runtime-contract.md`を読み、gateway、user、practice、
   restricted matter ACLをlive preflight。失敗時はintake draftだけで登録済みと
   表示しません。
2. leave/medical/accommodationはgeneral workspaceがoffでもrestricted matterです。
   identity mapping、medical detail、central pseudonymous indexを分けます。
3. exact leave type、establishment/prefecture、actual schedule、current sourceを確認。
4. job protection、employer procedure、insurance benefit、annual leave、
   health accommodationを別track。
5. new caseはfull canonical key、`recordId: leave:[leaveId]`,
   `expectedAbsent: true`、unique`idempotencyKey`でcreate。updateと混ぜません。
6. AIはeligibility/approval/denial、medical sufficiency、payroll/benefit、
   accommodation、return、terminationを決めません。
7. automation/scheduleは`references/automation-contract.md`のproofがある場合だけ。
8. Cowork内DLP必須ならsensitive dataを投入せずproduction停止です。

schema: `references/leave-records.md`。

## 会話state

`intake-minimize` → `classify-tracks` → `research-current-law` →
`show-record-candidate` → `confirm-create` → `conditional-create` →
`audit` → `show-next-review-status`

## Single-block intake

- employee pseudonym（氏名不要）
- entity/establishment/prefecture
- leave/measure type
- requested start/end、intermittent
- actual normal schedule
- child DOB/ageまたはcovered family category（必要な場合だけ）
- eligibility/exclusion agreement facts
- employer notice/confirmation/hearing/accommodation status
- insurance benefit owner/status
- expected return/work restriction（known only）
- authorized viewers、retention/legal hold

diagnosis、detailed medical history、family narrativeを求めません。

## Classify

current Japanese sourceに基づき:

- maternity
- childcare / post-birth childcare
- child-care leave days
- family-care leave / family-care leave days
- overtime/night restriction、short hours/flexible measures
- annual paid leave
- occupational injury
- disability/health accommodation
- company leave

を分類します。employer-paid leaveとinsurance benefitを混同しません。

## First decision point

source/effective date、clock owner、calculation inputs、missing factsからcandidateを
示します。移行元の固定5 business days、15 days、75% exhaustion等をJapanへ
適用しません。internal alert windowも未設定なら設定を求めます。

## Create

record candidate、source、restricted destination、viewer、retention、automation
statusを示し、fresh confirmation後にconditional createします。duplicate/timeoutでは
recreateせずsame key/idempotencyを照合します。

completion:

```text
Registered: [leaveId / pseudonym / type / establishment]
First decision point: [candidate or unknown]
Automation: [verified scheduled status | not scheduled]
Open review: [law/fact/human decision]
```

schedule proofがなければ自動alertを約束しません。

## 行わないこと

- local leave registerを作成
- employee name/diagnosisをrecord ID/auditへ入れる
- U.S. form/deadlineを使用
- leave/benefit/accommodationをapprove/deny
- HRIS/payrollへwrite
