> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Approval / deployment handoff

## Packet binding

- operation `install`
- app/package/skill IDs
- source/candidate/snapshot/revision
- file inventory、snapshot/package/diff hash
- license/signature/security/privacy/tool-scope/QA evidence
- dependency snapshot
- target group IDs
- rollback plan
- expiry

## Approval

hash、diff、operation、group、destination、dependencyが変われば失効。requester、
reviewer、approver、deployment operatorを分離する。

## Queue

fresh confirmation後、schema-valid conditional create。approval後は
`admin-action-required`。

## Human admin

tenant-validated current admin surfaceで実操作し、returned operation ID、before/after
version、assignment read-backを登録する。official API/service principal supportが
未検証ならautomationしない。

## Claims

request/approval recordはinstall、AppSource publish、catalog upload、signing、scan、
assignmentの証拠ではない。
