---
name: fto-triage
description: >
  日本で製造・使用・販売・申出・輸出入・program transmissionを行うproduct/processについて、特許・実用新案・意匠のsearch scope、claim chart、Ball Spline equivalents、Article 101、Article 104-3、Customsをfirst passで整理する。FTO opinionまたはlaunch clearanceは出さない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: ip-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Freedom-to-operate triage

旧来の参照label:
`/ip-legal:fto-triage [describe the product / process / feature and jurisdictions]`。

## Loudest guardrail

> **これはFTO opinionではありません。**
> formal FTOにはcomprehensive search、current claims/status、prosecution/
> invalidation record、claim construction、element-by-element analysis、
> Japanese patent counselの判断が必要です。hitなしはclear to launchを意味しません。

## Mandatory patent/security gate

1. [保存契約](references/common/cowork-runtime-contract.md)を読み、gateway、
   scope、ACL、source/destinationをpreflight。失敗時はread-only。
2. exact user/practice/matter、patent counsel、jurisdictions、integrationsを読みます。
3. matter scopeはactive/unexpired binding、practice modeはfresh session。
4. 未公開technical contentをexternal tool/foreign partyへ送る前に
   [特許非公開P0](references/common/jurisdictions/ja-jp/patents-utility-designs.md)。
   不明なら送信しません。
5. source exact item/version、technical coverage、manufacture/use/sale/import routeを
   確認します。
6. 日本ならPatent/Utility Model/Design Actsとcurrent JPO recordを使います。
7. claim text、status、annuity、term、recordalをofficial sourceで確認できない場合、
   `[verify]`として結論を限定。
8. AIはlaunch、design-around採用、licence、challenge、filingを決定・実行しません。

## Intake

- product/process/featureのtechnical essence
- diagrams/spec/code excerpt等のauthorized source
- where made、used、sold、offered、exported/imported、transmitted
- launch timing
- known patents/applications/utility models/designs
- competitors、standards/SEP、licence/pool
- confidential/economic-security restrictions

vagueなmarketing descriptionだけではclaim chartへ進みません。

## Search

日本scope:

- J-PlatPat granted patents、utility models、published applications、designs
- claims in Japanese、family、priority
- prosecution、correction、opposition/invalidation
- annuity/in-force、term extension
- assignee/owner/recordal
- named competitor、classification、keyword、citation

Patent Act Art. 64の18-month publication blind spotを必ず明示します。
database accessがない場合:

> **Patent database searchは実行していません。** 以下は利用者が指定した
> rightsだけのfirst passです。launch decision前にJ-PlatPatと関係法域の
> comprehensive searchが必要です。

## Japanese legal frame

- territorial acts: Patent Act Arts. 2/68
- scope: Art. 70、claims/specification/drawings。abstractで決めない
- literal analysis
- equivalents: *Ball Spline* five requirements **[C]**
- intentional exclusion: *Maxacalcitrol* **[C]**
- indirect infringement: Art. 101 category
- defenses/limits: prior use、experiment/research、licence、exhaustion、
  Art. 104-3、utility-model-specific requirements
- appearance: Design Act Art. 24 + UCPA product configuration
- imports: Customs Act Art. 69-11

U.S. induced/contributory terminology、`Alice/Mayo`、`Egyptian Goddess`、
§284 willfulness/treble damagesを日本analysisへ使いません。JapanにはU.S.
treble-damages regimeがなく、Patent Act Art. 103 negligence presumptionを別に
扱います。

## Claim chart

2–5 most plausible rightsを選び、各independent claimを全部扱います。

| Exact claim element | Mapping | Evidence/source | Read |
|---|---|---|---|
| [official claim text] | yes / no / possible / construction-dependent | [item/page/version] | literal |

rules:

- every element matters
- term constructionがdispositiveなら両readingを示す
- literal後にequivalentsを別欄
- Art. 101、divided acts、cross-border supplyは別flag
- dependent claimsを落とした場合は明示
- claim quoteをmemoryで補完しない

## Design / utility model branch

- utility modelはtechnical opinion、term/fee、enforcement gateを別に確認。
- designはapplication/drawings、claimed portion、consumer aesthetic impression、
  prior design、functionality、related/secret designを確認。
- UCPA product configuration、trademark/trade dress相当riskを別track。

## Output

- reviewer note
- subject/acts/jurisdictions/timing
- source/search coverage and blind spot
- rights table: number、owner、priority、status、term、source
- claim charts
- equivalents/Art. 101/defense/design/Customs flags
- open questions
- options: formal FTO、design-around study、licence、validity review、more facts

結論:

- every element maps on literal first pass; stop and obtain counsel review
- one or more elements unclear/absent; construction/equivalents review required
- no database search or blind spot remains; no launch conclusion

specific rightをsurfacedしたこと自体をJapanese treble-damages warningにしません。
confidentialityとcounsel routingは維持します。

## Other jurisdictions

[移行元U.S./global logic](references/common/original-ip-logic.md)をseparate sectionで
適用します。family memberごとにjurisdictionを分けます。

## 行わないこと

- FTO opinion、non-infringement、clear-to-launchを出す
- claimsをdraft/construe definitively
- validity/enforceabilityを最終判断
- specific patent、claim、status、expirationを創作
- technical disclosureをP0 screenなしにexternal toolへ送る
- file、pay、license、challenge、launchを実行
- local filesystem、agent、hook、subagentを使う
