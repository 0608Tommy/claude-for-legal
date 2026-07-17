> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 移行元global regulatory source catalog

移行元catalogのU.S./EU/UK/international sourceを保持する。URL確認基準日は
**2026年5月**。日本のsourceは
[日本source register](ja-jp/source-register.md)を使う。
feed URLは変わるため、利用前にlive probeする。

Federal RegisterはU.S. federal sourceだけに使う。EUはEUR-Lex / Official Journal、
UKはlegislation.gov.ukと各regulator、その他はjurisdiction-specific official
sourceを使う。Federal Registerをnon-U.S.またはglobal fallbackにしない。

## 読み方

- JSON APIはstructured primary source、RSS/Atomはsemi-structured、HTMLはchange
  detection、email-onlyはapproved mail connectorが必要。
- Primaryは当局自身、Secondaryはlead。secondaryからprimaryへ遡る。
- `None`、`Key`、`Paid`のauthを区別する。
- declaration、URL listing、200 responseだけでsource completenessを保証しない。

## U.S. federal primary

| Source | URL / method | Note |
|---|---|---|
| Federal Register | https://www.federalregister.gov/api/v1/documents.json | agency/date/type filter。U.S. federal ruleのbaseline |
| Regulations.gov | https://api.regulations.gov/v4/documents | free API key。docket/comment/supporting documents |
| Congress.gov | https://api.congress.gov/v3/bill | free API key。bill/law/committee |
| SEC | https://www.sec.gov/news/pressreleases.rss | rule/enforcement/speech。Federal Registerとdedupe |
| FTC | https://www.ftc.gov/feeds/press-release.xml | enforcement/rule/blog/settlement |
| CFPB | https://www.consumerfinance.gov/about-us/newsroom/ | page RSS/activity logをlive確認 |
| DOJ Antitrust | https://www.justice.gov/atr/news-feeds | multiple feeds |
| DOJ Main | https://www.justice.gov/news/rss | client-side topic filter |
| FCC | https://www.fcc.gov/news-events/rss-feeds-and-email-updates-fcc | RSS/email、ECFS docket feed |
| HHS OCR | https://www.hhs.gov/ocr/newsroom/index.html | HHS-wide RSS補完 |
| OFAC | https://ofac.treasury.gov/recent-actions | RSSは2025-01-31終了。email/page |
| BIS | https://www.bis.gov/news-updates | HTML。ruleはFederal Registerも確認 |
| DOL | https://www.dol.gov/rss/releases.xml | press releases |
| NIST Cybersecurity | https://www.nist.gov/news-events/cybersecurity/rss.xml | topic feed |
| CISA | https://www.cisa.gov/news-events/cybersecurity-advisories | page上のfeedを確認 |

## U.S. state primary

coverageは不均一。RSSがなければmanual/email/change detectionと明示する。

| Source | URL |
|---|---|
| California AG | https://oag.ca.gov/news/feed/729/oag.ca.gov |
| CPPA | https://cppa.ca.gov/announcements/ |
| New York AG | https://ag.ny.gov/press-releases |
| Texas AG | https://www2.texasattorneygeneral.gov/feeds/feeds.php?feed=pr |
| Illinois AG | https://illinoisattorneygeneral.gov/news-room/ |
| Washington AG | https://www.atg.wa.gov/news |
| Colorado AG | https://coag.gov/press-releases/ |
| Connecticut AG | https://portal.ct.gov/ag/press-releases/press-releases |
| Virginia AG | https://www.oag.state.va.us/media-center/news-releases |
| Massachusetts AG | https://www.mass.gov/orgs/office-of-attorney-general-maura-healey/news |
| NYDFS | https://www.dfs.ny.gov/reports_and_publications/press_releases |

## EU / UK primary

| Source | URL / method | Note |
|---|---|---|
| EDPB | https://www.edpb.europa.eu/news/news_en | guidelines/opinions/decisions |
| European Commission Press Corner | https://ec.europa.eu/commission/presscorner/ | RSS/email |
| EUR-Lex | https://eur-lex.europa.eu/ | OJ、webservice/search RSS |
| UK legislation | https://www.legislation.gov.uk/ | enacted legislation、official text |
| ICO | https://ico.org.uk/global/rss-feeds/ | news/enforcement/blog |
| CNIL | https://www.cnil.fr/en/rss.xml | live verify |
| DPC Ireland | https://www.dataprotection.ie/en/news-media/latest-news | HTML。critical source |
| BfDI | https://www.bfdi.bund.de/EN/Home/home_node.html | HTML |
| ENISA | https://www.enisa.europa.eu/news | RSS discontinued、email mechanism確認 |
| FCA | https://www.fca.org.uk/news/rss.xml | live verify、email supported |
| EDPS | https://www.edps.europa.eu/press-publications/press-news_en | HTML/RSS option |

## International

| Source | URL |
|---|---|
| OECD AI Policy Observatory | https://oecd.ai/en/ |
| Council of Europe | https://www.coe.int/en/web/portal/news |
| UK Parliament Bills | https://bills.parliament.uk/rss/publicbills.rss |

## Secondary / aggregators

primary actionのleadとしてのみ使用し、`[secondary — verify against primary]`を付ける。

| Source | URL |
|---|---|
| IAPP Daily Dashboard | https://iapp.org/rss/daily-dashboard/ |
| Future of Privacy Forum | https://fpf.org/feed/ |
| Hogan Lovells | https://www.hoganlovells.com/en/rss |
| Covington topic blogs | https://www.cov.com/ |
| WilmerHale | https://www.wilmerhale.com/ |
| Wilson Sonsini | https://www.wsgr.com/ |
| Lexology | https://www.lexology.com/account/rss |
| JD Supra | https://www.jdsupra.com/legal-news/rss-law-feeds.aspx |
| Artificial Lawyer | https://www.artificiallawyer.com/feed/ |
| LawSites | https://www.lawsitesblog.com/feed |

## Feedなしまたはretired

OFAC、ENISA、DPC、CPPA、多くのstate AG、NYDFS、BIS、HHS OCR standalone、
BfDI、一部law firmはemail/manual/change detectionが必要。未実装のweb-page change
detectionやmail ingestionを存在すると表示しない。

## Starter packの考え方

- privacy U.S./EU: Federal Register、FTC、CFPB、CA AG、CPPA、NY AG、EDPB、
  ICO、CNIL、DPC、IAPP、FPF。
- broad regulatory: Federal Register、SEC、CFPB、DOJ、FCC、DOL、BIS、OFAC、
  Commission、FCA、aggregator。
- AI governance: Federal Register、NIST、Commission、EDPB、OECD、Council of
  Europe、IAPP、FPF。

watchlist、jurisdiction、sectorに合わないstarter packをdefault coverageとして
押し付けない。追加sourceはfeed URL、format、coverage、auth、terms、health、
fallbackを記録し、live probe後だけconnectedとする。
