> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Administrator automation compatibility contract

移行元`registry-sync` agentとpackage lifecycle operationは、本ZIP内のagent、hook、
scheduleではない。別のtenant-governed automationまたはhuman admin runbookとして
実装し、Cowork skillへcatalog/deployment権限を与えない。

## `builder-registry-sync`

- source agent: `legal-builder-hub/agents/registry-sync.md`
- target key: `builder-registry-sync`
- trigger candidate: `weekly-admin-only`
- activation default: `false`

stages:

1. `registry-reader`
2. `quarantine-and-qa`
3. `administrator-approval`
4. `catalog-writer`

sourceの「Applied N updates」はtargetで禁止する。syncはnew/changed candidate、
diff、freshness、review statusのdigestを作るだけで、updateを適用しない。

## Registry reader

許可:

- approved registry metadataのread
- cursorに基づくimmutable revision discovery
- restricted candidate/staging create

禁止:

- unknown registry fetch
- package contentをcatalogへ直接保存
- approval、catalog write、deployment
- raw sourceをnotificationへ貼る

registry ownership、redirect、publisher、revision、rate limit、source authを確認する。

## Quarantine and QA

readerと別identity。snapshot file inventory/hash、deterministic scan、raw review、
13-parameter QA、license/signature/security/privacy/tool-scope/dependencyをrecordする。

`REFUSE`はterminal。`MATERIAL CONCERNS`はremediationまたは正式exception route。
automation自身がfindingをfalse positiveとして閉じない。

## Administrator approval

requester、reviewer、approver、deployment operatorを分離する。approvalはexact
snapshot/package/hash/diff/audienceへ束縛し、expiryを持つ。sourceまたはevidenceが
変われば再承認する。

## Catalog writer

writerはapproved structured recordだけを読み、raw sourceを読まない。catalog write後、
returned item/row ID、version、eTag、before/after hashをauditする。catalog追加は
deploymentではない。

## Package lifecycle runbook

### Install/update/rollback

Coworkはqueue requestまで。human deployment operatorがtenant-validated current
admin surfaceで実行する。official API automationはtenantでsupportとleast privilegeを
検証するまで利用しない。

### Disable/enable

assignment/availabilityと関連flowの停止・再開候補。package、config、audit、
retention対象を保存する。first-party protected assetは拒否する。

### Uninstall

active/disabled両方からdependency、retention、replacement、rollbackを確認した
配布解除。source、audit、decision historyを削除しない。

## Notification

Teams/Outlookまたはapproved delivery flowを優先する。destination、group ID、
external sharing、confidentiality、DLP、artifact hash、approval IDを確認する。

Slack declarationだけでpostしない。delivery未設定またはfailure時はin-session/manual
digestを返し、送信済みと表示しない。

## Manual fallback

automationが未導入、disabled、unhealthy、scope mismatchの場合:

- read-only registry/catalog search
- candidate/review/queue JSONまたはMarkdown draft
- exact admin checklist
- unresolved blocker

を返す。cursor更新、schedule実行、catalog同期、通知送信、tenant operationを
主張しない。

## Audit and no-secret rule

run ID、stage、source item/revision、hash、decision、result、retryをappendする。
raw source、credential、token、client document、private package contentをrun log、
notification、dead-letterへ複製しない。
