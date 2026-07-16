---
name: infringement-triage
description: >
  商標、特許・実用新案、意匠、著作権、営業秘密、商品形態の侵害可能性を権利別にfirst passで整理する。日本法の各Act、Hyozan、Ball Spline、Esashi Oiwake、Customsを適用し、侵害・非侵害の結論や自動C&D/takedownを行わない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: ip-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Infringement triage

旧来の参照label:
`/ip-legal:infringement-triage [describe the facts and which right]`。

## Loudest guardrail

> **これは侵害・非侵害のfindingではありません。**
> right、scope、facts、jurisdiction、defense、remedyをflagするtriageです。
> C&D、takedown、訴訟、design-around、no-actionの前に有資格者が判断します。

## Mandatory gate

1. [保存契約](references/common/cowork-runtime-contract.md)を読み、gateway、
   user/practice/matter scope、ACL、destinationをpreflight。
2. party postureを`senior | accused`、rightを
   `trademark | patent | utility-model | design | copyright | trade-secret |
   product-configuration | mixed`から確認。mixedは別々に分析。
3. matter scopeならactive/unexpired binding。practice modeはfresh session。
4. jurisdictionを`request > matter > practice-profile > tenant-default`で解決。
5. evidence/source exact item/version、coverage、capture dateを記録。
6. registration/status/owner/recordal、claim/drawing、copyright chain、
   secrecy controlsをcurrent sourceで確認。
7. trade secret/未公開発明はDLP・economic-security・destinationを確認。
8. outputはinternal draft。AIはassert、send、submit、file、takedownをしません。

[source/provenance rule](references/common/source-provenance-and-review.md)と
[日本法router](references/common/jurisdictions/ja-jp/README.md)を使います。

## Common intake

- senior/accused posture
- parties/relationship
- jurisdiction、market、manufacture/import/platform
- timing、first knowledge、stated deadline
- exact right and source
- accused work/product/process/sign
- evidence、access、licence、agreement
- business harm、customer confusion
- insurance/indemnity、outside counsel

## Trademark

- Trademark Act Arts. 25, 26, 37、prior use、limitation **[B]**
- UCPA well-known/famous indication、false facts **[B]**
- *Hyozan* appearance、sound、concept、trading circumstances **[C]**
- registration/designated goods、actual use、strength/fame evidence
- consumer/channel、actual confusion、intent evidence

Lanham factors、TDRA dilution test、common-law priorityを日本ruleとして使いません。

## Patent / utility model

[特許module](references/common/jurisdictions/ja-jp/patents-utility-designs.md)に従い:

- official current claim/status
- Art. 70 scope、literal mapping
- *Ball Spline* equivalents、*Maxacalcitrol*
- Art. 101 indirect infringement
- prior use、licence、exhaustion、Art. 104-3
- utility-model technical opinion/enforcement requirements
- damages/evidence/Art. 103をseparate

U.S. willfulness/treble damagesを日本へ移植しません。

## Design

- registration/application/drawings、claimed scope
- Design Act Art. 24 consumer aesthetic impression
- prior design、functionality、related/secret design
- UCPA product configuration parallel track

`D`-number、*Egyptian Goddess*、point-of-novelty、§289 total profitsを使いません。

## Copyright

- authorship/ownership/exclusive authority
- protected expression、reliance、reproduction/adaptation
- specific statutory exception
- *Esashi Oiwake* direct perceptibility **[C]**
- moral rights、licence、limitation
- provider/platform route

Japanese suitにU.S. registration prerequisiteを要求せず、open-ended §107 fair useを
日本ruleとして使いません。

## Trade secret

- UCPA secrecy management、usefulness、non-publicity
- enumerated acquisition/use/disclosure act
- access control、NDA、marking、training、exit、logs
- lawful reverse engineering、independent development

DTSA/UTSA reasonable-measures terminology、state preemption、inevitable disclosureを
日本ruleとして使いません。

## Product configuration

UCPAの商品形態模倣をtrademark/trade dressと分離し、first Japanese saleから原則
3-year period、common form、function、lawful imitation/exceptionをcurrent sourceで
確認します。

## Evidence and Customs

dated page/screenshot、physical sample、receipt、hash/version、access log、
assignment/licence chain、confidentiality controlをpreserve candidateとして示します。
import goodsなら[Customs route](references/common/jurisdictions/ja-jp/enforcement-customs.md)。

evidence preservationは**[I]**であり、AIがcollection/surveillance/purchaseを
実行したとは表示しません。

## Output

```markdown
# Infringement Triage — [right] (NOT A FINDING)

## Posture/scope/source
## Right/status/standing
## Factor or element analysis
## Defenses/limitations
## Evidence gaps
## Remedy/routing options
## Counsel questions
```

各factorを`senior | accused | mixed | unknown`で示し、結論は
`attorney judgment required`に限定します。上流severityを理由なく下げません。

## Handoff

人が選んだ場合だけ:

- `cease-desist`へfacts/sourceをhandoff
- hosted **copyright** contentは`takedown`
- own product patent issueは`fto-triage`
- litigation claim chartは旧参照label`/litigation-legal:claim-chart`

handoffは提案であり、自動invoke/draft/saveしません。
trademark、design、patent、trade-secret claimをDMCA/copyright takedownへroute
しません。provider-specific non-copyright procedureがある場合はcurrent
official/contract routeを別途調査します。

## Other jurisdictions

[U.S./global layer](references/common/original-ip-logic.md)をright/jurisdiction別に
separate sectionで適用します。

## 行わないこと

- infringement/non-infringement、fair use、validityを最終判断
- C&D/takedown/complaintを自動draft・send
- U.S. doctrineを日本へ移植
- evidenceを取得済みと偽る
- local filesystem、agent、hook、subagentを使う
