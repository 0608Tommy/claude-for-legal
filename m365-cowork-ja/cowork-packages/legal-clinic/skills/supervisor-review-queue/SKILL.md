---
name: supervisor-review-queue
description: >
  student workをpending、approved、edited-approved、returned、supersededで管理するSharePoint / Power Platform front end。software queueは選択可能でもsubstantive responsible-lawyer reviewは必須とし、authenticated reviewer、artifact item/version/hash、source/effective date、decision、edits、destination、release actorを記録する。auto-approval又はstudent releaseを許さない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: legal-clinic
  migration-target: power-platform
  logical-target-id: ja-jp.power.legal-clinic.supervisor-review-queue
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Supervisor review queue

canonical label:
`/legal-clinic:supervisor-review-queue [--approve ID | --return ID note | --edit ID]`

## Mandatory reviewer / version / release gate

1. `references/common/cowork-runtime-contract.md`と
   `references/common/power-platform-automation-contracts.md`、
   `references/common/clinic-state-payloads.schema.json`を読む。
2. scopeを`matter-mode | portfolio-mode`で先に確定する。
3. `matter-mode`はexact current user、responsible lawyer/supervisor role、**1件だけ**の
   active non-null expiring matter binding、artifact ACLを要求する。studentは
   submit/read-own/return-responseだけで、approve/releaseしない。
4. `portfolio-mode`はfresh unbound session、explicit portfolio authority、
   pseudonymous minimum metadataだけ。active binding又はclient identityがあれば停止。
   itemを開く場合はcurrent conversationを終了し、新しいbound conversationを要求する。
5. software workflow preferenceがformal queueでなくても、legal advice、accept/decline、
   conflict waiver、deadline、settlement、court/agency document、substantive client
   status、capacity/guardian、case closeのresponsible-lawyer reviewは必須。
6. gateway、state/outputs/audit、conditional write、retention/preservation、DLPをlive
   preflight。失敗時はread-only review list/manual review packageだけ。
7. review対象はexact artifact item ID、version、hash。latestというdisplay labelだけで
   approveしない。
8. reviewerのcurrent Japanese lawyer registration/authority、source/effective dates、
   destinationを確認する。status clickだけをsubstantive reviewの証明にしない。
9. consequential translationはresponsible-lawyer legal reviewとcompetent-language
   reviewの両方を同じartifact version/hashに要求する。
10. approve、edit、return、artifact promotion、send/file/releaseは別operation。
11. auto-approval、batch blanket approval、student impersonationを禁止する。
12. Cowork内DLPが必須ならconfidential artifactを投入しない。

## Queue availability

`formal-queue | configurable-flags | existing-structure`はsoftware preference。
formal queueがoffならpending workを既存supervision routeへdraft packageとして渡すが、
「review不要」と表示しない。

## Scope modes

### `matter-mode`

one active bindingのexact matterだけでlist/review/decisionを行う。writeは
`recordType: tracker-record`, `payload.trackerType: review`のstrict payload。outer
`scopeId == payload.matterId`とduplicated tenant/practice identityをsemantic validate。

### `portfolio-mode`

fresh unbound sessionでread-only listだけ。表示可能field:

- pseudonymous matter ID
- artifact type、priority、status
- submitted time、waiting time、deadline candidate/verified indicator

artifact content、source evidence、decision notes、client identity、safe-contactを
表示しない。itemを開く、edit、approve、returnする場合はnew bound conversation。

## Priority

1. verified or candidate legal deadline proximity
2. urgent safety/custody/adverse action
3. court/agency filing
4. substantive client communication
5. conflict/scope/capacity
6. standard internal work

waiting timeだけでpriorityを決めない。candidate deadlineを確定日と表示しない。

## Review record

machine正本はschemaの`reviewPayload`。source item IDs、versions、effective datesは
`sourceEvidence[]`、理由は`decisionNotes`に記録する。artifact item/version/hash、
destination、reviewer role、status、approval、release actor、legal/language reviewを
必須化し、undeclared fieldを拒否する。

`reviewSubjectTypes`でrouteする。

- legal proposition、deadline、engagement、conflict、scope、external legal content:
  `responsible-lawyer`
- pedagogy又はpure adminだけ: `supervisor`
- legalとpedagogy/adminのmixed artifact: `both`
- consequential translation: 上記に加えてcompetent language reviewer

supervisor titleだけでlegal reviewを満たさず、responsible-lawyer roleとauthorityを
別fieldで確認する。

## Modes

### List

authorized itemsだけをdeadline/safety priority、artifact type、student、waiting timeで表示。
restricted matter existenceをunauthorized viewerへ漏らさない。10件超ならdashboardを
提案するが自動生成しない。

### Review

clean artifact、separate reviewer note、source coverage、deadline status、conflict/
engagement/scope、destination、prior version/diffを示す。

### Approve

responsible lawyerがexact version/hash、sources、destinationを確認し、fresh approval。
approvalはartifact promotion permission候補であり、send/file/accept/close permissionへ
拡張しない。

translationがconsequentialなら、legal reviewとlanguage reviewのいずれかがpending/
blockedのartifactをapprove又はpromoteしない。

### Edit then approve

edited contentをnew artifact versionとして保存し、new hashへseparate approvalする。
originalをoverwriteせずdiffを残す。

### Return

specific issue、required source/fact、deadline impactを記録し、studentへrevision
candidateを返す。返却はexternal deliveryでない。

## Release

`artifact-promoter`がapproval IDとexact hashを照合してSharePoint `outputs`へpromote
できるが、本packageはflowを含まない。client send、court/agency file、case acceptance、
deadline calendar、case closeは別authorized human operation。

## Audit / teaching signal

各decision、edit、failure、promotionをappend-only auditへ記録する。pattern analysisは
coaching candidateであり、student competence又はdisciplineをAIが決定しない。

## 行わないこと

- automatic/batch blanket approval
- student approve/release
- different version/hashへのapproval reuse
- source/effective date未確認のsubstantive approvalをcleanと表示
- approvalをsend/file/accept/decline/settle/closeへ拡張
- flow、notification、promotionが実行済みと未検証で主張
