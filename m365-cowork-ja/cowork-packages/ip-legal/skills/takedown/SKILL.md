---
name: takedown
description: >
  online copyright等のtakedownを`--send`、`--respond`、`--counter`の会話stateで扱う。日本modeは著作権法・Platform Act・provider procedureとしてDMCAと分離し、U.S. modeだけで§512のfair-use、perjury、counter-notice、jurisdiction gateを使う。draftのみで自動submissionしない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: ip-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Takedown

正規label/flags:

- `/ip-legal:takedown --send`
- `/ip-legal:takedown --respond`
- `/ip-legal:takedown --counter`

flagなしならmodeを1回確認します。最初にjurisdiction/provider routeを決めます。

## Mandatory jurisdiction / submission gate

1. [保存契約](references/common/cowork-runtime-contract.md)を読み、gateway、
   user/practice/matter scope、destination、auditをpreflight。
2. exact right、owner/exclusive authority、work、material、URL、platform、
   territorial nexusを確認。
3. matter scopeならactive/unexpired binding。practice modeはfresh session。
4. `request > matter > practice-profile > tenant-default`でroute。
5. 日本なら[著作権・Platform Act](references/common/ja-jp/copyright-platform.md)。
   U.S. DMCAは[original layer](references/common/original-ip-logic.md)の別route。
6. licence、permission、statutory exception/fair use、misidentificationを確認。
7. outgoing notice/counter/appealとinternal analysisを別artifactにします。
8. AIはprovider webform、designated agent、court、authorityへsubmit/sendしません。
9. approver、signer、perjury/jurisdiction statement、destinationを人が確認。
10. Cowork内DLP必須なら機密materialを投入せずproduction停止。

## Conversation state

| state | action |
|---|---|
| `select-route` | Japan provider route / U.S. DMCA / other local regime |
| `send` | rights-holder notice draft |
| `respond` | incoming notice/platform action triage |
| `counter` | U.S. §512(g)(3) counter draft、または日本ではappeal optionsへroute |
| `ownership` | ownership/authority/licence |
| `material` | exact URL/content/evidence |
| `exception` | Japanese statutory exceptionまたはU.S. fair use |
| `draft` | external draft + internal memo |
| `gate` | source、authority、legal basis、signer、destination |

## Japan `send`

1. authorship/ownership/exclusive authority。
2. protected expression、exact material、URL/location、platform。
3. licence、permission、Japanese statutory exception。
4. providerのcurrent published infringement route。
5. work/right/material/URL/reason/evidence/contactをdraft。
6. Platform Act Art. 3とdesignated-large-provider dutyのapplicabilityを分ける。

§512(c)(3) perjury language、U.S. statutory cite、DMCA designated-agent formatを
日本routeへ挿入しません。

## Japan provider layer

- technical ability、knowledge/reasonable groundsとliability limitation
- reasonable belief/deletion safe harbor
- sender inquiry後7-day no-objection route
- designated large provider Arts. 22–28
- Art. 25 statutory maximum 14 daysとcurrent ministerial 7-day period
- complaint method、investigation、specialist、standard、result/reason
- sender identification request/orderは別procedure

designated status、period、provider formをcurrent official sourceで確認します。
automatic deletionまたはmandatory restorationを約束しません。

## Japan `respond` / `counter`

incoming itemから:

- claimant、provider、work/right、target URL
- action date、reason、provider terms
- ownership/licence/exception
- notice defect/evidence gap
- business/account impact

Japanにはstatutory §512(g) counter-notice、federal-jurisdiction consent、
10–14-business-day restoration clockがありません。`--counter`と依頼された場合:

- platform appeal draft
- licence/evidence submission draft
- direct engagement draft
- provisional relief/counsel route
- sender-information procedure
- preserve/no-action

からoptionsを示します。「Japanese counter-notice」と偽りません。

## U.S. DMCA route

U.S. nexus/service providerを確認した場合だけ:

### `--send`

- §512(c)(3) elements
- ownership/exclusive authority
- specific URLs
- good-faith belief
- accuracy/authority under penalty of perjury
- *Lenz* fair-use consideration
- §512(f) risk

fair useがdebatable/likelyならattorney reviewまでdraftを停止。

### `--respond`

- notice facial compliance
- licence/fair use/misidentification
- host §512(g) handling
- options: comply / counter / engage / no-action

### `--counter`

- content was removed under §512
- good-faith mistake/misidentification
- signature、material/location
- name/address/phone
- federal district jurisdiction consent and service acceptance
- 10–14 business-day litigation/restoration mechanics

perjury/jurisdictionを「formality」と扱いません。

## Current Japan developments

- Copyright Act Art. 67-3は2026-04-01施行。official ruling/compensation routeであり
  self-help defenseではない。
- 2026 Copyright Amendment Act No. 48は2026-06-24公布、未施行。[F]として扱う。

## Output

internal:

- reviewer note、route、source、ownership、exception/fair use、risk、approver
- incoming triage/options

external:

- provider-specific content draft
- internal strategy/privilege noteなし
- `DRAFT — HUMAN/COUNSEL REVIEW REQUIRED — NOT SUBMITTED`

submission record、confirmation ID、watch dateをAIが自動作成済みと表示しません。
actual submission後にauthorized human-provided evidenceを別updateできます。

## Loud gate

> **このdraftは未提出です。**
> ownership/authority、material、licence/exception、legal route、accuracy、
> signer、perjury/jurisdiction statement（該当時）、approver、provider destinationを
> 人が確認するまでsubmitしないでください。

## 行わないこと

- notice、appeal、counter-noticeをsubmit/send
- JapanにDMCA counter mechanismがあると表示
- fair use/exceptionを最終判断
- providerが削除・復元すると保証
- unverified form、period、designated statusを使用
- local filesystem、agent、hook、subagentを使う
