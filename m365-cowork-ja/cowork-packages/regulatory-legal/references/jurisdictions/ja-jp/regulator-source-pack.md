> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本の当局・sector source pack

**状態:** DRAFT — qualified Japanese counsel review pending

**一次資料確認日:** 2026-07-16 JST

practice profileのwatchlistとsectorに応じて選ぶ。sourceを登録しただけでcoverage complete
またはmonitoring activeと表示しない。

## Core national sources

1. e-Gov open/result RSS。
2. e-Gov Law API revision。
3. 国会、官邸、内閣法制局。衆議院議案pageはShift_JIS。
4. 官報verification。site負荷制限と官報法16条のdatabase approval scopeを分ける。
5. watched authority/SRO RSS、public-comment、law/guidance、council、press。
6. local government footprintがあればlocal gazette/ordinance/consultation。

## FSA

- RSS: https://www.fsa.go.jp/fsaNewsListAll_rss2.xml
- public comments: https://www.fsa.go.jp/public/
- law: https://www.fsa.go.jp/common/law/index.html
- supervisory guidance: https://www.fsa.go.jp/common/law/guide.html
- notices/Q&A: https://www.fsa.go.jp/common/law/kokuji.html
- councils: https://www.fsa.go.jp/singi/index.html

FSA pageはlaw、supervisory guideline、notice、Q&A、consultation、enforcement等が
混在する。`expectedContentClasses`を設定し、itemごとにinstrument/force/lifecycle/
applicabilityを分類する。

## JPX / JSDA

JPX:

- RSS index: https://www.jpx.co.jp/rss/index.html
- site updates: https://www.jpx.co.jp/rss/site-updates.xml
- public comments: https://www.jpx.co.jp/rules-participants/public-comment/index.html
- comment policy:
  https://www.jpx.co.jp/rules-participants/public-comment/tvdivq000000tmrj-att/policy.pdf
- rule revisions: https://www.jpx.co.jp/rules-participants/rules/revise/index.html
- FIEA pinned revision:
  https://laws.e-gov.go.jp/api/2/law_data/323AC0000000025_20260525_506AC0000000052

JSDA:

- comments: https://www.jsda.or.jp/about/public/bosyu/index.html
- rules: https://www.jsda.or.jp/about/kisoku/index.html

JPXはgroup/site aggregatorとして表示される場合がある。documentごとにTokyo Stock
Exchange、Osaka Exchange、Japan Exchange Regulationその他のexact issuer、
trading/listing venue、approval authority/status、covered partyを保存する。
exchange/SRO ruleはstatuteでもordinary platform contractでもない。
TSE exchange-rule approvalはexact rule/exceptionをpinするまでunknown。
金融商品取引法149条をgeneral approval frameworkとしてbasisに記録するが、
個別ruleのapproval required/not-requiredを同条だけから決めない。

## JFTC

- comments:
  https://www.jftc.go.jp/soshiki/kyotsukoukai/p-comment/p_comment.html
- results:
  https://www.jftc.go.jp/soshiki/kyotsukoukai/p-comment/p-commentend.html
- Antimonopoly Act: https://laws.e-gov.go.jp/law/322AC0000000054
- guidelines: https://www.jftc.go.jp/dk/guideline/
- press: https://www.jftc.go.jp/houdou/pressrelease/index.html

JFTC pagesはlaw、guideline、consultation/result、commitment/decision、press、
study groupが混在する。JFTC path /dk/guideline/をlaw sourceと呼ばない。automated retrievalは
adapter-requiredまたはmanual fallbackとし、item-level classificationを行う。

## PPC

- law/guidelines: https://www.ppc.go.jp/personalinfo/legal/
- public comments: https://www.ppc.go.jp/news/public-comment/
- committee material: https://www.ppc.go.jp/enforcement/minutes/
- press: https://www.ppc.go.jp/news/press/

PPC pageはlaw、guideline、consultation、committee material、pressが混在する。
`expectedContentClasses`を使い、committee materialやfuture amendmentをcurrent APPI
dutyとして扱わない。

## MHLW

- law/notices database: https://www.mhlw.go.jp/hourei/
- councils: https://www.mhlw.go.jp/stf/shingi/indexshingi.html
- press: https://www.mhlw.go.jp/stf/houdou/index.html
- e-Gov public-comment feed

law databaseはmonthly update。「登載準備中」も確認し、最新性を保証しない。

## METI

- law: https://www.meti.go.jp/intro/law/index.html
- law list: https://www.meti.go.jp/intro/law/ichiran.html
- councils: https://www.meti.go.jp/shingikai/
- press: https://www.meti.go.jp/press/
- RSS entry: https://www.meti.go.jp/rss/

METI HTML/page retrievalはadapter-requiredまたはmanual fallback。law、council、
press、guidelineをitem-levelに分類する。

## MIC

- law/orders/notices: https://www.soumu.go.jp/menu_hourei/
- councils: https://www.soumu.go.jp/menu_sosiki/singi/index.html
- research groups: https://www.soumu.go.jp/menu_sosiki/kenkyu/kenkyu.html
- news: https://www.soumu.go.jp/menu_news/s-news/index.html
- RSS: https://www.soumu.go.jp/news.rdf

RSSはShift_JIS。decoder、Unicode NFC、Japanese display fieldをtestする。

## Sector additions

- CAA law: https://www.caa.go.jp/law/laws/
- CAA archive: https://www.caa.go.jp/notice/archive/
- CAA press: https://www.caa.go.jp/notice/release/
- CAA/Consumer Commission Establishment Act:
  https://laws.e-gov.go.jp/api/2/law_data/421AC0000000048_20240401_505AC0000000036
- Consumer Commission: https://www.cao.go.jp/consumer/
- Digital Agency: https://www.digital.go.jp/laws
- MOF/NTA: https://www.mof.go.jp/about_mof/act/index.htm /
  https://www.nta.go.jp/law/
- MLIT: https://www.mlit.go.jp/policy/file000002.html
- MOE: https://www.env.go.jp/hourei/
- MAFF: https://www.maff.go.jp/j/shingikai/ — adapter-required/manual
- NPA: https://www.npa.go.jp/laws/shokanhourei/index.html
- PMDA safety: https://www.pmda.go.jp/safety/
- PMDA mixed new information: https://www.pmda.go.jp/0017.html
- 国家サイバー統括室: https://www.cyber.go.jp/
- BOJ: https://www.boj.or.jp/

## Source health record

```yaml
sourceId: "[stable ASCII ID]"
sourceSystem: "[canonical source system]"
sourceItemId: "[feed/page/API resource ID]"
sourceVersionOrRevisionId: "[feed/schema/page version]"
displayNameJa: "[Japanese name]"
canonicalUrl: "https://..."
format: json | rss | atom | html | email | licensed
encoding: UTF-8 | Shift_JIS | other
retrievalMode: direct | adapter-required | manual | licensed
expectedContentClasses: []
itemLevelClassificationRequired: true
termsCheckedAt: "[ISO-8601]"
lastProbeAt: "[ISO-8601]"
lastSuccessAt: "[ISO-8601 or null]"
health: healthy | degraded | failed | unverified
cursor: "[opaque or null]"
fallback: "[manual/licensed/none]"
```

source failureをall-clearへ変換しない。secondary sourceだけでmaterial classificationを
確定せずprimaryへ遡る。

`expectedContentClasses`はsource pageで予想されるlaw、guideline、consultation、
result、press、enforcement、council等のallowlistであり、個別itemのclassificationを
置き換えない。FSA/PPC/JFTC等のmixed pageへ単一`authorityClass`を付けない。

Cabinet decisionはitemごとにinstrumentClass、normativeForce、lifecycleStatus、
applicability、implementing instrumentを確認する。Cabinet decisionというsource名だけで
private-party obligation、guidance、deliberativeのいずれかへ一括分類しない。

`NISC`は国家サイバー統括室のhistorical aliasだけ。PMDA path /0017.htmlはnotices専用
pageではない。

CAA (`authorityType: agency`)とConsumer Commission
(`authorityType: cabinet-office-commission`)を分け、各authorityのmandateを
Establishment Actその他のofficial source/provisionsで固定する。CAA archive/pressは
mixed sourceであり、Consumer Commissionや他committeeのitemをCAA発出と推測しない。
CAAのestablishment/mandate provisionsは2条から4条。
Consumer Commissionのauthority-specific provisionsは6条から8条。
