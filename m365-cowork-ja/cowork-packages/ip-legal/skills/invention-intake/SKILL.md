---
name: invention-intake
description: >
  発明開示をnovelty signal、inventive-step flag、日本のsoftware/AI eligibility、Article 30 disclosure、従業者発明、inventorship、detectability、strategic value、意匠・営業秘密routeでscreenする。patentability opinionやclaim draftingは行わない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: ip-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Invention intake

旧来の参照label:
`/ip-legal:invention-intake [paste or describe the invention disclosure]`。

canonical result enum:
`PURSUE | INVESTIGATE | DECLINE`

## Loudest guardrail

> **これはnon-specialist first-pass screenでありpatentability opinionではありません。**
> prior-art search、claim strategy、filing decisionは日本の弁理士・弁護士が行います。
> 本skillは「patentable」と結論しません。

## Mandatory invention-security gate

1. [保存契約](references/common/cowork-runtime-contract.md)を読み、gateway、restricted
   ACL、matter、destination、DLPをpreflight。失敗時はread-only intake draft。
2. practice mix、patent strategy、technology area、budget posture、approver、
   prosecution counselを読みます。patent practiceがscope外ならroute。
3. matter scopeならactive/unexpired binding。unpublished inventionは
   `heightened | restricted | clean-team`を検討。
4. external search/tool/foreign partyへtechnical contentを送る前に
   [patent non-disclosure P0](references/common/ja-jp/patents-utility-designs.md)。
5. request/matter/practice/tenantでjurisdictionを解決。
6. inventor、employer/contractor、disclosure/filing chronologyをsource付きで確認。
7. AIはprior-art searchを正式searchと表示せず、claim、application、filingを作成・
   提出しません。

## Intake

- what is the invention / key mechanism
- problem solved
- difference from prior approach
- human contributors and contribution
- conception/reduction dates
- disclosure、sale/offer、demo、paper、repo、customer communication
- NDA/confidentiality
- use/roadmap
- technology area
- employee/contractor status、agreement/work rule
- intended jurisdictions
- AI tool contribution

half disclosureでは進まず、missing questionをまとめて示します。

## Screen 1 — novelty signals

- known technique in new field
- competitor already uses similar mechanism
- new mechanism/combination/unexpected result
- prior solution failure

これはPatent Act Art. 29/29-2のformal novelty searchではありません。

## Screen 2 — inventive-step flags

- predictable combination/routine optimization/design choice/obvious-to-try
- teaching away/unexpected result/long-felt need
- person skilled in the art、problem、motivation、effectを明示

formal conclusionを出さず`clear signal | investigate | red flag`。

## Screen 3 — eligibility

Patent Act Art. 2/29とJPO software/AI guidanceを使い、発明全体が自然法則を利用した
技術的思想の創作か、specific information processing/hardware cooperationかを確認。

`Alice/Mayo`、abstract-idea stepを日本testとして使いません。biotech/diagnosticは
Patent Act、guideline、public-order、enablement/sufficiencyをspecialistへroute。

## Screen 4 — disclosure / filing

- no public disclosure
- disclosure within one year
- more than one year
- involuntary disclosure
- foreign filing/right impact

JapanのArt. 30はqualifying disclosureに1-year exceptionがありますが、filing時の
claimと30日以内evidenceが必要です。foreign rightsを回復せず、intervening prior artを
消しません。「日本ではany disclosureがfatal」と表示しません。

time-sensitiveならtopへactual date、candidate last date、source、unverified itemを
出し、counselへimmediate route。deadlineはofficial procedureと人が確認します。

## Screen 5 — inventorship / employee invention

- each human contribution
- natural-person inventor current position
- employer/employee/contractor
- pre-existing agreement/work rule
- reasonable monetary/other economic benefit
- consultation/disclosure/comment process
- contractor assignment

AI systemをinventorとして記録せず、AI-assisted contributionはhuman contribution
evidenceとcurrent law watchへroute。

## Screen 6 — detectability / strategy

- distributed/observable/reverse-engineerable
- server-side/internal process/training dataでlow detectability
- offensive/defensive/licensing strategy
- core/peripheral、competitive field、budget

low detectabilityならpatent-vs-trade-secretを
[営業秘密module](references/common/ja-jp/trade-secrets-oss.md)で
比較します。ornamental/UI/building/interiorならDesign Act routeを追加。

## Output

| Screen | Verdict | Source/reason |
|---|---|---|
| Novelty signal | ✓ / 🟡 / 🔴 | [...] |
| Inventive-step flag | ✓ / 🟡 / 🔴 | [...] |
| Japanese eligibility | ✓ / 🟡 / 🔴 | [...] |
| Disclosure / Art. 30 | ✓ / 🟡 / 🔴 | dates/source |
| Inventorship / employee | ✓ / 🟡 / 🔴 | [...] |
| Detectability | ✓ / 🟡 / 🔴 | [...] |
| Strategic value | ✓ / 🟡 / 🔴 | [...] |
| Design/trade secret | route / none / review | [...] |

bottom line:

- `PURSUE`: prior-art searchとregistered practitioner reviewへ進む価値
- `INVESTIGATE`: specific open item
- `DECLINE`: concrete, reviewable reason

`DECLINE`でも「not patentable」と書きません。

## Next options

prior-art search request draft、inventor questions、counsel transmittal、
decline thank-you draft、trade-secret classification draftから人に選んでもらいます。

## 行わないこと

- patentable/non-patentableを結論
- claim/applicationをdraft/file
- formal prior-art searchをしたと表示
- Art. 30 deadlineをmemoryだけで確定
- unpublished contentをP0/DLP checkなしに外部共有
- local filesystem、agent、hook、subagentを使う
