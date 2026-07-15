> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本 — 消費者契約、通信販売、電子申込み

**状態:** DRAFT — qualified Japanese counsel review pending

**一次資料確認日:** 2026-07-16

## Scope

相手方が事業目的で契約する法人/個人事業者か、consumerかを先に確認する。B2B vendor agreementへconsumer ruleを自動適用せず、consumer-facing SaaSへB2B fallbackだけを適用しない。

## 消費者契約法

URL: https://laws.e-gov.go.jp/law/412AC0000000061

e-Govで確認した主要事項:

- 第4条: 不実告知等による申込み・承諾の取消し
- 第8条: 事業者の損害賠償責任を免除する条項等
- 第9条: consumerが支払う損害賠償予定等
- 第10条: consumer利益を一方的に害する条項

review:

- solicitation、claim、omission、important fact
- liability exclusion、`重大な過失`等
- cancellation fee、early termination charge
- auto-renewal、silence/deemed consent
- unilateral change
- arbitration、forum、burden shift

個別条項の無効性をAIが確定せず、exact textと事実を日本法有資格者へ回す。

## 特定商取引法

URL: https://laws.e-gov.go.jp/law/351AC0000000057

通信販売等のtransaction categoryとscopeを確認する。e-Govで確認した主要事項:

- 第11条: 通信販売広告の表示
- 第12条: 誇大広告等の禁止
- 第12条の6: 最終確認画面等の表示と誤認表示の禁止
- 第14条: 行政上の指示等
- 第15条の4: 禁止行為により誤認した場合の取消し

第12条の6等の最終確認画面regimeは2022-06-01施行。subscription/
auto-renewalでは、最終確認画面、総額、期間、更新、cancel method、deadline、
trial conversion、quantity、返品・解約条件を確認する。消費者庁official
guide:

https://www.caa.go.jp/policies/policy/consumer_transaction/specified_commercial_transactions/
https://www.no-trouble.caa.go.jp/what/mailorder/guidelines.html

guide、FAQ、検討会資料をbinding lawと混同しない。

## 電子消費者契約法

現行title:

`電子消費者契約に関する民法の特例に関する法律`

URL: https://laws.e-gov.go.jp/law/413AC0000000095

第3条は、一定の送信mistakeについて、確認措置を講じた場合またはconsumerが
確認不要と意思表示した場合を除き、民法第95条第3項の重大な過失による制限
を適用しない特例である。一般的なfinal-screen、auto-renewal、cancel表示義務
そのものではない。現行titleは2020-04-01から使用され、旧title
`電子消費者契約及び電子承諾通知に関する民法の特例に関する法律`は
historical referenceとしてのみ扱う。

check:

- confirmation screen
- correction mechanism
- button/labelの明確性
- quantity、price、term、renewal
- accidental duplicate order
- evidence of presented terms

button clarity、correction mechanism、screen capture、timestamp、duplicate-order
check等には特定商取引法・施行規則とoperational controlが含まれるため、
電子消費者契約法の単独要件として表示しない。

## Auto-renewal

日本法上、全B2B auto-renewalへ一律のnotice ruleがあるとは断定しない。consumer、通信販売、定型約款、individual sector、contract wording、representationを分ける。

internal trackerは法定義務とは別に、`send_by_effective`前に人が判断できるoperational controlである。

## Gate

consumer-facing output、purchase flow、terms version、final screenを読めない場合、contract textだけでcomplianceを確定しない。screen capture、URL、timestamp、locale、device flowを求める。
