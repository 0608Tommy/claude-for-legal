> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本 — Payments、financial、medical、sector trigger

**状態:** DRAFT — qualified Japanese counsel review pending

**一次資料確認日:** 2026-07-16 JST

## Payments / financial

次の機能はspecialist reviewへrouteする。

- stored value、points、prepaid instrument
- transfer、remittance、withdrawal、redemption
- stablecoin、cryptoasset
- lending、credit、installment
- investment advice、brokerage、securities
- insurance
- account aggregation、bank API
- card-number handling、merchant/acquirer role

資金決済法2025 amendmentは2026-06-01施行と記録するが、service category、
registration、exception、transitionをcurrent consolidated textで確認する。
銀行法、金商法、割賦販売法、industry ruleもactivityごとに確認する。

閣法57号の金商法・資金決済法等改正案は2026-07-15に国会で成立したが、
2026-07-16時点で公布・法律番号を確認できない。[F]として、cryptoasset関連業務の
金商法への移行、crypto disclosure/insider rule、非財務情報の報告・保証等を
current obligationへ先行適用しない。既に2026-06-01施行の2025 amendmentと分ける。

payment processor、bank partner、app-store billing、merchant-of-record contractが
あるだけでproduct operatorのstatutory roleが消えるとは書かない。

## Financial claims and UX

- yield、return、fee、rate、risk、guarantee
- ranking、recommendation、personalization
- suitability/target user
- withdrawal/redemption timing
- complaint、refund、error correction
- dark pattern、default、subscription

claim、product functionality、licence/registration、disclosure、[P] partner/card
policyを分ける。

## Medical / health

intended diagnosis/treatment purpose、clinical consequence、patient risk、target
userがSaMD triageを支配する。`wellness`というmarketing labelだけでscope外としない。

分ける:

- PMD Act medical-device claim / SaMD
- hospital/clinic advertising under Medical Care Act
- drug/cosmetic/device claim
- food labeling/health claim under Food Labeling Act、Health Promotion Act等
- APPI special-care personal information
- medical/care PPC guidance

確認:

- intended use、instruction、output/action
- clinician/human review
- validation、limitation、false positive/negative
- emergency/escalation route
- data、vendor、security
- claim evidence、audience、channel

PMD Act令和7年法律第37号は段階施行である。2025-11-20、2026-05-01に施行済みの
部分と後続の将来施行部分を分け、`2025 amendment`全体をcurrentまたはfutureの
一色にしない。

## False equivalence

U.S. state money-transmitter model、GLBA/CFPB/Reg E/Reg Z、HIPAA/FDA conceptは、
独自nexusがある場合だけ[X]。日本ではFSA/METI/MHLW/PPCの[B/G]を別に確認する。

## Gate

required registration、medical-device route、mandatory disclosure、qualified
supervision、safety evidenceがない場合、launch optionとして`ship as designed`を
示さない。finance、medical、privacy、security、claimsのhuman ownerを指定する。
