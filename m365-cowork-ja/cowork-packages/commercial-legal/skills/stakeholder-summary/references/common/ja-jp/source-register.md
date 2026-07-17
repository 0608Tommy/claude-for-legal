> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本商事契約module — 公式情報源台帳

**状態:** DRAFT — qualified Japanese counsel review pending

**確認日:** 2026-07-16

`checked`は公式URL、現行title、公開状態を確認した日であり、個別案件への適用または有資格者承認を意味しない。e-Gov法令APIで現行title・law numberを確認した。

## Binding law

| 分野 | 現行法・law number | 公式URL | 取扱い |
|---|---|---|---|
| 契約一般 | 民法（明治二十九年法律第八十九号） | https://laws.e-gov.go.jp/law/129AC0000000089 | 成立・方式、債務不履行、解除、定型約款等。施行versionを案件時に再確認 |
| 商行為 | 商法（明治三十二年法律第四十八号） | https://laws.e-gov.go.jp/law/132AC0000000048 | 商人・商行為に適用し得る。民法との関係を確認 |
| 準拠法 | 法の適用に関する通則法（平成十八年法律第七十八号） | https://laws.e-gov.go.jp/law/418AC0000000078 | choice of law、消費者・労働等のspecial ruleを確認 |
| 電子署名 | 電子署名及び認証業務に関する法律（平成十二年法律第百二号） | https://laws.e-gov.go.jp/law/412AC0000000102 | 第3条の真正成立推定。すべてのe-signatureの有効性を一律判定しない |
| 電子消費者契約 | 電子消費者契約に関する民法の特例に関する法律（平成十三年法律第九十五号） | https://laws.e-gov.go.jp/law/413AC0000000095 | consumerの電子申込みにおけるerror確認等。B2B一般ruleではない |
| 個人情報 | 個人情報の保護に関する法律（平成十五年法律第五十七号） | https://laws.e-gov.go.jp/law/415AC0000000057 | 現行法・PPC規則guideをdata flowごとに確認 |
| 中小受託 | 製造委託等に係る中小受託事業者に対する代金の支払の遅延等の防止に関する法律（昭和三十一年法律第百二十号） | https://laws.e-gov.go.jp/law/331AC0000000120 | 略称`中小受託取引適正化法`, `取適法`。2026-01-01施行の現行title |
| Freelance | 特定受託事業者に係る取引の適正化等に関する法律（令和五年法律第二十五号） | https://laws.e-gov.go.jp/law/505AC0000000025 | 略称`フリーランス・事業者間取引適正化等法` |
| Consumer | 消費者契約法（平成十二年法律第六十一号） | https://laws.e-gov.go.jp/law/412AC0000000061 | solicitation、免責、予定損害、unfair terms |
| 通信販売等 | 特定商取引に関する法律（昭和五十一年法律第五十七号） | https://laws.e-gov.go.jp/law/351AC0000000057 | transaction type、広告、final confirmation、民事rule |
| Competition | 私的独占の禁止及び公正取引の確保に関する法律（昭和二十二年法律第五十四号） | https://laws.e-gov.go.jp/law/322AC0000000054 | 不公正な取引方法、優越的地位等 |
| Trade secret | 不正競争防止法（平成五年法律第四十七号） | https://laws.e-gov.go.jp/law/405AC0000000047 | 営業秘密、限定提供data等の要件を確認 |
| Product liability | 製造物責任法（平成六年法律第八十五号） | https://laws.e-gov.go.jp/law/406AC0000000085 | product/defect/damage scopeを確認 |
| Corporate authority | 会社法（平成十七年法律第八十六号） | https://laws.e-gov.go.jp/law/417AC0000000086 | signer authority、機関決定、代表権を確認 |
| Arbitration | 仲裁法（平成十五年法律第百三十八号） | https://laws.e-gov.go.jp/law/415AC0000000138 | 仲裁合意とconsumer special measureを確認 |
| Copyright | 著作権法（昭和四十五年法律第四十八号） | https://laws.e-gov.go.jp/law/345AC0000000048 | 第15条、第59条、第61条第2項等を確認 |
| Patent | 特許法（昭和三十四年法律第百二十一号） | https://laws.e-gov.go.jp/law/334AC0000000121 | employee invention、assignment、licenseを確認 |
| Trademark | 商標法（昭和三十四年法律第百二十七号） | https://laws.e-gov.go.jp/law/334AC0000000127 | brand license/assignment時 |
| Design | 意匠法（昭和三十四年法律第百二十五号） | https://laws.e-gov.go.jp/law/334AC0000000125 | design license/assignment時 |
| Consumer claims | 不当景品類及び不当表示防止法（昭和三十七年法律第百三十四号） | https://laws.e-gov.go.jp/law/337AC0000000134 | 表示・claim・広告を確認 |
| Digital platform | 取引デジタルプラットフォームを利用する消費者の利益の保護に関する法律（令和三年法律第三十二号） | https://laws.e-gov.go.jp/law/503AC0000000032 | marketplace/platform時に確認 |
| 秘密・手続 | 弁護士法（昭和二十四年法律第二百五号） | https://laws.e-gov.go.jp/law/324AC1000000205 | 第23条等。米国privilegeと同一視しない |
| 文書提出 | 民事訴訟法（平成八年法律第百九号） | https://laws.e-gov.go.jp/law/408AC0000000109 | 第197条、第220条、第223条等を確認 |

## Official guidance

| 分野 | 公式資料 | URL | 法的位置付け |
|---|---|---|---|
| 取適法 | 公正取引委員会 取適法portal | https://www.jftc.go.jp/toriteki/ | official explanation、rule、text。法律本文と区別 |
| Freelance | 公正取引委員会 フリーランス法portal | https://www.jftc.go.jp/freelancelaw_2024/ | official explanation、Q&A。各条文scopeを別途確認 |
| 個人情報 | PPC 法令・guideline | https://www.ppc.go.jp/personalinfo/legal/ | official rule/guidance collection |
| 個人情報 | 個人情報保護法施行規則 | https://laws.e-gov.go.jp/law/428M60020000003 | binding ministerial rule |
| 個人情報 | PPC通則guideline | https://www.ppc.go.jp/files/pdf/260614_guidelines01.pdf | 2026-06版。適用時に最新版を再確認 |
| 国外移転 | PPC外国第三者提供guideline | https://www.ppc.go.jp/files/pdf/251212_guidelines02.pdf | 2025-12版。適用時に最新版を再確認 |
| 特商法 | 消費者庁 特定商取引法 | https://www.caa.go.jp/policies/policy/consumer_transaction/specified_commercial_transactions/ | official guide・執行情報 |
| 消費者契約 | 消費者庁 消費者契約法 | https://www.caa.go.jp/policies/policy/consumer_system/consumer_contract_act/ | official material。検討会資料は未施行policyと区別 |
| Competition | 公正取引委員会 legislation/guidelines | https://www.jftc.go.jp/en/legislation_gls/index.html | official English access point。日本語原文を優先 |
| 知財・data取引 | 知的財産権・ノウハウ・データの適切な取引のための優越的地位の濫用等に関する指針 | https://www.jftc.go.jp/dk/guideline/unyoukijun/chizaitorihiki.pdf | 2026-06-24公表official guidance。法律ではない |
| AI契約 | METI AIの利用・開発に関する契約チェックリスト | https://www.meti.go.jp/press/2024/02/20250218003/20250218003.html | 2025-02-18公表official guidance。契約義務ではない |
| Electronic commerce | METI 電子商取引等に関する準則 | https://www.meti.go.jp/press/2024/02/20250212003/20250212003.html | official guidance。個別契約へ自動適用しない |
| Superior position | JFTC 優越的地位の濫用guidance | https://www.jftc.go.jp/dk/guideline/unyoukijun/yuetsutekichii.html | official guidance |
| IP antitrust | 知的財産の利用に関する独占禁止法上の指針 | https://www.jftc.go.jp/dk/guideline/unyoukijun/chitekizaisan.html | official guidance |
| Trade secret | METI 営業秘密管理指針 | https://www.meti.go.jp/policy/economy/chizai/chiteki/trade-secret.html | official guidance |

## 2026 status

### 取適法

2025-05-23公布の令和七年法律第四十一号による改正後のtitleがe-Govへ反映され、JFTCは2026-01-01施行として案内している。旧`下請代金支払遅延等防止法`、旧`下請法`はmigration/history labelとしてのみ使い、現行成果物では`中小受託取引適正化法（取適法）`を併記する。

- 改正法: https://laws.e-gov.go.jp/law/507AC0000000041
- 法令・規則: https://www.jftc.go.jp/toriteki/legislation/index.html

### APPI amendment

PPCは2026-04-07に「個人情報の保護に関する法律等の一部を改正する法律案」
の閣議決定を公表した。2026-05-26衆議院可決、2026-07-10参議院可決・成立、
2026-07-14内閣が公布を決定した。

- PPC: https://www.ppc.go.jp/news/press/2026/260407/
- 参議院要旨: https://www.sangiin.go.jp/japanese/joho1/kousei/gian/221/meisai/m221080221054.htm
- 2026-07-14公布決定: https://www.kantei.go.jp/jp/kakugi/2026/kakugi-2026071401.html

2026-07-16時点で参議院の公布年月日・法律番号欄は空欄であり、公布そのもの、
law number、施行政令、PPC規則、e-Gov consolidated textへの反映を本module
では確認できていない。国会成立・公布決定と、現行適用・施行を分ける。
主要規定は公布日から2年以内の政令指定日に施行予定であり、施行前内容を
現在利用可能なexceptionまたは義務として使わない。

### 2026 IP / know-how / data guidance

JFTC・中小企業庁・特許庁は2026-06-24に知財・know-how・data取引の指針と契約書ひな形を公表した。これは独禁法等の考え方を示すofficial guidanceであり、各例がそのまま違法性結論になるわけではない。

## 更新rule

1. 署名日、effective date、threshold、適用scopeに依存する場合は公式原文を再取得する。
2. e-Govのlatest textがfuture amendmentを含む可能性があるため、supplementary provisionと施行日を確認する。
3. secondary sourceで変更を知った場合、primary source取得まで結論を変更しない。ただし疑義を`[verify]`で示す。
4. 日本法有資格者review recordがない限りstatusを`pending`から変更しない。
