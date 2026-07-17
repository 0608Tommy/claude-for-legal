> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本規制対応 — 公式情報源台帳

**状態:** DRAFT — qualified Japanese counsel review pending

**確認日:** 2026-07-16 JST

`checked`はURL、公表状態、technical accessの確認日であり、個別案件への適用または
法的見解の承認を意味しない。Japanese text、revision、附則、designation、deadlineを
作業ごとに再取得する。

## 法令、官報、国会、内閣

| Source | role | URL | 2026-07-16時点 |
|---|---|---|---|
| e-Gov法令検索 | current/consolidated text、navigation | https://laws.e-gov.go.jp/ | official |
| Law API v2 | structured law/revision retrieval | https://laws.e-gov.go.jp/api/2/swagger-ui/ | official API |
| Law API OpenAPI | implementation contract | https://laws.e-gov.go.jp/api/2/swagger-ui/lawapi-v2.yaml | official |
| Revision API | historical/current/future revision | https://laws.e-gov.go.jp/api/2/law_revisions/405AC0000000088 | endpoint patternを確認 |
| APA revision-pinned Text API | 2026-06-24 version-pinned Japanese text | https://laws.e-gov.go.jp/api/2/law_data/405AC0000000088_20260624_508AC0000000046 | exact revision |
| Bulk data | change discovery candidate | https://laws.e-gov.go.jp/bulkdownload/ | deployment validation後 |
| 電子官報 | promulgation、signed official PDF | https://www.kanpo.go.jp/ | 2025-04-01電子化 |
| 官報利用規約・案内 | authenticity、retention、automation restriction | https://www.kanpo.go.jp/guidance.html | robot負荷禁止等を確認 |
| 官報検索 | licensed archive/search | https://search.npb.go.jp/kanpou/ | access terms確認 |
| 内閣法制局 法律成立まで | bill/passage/promulgation/commencement説明 | https://www.clb.go.jp/recent-laws/process/ | authoritative process |
| 内閣法制局 最近の法律 | Cabinet bills/promulgated Acts | https://www.clb.go.jp/recent-laws/ | official index |
| 衆議院 議案 | bill text/status | https://www.shugiin.go.jp/internet/itdb_gian.nsf/html/gian/menu.htm | Shift_JIS、decoder required |
| 参議院 議案 | bill text/status | https://www.sangiin.go.jp/japanese/joho1/kousei/gian/221/gian.htm | page 2026-07-15 |
| 首相官邸 閣議 | Cabinet decisions/policy | https://www.kantei.go.jp/jp/kakugi/index.html | itemごとにinstrument/force/applicabilityを分類 |
| 日本法令索引 | legislative/amendment history | https://hourei.ndl.go.jp/ | cross-check |
| 日本法令外国語訳DB | reference translation | https://www.japaneselawtranslation.go.jp/?re=english | official textではない |

電子官報は2025-04-01開始。官報法（令和5年法律第85号）は2023-12-13公布、
2025-04-01施行:

- https://laws.e-gov.go.jp/api/2/law_data/505AC0000000085
- https://www.npb.go.jp/product_service/books/kanpo/denshika.html

2026-07-16 08:30の官報site表示は本紙第1749号、号外第159号、政府調達第131号。
この観測は将来のissue番号を保証しない。

官報法16条は、電子官報の全記録を含み他人の利用に供するdatabaseに承認を要求する。
site termsは負荷を与えるrobot/crawler collectionを禁止するが、あらゆるautomation
requestを一律禁止するものとして扱わない。coverage、用途、提供先、rate、terms、
Art.16該当性を別々に確認する。

## e-Gov意見公募

| Source | role | URL |
|---|---|---|
| 案件一覧 | case search/lifecycle | https://public-comment.e-gov.go.jp/pcm/list |
| 制度説明 | 行政手続法用語・procedure | https://public-comment.e-gov.go.jp/contents/about-public-comment/ |
| 募集中RSS | new/open cases | https://public-comment.e-gov.go.jp/rss/pcm_list.xml |
| 結果RSS | result/non-adoption/exception | https://public-comment.e-gov.go.jp/rss/pcm_result.xml |
| RSS guide | supported feed behavior | https://public-comment.e-gov.go.jp/contents/help/guide/rss.html |

## Core authorities

| Authority | official source |
|---|---|
| FSA | https://www.fsa.go.jp/fsaNewsListAll_rss2.xml |
| FSA public comments | https://www.fsa.go.jp/public/ |
| FSA law | https://www.fsa.go.jp/common/law/index.html |
| FSA supervisory guidance | https://www.fsa.go.jp/common/law/guide.html |
| FSA notices/Q&A | https://www.fsa.go.jp/common/law/kokuji.html |
| FSA councils | https://www.fsa.go.jp/singi/index.html |
| JPX RSS | https://www.jpx.co.jp/rss/index.html |
| JPX site updates | https://www.jpx.co.jp/rss/site-updates.xml |
| JPX public comments | https://www.jpx.co.jp/rules-participants/public-comment/index.html |
| JPX rule revisions | https://www.jpx.co.jp/rules-participants/rules/revise/index.html |
| Financial Instruments and Exchange Act pinned revision | https://laws.e-gov.go.jp/api/2/law_data/323AC0000000025_20260525_506AC0000000052 |
| JFTC comments | https://www.jftc.go.jp/soshiki/kyotsukoukai/p-comment/p_comment.html |
| JFTC results | https://www.jftc.go.jp/soshiki/kyotsukoukai/p-comment/p-commentend.html |
| 独占禁止法 | https://laws.e-gov.go.jp/law/322AC0000000054 |
| JFTC guidelines | https://www.jftc.go.jp/dk/guideline/ |
| JFTC press | https://www.jftc.go.jp/houdou/pressrelease/index.html |
| PPC law/guidelines | https://www.ppc.go.jp/personalinfo/legal/ |
| PPC comments | https://www.ppc.go.jp/news/public-comment/ |
| PPC committee | https://www.ppc.go.jp/enforcement/minutes/ |
| PPC press | https://www.ppc.go.jp/news/press/ |
| MHLW law database | https://www.mhlw.go.jp/hourei/ |
| MHLW councils | https://www.mhlw.go.jp/stf/shingi/indexshingi.html |
| MHLW press | https://www.mhlw.go.jp/stf/houdou/index.html |
| METI law | https://www.meti.go.jp/intro/law/index.html |
| METI law list | https://www.meti.go.jp/intro/law/ichiran.html |
| METI councils | https://www.meti.go.jp/shingikai/ |
| METI press | https://www.meti.go.jp/press/ |
| METI RSS | https://www.meti.go.jp/rss/ |
| MIC law/orders/notices | https://www.soumu.go.jp/menu_hourei/ |
| MIC councils | https://www.soumu.go.jp/menu_sosiki/singi/index.html |
| MIC research groups | https://www.soumu.go.jp/menu_sosiki/kenkyu/kenkyu.html |
| MIC news | https://www.soumu.go.jp/menu_news/s-news/index.html |
| MIC RSS | https://www.soumu.go.jp/news.rdf |

MIC RSSと衆議院議案pageはShift_JIS。MHLW law databaseはmonthly updateと
「登載準備中」を確認する。JFTC/METI/MAFF pageのautomated retrievalは
adapter-requiredまたはmanual fallbackとして扱う。

FSA、PPC、JFTCのindex/pageはlaw、guideline、consultation、result、press、
enforcement、council等が混在し得る。source-level `authorityClass`を1つ付けず、
`expectedContentClasses`を設定してitem-level classificationを行う。

## Sector additions

- Consumer Affairs Agency: https://www.caa.go.jp/law/laws/
- CAA new-information archive: https://www.caa.go.jp/notice/archive/
- CAA press releases: https://www.caa.go.jp/notice/release/
- CAA/Consumer Commission Establishment Act pinned revision:
  https://laws.e-gov.go.jp/api/2/law_data/421AC0000000048_20240401_505AC0000000036
- Consumer Commission: https://www.cao.go.jp/consumer/
- Digital Agency: https://www.digital.go.jp/laws
- Digital Agency procedures: https://www.digital.go.jp/get-involved/procedure
- MOF: https://www.mof.go.jp/about_mof/act/index.htm
- NTA: https://www.nta.go.jp/law/
- MLIT: https://www.mlit.go.jp/policy/file000002.html
- MOE: https://www.env.go.jp/hourei/
- MAFF: https://www.maff.go.jp/j/shingikai/
- NPA law: https://www.npa.go.jp/laws/shokanhourei/index.html
- NPA notices: https://www.npa.go.jp/laws/notification/index.html
- PMDA safety: https://www.pmda.go.jp/safety/
- PMDA mixed new information: https://www.pmda.go.jp/0017.html
- 国家サイバー統括室: https://www.cyber.go.jp/
- JSDA comments: https://www.jsda.or.jp/about/public/bosyu/index.html
- JSDA rules: https://www.jsda.or.jp/about/kisoku/index.html
- BOJ: https://www.boj.or.jp/
- Cabinet Office holidays: https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html

national sourceはprefectural/municipal ordinance、local gazette、local consultationを
coverageしない。practice footprintごとにlocal official sourceを追加する。

`NISC`は国家サイバー統括室のhistorical aliasとしてだけ保持する。PMDA path
/0017.htmlはnotices専用ではなくmixed new-information pageなのでitem-levelに
classifyする。

JPX group siteをrule issuerと推測しない。Tokyo Stock Exchange、Osaka Exchange、
Japan Exchange Regulation等について、documentごとにexact issuer、venue、
approval authority/status、covered partyを記録する。exchange/SRO ruleはstatuteでも
ordinary platform contractでもない。
TSE exchange-rule approvalはexact rule/exceptionがpinされるまでunknownとし、
金融商品取引法149条をgeneral approval frameworkとしてapproval basisへ記録する。

消費者庁と消費者委員会を同一authorityとして扱わない。authorityはstable ID、
authorityType、official mandate source/provisionsを持つstructured recordにする。
CAA archive/press itemがConsumer Commission、消費者安全調査委員会その他のbodyを
参照する場合もitem-level issuer/mandateを確認する。
CAAのestablishment/mandateはpinned revisionの2条から4条を記録する。
Consumer Commissionは同revisionの6条から8条をauthority-specific provisionsとして
記録する。
