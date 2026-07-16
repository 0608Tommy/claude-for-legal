> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本向けtenant governance review — DRAFT

本checklistは日本法の結論ではなく、qualified reviewerへ渡すadmin workflow用の
論点整理である。法的character、適用法、業法、契約、労務、規制当局guidanceは
tenantと利用形態ごとに確認する。

## Review owners

| Area | Human owner候補 | Required evidence |
|---|---|---|
| tenant/app administration | Microsoft 365 tenant admin | current supported deployment method、group scope |
| security | CISO/Security | scan、identity、logging、incident、least privilege |
| privacy/data governance | Privacy/DPO | data map、purpose、retention、transfer、processor/vendor |
| license/IP | Legal/Open Source review | SPDX、LICENSE/NOTICE、distribution context |
| legal service/workflow | Japanese qualified counsel | role、supervision、confidentiality、substantive law boundary |
| records/retention | Records/Compliance | retention、legal hold、audit immutability |
| procurement/vendor | Procurement/Legal | vendor terms、entitlement、support、exit |

## Tenant governance questions

- 誰がrequester、reviewer、approver、deployment operator、auditorか
- self-approvalと同一credential兼任を防げるか
- packageをどのtenant/group/userへ配布するか
- first-party protected assetとcommunity/vendor packageを区別できるか
- rollback、disable、uninstallのownerと復旧時間は何か
- package、source、approval、deployment evidenceを何年保持するか
- incident時にassignment、connector、flowをどう停止するか
- tenant外共有、guest、external collaborationをどう制御するか

## Privacy/security review

- raw packageに個人情報、client data、credential、telemetry endpointがないか
- external connector/operatorへ送るfieldとdestination
- data minimization、purpose、retention、deletion/holdの両立
- access log、review log、admin evidenceに不要な本文を複製しないか
- cross-border processing、subprocessor、data residencyを契約・設定で確認したか
- employee/user monitoringまたは利用logのnotice・internal policyが必要か
- incident response、credential rotation、publisher compromise手順があるか
- Cowork prompt/task内DLPが必要なworkloadをblockしているか

## Legal/license review

- source/publisherの権利とpackageのlicenseは一致するか
- Apache-2.0等のNOTICE、変更表示、再配布条件を満たすか
- proprietary、custom、copyleft、no-licenseをdeployment contextでreviewしたか
- trademark/vendor名をapprovalなくendorsementとして使っていないか
- community skillが法的助言、資格、privilege、security approvalを過剰claimしないか
- 日本以外の法律・procedureを日本の同義語として適用していないか
- substantive legal contentはcurrent primary sourceとqualified reviewerを持つか

## CoCounsel blocker

Thomson Reutersの書面承認がない限り、CoCounselのブランド、翻訳派生物、connector、
tenant配布、generic fallback under same IDを承認しない。statusは
`blocked-vendor-approval`。

## Draft output

```markdown
## 日本向けtenant governance review — DRAFT

- Scope/tenant/group: [...]
- Admin method: [verified / unverified]
- Security/privacy: [...]
- License/vendor: [...]
- Records/DLP: [...]
- Qualified Japanese review: [pending / reviewer/evidence]
- Blocking items: [...]
- Decision requested from: [...]
```

AIは法的承認、security clearance、privacy approval、tenant deployment decisionを
行わない。reviewer名、evidence、dateがなければapprovedと表示しない。
