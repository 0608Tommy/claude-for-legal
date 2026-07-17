> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、日本のM&A・開示・競争・外資規制workflowを追加した派生ファイルです。

# 日本のM&A、開示、merger control、foreign investment

**Status:** `DRAFT / qualified Japanese counsel review pending`

## Transaction structureを最初に固定する

`share sale | business transfer | merger | company split | share exchange |
share transfer | share delivery | other`

`share transfer`は法定の株式移転（new wholly owning parentを設立）、
`share delivery`は法定の株式交付（KK-to-KKの子会社化）を指す場合だけ使う。
`restricted shares`は原則`譲渡制限株式`とし、報酬restricted stockと混同しない。

structureが未確定なら、contract/employee/asset/licence succession、approval、
creditor procedure、appraisal、registry、tax、FIEA、JFTC、FEFTAの結論を確定しない。

### structure差

- **Share sale:** target legal entity、employer、contract partyは通常同一だが、
  change-of-control、restricted shares、licence ownership/control、FIEA/JFTC/FIEA
  public-company ruleをscreenする。
- **Business transfer:** asset、claim、obligation、contractual position、employee、
  licenceを個別に分析する。board/shareholder approval、business transfer
  definition、employee consent/consultation、counterparty consent、perfectionを確認。
- **Merger / company split:** universal successionの範囲とspecial statutory
  exceptions、creditor objection、employee succession、licence、registration、
  effective dateを確認する。
- **Share exchange / transfer / delivery:** approval、shareholder treatment、
  appraisal、disclosure、registration、listed-company ruleをstructure別に確認。

## Corporate action checklist

structureごとに次をscreenする。

- board/shareholder/class shareholder approval
- special-interest director、conflict、MBO/controlling shareholder process
- articles、shareholder agreement、restricted-share approval
- advance/post disclosure documents
- creditor objection/public notice
- appraisal/purchase demand rightsとperiod
- employee notice/objection/consultation
- shareholder register update、share certificate handling
- effective date、closing condition、registration

business transferはCompanies Act Art. 467の全部・重要な一部
（total assets 20% exclusionを含む）と他社事業全部の譲受けを確認し、
Art. 468の90% short-form、20% net-assets simplified exceptionを別に判定する。
reorganizationではstructureに応じ、special resolution、short/simplified
exception、原則1か月以上のcreditor-objection period、appraisal notice/
exercise、advance/post-effective disclosure、原則2週間のregistrationを
official textで確認する。
- licence/permit consent、real estate/IP perfection

METI Fair M&A GuidelinesとTakeover Guidelinesはsoft lawとしてlabelし、
statutory requirementと混同しない。

## FIEA / public-company workflow

次を別calendar/decision treeで扱う。

1. Companies Act corporate record
2. FIEA statutory filing via EDINET
3. JPX timely disclosure via TDnet
4. governance report / comply-or-explain
5. insider lists/trading controls
6. officer/major shareholder report under Art. 163
7. insider rules under Arts. 166/167
8. large-holding report
9. tender offer rule

### 2026-05-01 amendments

2024 Act No. 32関連のtender-offer/large-holding改正は2026-05-01施行として
official ruleを確認する。tender-offer thresholdは30%へ変更され、exchange-market
transactionも対象に含まれる改正がある。旧1/3 thresholdを使わない。

large holdingはover 5%、原則5 business daysのcurrent portal/ruleを確認する。
joint holder、special report、change report、cash-settled derivative等のactual
definition/exceptionを省略しない。

- TOB period: 20～60行政機関の休日を除く日
- target opinion report: 10 business days
- bidder response to questions: 5 business days
- result: period満了翌日に公表し、同日にreport
- post-TOB ownershipが原則3分の2以上となる場合のall-holders solicitation
- large-holding change report: 原則1 percentage pointまたはmaterial changeを
  5 business days以内
- Art. 163 major shareholderは原則voting rights 10%、reportは翌月15日まで
- annual securities reportは原則3か月以内、listed half-year reportは原則
  45日（specified financial businesses 60日）をcurrent ruleで確認

JPX timely disclosure guideは2025-04 full guideに2026-04/07 extractがあるため、
versionless `current`と表示しない。

quarterly-report abolitionとhalf-year reportは2024-04-01施行のofficial materialを
確認し、旧10-Q相当calendarを流用しない。

決定事実/発生事実のTDnet timingとEDINET statutory filingを一つの「disclosure」
itemへ潰さない。source、approver、deadline、system、evidenceを別fieldにする。

## JFTC merger control

current core screenとして、少なくとも次をofficial sourceで確認する。

- acquiring group domestic turnover band: ¥20bn
- target group domestic turnover band: ¥5bn
- acquisition crossing 20% / 50% voting-right bands
- standard 30-day closing prohibition
- other transaction formsのthreshold/rule
- high-value below-threshold transactionのconsultation policy

share acquisitionではacquiring group Japan turnover >¥20bn、target group
>¥5bn、post-acquisition voting ratioが新たに20%/50%を超えるかを確認する。
merger/share transferは¥20bn/¥5bn、whole/important business acquisitionには
transferred business ¥3bn thresholdを確認する。high-value policyの
transaction value >¥40bn + Japan nexusはconsultation guidanceであり、
mandatory filing thresholdではない。Phase II order periodはcomplete response
後のperiodを含めcurrent sourceで確認する。

thresholdはtask時に再確認する。turnover calculation、group scope、Japan sales、
joint control、series transaction、filing party、waiting-period shortening、
Phase reviewを推測しない。

checklist itemには`legal_basis`, `source_version`, `effective_date`,
`evidence_required`, `filing_system`, `waiting_period_end`, `waivable`を保持する。
AIはnotificationをfileせず、waiting period satisfactionをcertifyしない。

## FEFTA foreign investment

次を取引初期にscreenする。

- foreign investor status
- ultimate control、specified foreign investor relationship
- listed share acquisitionの1% band
- unlisted share acquisition
- designated business / core business
- board seat、proposal、business transfer等のcovered action
- prior notification、exemption、post-report
- investor/target activity、licence、technology、economic-security facts
- filing form、submission route、waiting period、clearance evidence

2025 rulesは2025-05-19施行として、specified foreign investor等のexemption
restrictionを確認する。CFIUS terminology、U.S. control test、U.S. formを代用しない。
MOF/BOJ current portal、form、Q&Aをtaskごとに読む。

listed-share 1% testはinvestor、close relationship、specified discretionary
management holdingsを集計する。unlisted acquisition from another foreign
investorはspecified acquisition等の別routeを確認する。prior notificationの
statutory standstillは30 calendar daysで、短縮・延長可能性がある。多くの
post-reportはform-specific 45日を確認する。

Law No. 30 of 2026（2026-06-05公布）はindirect overseas acquisition、
risk-mitigation filing、anti-circumvention等を追加するが、多くは1年以内の
政令施行待ちで`PENDING`。現行義務へ先行適用しない。

- https://laws.e-gov.go.jp/law/508AC0000000030
- https://www.mof.go.jp/policy/international_policy/gaitame_kawase/press_release/20260312152131.html

## Disclosure scheduleとstatutory register

PAのMaterial Contract definitionとdisclosure scheduleはcontractual testである。
別に次のstatutory/regulatory exceptions registerを持つ。

- Companies Act corporate approvals/disclosure
- FIEA/EDINET
- JPX/TDnet
- JFTC
- FEFTA
- sector licence
- labour
- APPI
- tax/economic security

Economic Security Promotion ActのLaw No. 38 of 2026（2026-06-17公布）による
specified medical activities追加等は多くが政令施行待ちである。

- https://laws.e-gov.go.jp/law/508AC0000000038

scheduleへ載らないことをstatutory obligationなしと解釈しない。逆にstatutory
filing itemをPA scheduleへ無断で混ぜない。

## Closing evidence

itemごとに:

```yaml
legal_basis: "[law/rule/guidance/contract]"
source_version: "[official or contract version]"
effective_date: "[date]"
evidence_required: "[approval, receipt, certificate, consent, register extract]"
filing_system: "[EDINET | TDnet | JFTC | BOJ/MOF | registry | authority | N/A]"
waiting_period_end: "[ISO date or null]"
waivable: false
```

waiver可否はPA上のwaiverとmandatory lawを分ける。mandatory waiting periodや
filingをPA waiverで消せると表示しない。
