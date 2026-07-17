> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本 — 取適法、Freelance Act、委託取引

**状態:** DRAFT — qualified Japanese counsel review pending

**一次資料確認日:** 2026-07-16

## 先にscopeを判定する

契約名が`業務委託契約`、`NDA`、`SOW`だから適用/不適用とは決めない。

確認:

- 委託内容: 製造、修理、情報成果物、役務、特定運送、その他
- 発注者・受注者の資本金、常時使用従業員、組織形態
- 自社使用か、業として提供するものか
- 受託者が従業員を使用するか、one-person companyか
- contract duration、更新、解除
- delivery/acceptance、検査、payment
- effective date

取適法とFreelance Actは定義・thresholdが異なるため、各法を別々に判定し、片方を確認しただけで終わらない。

## 中小受託取引適正化法（取適法）

現行title:

`製造委託等に係る中小受託事業者に対する代金の支払の遅延等の防止に関する法律`

law number: `昭和三十一年法律第百二十号`

URL: https://laws.e-gov.go.jp/law/331AC0000000120

2026-01-01施行の改正後title。旧`下請法`はhistory labelである。

- 改正法: https://laws.e-gov.go.jp/law/507AC0000000041
- JFTC法令ページ: https://www.jftc.go.jp/toriteki/legislation/index.html

2026改正では従業員数基準、特定運送委託、支払手段規制、協議に応じない
一方的な代金決定禁止等のscope拡張を確認する。

e-Govで確認した主要事項:

- 第4条: 給付内容、代金額、支払期日・方法等を直ちに書面または電磁的方法で明示
- 第5条: 委託事業者のprohibited conduct
- 第6条: 受領日から60日経過後の遅延利息
- 第7条: 書類・電磁的recordの作成・保存

レビューでは、条文・JFTC ruleのcurrent listに照らし、受領拒否、支払遅延、減額、返品、買いたたき、購入・利用強制、報復、一方的な価格決定、支払手段等を確認する。網羅listは毎回official textで再確認する。

contract clauseだけでなくactual process（PO、acceptance、invoice、payment system、change order）も確認する。

## Freelance Act

正式title:

`特定受託事業者に係る取引の適正化等に関する法律`

law number: `令和五年法律第二十五号`

URL: https://laws.e-gov.go.jp/law/505AC0000000025

施行日: `2024-11-01`

current portal: https://www.jftc.go.jp/freelancelaw_2024/

e-Govで確認した主要事項:

- 第3条: 給付内容、報酬、支払期日等の書面・電磁的方法による明示
- 第4条: 原則60日以内かつできる限り短い支払期日
- 第5条: 一定期間以上の委託における遵守事項
- 第12条: 募集情報の的確表示
- 第13条: 妊娠・出産・育児・介護への配慮
- 第16条: 継続的業務委託の解除・不更新の原則30日前予告

第3条の明示義務は業務委託事業者に、第4条・第5条等は従業員を使用する
特定業務委託事業者に適用されるためactorを区別する。施行令第1条の第5条
期間は1か月、同令第3条の継続的業務委託は6か月である。第13条は6か月以上
では必要な配慮義務、短期委託では努力義務。第16条には省令上の例外と理由
開示義務がある。再委託の支払期日特則も確認する。

- 施行令: https://laws.e-gov.go.jp/law/506CO0000000200

適用対象、継続期間、exception、省令、公正取引委員会・中小企業庁・厚生
労働省の各所管をcurrent official sourceで確認する。

## 契約check

- required particularsとelectronic delivery evidence
- scope/change control、acceptance、rejection
- fee、tax、expense、rate revision、cost pass-through
- payment due、offset、chargeback、promissory note等
- IP/know-how/dataの帰属と対価
- materials/tool purchase、exclusive dealing
- termination/non-renewal notice
- harassment consultation、work environment等（Freelance Act scope時）
- record retention、audit trail

## Internal playbookとの分離

30日notice、60日payment等の法定ruleと、社内standard（例: net 30、90日前renewal alert）を分ける。社内standardが厳しい場合はplaybook deviation、法律のminimumを下回る可能性があればlegal issueとして示す。

## Worker classification

契約で`independent contractor`と書くだけで労働者性を否定しない。指揮命令、時間・場所、代替性、報酬、事業者性等の実態に疑義があればemployment specialistへ回し、本moduleだけで確定しない。
