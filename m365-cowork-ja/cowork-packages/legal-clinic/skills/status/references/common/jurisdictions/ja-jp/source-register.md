> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本のリーガルクリニック一次資料台帳

checked through: `2026-07-16 JST`
qualified reviewer: `not recorded`
clinic supervisor reviewer: `not recorded`
status: `pending`

release前、期限計算、受任・利益相反・守秘判断の各会話でcurrent official sourceを
再取得する。

## 資格、職務、監督

| Source | Layer | Official URL | Checked note |
|---|---|---|---|
| 弁護士法 | `binding-law` | https://laws.e-gov.go.jp/law/324AC1000000205 | Act No. 205 of 1949。e-Gov revision metadataを再確認 |
| 弁護士法23条 | `binding-law` | https://laws.e-gov.go.jp/law/324AC1000000205 | 秘密保持。範囲と例外は責任弁護士review |
| 弁護士法25条 | `binding-law` | https://laws.e-gov.go.jp/law/324AC1000000205 | 受任制限・conflict論点 |
| 弁護士法56条 | `binding-law` | https://laws.e-gov.go.jp/law/324AC1000000205 | 懲戒 |
| 弁護士法72条・74条 | `binding-law` | https://laws.e-gov.go.jp/law/324AC1000000205 | 非弁行為・表示。clinic model固有review必須 |
| 日弁連第3部会規page | `professional-rule` | https://www.nichibenren.or.jp/jfba_info/rules/society-laws.html | 弁護士職務基本規程等のcurrent official landing page |
| 日弁連法規集page | `professional-rule` | https://www.nichibenren.or.jp/jfba_info/rules.html | official collection。版・改正日を再確認 |
| 日弁連弁護士情報検索 | `official-database` | https://member.nichibenren.or.jp/general_search | 登録確認source candidate。authority/専門性/engagementの証明ではない |
| 弁護士等の業務広告に関する規程 | `professional-rule` | https://www.nichibenren.or.jp/library/ja/jfba_info/rules/pdf/kai44.pdf | public description/claim用。職務基本規程と混同しない |
| 業務広告に関する指針 | `official-guidance` | https://www.nichibenren.or.jp/library/ja/jfba_info/rules/pdf/shishin.pdf | 規程とはlayerを分け、current official pageから改正有無を再確認 |
| 弁護士情報セキュリティ規程 No.117 | `professional-rule` | https://www.nichibenren.or.jp/library/pdf/jfba_info/rules/kaiki/kaiki_no_117.pdf | adopted 2022-06-10、effective 2024-06-01 |
| JFBA security notice | `official-guidance` | https://www.nichibenren.or.jp/document/newspaper/year/2024/600.html | security rule implementation material |

## 民事、刑事、行政

| Source | Layer | Official URL | Checked note |
|---|---|---|---|
| 民法 current text | `binding-law` | https://laws.e-gov.go.jp/law/129AC0000000089 | revision ID `129AC0000000089_20260624_508AC0000000045`; 2026-06-24 revision metadataをmatterごとに再取得 |
| 民法138条 | `binding-law` | https://laws.e-gov.go.jp/api/2/law_data/129AC0000000089?asof=2026-07-16&elm=MainProvision-Article_138&response_format=json | 期間計算の通則。法令・裁判命令・法律行為のspecial ruleを先に確認 |
| 民法139条 | `binding-law` | https://laws.e-gov.go.jp/api/2/law_data/129AC0000000089?asof=2026-07-16&elm=MainProvision-Article_139&response_format=json | 時間による期間の起算 |
| 民法140条 | `binding-law` | https://laws.e-gov.go.jp/api/2/law_data/129AC0000000089?asof=2026-07-16&elm=MainProvision-Article_140&response_format=json | 日・週・月・年の初日不算入と午前零時例外 |
| 民法141条 | `binding-law` | https://laws.e-gov.go.jp/api/2/law_data/129AC0000000089?asof=2026-07-16&elm=MainProvision-Article_141&response_format=json | 末日の終了による満了 |
| 民法142条 | `binding-law` | https://laws.e-gov.go.jp/api/2/law_data/129AC0000000089?asof=2026-07-16&elm=MainProvision-Article_142&response_format=json | 休日と取引をしない慣習。CPC95又は行政期限へ自動転用しない |
| 民法143条 | `binding-law` | https://laws.e-gov.go.jp/api/2/law_data/129AC0000000089?asof=2026-07-16&elm=MainProvision-Article_143&response_format=json | 週・月・年の暦計算 |
| 民法147～149条 | `binding-law` | https://laws.e-gov.go.jp/law/129AC0000000089 | 裁判上の請求等、強制執行等、仮差押え等による完成猶予・更新の区別 |
| 民法150条 | `binding-law` | https://laws.e-gov.go.jp/law/129AC0000000089 | 催告による完成猶予。再催告等をcurrent textで確認 |
| 民法151条 | `binding-law` | https://laws.e-gov.go.jp/law/129AC0000000089 | 協議合意による完成猶予と期間・再合意を確認 |
| 民法152条 | `binding-law` | https://laws.e-gov.go.jp/law/129AC0000000089 | 承認による更新を確認 |
| 民法153条 | `binding-law` | https://laws.e-gov.go.jp/api/2/law_data/129AC0000000089?asof=2026-07-16&elm=MainProvision-Article_153&response_format=json | 完成猶予/更新の効力が及ぶ当事者・承継人の範囲 |
| 民事訴訟法 | `binding-law` | https://laws.e-gov.go.jp/law/408AC0000000109 | revision effective 2026-06-24とresearch記録。再取得 |
| 民事訴訟法55条 | `binding-law` | https://laws.e-gov.go.jp/api/2/law_data/408AC0000000109?asof=2026-07-16&elm=MainProvision-Article_55&response_format=json | 民事の訴訟代理権範囲・特別委任事項だけ。刑事の期間計算へ使わない |
| 民事訴訟法95条 | `binding-law` | https://laws.e-gov.go.jp/api/2/law_data/408AC0000000109?asof=2026-07-16&elm=MainProvision-Article_95&response_format=json | 期間計算、court-set start、末日調整 |
| 民事訴訟法109条の2 | `binding-law` | https://laws.e-gov.go.jp/api/2/law_data/408AC0000000109?asof=2026-07-16&elm=MainProvision-Article_109_2&response_format=json | electronic service method、notice、届出 |
| 民事訴訟法109条の3 | `binding-law` | https://laws.e-gov.go.jp/api/2/law_data/408AC0000000109?asof=2026-07-16&elm=MainProvision-Article_109_3&response_format=json | 閲覧・user file記録・通知発出後1週間の最早時と不算入期間 |
| 民事訴訟規則 | `binding-rule` | https://www.courts.go.jp/assets/080521minnsokisoku.pdf | current PDFを各matterで確認 |
| 民事訴訟digitalization | `official-guidance` | https://www.courts.go.jp/saiban/minjidejitaruka/index.html | ordinary civil full phase effective 2026-05-21。対象手続と経過措置を確認 |
| 民事訴訟digital概要 | `official-guidance` | https://www.courts.go.jp/saiban/minjidejitaruka/minso_gaiyou/index.html | electronic filing/service overview |
| mints概要 | `official-guidance` | https://www.courts.go.jp/saiban/minjidejitaruka/mints_gaiyou/index.html | My Number card upload禁止等をcurrent pageで確認 |
| 刑事訴訟法 | `binding-law` | https://laws.e-gov.go.jp/law/323AC0000000131 | counsel、押収、守秘、上訴。civil flowと分離 |
| 刑事訴訟法55条 | `binding-law` | https://laws.e-gov.go.jp/api/2/law_data/323AC0000000131?asof=2026-07-16&elm=MainProvision-Article_55&response_format=json | 刑事の時間/日月年、初日、暦、末日、時効期間例外の計算。`criminal-procedure-code-55` |
| 行政不服審査法 | `binding-law` | https://laws.e-gov.go.jp/law/426AC0000000068 | Art.18等。special statuteを確認 |
| 行政事件訴訟法 | `binding-law` | https://laws.e-gov.go.jp/law/337AC0000000139 | Art.14等。処分・知った日・経過措置を確認 |
| 行政機関の休日に関する法律1条 | `binding-law` | https://laws.e-gov.go.jp/api/2/law_data/363AC0000000091?asof=2026-07-16&elm=MainProvision-Article_1&response_format=json | 国の行政機関の休日と対象機関 |
| 行政機関の休日に関する法律2条 | `binding-law` | https://laws.e-gov.go.jp/api/2/law_data/363AC0000000091?asof=2026-07-16&elm=MainProvision-Article_2&response_format=json | 国の行政庁への法定申請等の期限特例。別段の定めと対象を確認 |
| MOJ 2026-04-01 family reform page | `official-guidance` | https://www.moj.go.jp/MINJI/minji07_00357.html | binding sourceはcurrent民法等。施行日・経過措置・DV/虐待factsを確認 |
| Family reform Q&A | `official-guidance` | https://www.moj.go.jp/MINJI/minji07_00377.html | binding textでなくofficial explanation |
| DV防止法 | `binding-law` | https://laws.e-gov.go.jp/law/413AC0100000031 | 保護命令、管轄、要件をcurrent textで確認 |
| DV保護命令案内 | `official-guidance` | https://www.courts.go.jp/saiban/syurui/syurui_minzi/minzi_25_23/index.html | 地方裁判所route。family courtへ誤routingしない |
| 児童虐待防止法 | `binding-law` | https://laws.e-gov.go.jp/law/412AC1000000082 | 6条の通告義務・守秘との関係をhuman lawyerが直ちに確認 |

## 個人情報、My Number、安全

| Source | Layer | Official URL | Checked note |
|---|---|---|---|
| 個人情報保護法 | `binding-law` | https://laws.e-gov.go.jp/law/415AC0000000057 | 利用目的、適正取得、安全管理、委託、提供等 |
| 個人情報保護法58条 | `binding-law` | https://laws.e-gov.go.jp/api/2/law_data/415AC0000000057?asof=2026-07-16&elm=MainProvision-Article_58&response_format=json | 公立大学等を含むhost/業務ごとの適用特例。clinic host regimeを先に選定 |
| PPC通則guideline | `official-guidance` | https://www.ppc.go.jp/personalinfo/legal/guidelines_tsusoku/ | partially revised 2026-06。current PDF/page再確認 |
| PPC行政機関等編guideline | `official-guidance` | https://www.ppc.go.jp/personalinfo/legal/guidelines_administrative/ | public-sector/Article 58適用関係をhost・業務単位で確認 |
| PPC行政機関等編Q&A | `official-guidance` | https://www.ppc.go.jp/personalinfo/legal/koutekibumon_qa/ | guidelineとbinding textを分ける |
| PPC生成AI注意喚起 | `official-guidance` | https://www.ppc.go.jp/news/press/2023/230602kouhou/ | 2023-06-02 |
| My Number Act | `binding-law` | https://laws.e-gov.go.jp/law/425AC0000000027 | Specific Personal Informationの目的・提供・収集・保管 |
| PPC My Number guideline | `official-guidance` | https://www.ppc.go.jp/legal/policy/my_number_guideline_jigyosha/ | partially revised 2025-06 |
| 障害者差別解消法 | `binding-law` | https://laws.e-gov.go.jp/law/425AC0000000065 | private-sector reasonable accommodation duty effective 2024-04-01 |
| Cabinet Office accessibility notice | `official-guidance` | https://www.cao.go.jp/press/new_wave/20240520.html | reasonable accommodation material |
| 意思決定支援guideline | `official-guidance` | https://www.courts.go.jp/vc-files/courts/2021/20201030guideline.pdf | 2020-10-30。general capacity ruleと誤表示しない |

## Legal aid、教育、communication

| Source | Layer | Official URL | Checked note |
|---|---|---|---|
| 総合法律支援法 | `binding-law` | https://laws.e-gov.go.jp/law/416AC0000000074 | Houterasuのstatutory framework |
| Houterasu法律相談援助 | `official-guidance` | https://www.houterasu.or.jp/site/bengoshitou-fujo/ | 無料法律相談のprogram/要件。代理援助と分ける |
| Houterasu代理援助 | `official-guidance` | https://www.houterasu.or.jp/site/about-houterasu/minjihouritsufujo.html | 代理費用等の立替program。相談援助・書類作成援助と分ける |
| Houterasu書類作成援助 | `official-guidance` | https://www.houterasu.or.jp/site/about-houterasu/minjihouritsufujo.html | 裁判所提出書類作成費用等の立替program。代理権を自動生成しない |
| Houterasu国選弁護等関連業務 | `official-guidance` | https://www.houterasu.or.jp/site/bengoshitou-koukusenbengo/ | 裁判所による選任と法テラスの契約・報酬関連。民事扶助と分離 |
| 法科大学院教育法 | `binding-law` | https://laws.e-gov.go.jp/law/414AC0000000139 | practical educationをsupportするがstudent-practice licenceを付与しない |
| MEXT clinical education example | `official-guidance` | https://www.mext.go.jp/content/20241220-mxt_senmon02-000039072_03.pdf | 2024-12-20 educational example |
| やさしい日本語guidance | `official-guidance` | https://www.bunka.go.jp/koho_hodo_oshirase/hodohappyo/92488301.html | 2020-08 material |
| やさしい日本語PDF | `official-guidance` | https://www.bunka.go.jp/seisaku/kokugo_nihongo/kyoiku/yasashii_nihongo/pdf/92309501_01.pdf | reading-grade ruleとして扱わない |
| 児童相談所虐待対応ダイヤル189 | `official-guidance` | https://www.cfa.go.jp/policies/jidougyakutai/gyakutai-taiou-dial/ | Art.6のhuman通告/相談route candidate。AI又はqueueが通告したと表示しない |
| DV相談ナビ #8008 | `official-guidance` | https://www.gender.go.jp/policy/no_violence/dv_navi/ | 最寄りの相談窓口へつなぐroute。safe-contact、利用可能端末、受付時間を確認 |

## Research source

| Source | Layer | Official URL | Checked note |
|---|---|---|---|
| 官報 | `official-database` | https://www.kanpo.go.jp/ | electronic issue from 2025-04-01 |
| 官報説明 | `official-guidance` | https://www.cao.go.jp/others/soumu/kanpo/about/kanpo_about.html | current issuance explanation |
| 裁判所裁判例検索 | `official-database` | https://www.courts.go.jp/hanrei/search1/index.html | 全裁判例を掲載しない |
| 日本法令外国語訳DB | `official-reference` | https://www.japaneselawtranslation.go.jp/en/ | translation is not authoritative |

## Future law

| Source | Layer | Official URL | Checked note |
|---|---|---|---|
| 2026 APPI amendment PPC material | `future-law` | https://www.ppc.go.jp/news/press/2026/260407/ | Cabinet-approved 2026-04-07 |
| Diet bill status | `future-law` | https://www.sangiin.go.jp/japanese/joho1/kousei/gian/221/gian.htm | research record: passed 2026-07-10。effective date provision-specific |
| Bill detail | `future-law` | https://www.sangiin.go.jp/japanese/joho1/kousei/gian/221/meisai/m221080221054.htm | under-16/biometric/statistical-use等をcurrent lawへ早期適用しない |

## Release rule

official URL、revision/effective date、binding scope、事件固有source、human verifierが
揃わないlegal conclusion又はdeadlineをproduction-readyにしない。
