> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、日本法公式情報源台帳を追加した派生ファイルです。

# 日本法公式情報源台帳

**Checked:** `2026-07-16 JST`

**Review:** `qualified Japanese counsel review pending`

URLを取得しただけでpropositionがverifiedになるわけではない。taskごとに
actual text、supplementary provisions、effective date、forms、FAQ versionを読む。

## Corporate / registration / records

| ID | Source | Layer / status | 主な用途 |
|---|---|---|---|
| `JP-CORP` | 会社法 https://laws.e-gov.go.jp/law/417AC0000000086 | `LAW`, current | 319、369–371、440、467以降、911、915等 |
| `JP-CORP-R` | 会社法施行規則 https://laws.e-gov.go.jp/law/418M60000010012 | `RULE`, current | 議事録101、electronic signature 225等 |
| `JP-CORP-2019` | 2019年改正案内 https://www.moj.go.jp/MINJI/minji07_00001.html | `OFFICIAL GUIDANCE` | 原則2021-03-01、株主総会資料electronic provision 2022-09-01 |
| `JP-CORP-PENDING` | 2026-03-18会社法制interim proposal https://www.moj.go.jp/shingi1/shingi04900001_00333.html | `PENDING`, not law | future watch。現行義務へ適用しない |
| `JP-REG` | 商業登記法 https://laws.e-gov.go.jp/law/338AC0000000125 | `LAW`, current | registration、attachment、registry evidence |
| `JP-REG-FORMS` | 法務局商業・法人登記forms https://houmukyoku.moj.go.jp/homu/COMMERCE_11-1.html | `OFFICIAL PROCEDURE` | form、attachment、submission |
| `JP-REG-ONLINE` | 登記・供託online system https://www.touki-kyoutaku-online.moj.go.jp/toukinet/shogyo/shogyo.html | `OFFICIAL PROCEDURE` | filing system |
| `JP-REG-EATTACH` | electronic attachment media https://www.moj.go.jp/MINJI/minji41.html | `OFFICIAL PROCEDURE` | CD-R/DVD-R等をpaper applicationへ添付する手続を中心に扱う |
| `JP-REG-BRANCH` | branch-location registration abolition https://www.moj.go.jp/MINJI/minji06_00166.html | `LAW/PROCEDURE`, 2022-09-01 | head-office registryのbranch particularsと区別 |
| `JP-REG-ADDRESS` | representative-address non-display https://www.moj.go.jp/MINJI/minji06_00210.html | `PROCEDURE`, 2024-10-01 | eligibility/effectを確認 |
| `JP-REG-SHLIST` | shareholder-list attachment https://www.moj.go.jp/MINJI/minji06_00095.html | `PROCEDURE` | meeting/class meeting/Art.319 registration |
| `JP-SEAL` | online seal submission optional from 2021-02-15 https://www.moj.go.jp/MINJI/minji06_00070.html | `OFFICIAL PROCEDURE` | seal handling |
| `JP-BO-LIST` | 実質的支配者list制度 https://www.moj.go.jp/MINJI/minji06_00116.html | `OFFICIAL PROCEDURE`, from 2022-01-31 | request-based list。annual filingではない |
| `JP-ESIGN` | 電子署名及び認証業務に関する法律 https://laws.e-gov.go.jp/law/412AC0000000102 | `LAW`, current | Art. 3 evidentiary presumption |
| `JP-ESIGN-QA` | cloud signature Q&A https://www.soumu.go.jp/main_content/000754533.pdf | `OFFICIAL GUIDANCE` | service型electronic signature |
| `JP-ERECORD` | 電子帳簿保存法 https://laws.e-gov.go.jp/law/410AC0000000025 and NTA https://www.nta.go.jp/law/joho-zeikaishaku/sonota/jirei/tokusetsu/01.htm | `LAW/GUIDANCE` | 2024-01-01 electronic preservationとstatutory relief/exceptionを確認 |

## Public company / securities / listing

| ID | Source | Layer / status | 主な用途 |
|---|---|---|---|
| `JP-FIEA` | 金融商品取引法 https://laws.e-gov.go.jp/law/323AC0000000025 | `LAW`, current | securities reports、tender offer、large holding、insider |
| `JP-FIEA-2026` | 2024 Act No. 32 implementing rules https://www.fsa.go.jp/news/r7/shouken/20250704/20250704.html | `LAW/RULE`, effective 2026-05-01 | tender-offer 30%、exchange-market inclusion、large-holding revisions |
| `JP-LARGE-HOLDING` | 大量保有報告portal https://www.fsa.go.jp/common/shinsei/tairyohoyu/index.html | `LAW/PROCEDURE` | over 5%、原則5 business days。actual exception確認 |
| `JP-HALF-YEAR` | quarterly-report abolition / half-year reports https://www.fsa.go.jp/news/r5/sonota/20240327/20240327.html | `LAW/RULE`, effective 2024-04-01 | reporting calendar |
| `JP-EDINET` | EDINET https://disclosure2.edinet-fsa.go.jp/ | `OFFICIAL SYSTEM` | statutory disclosure filing |
| `JP-OFFICER-REPORT` | officer/major shareholder reporting FAQ https://www.fsa.go.jp/common/shinsei/baibaihoukoku/faq.html | `OFFICIAL GUIDANCE` | FIEA Art. 163 reporting |
| `JP-INSIDER` | insider Q&A https://www.fsa.go.jp/news/r5/shouken/20240419/240419insider_qa_.pdf | `OFFICIAL GUIDANCE` | Arts. 166/167 |
| `JP-JPX-DISC` | timely disclosure guide https://www.jpx.co.jp/equities/listing/disclosure/guidebook/index.html | `LISTING`, full guide 2025-04 + 2026 extracts | TDnet decision/fact disclosure。EDINETと別 |
| `JP-CG-CODE` | Corporate Governance Code https://www.jpx.co.jp/equities/listing/cg/ | `SOFT LAW / listing framework`, 2021-06-11 revision | comply-or-explain等 |
| `JP-VIRTUAL-SHM` | virtual-only shareholder meeting route https://www.meti.go.jp/policy/economy/keiei_innovation/keizaihousei/corporategovernance/virtual-only-shareholders-meeting.html | `LAW/GUIDANCE` | special statutory routeとconfirmations |

## Competition / foreign investment / M&A guidance

| ID | Source | Layer / status | 主な用途 |
|---|---|---|---|
| `JP-COMP` | 独占禁止法 https://laws.e-gov.go.jp/law/322AC0000000054 | `LAW`, current | business combination control |
| `JP-COMP-SHARE` | share acquisition notification https://www.jftc.go.jp/dk/kiketsu/kigyoketsugo/todokede/kabu2.html | `LAW/PROCEDURE` | acquiring-group/target-group turnover、20%/50%、30-day prohibition |
| `JP-COMP-REVIEW` | review procedure/current policy https://www.jftc.go.jp/dk/kiketsu/guideline/guideline/taiouhoushin.html | `OFFICIAL GUIDANCE` | consultation、high-value below-threshold transaction |
| `JP-FDI` | 外国為替及び外国貿易法 https://laws.e-gov.go.jp/law/324AC0000000228 | `LAW`, current | inward direct investment、prior notification/post-report |
| `JP-FDI-MOF` | MOF foreign investment portal https://www.mof.go.jp/policy/international_policy/gaitame_kawase/fdi/index.htm | `OFFICIAL PROCEDURE` | designated/core business、exemption、forms |
| `JP-FDI-2025` | 2025 rules https://www.mof.go.jp/english/policy/international_policy/fdi/News_and_Communications/20250331134457.html | `RULE`, effective 2025-05-19 | specified foreign investorのexemption restriction等 |
| `JP-FDI-BOJ` | BOJ forms https://www.boj.or.jp/about/services/tame/t-down.htm | `OFFICIAL PROCEDURE` | forms/submission |
| `JP-FDI-QA` | BOJ Q&A https://www.boj.or.jp/about/services/tame/faq/data/tn-qa.pdf | `OFFICIAL GUIDANCE` | filer、timing、form |
| `JP-FDI-2026` | FEFTA amendment Law No. 30 of 2026 https://laws.e-gov.go.jp/law/508AC0000000030 | `PENDING IN PART`, promulgated 2026-06-05 | indirect acquisition/risk mitigation等。施行待ちを先行適用しない |
| `JP-MA-FAIR` | Fair M&A Guidelines 2019 https://www.meti.go.jp/policy/economy/keiei_innovation/keizaihousei/fair-ma-rule/ma-guideline-publications.html | `SOFT LAW` | MBO、controlling shareholder transaction |
| `JP-TAKEOVER-G` | Guidelines for Corporate Takeovers 2023-08-31 https://www.meti.go.jp/press/2023/08/20230831003/20230831003.html | `SOFT LAW` | listed takeover process、board conduct |
| `JP-TAKEOVER-PENDING` | 2026 takeover-guidance draft interpretation/Q&A https://www.meti.go.jp/press/2026/06/20260618004/20260618004.html | `PENDING PUBLIC COMMENT`, 2026-06-18–07-17 | current guidanceへ先行適用しない |

## Labour / privacy / IP / sector

| ID | Source | Layer / status | 主な用途 |
|---|---|---|---|
| `JP-LSA` | 労働基準法 https://laws.e-gov.go.jp/law/322AC0000000049 | `LAW`, current | employment obligations |
| `JP-LCA` | 労働契約法 https://laws.e-gov.go.jp/law/419AC0000000128 | `LAW`, current | employment contract、transfer/change |
| `JP-LUA` | 労働組合法 https://laws.e-gov.go.jp/law/324AC0000000174 | `LAW`, current | union/CBA/unfair labour practice |
| `JP-DISPATCH` | 労働者派遣法 https://laws.e-gov.go.jp/law/360AC0000000088 | `LAW`, current | dispatch/licence/transfer diligence |
| `JP-PTFT` | パートタイム・有期雇用労働法 https://laws.e-gov.go.jp/law/405AC0000000076 | `LAW`, current | treatment/classification |
| `JP-SPLIT-LAB` | 会社分割に伴う労働契約の承継等に関する法律 https://laws.e-gov.go.jp/law/412AC0000000103 | `LAW`, current | company split labour succession |
| `JP-CIVIL` | 民法 https://laws.e-gov.go.jp/law/129AC0000000089 | `LAW`, current | assignment、contractual position、Art. 625 |
| `JP-LAB-HUB` | MHLW reorganization hub https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/koyou_roudou/roudouseisaku/saihen/index.html | `OFFICIAL GUIDANCE` | merger/split/business transfer |
| `JP-LAB-2026` | business-transfer/merger guidance https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/koyou_roudou/roudouseisaku/saihen/68297_00001.html | `GUIDANCE`, amended 2026-01-20, effective 2026-05-25 | employee explanation/consultation |
| `JP-DATA` | 個人情報保護法 https://laws.e-gov.go.jp/law/415AC0000000057 | `LAW`, current | diligence、integration、foreign transfer |
| `JP-MYNUMBER` | 番号法 https://laws.e-gov.go.jp/law/425AC0000000027 | `LAW`, current | specific personal informationをAPPI M&A exceptionへ混ぜない |
| `JP-PPC-GENERAL` | PPC General Guidelines https://www.ppc.go.jp/personalinfo/legal/guidelines_tsusoku/ | `OFFICIAL GUIDANCE`, June 2026 partial amendment shown | APPI interpretation |
| `JP-PPC-MA` | M&A/reorganization warning https://www.ppc.go.jp/news/careful_information/gappei_soshikisaihen/ | `OFFICIAL GUIDANCE` | reorganization data handling |
| `JP-PPC-DD` | pre-closing diligence safeguard example https://www.ppc.go.jp/all_faq_index/faq1-q2-11/ | `OFFICIAL GUIDANCE`, real-estate example | universal M&A safe harborではない。current Art.27(5)(ii)を確認 |
| `JP-PPC-XFER` | foreign-transfer guidance https://www.ppc.go.jp/personalinfo/legal/guidelines_offshore/ | `OFFICIAL GUIDANCE` | overseas transfer |
| `JP-APPI-PENDING` | 2026 bill materials https://www.ppc.go.jp/news/press/2026/260407/ and https://www.sangiin.go.jp/japanese/joho1/kousei/gian/221/meisai/m221080221054.htm | `PENDING` at 2026-07-16 | Diet-passed; promulgation/commencement unconfirmed |
| `JP-PATENT` | 特許法 https://laws.e-gov.go.jp/law/334AC0000000121 | `LAW`, current | title、employee invention、recordal |
| `JP-UTILITY` | 実用新案法 https://laws.e-gov.go.jp/law/334AC0000000123 | `LAW`, current | utility-model title/recordal |
| `JP-TM` | 商標法 https://laws.e-gov.go.jp/law/334AC0000000127 | `LAW`, current | title、recordal |
| `JP-DESIGN` | 意匠法 https://laws.e-gov.go.jp/law/334AC0000000125 | `LAW`, current | title、recordal |
| `JP-COPYRIGHT` | 著作権法 https://laws.e-gov.go.jp/law/345AC0000000048 | `LAW`, current | Art. 15、moral rights、assignment/perfection |
| `JP-UCPA` | 不正競争防止法 https://laws.e-gov.go.jp/law/405AC0000000047 | `LAW`, current | trade secret、confidential information |
| `JP-JPO-XFER` | JPO transfer procedure https://www.jpo.go.jp/system/process/toroku/iten/index.html | `OFFICIAL PROCEDURE` | patent/trademark/design recordal |
| `JP-EMP-INVENT` | employee invention guideline https://www.jpo.go.jp/system/patent/shutugan/shokumu/shokumu_guideline.html | `OFFICIAL GUIDANCE` | Patent Act Art. 35 |
| `JP-COPY-REG` | copyright registration https://www.bunka.go.jp/seisaku/chosakuken/seidokaisetsu/toroku_seido/ | `OFFICIAL PROCEDURE` | third-party perfection等 |
| `JP-TRADE-SECRET` | March 2025 trade-secret guideline https://www.meti.go.jp/policy/economy/chizai/chiteki/guideline/r7ts.pdf | `OFFICIAL GUIDANCE` | reasonable management measures |

## Representative sector trigger set

この一覧はtrigger setであり網羅的ではない。

- Banking Act: https://laws.e-gov.go.jp/law/356AC0000000059
- Insurance Business Act: https://laws.e-gov.go.jp/law/407AC0000000105
- Payment Services Act: https://laws.e-gov.go.jp/law/421AC0000000059
- Telecommunications Business Act:
  https://laws.e-gov.go.jp/law/359AC0000000086
- Radio Act: https://laws.e-gov.go.jp/law/325AC0000000131
- PMD Act: https://laws.e-gov.go.jp/law/335AC0000000145
- 建設業法:
  https://laws.e-gov.go.jp/law/324AC0000000100
- Economic Security Promotion Act:
  https://laws.e-gov.go.jp/law/504AC0000000043
- 2026 amendment Law No. 38:
  https://laws.e-gov.go.jp/law/508AC0000000038
- critical infrastructure guidance:
  https://www.cao.go.jp/keizai_anzen_hosho/suishinhou/infra/infra.html

## AI / professional confidentiality / entity periodic sources

| ID | Source | Layer / status | 主な用途 |
|---|---|---|---|
| `JP-AI-ACT` | AI Promotion Act, Act No. 53 of 2025 https://laws.e-gov.go.jp/law/507AC0000000053 and https://www8.cao.go.jp/cstp/ai/ai_act/ai_act.html | `LAW`, fully effective 2025-09-01 | programmatic law。data/privilege safe harborではない |
| `JP-AI-G` | AI Business Guidelines v1.2 https://www.soumu.go.jp/main_sosiki/kenkyu/ai_network/02ryutsu20_04000019.html and https://www.soumu.go.jp/main_content/001064279.pdf | `GUIDANCE`, published 2026-03-31 | AI handoff governance |
| `JP-PPC-AI` | generative-AI warning https://www.ppc.go.jp/news/press/2023/230602kouhou/ | `OFFICIAL GUIDANCE` | personal data input/output |
| `JP-AI-PLAN` | AI Basic Plan 2026-07-14 https://www8.cao.go.jp/cstp/ai/ai_plan/aiplan_20260714.pdf | `POLICY` | current policy context |
| `JP-ATTORNEY` | 弁護士法 https://laws.e-gov.go.jp/law/324AC1000000205 | `LAW` | attorney role/confidentiality |
| `JP-CCP` | 民事訴訟法 https://laws.e-gov.go.jp/law/408AC0000000109 | `LAW` | production/withholding analysis |
| `JP-JFBA` | JFBA professional rules https://www.nichibenren.or.jp/jfba_info/rules/society-laws.html | `PROFESSIONAL RULE` | attorney duties |
| `JP-JFTC-CONF` | JFTC limited confidentiality procedure https://www.jftc.go.jp/dk/seido/hanbetsu/hanbetsu.html and https://www.jftc.go.jp/dk/guideline/unyoukijun/hanbetsu.html | `OFFICIAL PROCEDURE/GUIDANCE`, operative 2020-12-25 | narrow cartel-investigation context only |
| `JP-ACCOUNTS-NOTICE` | Companies Act Art. 440 in `JP-CORP` | `LAW` | financial statement public notice/exemption analysis |
| `JP-CORP-TAX` | corporate tax filing portal https://www.nta.go.jp/taxes/tetsuzuki/shinsei/annai/hojin/shinkoku/01.htm | `OFFICIAL PROCEDURE` | corporate tax filing |
| `JP-SOCIAL` | social insurance changes https://www.nenkin.go.jp/service/kounen/tekiyo/jigyosho/20140815.html | `OFFICIAL PROCEDURE` | office/entity change notices |

## 使用rule

- official URLを取得できない、403、version不明なら取得済みと表示しない。
- e-Gov consolidated textとsupplementary provisionでeffective dateを確認する。
- JPX timely disclosureとEDINET statutory filingを統合しない。
- PA scheduleとstatutory/regulatory disclosureを統合しない。
- Companies Act proposal、APPI amendment等の`PENDING`をcurrent obligationへ
  適用しない。
- source statusをauditし、qualified Japanese counsel reviewは`pending`のまま
  保持する。
