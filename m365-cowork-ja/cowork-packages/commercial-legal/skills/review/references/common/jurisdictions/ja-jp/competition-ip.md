> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本 — 競争、優越的地位、知財・know-how・data

**状態:** DRAFT — qualified Japanese counsel review pending

**一次資料確認日:** 2026-07-16

## Binding law

- 独占禁止法: https://laws.e-gov.go.jp/law/322AC0000000054
- 不正競争防止法: https://laws.e-gov.go.jp/law/405AC0000000047

独占禁止法第19条は不公正な取引方法を用いることを禁止する。優越的地位の
濫用は第2条第9項第5号、designation、guideline、事実関係を確認する。

## Contract check

- exclusive dealing、non-compete、non-solicit
- MFN、price parity、resale restriction
- tying、bundling、minimum purchase
- discriminatory term、refusal to deal
- unilateral fee/term change
- data access/portability、switching cost、lock-in
- IP assignment、grant-back、royalty
- know-how disclosure、prototype、source code
- NDAの片務性、residuals、目的外利用
- termination・renewalを利用したpressure

条項が存在するだけで違法としない。market position、dependency、alternatives、transaction history、countervailing benefit、scope/duration等を確認する。

## 優越的地位

legal standardとinternal fairness policyを分ける。大企業/中小企業というlabelだけで優越的地位を確定しない。

確認:

- 相手方の取引依存度
- 代替取引先・switching cost
- 自社のmarket/negotiation position
- 要請の必要性・合理性
- 不利益の内容、対価、説明、協議
- 断った場合の報復・更新拒否

取適法・Freelance Actのscopeも並行screenする。

## 2026 official guidance

JFTC・中小企業庁・特許庁:

`知的財産権・ノウハウ・データの適切な取引のための優越的地位の濫用等に関する指針`

https://www.jftc.go.jp/dk/guideline/unyoukijun/chizaitorihiki.pdf
https://www.jftc.go.jp/houdou/pressrelease/2026/jun/260624_chizaitorihiki.html

2026-06-24公表。契約書ひな形とともに、秘密情報、無償transfer、不当に低い対価、joint development、data等の取引を扱うofficial guidanceである。法律そのものではなく、個別違法性を自動判定するtemplateではない。

## Trade secret / data

営業秘密は、不正競争防止法第2条第6項の秘密管理性、有用性、非公知性を
別々に確認する。限定提供データ（同条第7項）は、業として特定の者に提供する
情報として電磁的方法により相当量蓄積・管理された技術上または営業上の情報
（営業秘密を除く）であり、営業秘密と同じ要件ではない。access control、
recipient、use purpose等は事実評価または契約controlであり、法定要件の
置換ではない。

NDAでは:

- definitionとmarking
- permitted use/recipient
- compelled disclosure
- return/destruction/backup
- residuals
- duration/trade secret survival
- remedy

をreviewし、IP/know-how/dataを一括で`all rights assigned`としない。

## AI / SaaS

AI training、usage data、derived data、output、prompt、RAG corpusを別々に定義する。上流model providerへdataが渡る場合、top-level vendorの責任、flow-down、opt-out、deletion、competitive isolationを確認する。

METI official checklist:
https://www.meti.go.jp/press/2024/02/20250218003/20250218003.html

これは2025-02-18公表のofficial guidanceであり、個別契約のbinding term
ではない。
