> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本 — Consumer contract、通信販売、表示、stealth marketing

**状態:** DRAFT — qualified Japanese counsel review pending

**一次資料確認日:** 2026-07-16 JST

## Consumer / B2B split

相手方が個人でも事業目的ならgenuine B2Bの可能性がある。buyer、purpose、sales
channel、account type、actual solicitationを確認し、consumer ruleを全B2Bへ自動
適用せず、consumer-facing flowへB2B fallbackだけを使わない。

## Consumer Contract Act

screen:

- solicitation、misrepresentation、important omission
- liability exclusion、gross negligence等
- cancellation fee、early termination charge
- unilateral change、deemed consent
- clause that unilaterally prejudices consumer

AIが条項無効を確定せず、exact text、flow、factを日本法有資格者へ回す。

## Specified Commercial Transactions Act

通信販売、subscription、free trial、auto-renewal、in-app purchaseではactual
purchase flowを確認する。termsだけでは足りない。

- **第11条の広告表示:** seller identity/contact、price/fees、payment、
  delivery、return special terms等、該当する広告表示事項。
- **第12条の6の最終確認画面:** 申込み直前に省令所定の申込内容を表示し、
  product/service、quantity、total price/fees、payment/delivery、duration、
  renewal/trial conversion、withdrawal/cancellation等の該当事項を確認・訂正できるか。
- **flow evidence:** final confirmation screen、button/label、correction path、
  duplicate-order prevention、locale/device/timestamp。

最終確認画面regimeは2022-06-01施行。locale、device、timestamp、landing page、
checkout、final screenを保存し、表示の順序・近接性・視認性を確認する。

通信販売には一般的な法定cooling-off制度がない。第15条の2の返品rule、広告に
表示した特約、事業者の契約上の解約・返金policy、別取引類型のcooling-offを
混同せず、`cancellation method`だけから法定解除権を創作しない。

## Electronic Consumer Contract Act

error-confirmation特例を一般的な日本版`click-to-cancel`または全subscriptionの
final-screen lawとして説明しない。mistake、confirmation measure、consumer
instruction、Civil Code effectをexact factで確認する。

電子署名法の成立推定等は別論点であり、電子申込み、最終確認画面、本人確認、
署名権限を1つの`e-signature compliance`へまとめない。

## Premiums and Representations Act

expressだけでなくcomplete consumer impression、visual、ranking、comparison、
disclaimer、placement、audienceを確認する。

- superiority / advantage misrepresentation
- specific factual or performance claim
- comparative claim
- ranking、award、certification
- review/testimonial、synthetic person
- security、accuracy、fairness、medical/financial effect

unsubstantiated-advertising procedureでは合理的根拠資料の提出期間が一般に15日と
説明されるため、publication前にevidence、method、comparison basis、date、sample、
representativenessを保存する。exact current procedureはofficial sourceで確認する。

2023 amendmentのcommitment procedureとspecified misleading representationへの
direct penaltiesは2024-10-01施行と記録する。

## Stealth marketing

designationは2023-10-01施行。direct regulated partyは通常advertiser/supplierで、
influencerだけへ責任を移さない。

確認:

- supplier/advertiserの表示と評価できる関与・指示・対価・review processか
- 全体表示から一般消費者が広告であることを判別できるか
- content creation/review process
- `広告`, `PR`, platform toggleの表示
- placement、font、timing、surrounding content
- overall presentationでcommercial natureが明瞭か

`#ad`やplatform labelはmagic safe harborではない。AI-generated review/personを
actual user experienceと誤認させない。`material connection`は外国法または
社内taxonomyとして補助的に使えても、日本の告示上の独立要件として置かない。

## AI/disclosure

2026-07-16時点で、すべてのAI-assisted outputへ一律labelを要求する一般日本法は
確認できない。景品表示法、stealth、impersonation、IP/privacy、election、
sector rule、[P] platform policyを個別に確認する。

## False equivalence

FTC Act §5、NAD、FTC Endorsement Guides、ROSCA、U.S. state UDAP/dark-pattern lawは、
独自nexusがある場合だけ[X]として並行適用する。日本の[B/G]をそれらで置き換え
ない。marketing house standardは[I]として別に示す。

## Output gate

rendered asset、surrounding page、locale、device、destination、advertiser identity、
evidence、actual product/spec、final purchase screenが不足する場合、claimまたはflowを
公開可能と結論しない。
