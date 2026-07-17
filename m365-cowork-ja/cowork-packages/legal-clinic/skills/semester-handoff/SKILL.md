---
name: semester-handoff
description: >
  学期末のactive clinic matterをoutgoingからincoming studentへ引き継ぐSharePoint / Power Platform front end。incoming conflict clearance前のidentity/file accessを禁止し、responsible lawyerと両studentがdeadline、scope、safe contact、language、capacity、originals、open issuesを確認する。departing accessをrevokeし、semester endでmatter close/archive/deleteしない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: legal-clinic
  migration-target: power-platform
  logical-target-id: ja-jp.power.legal-clinic.semester-handoff
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Semester handoff

canonical label:
`/legal-clinic:semester-handoff [--semester=term] [--case=matter-id]`

## Mandatory conflict / deadline / access gate

1. `references/common/cowork-runtime-contract.md`と
   `references/common/power-platform-automation-contracts.md`、
   `references/common/clinic-state-payloads.schema.json`を読む。
2. exact current user、responsible lawyer、supervisor、term、active matter、
   outgoing assignment、authorized ACLを確認する。
3. incoming studentはconflict pre-screen/clearance前にclient identity、safe contact、
   document、substantive handoffを読まない。
4. incoming conflict statusは`pending | clear | restricted | blocked`。AIがclearしない。
5. outgoing、incoming、responsible lawyer、docket ownerが全open deadlineのtrigger、
   service、source、candidate/verified status、ownerを再確認する。
6. identity、safe contact、health/capacity、immigration、criminal、child/family/DV、
   interpreter dataはrestricted referencesだけを渡す。
7. gateway、matters/state/audit、conditional write、ACL grant/revoke、retention/preservation、
   storage/flow DLPをlive preflight。失敗時はmanual handoff draftだけ。
8. handoff draft、lawyer review、incoming access grant、departing access revoke、
   client notice、matter closeは別operation。
9. semester endをclose/archive/delete triggerにしない。
10. Cowork内DLPが必須ならconfidential contentを投入しない。
11. handoff writeは`tracker-record` + `payload.trackerType: handoff`へvalidateし、outer
    `scopeType: matter`、`scopeId == payload.matterId`、duplicated tenant/practice
    identityの一致をsemantic validateする。

## 会話state

`scope` → `conflict-check` → `source-read` → `deadline-reconcile` →
`handoff-draft` → `lawyer-review` → `access-plan` → `confirm-write` →
`conditional-write` → `audit`

portfolio modeはexplicit supervisor authorityとpseudonymous minimum indexを要求する。

## Source read

- exact matter profile、engagement/scope、responsible lawyer
- verified/candidate deadlines
- communication summary with source entry IDs
- filed/reviewed/draft artifact pointers
- safe contact/language/accessibility restricted references
- capacity/representative authority status
- original documents/property inventory
- legal aid/program status
- open incidents/complaints、internal preservation controls、court orders、retention
- outgoing student notesとcoverage

source unavailable又はpartialなら未読範囲を表示し、complete handoffとしない。

## Per-matter handoff

`internal-memo` artifactとして:

1. matter pseudonymous code、forum、scope、responsible lawyer
2. current postureとverified events
3. deadline table:
   candidate/verified、source、owner、first action
4. work completed、artifact item/version/status
5. open factual/legal/strategic questions
6. communication summary、safe-contact restricted pointer
7. language/interpreter/accessibility
8. capacity/representative status
9. originals、property、filing/service evidence
10. legal aid/program and client notice status
11. preservation/retention/DLP
12. first-week priorities

accepted risk、credibility、internal legal analysisをclient noticeへ流用しない。

## Deadline reconciliation

unknown又はunverified dateはurgent calculation task。calendar factにしない。semester start
近辺のcandidateをpriority表示するが、extension又はresponseを保証しない。責任弁護士と
docket ownerの双方が確認してもcalendar writeは別operation。

## Access plan

1. incoming conflict `clear/restricted` evidence。
2. responsible lawyer assignment approval。
3. exact Entra group/object IDとleast-privilege ACL。
4. fresh sessionでnew matter binding。
5. departing studentの対象matter bindingをexact queryし、access、shared links、
   exports/local copiesのrevoke plan。
6. each operationのfresh confirmation、result、audit。

same-sessionでoutgoingからincomingへbindingを移さない。

## Matter closure

closed candidateがある場合も本skillはcloseしない。責任弁護士がclient notice、final
deadline、originals、fees/legal aid、appeal/execution、retention/destruction、
preservation control/court orderを別close processで確認する。全binding revoke失敗時は
closeをblockする。

archive/close processは最初のatomic conditional operationでmatterを
`archive-pending`又は`close-pending`へfenceし、binding generationを増やす。
fence成功後に全bindingをenumerateし、activeだけをrevocation対象としてrevokeする。
already-revokedはsatisfiedとして再更新せず、zero active確認後だけ`archived`又は
`closed`へconditional finalizeする。fence前にcommitしたcreateはenumerationで
捕捉され、fence後のcreateはexact
matter precondition/generationで失敗する。途中失敗はfenced stateを維持して
fail closed。reactivateはgenerationを増やし、incoming/outgoingを含む旧bindingを
再利用せず、fresh conversation/bindingを要求する。

## Cohort summary

pseudonymous IDs、outgoing/incoming status、practice area、deadline urgency、assignment
gapだけを表示する。restricted matterの存在又はidentityをunauthorized viewerへ出さない。
10件超ならdashboardを提案するが自動生成しない。

## Automation status

solution/flow ID、version、owner、connection、scope、last run、access-controller proofを
確認できる場合だけautomatedと表示する。packageはflowを含まない。

## 行わないこと

- incoming conflict clearance又はassignment決定
- semester endでmatter close/archive/delete
- unverified deadlineを確定日としてhandoff
- client noticeのsend
- same-session matter/user switch
- departing access revoke又はincoming grantを未検証で主張
- Power Platform solutionのprovision claim
