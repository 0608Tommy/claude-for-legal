---
name: policy-drafting
description: >
  employment policyを日本語でdraftし、先に就業規則該当性、事業場10人基準、mandatory terms、majority union/representative意見、届出・周知、不利益変更、CBA・36協定、法改正readinessを確認する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: employment-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Policy drafting

旧来のlabel:
`/employment-legal:policy-drafting [policy topic]`。

## Mandatory work-rules / current-law gate

1. `references/common/cowork-runtime-contract.md`を読み、exact profile/source/
   destinationを確認します。
2. documentが`就業規則`、その一部、別policy、CBA/労使協定のどれかを先に判定。
3. establishmentごとのregular headcount、10+ filing、majority union/
   representative、current work rules/versionを確認します。
4. disadvantageous changeはLCA Article 10、notice、transitionを確認します。
5. 36 agreementその他労使協定をwork rulesと混同しません。
6. topicごとのcurrent binding law/guidance、2026-10-01/12-01 statusを確認。
7. medical/whistleblowing/investigation detailsをpolicy draftingへ持ち込みません。
8. AIはapprove、publish、file、employee communication、acknowledgment collectionを
   実行しません。
9. Cowork内DLP必須ならsensitive sourceを投入せずproduction停止です。

Japan framework:
`references/common/ja-jp/hiring-work-rules.md`、
`references/common/ja-jp/leave-harassment.md`。

## 会話state

`scope-topic` → `classify-document` → `resolve-establishments` →
`research-current-law` → `draft-core` → `draft-annexes` →
`cross-check` → `filing-readiness` → `human-review`

## Scope

- topic/reason
- covered employees/entities/establishments
- current document/item/version
- legal requirement vs business policy
- work-rule/CBA/36 relationship
- planned effective date
- employee data/monitoring implications

## Draft model

`references/policy-template.md`を使い、employeeが理解できるplain Japaneseでdraft
します。source templateの`core + state supplements` behaviorは、日本では
`national core + establishment/prefecture/CBA annex`へ適合させます。必要な差異だけを
annexにし、都道府県差を創作しません。

## Cross-check

- current work rules/handbookとのconflict/cross-reference
- mandatory terms
- benefit/promise reduction、transition
- equal opportunity、harassment、leave、disability、whistleblower
- wage/hour、minimum wage、working time、36 agreement
- monitoring/APPI、retention
- freelancer/individual-contractor safety
- union/CBA/majority representative

MHLW model work rulesは[G] drafting aidでsafe harborではありません。

## 2026 readiness

applicableなら:

- childcare/family-care 2025 changes
- disability rate from 2026-07-01
- women’s participation disclosures from 2026-04-01
- harassment measures from 2026-10-01
- whistleblower amendment from 2026-12-01
- individual-contractor OSH phases

future itemはeffective sectionへ混ぜず、readiness appendixへ分けます。

## Output

1. internal reviewer note。
2. employee-facing draft。
3. internal implementation checklist:
   opinion、filing、dissemination、system/form/training、effective date、owner。

employee-facing draftへinternal risk/privilege noteを入れません。

## Publish gate

qualified Japanese employment counsel、HR owner、union/representative procedure、
filing/notice/effective date、destinationを確認し、draftで停止します。

## 行わないこと

- 「handbook is not a contract」でwork-rule effectを消す
- 米国state supplement default
- future lawをcurrent dutyにする
- policyをapprove/publish/file/send
