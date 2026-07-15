> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本 — 契約一般、電子署名、責任、解除

**状態:** DRAFT — qualified Japanese counsel review pending

**一次資料確認日:** 2026-07-16

## 契約成立と方式

民法第522条は、申込みと承諾による成立を定め、法令に特別の定めがない限り、書面作成その他の方式を要しないとする。したがって「押印がないから無効」「電子署名だから必ず有効」と一律に書かない。

英米法上の`consideration`を日本法上の一般的な成立要件として追加しない。

確認:

- offer、acceptance、counteroffer、effective date
- signerのauthority、delegation、corporate approval
- conditions precedent
- order formとmaster termsの優先順位
- URL termsのversion、変更権、notice
- 法令上または取引上必要な書面・電磁的方法

## 電子署名

電子署名法第3条は、本人だけが行えるよう必要な符号・物件を適正管理して
行われた本人の電子署名がある電磁的recordについて、真正成立を推定する。
対象となる電子署名は第2条第1項の、作成者を示す措置と改変の有無を確認
できる措置の双方を満たす必要がある。

- 第2条Q&A: https://www.moj.go.jp/content/001323974.pdf
- 第3条Q&A: https://www.moj.go.jp/content/001327658.pdf

これは次を自動的に意味しない。

- すべてのclick、typed name、platform signatureが第3条要件を満たす
- 署名者に契約締結権限がある
- 内容、意思表示、fraud、mistake、duressの争いがない
- 契約固有のnotice/署名方式が満たされる

DocuSign等のstatus、service architecture、認証、credential control、
audit trailは証拠評価の一部である。envelope送信・署名を人の明示確認まで
行わないことはoperational controlであり、電子署名法上の要件そのものでは
ない。

## 定型約款・online terms

民法第548条の2～第548条の4について、少なくとも次を確認する。

- `定型取引`・`定型約款`に該当するか
- 契約内容とする旨の合意または表示
- 内容表示請求への対応
- unilateral changeの要件、reasonableness、周知時期
- negotiated agreement、order form、policy、online termsの優先順位

単に「websiteにある」だけでincorporationを確定しない。取得したversion、URL、access date、change historyを記録する。

## 債務不履行・損害

民法第415条、第416条、第420条等を案件に応じて確認する。

- obligation、breach、attribution、causation
- ordinary/special damages、foreseeability
- liquidated damages、penalty-like effect
- limitation/exclusionと強行法
- indemnityとdamagesの重なり
- direct / indirect / consequentialの契約定義

`direct / indirect / consequential`は民法の法定categoryではない。第416条の
通常損害・特別事情による損害と、契約上の定義を分ける。第420条は損害賠償
額の予定を認め、`違約金`を予定額と推定するため、英米のpenalty doctrineを
自動適用しない。indemnityも第三者請求限定、attorneys' fees込み等の英米
defaultを仮定しない。

playbook上のcapを法律上の当然の上限と書かない。capは4次元
（direct/indirect、base、carveout、各position）で比較する。故意・重大な
過失、personal injury、consumer、product liability、data、IP等の扱いは
個別に有資格者へ回す。

## 解除・期間・更新

民法第541条・第542条、契約条項、special statuteを分ける。

- cure notice、cure period、materiality
- immediate termination trigger
- termination for convenience
- insolvency、change of control、security incident
- initial/current term、auto-renewal、non-renewal window
- survival、data return/deletion、transition

契約上の解除権がないことを「解除不能」と断定せず、法定解除その他の権利を別に確認する。更新・解約noticeは契約のmethod、address、receipt/deemed receipt、business day、time zoneを読む。

## Notice deadline

calendar arithmeticだけで確定しない。

1. current term end
2. notice period
3. notice method
4. `received by` / `sent by`
5. contract-defined business day
6. holiday、weekend、time zone
7. transit buffer

tracker dateは`[model calculation — verify against the notice clause]`を保持し、送信前に契約原文と日本のcalendarを人が確認する。

## Governing law

法の適用に関する通則法、forum clause、arbitration、mandatory ruleを分ける。choice-of-lawがあっても、consumer、worker、competition、privacy、取適法・Freelance Act等が別途問題となり得る。

複数法域では:

- governing law
- forum/arbitration seat
- place of performance
- party/data subject/consumer/worker location
- overriding mandatory rule

を別欄にする。

## Confidentiality、IP、product

- confidential information definition、carveouts、residuals、permitted recipients
- return/destruction、backup、legal retention
- trade secret管理と不正競争防止法上の要件
- background/foreground IP、license、assignment、moral rights対応
- product/service defect、warranty、support、recall、PL exposure

秘密情報labelだけで営業秘密要件を満たすと断定しない。SaaS output、usage data、derived data、AI training rightsは別々に定義する。

委託制作物がcustomerへ当然帰属する、または米国の`work made for hire`と
同じになると仮定しない。著作権法第15条、第59条、第61条第2項、特許法
第35条等を確認する。製造物責任法第2条の製造・加工された動産にpure
software/SaaS/serviceが当然該当するとも扱わない。

## 法律・guidance・playbook

- 上記法令: binding law
- 省庁Q&A・checklist: official guidance
- standard/fallback/never: internal playbook

「法的に可能」と「playbookに合う」、「playbook違反」と「違法」を混同しない。
