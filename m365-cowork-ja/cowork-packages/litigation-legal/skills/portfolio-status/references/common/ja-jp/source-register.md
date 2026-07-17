> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本の訴訟・紛争一次資料台帳

checked through: `2026-07-16 JST`
qualified reviewer: `not recorded`
status: `pending`

release前と期限計算の各会話で再取得する。

| Source | Layer | Official URL | Checked note |
|---|---|---|---|
| 日本国憲法77条 | binding-law | https://laws.e-gov.go.jp/api/2/law_data/321CONSTITUTION?asof=2026-07-16&elm=MainProvision-Article_77&response_format=json | 最高裁判所規則の根拠 |
| 民事訴訟法 | binding-law | https://laws.e-gov.go.jp/law/408AC0000000109 | revision ID `408AC0000000109_20260624_508AC0000000046` |
| 民訴法95条 | binding-law | https://laws.e-gov.go.jp/api/2/law_data/408AC0000000109?asof=2026-07-16&elm=MainProvision-Article_95&response_format=json | 期間末日 |
| 民訴法96条 | binding-law | https://laws.e-gov.go.jp/api/2/law_data/408AC0000000109?asof=2026-07-16&elm=MainProvision-Article_96&response_format=json | 期間伸縮 |
| 民訴法97条 | binding-law | https://laws.e-gov.go.jp/api/2/law_data/408AC0000000109?asof=2026-07-16&elm=MainProvision-Article_97&response_format=json | 追完 |
| 民訴法109条の3 | binding-law | https://laws.e-gov.go.jp/api/2/law_data/408AC0000000109?asof=2026-07-16&elm=MainProvision-Article_109_3&response_format=json | 閲覧・記録・通知後1週の最早時 |
| 民訴法109条の2 | binding-law | https://laws.e-gov.go.jp/api/2/law_data/408AC0000000109?asof=2026-07-16&elm=MainProvision-Article_109_2&response_format=json | electronic-service notice prerequisite |
| 民訴法132条の11 | binding-law | https://laws.e-gov.go.jp/api/2/law_data/408AC0000000109?asof=2026-07-16&elm=MainProvision-Article_132_11&response_format=json | 電子提出義務対象 |
| 民訴法163条 | binding-law | https://laws.e-gov.go.jp/api/2/law_data/408AC0000000109?asof=2026-07-16&elm=MainProvision-Article_163&response_format=json | 当事者照会 |
| 民訴法186条 | binding-law | https://laws.e-gov.go.jp/api/2/law_data/408AC0000000109?asof=2026-07-16&elm=MainProvision-Article_186&response_format=json | 調査嘱託 |
| 民訴法197条 | binding-law | https://laws.e-gov.go.jp/api/2/law_data/408AC0000000109?asof=2026-07-16&elm=MainProvision-Article_197&response_format=json | 証言拒絶 |
| 民訴法202条 | binding-law | https://laws.e-gov.go.jp/api/2/law_data/408AC0000000109?asof=2026-07-16&elm=MainProvision-Article_202&response_format=json | 尋問順序 |
| 民訴法220条 | binding-law | https://laws.e-gov.go.jp/api/2/law_data/408AC0000000109?asof=2026-07-16&elm=MainProvision-Article_220&response_format=json | 文書提出義務・除外 |
| 民訴法221～226条 | binding-law | https://laws.e-gov.go.jp/law/408AC0000000109 | 提出命令・送付嘱託 |
| 民訴法234条 | binding-law | https://laws.e-gov.go.jp/api/2/law_data/408AC0000000109?asof=2026-07-16&elm=MainProvision-Article_234&response_format=json | 証拠保全 |
| 民訴法231条の2・3 | binding-law | https://laws.e-gov.go.jp/law/408AC0000000109 | PDF copy/native electronic evidence |
| 民訴法381条の2以下 | binding-law | https://laws.e-gov.go.jp/law/408AC0000000109 | 法定審理期間訴訟手続 |
| 民訴法267条 | binding-law | https://laws.e-gov.go.jp/api/2/law_data/408AC0000000109?asof=2026-07-16&elm=MainProvision-Article_267&response_format=json | 裁判上の和解等 |
| 民訴法285条 | binding-law | https://laws.e-gov.go.jp/api/2/law_data/408AC0000000109?asof=2026-07-16&elm=MainProvision-Article_285&response_format=json | 控訴2週間の不変期間 |
| 民事訴訟規則 | binding-rule | https://www.courts.go.jp/assets/080521minnsokisoku.pdf | 2026-05-21 rollout版 |
| 民事digitalization | official-guidance | https://www.courts.go.jp/saiban/minjidejitaruka/index.html | new ordinary cases from 2026-05-21中心。別手続feature matrix |
| current mints | official-system | https://www.courts.go.jp/saiban/minjidejitaruka/mints_gaiyou/index.html | system継続。旧rules廃止と区別 |
| 法務省改正説明 | official-guidance | https://www.moj.go.jp/MINJI/minji07_00316.html | last updated 2026-03-25 |
| 民事保全法 | binding-law | https://laws.e-gov.go.jp/law/401AC0000000091 | revision ID `401AC0000000091_20260521_505AC0000000053`; 13,20,23,43条 |
| 民事保全規則 | binding-rule | https://www.courts.go.jp/assets/080521minjihozenkisoku.pdf | current PDF確認 |
| 民事執行法 | binding-law | https://laws.e-gov.go.jp/law/354AC0000000004 | revision ID `354AC0000000004_20260521_505AC0000000053` |
| 民事執行法22条 | binding-law | https://laws.e-gov.go.jp/api/2/law_data/354AC0000000004?asof=2026-07-16&elm=MainProvision-Article_22&response_format=json | 債務名義 |
| 民事執行規則 | binding-rule | https://www.courts.go.jp/assets/20260401minjisikkoukisoku.pdf | 2026-04-01 snapshot |
| 労働審判法 | binding-law | https://laws.e-gov.go.jp/law/416AC0000000045 | revision effective 2026-05-21 |
| 労働審判法15条 | binding-law | https://laws.e-gov.go.jp/api/2/law_data/416AC0000000045?asof=2026-07-16&elm=MainProvision-Article_15&response_format=json | 原則3回以内 |
| 労働審判法21条 | binding-law | https://laws.e-gov.go.jp/api/2/law_data/416AC0000000045?asof=2026-07-16&elm=MainProvision-Article_21&response_format=json | 異議2週間の不変期間 |
| 労働審判法22条・26条 | binding-law | https://laws.e-gov.go.jp/law/416AC0000000045 | action deemed filed / record access |
| 労働審判規則 | binding-rule | https://www.courts.go.jp/toukei_siryou/kisokusyu/minzi_kisoku/roudou/index.html | 13, 14, 27条等 |
| 裁判所労働審判説明 | official-guidance | https://www.courts.go.jp/saiban/syurui/syurui_minzi/minzi_25_21/index.html | 3回、40日、裁判所指定答弁期限 |
| 民法 | binding-law | https://laws.e-gov.go.jp/law/129AC0000000089 | limitation/settlement |
| 民法150条 | binding-law | https://laws.e-gov.go.jp/api/2/law_data/129AC0000000089?asof=2026-07-16&elm=MainProvision-Article_150&response_format=json | 催告6か月、再催告不可 |
| 2020年時効改正説明 | official-guidance | https://www.moj.go.jp/MINJI/minji06_001070000.html | transitional law |
| 内容証明 | official-guidance | https://www.post.japanpost.jp/service/send/domestic/option/syomei/ | 内容・差出日 |
| 配達証明 | official-guidance | https://www.post.japanpost.jp/service/send/domestic/option/haitatsu/ | delivery proof |
| 弁護士法 | binding-law | https://laws.e-gov.go.jp/law/324AC1000000205 | secrecy/inquiry |
| 弁護士法23条 | binding-law | https://laws.e-gov.go.jp/api/2/law_data/324AC1000000205?asof=2026-07-16&elm=MainProvision-Article_23&response_format=json | 秘密保持の権利義務 |
| 弁護士法23条の2 | binding-law | https://laws.e-gov.go.jp/api/2/law_data/324AC1000000205?asof=2026-07-16&elm=MainProvision-Article_23_2&response_format=json | 弁護士会照会 |
| 特許法 | binding-law | https://laws.e-gov.go.jp/law/334AC0000000121 | revision metadata updated 2026-06-24 |
| 特許法70条 | binding-law | https://laws.e-gov.go.jp/api/2/law_data/334AC0000000121?asof=2026-07-16&elm=MainProvision-Article_70&response_format=json | claim scope |
| 東京地裁特許モデル | official-guidance | https://www.courts.go.jp/tokyo/saiban/minzi_section29_40_46_47/tokkyokenn_sinngai/index.html | actual panel may vary |
| Ball Spline | case-sensitive | https://www.courts.go.jp/assets/hanrei/hanrei-pdf-52790.pdf | 1998-02-24, 平成6年(オ)1083 |
| Maxacalcitrol | case-sensitive | https://www.courts.go.jp/assets/hanrei/hanrei-pdf-86634.pdf | 2017-03-24, equivalent fifth condition |
| JPO審査基準2026改訂 | official-guidance | https://www.jpo.go.jp/system/laws/rule/guideline/patent/tukujitu_kijun/kaitei2/r8_shinsa_kijun_kaitei.html | page dated 2026-07-01 |
| J-PlatPat | official database | https://www.j-platpat.inpit.go.jp/ | patent records |
| J-PlatPat disclaimer | official-guidance | https://www.inpit.go.jp/j-platpat_info/guide/j-platpat_notice.html | error/omission/status lag |
| 民訴法91・91条の2 | binding-law | https://laws.e-gov.go.jp/law/408AC0000000109 | inspection vs copies/interest |
| 民訴法92条 | binding-law | https://laws.e-gov.go.jp/api/2/law_data/408AC0000000109?asof=2026-07-16&elm=MainProvision-Article_92&response_format=json | third-party record access restriction |
| 裁判所裁判例検索 | official database | https://www.courts.go.jp/hanrei/search1/index.html | 全判決等を掲載しない |

## Release rule

source URL、effective date、revision、binding scope、human verifierが揃わないdeadline /
legal conclusionはproduction-readyにしない。official pageが変わった場合、silentに
旧ruleを使わずcurrency eventを作る。
