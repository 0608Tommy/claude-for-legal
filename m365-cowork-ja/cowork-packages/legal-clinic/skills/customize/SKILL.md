---
name: customize
description: >
  approved clinic profile又はpractice guideを1変更ずつ安全に更新するadmin skill。current value、proposed diff、downstream impact、authorityを示し、exact item ID・ETag・version・idempotencyとfresh confirmationでconditional updateする。studentはprivacy、retention、conflict、lawyer review、student participation等のload-bearing controlを弱められない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: legal-clinic
  migration-target: admin
  logical-target-id: ja-jp.admin.legal-clinic.customize
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Customize

canonical label: `/legal-clinic:customize [section or change]`

## Mandatory authority / one-change gate

1. `references/common/cowork-runtime-contract.md`、
   `references/common/clinic-state-payloads.schema.json`を読み、exact current user、
   canonical nested profile/guide、gateway、profiles/auditをlive preflightする。
2. profile未設定、legal review blocked、複数record、scope conflictではcold-startへroute。
3. 1runで1logical change。related fieldsはatomic patchとして示す。
4. clinic name、semester、pedagogy等はsupervisorが変更できる。responsible lawyer identity、
   student participation、conflict、engagement/scope、substantive review、privacy/DLP、
   retention/preservation、emergency、external operationはresponsible lawyer approval必須。
5. studentはproposalだけ。guardrail degradationをapproveしない。
6. current official source又はfuture-lawに影響する変更はsource/effective dateを再確認。
7. exact item ID、latest ETag/version、unique idempotency、diff、impact、fresh confirmationで
   conditional updateし、auditへappendする。
8. stale/partial/timeoutでは上書きせず再読取りする。

## Customizable map

- clinic / host / practice area
- jurisdiction / forum / official source
- responsible lawyer / supervisor
- student participation matrix
- conflict / engagement / scope process
- supervision workflow preference
- pedagogy and practice guide
- data / safe contact / ACL / APPI regime / retention / preservation / DLP
- source cards / Houterasu program roles / translation reviewers
- legal review:
  `pending | in-review | approved | blocked`
- semester / access review / handoff
- integration status reference

## Guardrail degradation

次の削除又は緩和は拒否し、必要ならcold-start legal reviewへ戻す。

- conflict-first pre-screen
- responsible lawyer gate
- no attorney-client relationship/representation claim
- disclaimer is not determinative of actual engagement/scope
- information barrier is not conflict clearance/waiver
- student matrix is internal policy, not authority/Article 72 cure
- active non-null expiring matter binding
- fresh-session matter switch
- restricted sensitive-data ACL
- deadline candidate dual verification
- current/future source separation
- external artifact version-specific review
- destination/DLP/retention/preservation check
- no auto send/post/file/accept/decline/close

`formal-queue | configurable-flags | existing-structure`の変更はsoftware preferenceだけ。
substantive lawyer reviewを無効化しない。

profile write pathは
`payload.clinic | authority | conflicts | engagement | studentParticipation |
supervision | pedagogy | data | urgentRouting | sourceCards | houterasuPrograms |
semester | integrations | legalReview | activationApprovalIds`
だけ。flat alias又は別名fieldへwriteしない。`profileStatus: active`はJapan counselと
clinic supervisorが双方`approved`の場合だけ。

## Update sequence

1. exact current value、source、item ID/eTag/version。
2. proposed patch、reason、downstream skills/artifactsへの影響。
3. inconsistency、data migration、access、retention、future-law impact。
4. required approver。
5. fresh confirmation。
6. canonical schema validation。
7. conditional update。
8. returned item ID/eTag/version。
9. append-only audit。

practice areaのarchiveはpast matter/historyをdeleteしない。semester rolloverはactive
matterをcloseせず、handoff/access-review candidateを作る。integration statusはlive probe
なしに`connected`へ変更しない。

matter archive/close/reactivateを依頼された場合はprofile customizationとして処理しない。
archive/closeはgatewayの`binding-revocation-batch`へrouteし、matterを先に
pending statusへfenceする。active bindingだけをrevokeし、already-revokedは
satisfiedとして扱い、zero active後だけfinalizeする。failure時はfenced stateを
維持する。reactivateは別transitionでbinding generationを増やし、
`reactivation-pending`中はaccessを拒否し、新しいconversationでfresh bindingを要求する。

## Completion

changed field、old/new value、approver、exact version、downstream effect、unresolved
reviewを表示する。next outputが変更を使うのはapproved write成功後だけ。

## 行わないこと

- full interviewのsilent再実行
- studentによるlegal/security control変更
- approved historyのdelete/overwrite
- semester rolloverでmatter close/archive
- setup/interview completionをlegal approvalと表示
- connector/flowを未検証でavailableと表示
- external send、file、access grant、retention destructionの実行
