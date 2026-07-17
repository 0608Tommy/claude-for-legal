---
name: investigation-open
description: >
  internal investigationを日本法に合わせてclassifyし、一般workspaceがoffでもrestricted matter、whistleblower identity分離、APPI、interview notice、source checklist、five-mode stateをcanonical SharePoint recordsとして開く。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: employment-legal
  migration-target: power-platform
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Investigation — open

旧来のlabel:
`/employment-legal:investigation-open [brief allegation]`。

hidden `internal-investigation`は登録せず、本callerの
`references/investigation-framework.md`へcompileしています。本skillはMode 1だけを
実行します。

## Mandatory formation / restricted / current-law gate

1. `references/common/cowork-runtime-contract.md`を読み、gateway、restricted
   SharePoint matter/state/audit、item-level ACLをlive preflight。失敗時はsensitive
   factsを保存せずintake/checklist draftだけです。
2. investigationはgeneral workspace設定にかかわらずrestricted matterを要求します。
3. counsel/investigatorのclient、purpose、legal/business mixed purposeを確認し、
   labelだけで日本のprivilegeが成立すると表示しません。
4. complaintをharassment、whistleblowing、discrimination、safety、financial、
   executive、ordinary conductへclassifyし、overlapを許します。
5. whistleblower identityはappointed handler限定のseparate item/ACLです。
6. APPI、sensitive data、vendor/foreign transfer、retention/legal holdをcollection前に
   確認します。
7. 2026-12-01前はwhistleblower amendmentをfuture readinessとします。
8. union/CBA/public-sector lawが関係する場合、日本のcurrent ruleを調査します。
9. AIはinterview、interim measure、substantiation、discipline、terminationを決定・
   実行しません。
10. Cowork内DLP必須ならmatter contentを投入せずproduction停止です。

Japan:
`references/common/ja-jp/termination-investigations.md`。

## 会話state

`intake` → `classify` → `formation-review` → `restricted-matter-candidate` →
`source-checklist` → `confirm-create` → `conditional-create` → `audit`

## Intake

frameworkのsingle-block intakeを使い、allegation/parties/timeframe、counsel purpose、
whistleblower、union/CBA、immediate safety/retaliation/preservation、viewer、
recording、retention、evidentiary standardを確認します。

interview noticeはinvestigator role、counselのclient、purpose、cooperation、
confidentiality limits、data uses、non-retaliation、recording statusです。foreign
warning/right/immunityを自動適用しません。

## Create separation

1. restricted matter profileを`matter-workspace` protocolで別create。
2. new session bindingは別switch/new-session operation。
3. investigation case/checklistを
   `references/investigation-records.md`でseparate creates。
4. identity mapping/whistleblower itemはseparate ACL。

1つのconfirmationを全operationへ拡張しません。

## Completion

matter/case/checklist IDs、source gaps、formation caveat、future-law status、
authorized viewersを示します。evidence追加やinterviewを自動開始しません。
