> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本 — APPI/PPC、security、外部送信、通信

**状態:** DRAFT — qualified Japanese counsel review pending

**一次資料確認日:** 2026-07-16 JST

## APPI classification

少なくとも次を分ける。

- `個人情報`
- `個人データ`
- `保有個人データ`
- `要配慮個人情報`
- `個人関連情報`
- 委託
- 第三者提供
- 共同利用
- 外国にある第三者への提供

GDPR `controller/processor`を自動対応させず、取得、利用目的、独自利用、recipient、
instructions、再提供、本人との関係を確認する。

launch check:

- new data field、inference、identifier、biometric、health
- purpose change、combination、training、personalization
- recipient/vendor/model、independent use
- disclosure/consent/opt-out、privacy notice/CMP/label
- retention、deletion、rights handling
- foreign transfer、remote access、storage

## PIA

PPCはPIAを促進しているが、日本の民間一般processingすべてに一律の法定PIA義務が
あるとは書かない。

- `[B]` formal assessment triggerが別法にあるか
- `[G]` PPC recommended PIAか
- `[I]` company policyのPIA/AIAか
- `[X]` GDPR等のDPIAか

を分ける。

## Breach/security

reportable categoryには、要配慮個人情報、財産的被害のおそれ、不正目的行為、
1,000人超等が含まれ得る。exact factsとcurrent ruleを確認する。

- preliminary reportは速やかに。PPC guidanceの3–5日程度は[G]目安であり、
  固定statutory deadlineと書かない。
- final reportは原則30日、悪意ある行為等は60日となるcategoryをcurrent ruleで
  確認する。
- affected-person notice、security team、contractual incident clock、sector
  reportingを別にする。

## External transmission

電気通信事業法27条の12等は2023-06-16施行。まずserviceが対象電気通信役務かを
確認し、その後でrouteを選ぶ。

- notice / readily knowable state
- consent
- qualifying opt-out
- applicable exception

SDK、analytics、ad-tech、crash report、embedded browser、link decoration等について、
recipient、送信data、purpose、trigger、user control、screenを実測する。

「日本のcookieはすべてopt-in」も「cookieは日本法の対象外」も誤りになり得る。
APPI、個人関連情報、外部送信、通信の秘密、外国lawを別々に確認する。

## Communications secrecy / telecom role

productがmessage、call、email、network、carrier/service-provider機能を扱う場合、
電気通信事業該当性、届出/登録、通信の秘密、lawful access、metadata/content、
outsourcingを確認する。FCC/CPNIを日本法上の結論として使わない。

## 2026 APPI amendment

閣法54号は2026-04-07に閣議決定・提出され、2026-07-10に国会で成立した。
2026-07-16官報まで公布・法律番号は確認できず、主要部は公布後2年以内の
政令指定日施行である。under-16、特定生体個人情報、contactable related
information、統計等の例外、surcharge等を[F]とし、公布、法律番号、附則、
PPC rule、政令指定日が確認できるまでcurrent obligation/exceptionへ使わない。

under-16案はnotice、consent、rights等を法定代理人へrouteする将来規定であり、
すべての取得・処理へ一律のparental opt-inを課すCOPPA型ruleと説明しない。

## Output gate

data map、SDK/network trace、recipient、actual screen、notice version、affected
users、launch dateがなければcomplianceを確定しない。findingには[B/G/I/F/X]、
source、effective date、facts needed、privacy/security/telecom ownerを付ける。
