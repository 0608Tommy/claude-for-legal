> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本 — 越境移転とDPA

**状態:** DRAFT — qualified Japanese counsel review pending

## 日本から外国

APPI Article 28とPPC外国提供guidelineをcurrent確認する。routeを混ぜない。

1. PPCが同等水準として指定する外国
2. 相当措置を継続的に講ずる体制を整備した受領者
3. 外国第三者提供についての事前本人同意
4. 法27条1項各号の例外

委託、事業承継、共同利用という法27条5項上の分類だけでは、外国提供に
関する法28条の規律を免れない。

本人同意routeでは国名、外国制度、提供先措置等の法定情報を事前に示す。国が特定できない場合の説明ruleを確認する。

基準適合体制routeでは、契約・group rule等の相当措置、継続実施、外国制度の影響、定期的確認、問題時の是正・停止、本人求めへの情報提供を確認する。`SCC signed`というlabelだけでAPPI complianceとしない。

公式:
https://www.ppc.go.jp/personalinfo/legal/guidelines_offshore/

- 指定国: https://www.ppc.go.jp/files/pdf/h31kokuji1_rev2023April18.pdf
- 補完的ルール: https://www.ppc.go.jp/files/pdf/Supplementary_Rules_jp.pdf
- EU Decision 2019/419: https://eur-lex.europa.eu/eli/dec_impl/2019/419/oj

## EU/UK等から日本

EU→JapanはEU adequacy decisionと日本のSupplementary Rules、対象entity/data、onward transferをcurrent確認する。UK、Switzerland、他国は各国のcurrent mechanismを別に確認する。

日本がadequateであることは、日本から別国へのonward transferを自動承認しない。APPIと移転元regimeの両方を確認する。

## DPA role table

契約冒頭で法域別に分類する。

| 問い | Japan | GDPR / UK GDPR | California |
|---|---|---|---|
| 誰が目的を決めるか | APPIの事業者・委託等 | controller / joint controller | business等 |
| 独自利用できるか | 委託範囲・第三者提供 | processor instructions | service provider restrictions |
| 再委託 | 監督・契約・実態 | Article 28 authorization | statutory contract |
| 本人請求支援 | 保有個人データ主体を確認 | Article 28 assistance | consumer request support |

`controller = 個人情報取扱事業者`、`processor = 委託先`と機械的に置換しない。

## Clause checklist

- data / subject / purpose / duration
- role and instructions
- independent use / service improvement / training
- security annex
- incident trigger、timeline、cooperation
- subprocessor list、notice、objection
- location、remote access、support
- transfer route、country、onward transfer
- rights assistance
- audit / certification
- retention、return、deletion、backup
- regulator inquiry
- liability / MSA conflict

日本法にはGDPR Article 28と同じmandatory clause listが一律に存在するとは書かない。APPIの監督義務を実効化するcontract/controlと、外国法上のmandatory termsを分ける。

## Data residency

APPIが一般に国内保存を一律要求するとは仮定しない。sector、contract、security、government procurement、customer commitment、foreign access lawを確認する。

## Human gate

transfer route、adequacy、country safeguards、SCC module、Supplementary Rules、DPA redlineはcurrent-law reviewが必要。AIは署名、送付、transfer開始を行わない。
