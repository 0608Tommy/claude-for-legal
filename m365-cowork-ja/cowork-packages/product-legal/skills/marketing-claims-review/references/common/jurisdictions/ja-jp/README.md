> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# `ja-JP` プロダクト法務module

**状態:** DRAFT — qualified Japanese counsel review pending

**一次資料確認日:** 2026-07-16 JST

本moduleは日本に関係するlaunch、feature、marketing、commerce flowを追加確認する
layerであり、法的助言またはlaunch clearanceではない。

## 選択条件

`request > matter > practice-profile > tenant-default`

最終的に日本が含まれる場合、本moduleを適用する。`Japan`, `日本`, `JP`,
`ja-JP`が矛盾する、affected user/seller/operator所在地が不明、または外国法も
適用し得る場合は、対象ごとに法域を分ける。

## Authority class

| class | 内容 |
|---|---|
| `[B]` | binding law、政省令、規則 |
| `[G]` | official guidance、FAQ、行政資料 |
| `[P]` | exchange rule / platform policy。JPX上場規程等の自主規制ruleと、app store・marketplace等の契約policyをsubtypeで分ける |
| `[I]` | risk calibration、playbook、AIA/PIA、evidence retention等の内部control |
| `[F]` | future/pending、成立後公布確認待ち、未施行 |
| `[X]` | 独自nexusにより並行適用する外国法 |

各findingはclass、source URL、version/date、effective date、current/future status、
必要事実、human ownerを示す。

EDINETは提出systemであってauthority classではない。提出義務・記載事項は金商法、
開示府令等の[B]から、Fair Disclosure Ruleや行政資料は[B/G]から、JPX上場規程は
`[P: exchange-rule]`、JPX guideは[G]として別々に示す。

## 読み分け

| 論点 | 読むファイル |
|---|---|
| APPI/PPC、漏えい、外部送信、通信の秘密 | [appi-telecom.md](appi-telecom.md) |
| consumer contract、通信販売最終画面、表示、stealth | [consumer-commerce-claims.md](consumer-commerce-claims.md) |
| 製造物責任、製品安全、platform、e-commerce、UGC | [product-safety-platform.md](product-safety-platform.md) |
| accessibility、未成年、consent capacity | [accessibility-minors.md](accessibility-minors.md) |
| 決済、金融、医療、sector claims | [payments-financial-medical.md](payments-financial-medical.md) |
| cyber、AI governance/disclosure、著作権、営業秘密 | [cyber-ai-ip-content.md](cyber-ai-ip-content.md) |
| 上場会社開示、MNPI、秘密性・privilege | [public-company-privilege.md](public-company-privilege.md) |
| official URL、資料状態、確認日 | [source-register.md](source-register.md) |

## Mandatory Japan preflight

1. Japan nexus、entity、seller/operator、affected user。
2. consumerかgenuine B2Bか。
3. website/app/marketplace/content platform/app store/channel。
4. actual data、SDK、recipient、network flow。
5. physical product、embedded software、IoT。
6. under-18、capacity、representative consent。
7. stored value、points、transfer、redemption、credit、investment、insurance。
8. diagnosis/treatment、health、medical/food/cosmetic claim。
9. telecom role、external transmission、communications content。
10. AI、UGC、synthetic person/review、human escalation。
11. accessibility-critical flowとaccommodation request。
12. listed/reporting company、material information、IR/security handling。
13. launch dateとfuture commencement date。

## Current/future rule

- 2026年APPI改正は閣法54号として2026-04-07提出、2026-07-10成立。ただし
  2026-07-16官報まで公布・法律番号を確認できず、主要部は公布後2年以内の
  政令指定日施行であるため、under-16等は[F]。
- 2026年金融商品取引法・資金決済法等改正案は2026-07-15成立後、公布・法律番号
  未確認の[F]。cryptoasset、非財務情報開示等をcurrent dutyへ先行適用しない。
- 著作権法令和8年法律第48号の主要な実演家・レコード製作者報酬規定は、公布後
  3年以内の政令指定日まで[F]。30条の4のAI学習分析を変更したとは扱わない。
- PMD Act令和7年法律第37号は段階施行。既施行部分と将来施行部分を分ける。
- cyber special-infrastructure reporting orderは2026-10-01以後、designationと
  scopeを確認して適用する。
- election AI imagery ruleの主要部分は2027-03-01予定。一般的AI label義務ではない。
- platform policyは[P] living documentであり、launchごとにlive pageを取得する。
- JPX上場規程は`[P: exchange-rule]`としてlisting statusとlive ruleを確認し、
  app-store policyと同じ可変的product policyとして扱わない。

## False equivalence

- FTC/NAD/Endorsement Guidesは日本のcontrolling standardではない。
- COPPA under 13は日本の固定child thresholdではない。
- U.S. state privacy/AADC/dark-pattern lawは独自nexusがある場合だけ[X]。
- `MNPI`は社内controlまたは外国法用語として[I]/[X]に留め、日本法では金商法上の
  重要事実、Fair Disclosure Ruleの重要情報、JPXの会社情報を別々に分析する。
- FCC、HIPAA、GLBA/MTL/CFPB、DMCA/Section 230、EU AI Act、Form 8-K、
  `ATTORNEY WORK PRODUCT`を日本法へ同義変換しない。
- app-store approval、payment processor利用、`#ad`、AI labelは日本法complianceの
  safe harborではない。

## Gate

sourceを取得できない、事実が曖昧、future/currentが未確認、日本法有資格者reviewが
ない場合は`pending`または`[review]`とする。house calibrationは[B]/[P] floorを
下げない。
