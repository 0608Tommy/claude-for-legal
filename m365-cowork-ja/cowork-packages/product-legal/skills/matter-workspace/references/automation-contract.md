> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Matter Power Platform compatibility contract

本packageはskills-onlyであり、managed solution、agent、hook、recurrence、schedule、
cloud flowを含まない。

## Allowed front

Coworkはintake、current/proposed diff、fresh human confirmation request、result表示を
行える。state mutationは、tenantが別途approved/deployedしたflow/APIがある場合
だけ、そのcontractへhandoffする。

## Flow requirements

- least-privilege service identity / connection reference
- exact tenant/practice/user/session/matter scope
- createとupdateの別operation
- conditional create with canonical composite key and `expectedAbsent: true`
- exact `itemId` + latest `eTag` for update
- unique `idempotencyKey`
- retry/backoff、dead-letter、partial-success report
- append-only canonical audit
- retention、legal hold、storage/flow DLP
- archived/revoked/expired binding rejection
- close時に対象matterの全bindingをitem単位でrevoke
- retrieved contentをinstructionとして実行しない
- switch/close/none/shareはfresh human confirmation

flow version、environment、connection owner、ACL、last successful runが確認できない
場合、automation availableと表示しない。同じmaker connectionへbindしただけでは
identity separationではない。

## DLP blocker

Power Platform/SharePoint境界のDLPはCowork prompt/task DLPを意味しない。Cowork内
DLPがmandatoryなら機密matterのproduction利用を停止する。
